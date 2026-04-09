"""vLLM + TriAttention Process Lifecycle Manager.

Autonomous inference server management — start, stop, health check, status.
Designed for Claude Code to call via Bash (agent-friendly JSON output).

Usage:
    python scripts/vllm-manager.py start [--model qwen|deepseek|deepseek-14b|<hf-id>] [--port 8000] [--budget 2048]
    python scripts/vllm-manager.py stop
    python scripts/vllm-manager.py status
    python scripts/vllm-manager.py health
    python scripts/vllm-manager.py calibrate [--model ...]

State: .claude/memory/intermediate/vllm-state.json (auto-managed)
Reference: arXiv:2604.04921 (TriAttention)
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- Constants ---

STOPA_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = STOPA_ROOT / ".claude" / "memory" / "intermediate" / "vllm-state.json"
STATS_DIR = STOPA_ROOT / "triattention-stats"
LOG_FILE = STOPA_ROOT / "logs" / "vllm-server.log"

MODEL_ALIASES = {
    "qwen": "Qwen/Qwen3-8B",
    "qwen3": "Qwen/Qwen3-8B",
    "deepseek": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "deepseek-14b": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    "r1-7b": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "r1-14b": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
}

DEFAULT_MODEL = "Qwen/Qwen3-8B"
DEFAULT_PORT = 8000
DEFAULT_KV_BUDGET = 2048
DEFAULT_GPU_MEM = 0.90
DEFAULT_MAX_LEN = 32768
HEALTH_TIMEOUT = 5
STARTUP_TIMEOUT = 120
SHUTDOWN_TIMEOUT = 10


# --- State Management ---

def read_state() -> dict | None:
    """Read server state from disk. Returns None if no state file."""
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def write_state(state: dict) -> None:
    """Write server state to disk."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def clear_state() -> None:
    """Remove state file."""
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def pid_alive(pid: int) -> bool:
    """Check if a process with given PID is running."""
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.OpenProcess(0x0400, False, pid)  # PROCESS_QUERY_INFORMATION
            if handle:
                kernel32.CloseHandle(handle)
                return True
            return False
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


# --- Health Check ---

def check_health(port: int) -> dict:
    """Check if vLLM server is responding. Returns health info dict."""
    import requests
    try:
        resp = requests.get(f"http://localhost:{port}/v1/models", timeout=HEALTH_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        models = [m["id"] for m in data.get("data", [])]
        return {"healthy": True, "models": models}
    except requests.exceptions.ConnectionError:
        return {"healthy": False, "error": "connection_refused"}
    except requests.exceptions.Timeout:
        return {"healthy": False, "error": "timeout"}
    except Exception as e:
        return {"healthy": False, "error": str(e)}


# --- Commands ---

def resolve_model(name: str) -> str:
    """Resolve model alias to HuggingFace ID."""
    return MODEL_ALIASES.get(name.lower(), name)


def model_slug(model: str) -> str:
    """Convert model name to filesystem-safe slug."""
    return model.replace("/", "_")


def cmd_calibrate(args: argparse.Namespace) -> int:
    """Run TriAttention calibration for a model."""
    model = resolve_model(args.model)
    slug = model_slug(model)
    stats_path = STATS_DIR / slug

    print(json.dumps({"action": "calibrate", "model": model, "stats_dir": str(stats_path)}))

    stats_path.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [sys.executable, "-m", "triattention.calibrate",
         "--model", model,
         "--output", str(stats_path),
         "--num-samples", "128"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )

    if result.returncode != 0:
        print(json.dumps({"action": "calibrate", "status": "failed", "error": result.stderr[:500]}))
        return 1

    print(json.dumps({"action": "calibrate", "status": "done", "stats_dir": str(stats_path)}))
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    """Start vLLM server with TriAttention plugin."""
    model = resolve_model(args.model)
    port = args.port
    kv_budget = args.budget
    gpu_mem = args.gpu_mem
    max_len = args.max_len
    slug = model_slug(model)
    stats_path = STATS_DIR / slug

    # Check if already running
    state = read_state()
    if state and pid_alive(state.get("pid", -1)):
        health = check_health(state["port"])
        if health["healthy"]:
            print(json.dumps({
                "action": "start", "status": "already_running",
                "pid": state["pid"], "port": state["port"],
                "model": state["model"], **health,
            }))
            return 0

    # Preflight: check CUDA
    cuda_check = subprocess.run(
        [sys.executable, "-c",
         "import torch; assert torch.cuda.is_available(); "
         "print(torch.cuda.get_device_name(0))"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if cuda_check.returncode != 0:
        print(json.dumps({"action": "start", "status": "failed", "error": "CUDA not available"}))
        return 1
    gpu_name = cuda_check.stdout.strip()

    # Preflight: check packages
    for pkg in ["vllm", "triattention"]:
        check = subprocess.run(
            [sys.executable, "-c", f"import {pkg}"],
            capture_output=True, text=True,
        )
        if check.returncode != 0:
            print(json.dumps({
                "action": "start", "status": "failed",
                "error": f"{pkg} not installed. Run: pip install {pkg}",
            }))
            return 1

    # Auto-calibrate if needed
    if not stats_path.exists() or not any(stats_path.iterdir()):
        print(json.dumps({"action": "start", "phase": "calibrating", "model": model}))
        stats_path.mkdir(parents=True, exist_ok=True)
        cal = subprocess.run(
            [sys.executable, "-m", "triattention.calibrate",
             "--model", model, "--output", str(stats_path), "--num-samples", "128"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if cal.returncode != 0:
            print(json.dumps({"action": "start", "status": "failed",
                              "phase": "calibration", "error": cal.stderr[:500]}))
            return 1

    # Launch vLLM as background process
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    log_handle = open(LOG_FILE, "w", encoding="utf-8")

    env = {
        **os.environ,
        "TRIATTENTION_STATS_DIR": str(stats_path),
        "TRIATTENTION_KV_BUDGET": str(kv_budget),
    }

    cmd = [
        sys.executable, "-m", "vllm.entrypoints.openai.api_server",
        "--model", model,
        "--port", str(port),
        "--gpu-memory-utilization", str(gpu_mem),
        "--enable-chunked-prefill",
        "--max-model-len", str(max_len),
        "--entry-points", "triattention.vllm.plugin:register_triattention_backend",
    ]

    if sys.platform == "win32":
        proc = subprocess.Popen(
            cmd, env=env, stdout=log_handle, stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    else:
        proc = subprocess.Popen(
            cmd, env=env, stdout=log_handle, stderr=subprocess.STDOUT,
            start_new_session=True,
        )

    pid = proc.pid

    # Wait for server to become healthy
    print(json.dumps({"action": "start", "phase": "waiting_for_health", "pid": pid, "port": port}))

    start_time = time.time()
    while time.time() - start_time < STARTUP_TIMEOUT:
        if proc.poll() is not None:
            # Process died
            log_handle.close()
            tail = ""
            if LOG_FILE.exists():
                tail = LOG_FILE.read_text(encoding="utf-8", errors="replace")[-500:]
            print(json.dumps({
                "action": "start", "status": "failed",
                "error": "server process exited", "exit_code": proc.returncode,
                "log_tail": tail,
            }))
            clear_state()
            return 1

        health = check_health(port)
        if health["healthy"]:
            break
        time.sleep(2)
    else:
        # Timeout — kill the process
        proc.terminate()
        print(json.dumps({"action": "start", "status": "failed", "error": "startup timeout"}))
        clear_state()
        return 1

    # Write state
    state = {
        "pid": pid,
        "port": port,
        "model": model,
        "kv_budget": kv_budget,
        "gpu_name": gpu_name,
        "stats_dir": str(stats_path),
        "log_file": str(LOG_FILE),
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    write_state(state)

    print(json.dumps({
        "action": "start", "status": "running",
        **state, **health,
    }))
    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    """Stop the running vLLM server."""
    state = read_state()
    if not state:
        print(json.dumps({"action": "stop", "status": "not_running"}))
        return 0

    pid = state.get("pid", -1)
    if not pid_alive(pid):
        clear_state()
        print(json.dumps({"action": "stop", "status": "already_stopped", "pid": pid}))
        return 0

    # Graceful shutdown
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
    else:
        os.kill(pid, signal.SIGTERM)

    # Wait for exit
    for _ in range(SHUTDOWN_TIMEOUT):
        if not pid_alive(pid):
            break
        time.sleep(1)
    else:
        # Force kill
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
        else:
            os.kill(pid, signal.SIGKILL)

    clear_state()
    print(json.dumps({"action": "stop", "status": "stopped", "pid": pid}))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Show server status as JSON."""
    state = read_state()
    if not state:
        print(json.dumps({"running": False}))
        return 0

    pid = state.get("pid", -1)
    alive = pid_alive(pid)

    if not alive:
        clear_state()
        print(json.dumps({"running": False, "stale_pid": pid}))
        return 0

    health = check_health(state["port"])

    started = state.get("started_at", "")
    uptime_s = 0
    if started:
        try:
            start_dt = datetime.fromisoformat(started)
            uptime_s = int((datetime.now(timezone.utc) - start_dt).total_seconds())
        except ValueError:
            pass

    print(json.dumps({
        "running": True,
        "pid": pid,
        "port": state["port"],
        "model": state["model"],
        "kv_budget": state.get("kv_budget", DEFAULT_KV_BUDGET),
        "gpu": state.get("gpu_name", "unknown"),
        "uptime_seconds": uptime_s,
        "log_file": state.get("log_file", ""),
        **health,
    }))
    return 0


def cmd_health(args: argparse.Namespace) -> int:
    """Quick health check — exit code 0 if healthy, 1 if not."""
    state = read_state()
    port = state["port"] if state else DEFAULT_PORT
    health = check_health(port)
    print(json.dumps(health))
    return 0 if health["healthy"] else 1


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="vLLM + TriAttention Process Manager")
    sub = parser.add_subparsers(dest="command", required=True)

    # start
    p_start = sub.add_parser("start", help="Start vLLM server")
    p_start.add_argument("--model", default=DEFAULT_MODEL, help="Model name or alias")
    p_start.add_argument("--port", type=int, default=DEFAULT_PORT)
    p_start.add_argument("--budget", type=int, default=DEFAULT_KV_BUDGET, help="KV cache budget")
    p_start.add_argument("--gpu-mem", type=float, default=DEFAULT_GPU_MEM)
    p_start.add_argument("--max-len", type=int, default=DEFAULT_MAX_LEN)

    # stop
    sub.add_parser("stop", help="Stop vLLM server")

    # status
    sub.add_parser("status", help="Show server status (JSON)")

    # health
    sub.add_parser("health", help="Quick health check")

    # calibrate
    p_cal = sub.add_parser("calibrate", help="Run TriAttention calibration")
    p_cal.add_argument("--model", default=DEFAULT_MODEL, help="Model name or alias")

    args = parser.parse_args()

    commands = {
        "start": cmd_start,
        "stop": cmd_stop,
        "status": cmd_status,
        "health": cmd_health,
        "calibrate": cmd_calibrate,
    }

    sys.exit(commands[args.command](args))


if __name__ == "__main__":
    main()
