#!/usr/bin/env bash
# TriAttention vLLM Setup — Long-Reasoning KV Compression
# Usage: ./scripts/triattention-setup.sh [model] [--calibrate]
#
# Deploys vLLM with TriAttention plugin for 10.7× KV cache reduction.
# Default model: Qwen/Qwen3-8B (pre-calibrated stats available)
#
# Prerequisites:
#   pip install vllm triattention
#   CUDA GPU with 8+ GB VRAM (consumer GPU sufficient with TriAttention)
#
# Reference: arXiv:2604.04921

set -euo pipefail

MODEL="${1:-Qwen/Qwen3-8B}"
CALIBRATE="${2:-}"
PORT="${TRIATTENTION_PORT:-8000}"
KV_BUDGET="${TRIATTENTION_KV_BUDGET:-2048}"
MAX_MODEL_LEN="${TRIATTENTION_MAX_LEN:-32768}"

echo "=== TriAttention vLLM Setup ==="
echo "Model: $MODEL"
echo "KV Budget: $KV_BUDGET tokens"
echo "Max Length: $MAX_MODEL_LEN tokens"
echo "Port: $PORT"

# Step 1: Check dependencies
echo ""
echo "--- Checking dependencies ---"
python -c "import vllm; print(f'vLLM {vllm.__version__}')" 2>/dev/null || {
    echo "ERROR: vLLM not installed. Run: pip install vllm"
    exit 1
}
python -c "import triattention; print(f'TriAttention {triattention.__version__}')" 2>/dev/null || {
    echo "ERROR: TriAttention not installed. Run: pip install triattention"
    echo "  Or: pip install git+https://github.com/WeianMao/triattention.git"
    exit 1
}

# Step 2: Calibration (optional, for new models without pre-calibrated stats)
if [[ "$CALIBRATE" == "--calibrate" ]]; then
    echo ""
    echo "--- Calibrating TriAttention for $MODEL ---"
    echo "This computes Q/K concentration stats (takes ~5 min)..."
    python -m triattention.calibrate \
        --model "$MODEL" \
        --output "./data/triattention-stats-$(basename "$MODEL").json" \
        --num-samples 128 \
        --max-length "$MAX_MODEL_LEN"
    echo "Calibration done. Stats saved to ./data/"
fi

# Step 3: Launch vLLM with TriAttention
echo ""
echo "--- Launching vLLM + TriAttention on :$PORT ---"
echo "Connect with: LLM_BASE_URL=http://localhost:$PORT/v1"

# Environment for TriAttention plugin
export TRIATTENTION_ENABLED=1
export TRIATTENTION_KV_BUDGET="$KV_BUDGET"

python -m vllm.entrypoints.openai.api_server \
    --model "$MODEL" \
    --port "$PORT" \
    --max-model-len "$MAX_MODEL_LEN" \
    --gpu-memory-utilization 0.90 \
    --enable-chunked-prefill \
    --load-format auto \
    --entry-points triattention.vllm.plugin:register_triattention_backend \
    --trust-remote-code
