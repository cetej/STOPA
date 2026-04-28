import express from 'express';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createConnection } from 'net';
import { spawn, execSync } from 'child_process';
import { readFileSync, existsSync } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));

const EXEC_OPTS = { windowsHide: true, timeout: 5000 };

// Fix partially double-encoded UTF-8 from Windows git
function fixEncoding(buf) {
  let str = buf.toString('utf8');
  try {
    const rebuf = Buffer.from(str, 'latin1');
    const decoded = rebuf.toString('utf8');
    if (!/\ufffd/.test(decoded) && /[čřžšěůúýáíéďťň]/i.test(decoded)) return decoded;
  } catch { /* keep original */ }
  return str;
}

const ROOT = 'C:/Users/stock/Documents/000_NGM';
const PORT = 3200;

// ─── Project Registry ────────────────────────────────────────────────
const PROJECTS = [
  { id: 'monitor', name: 'MONITOR', path: `${ROOT}/MONITOR`, port: 3117,
    cmd: 'node', args: ['server.mjs'], tech: 'Express', stack: ['Node.js 22', 'Express 5', 'SSE'],
    desc: 'Signal Intelligence Terminal — 34 OSINT sources, LLM briefs, causal analysis',
    commands: [
      { cmd: 'node server.mjs', desc: 'Start dashboard on :3117' },
      { cmd: 'npm start', desc: 'Same via npm script' },
    ]},
  { id: 'ngrobot', name: 'NG-ROBOT', path: `${ROOT}/NG-ROBOT`, port: 5001,
    cmd: 'python', args: ['ngrobot_web.py'], tech: 'Flask', stack: ['Python', 'Flask', 'Claude API'],
    desc: 'Article translation pipeline — 10-phase Claude workflow, RSS, GDrive sync',
    commands: [
      { cmd: 'python ngrobot_web.py', desc: 'Start web UI on :5001' },
      { cmd: 'python run_server.py', desc: 'Watchdog — auto-restart on crash' },
      { cmd: 'python ngrobot.py --article URL', desc: 'Process single article (CLI)' },
    ]},
  { id: 'preklad', name: 'PREKLAD', path: `${ROOT}/PREKLAD`, port: 8507,
    cmd: 'python', args: ['-m', 'uvicorn', 'preklad.api.app:app', '--host', '127.0.0.1', '--port', '8507'],
    tech: 'FastAPI + HTMX', stack: ['Python', 'FastAPI', 'HTMX', 'python-docx', 'pdfplumber', 'Anthropic SDK'],
    desc: 'RTT translation pipeline EN→CZ — PDF/DOCX input, 8-phase Claude workflow, side-by-side DOCX output',
    commands: [
      { cmd: 'python -m uvicorn preklad.api.app:app --host 127.0.0.1 --port 8507', desc: 'Start web UI on :8507' },
      { cmd: 'python -m preklad', desc: 'Start via module entry (uses API_PORT env, default 8000)' },
      { cmd: 'pytest tests/', desc: 'Run unit tests' },
    ]},
  { id: 'adobe', name: 'ADOBE-AUTOMAT', path: `${ROOT}/ADOBE-AUTOMAT`, port: 8100,
    extraPorts: [{ port: 5173, label: 'UI' }],
    cmd: 'python', args: ['-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8100'],
    startCwd: `${ROOT}/ADOBE-AUTOMAT/backend`,
    tech: 'FastAPI + Svelte', stack: ['Python', 'FastAPI', 'Svelte 5', 'Tailwind 4', 'Adobe MCP'],
    desc: 'NGM Localizer — magazine localization, map text extraction, Adobe automation',
    commands: [
      { cmd: 'uvicorn main:app --host 127.0.0.1 --port 8100', desc: 'Start API backend (from backend/)' },
      { cmd: 'npm run dev', desc: 'Start Svelte frontend on :5173 (from frontend/)' },
      { cmd: 'npm run build', desc: 'Production frontend build' },
    ]},
  { id: 'grafik', name: 'GRAFIK', path: `${ROOT}/GRAFIK`, port: 8300,
    extraPorts: [{ port: 8503, label: 'UI' }],
    cmd: 'python', args: ['-m', 'uvicorn', 'grafik.api.app:app', '--port', '8300', '--host', '127.0.0.1'],
    tech: 'FastAPI + Streamlit', stack: ['Python', 'FastAPI', 'Streamlit', 'fal.ai', 'Pillow'],
    desc: 'Modular layered image editor — Qwen-Image-Layered, layer decomposition, map localization',
    commands: [
      { cmd: 'uvicorn grafik.api.app:app --port 8300', desc: 'Start API on :8300' },
      { cmd: 'streamlit run ui/app.py --server.port 8503', desc: 'Start Streamlit UI on :8503' },
      { cmd: 'grafik serve --port 8300', desc: 'Start via CLI' },
      { cmd: 'grafik decompose input.png --out layers/', desc: 'Decompose image to layers' },
    ]},
  { id: 'kartograf', name: 'KARTOGRAF', path: `${ROOT}/KARTOGRAF`, port: 8080,
    cmd: 'python', args: ['-m', 'kartograf.cli', 'serve', '--preset', 'krkonose'], tech: 'Python', stack: ['Python', 'MapLibre GL', 'rasterio', 'geopandas'],
    desc: 'Cartographic map generator — Copernicus DEM, Natural Earth, OSM, web + PNG output',
    commands: [
      { cmd: 'python -m kartograf.cli serve --preset krkonose', desc: 'Start web map on :8080' },
      { cmd: 'python -m kartograf.cli render --preset krkonose -o map.png', desc: 'Render static PNG' },
    ]},
  { id: 'polybot', name: 'POLYBOT', path: `${ROOT}/POLYBOT`, port: 8501,
    cmd: 'uv', args: ['run', 'python', '-m', 'polybot.dashboard'], tech: 'Streamlit', stack: ['Python', 'FastMCP', 'Streamlit', 'httpx'],
    desc: 'Polymarket prediction market — paper trading, MCP server for Claude, Streamlit dashboard',
    commands: [
      { cmd: 'uv run python -m polybot.dashboard', desc: 'Start Streamlit dashboard on :8501' },
      { cmd: 'uv run python -m polybot.server', desc: 'Start MCP server (stdio)' },
    ]},
  { id: 'ftip', name: 'FTIP', path: `${ROOT}/FTIP`, port: 3000,
    cmd: 'npm', args: ['run', 'dev'], tech: 'Next.js', stack: ['Next.js 16', 'React 19', 'Anthropic SDK'],
    desc: 'Humor generator — AI-powered joke creation with Anthropic SDK',
    commands: [
      { cmd: 'npm run dev', desc: 'Start Next.js dev server on :3000' },
      { cmd: 'npm run build && npm start', desc: 'Production build + start' },
    ]},
  { id: 'orakulum', name: 'ORAKULUM', path: `${ROOT}/ORAKULUM`, port: 8000,
    cmd: 'python', args: ['-m', 'uvicorn', 'orakulum.serve.app:create_app', '--factory', '--port', '8000'], tech: 'FastAPI', stack: ['Python', 'FastAPI', 'scikit-learn', 'Tigramite'],
    desc: 'Prediction & correlation engine — anomaly detection, causal inference, shared by MONITOR/POLYBOT',
    commands: [
      { cmd: 'uvicorn orakulum.serve.app:create_app --factory --port 8000', desc: 'Start API on :8000' },
      { cmd: 'orakulum', desc: 'CLI interface' },
    ]},
  { id: 'zachvev', name: 'ZACHVEV', path: `${ROOT}/ZACHVEV`, port: 8502,
    extraPorts: [{ port: 8001, label: 'API' }],
    cmd: 'python', args: ['-m', 'streamlit', 'run', 'ui/app.py', '--server.port', '8502'], tech: 'Streamlit + FastAPI', stack: ['Python', 'Streamlit', 'FastAPI', 'DistilBERT', 'HDBSCAN'],
    desc: 'Opinion avalanche detection — Reddit narrative cascades, EWS, CRI index, embedding clustering',
    commands: [
      { cmd: 'streamlit run ui/app.py --server.port 8502', desc: 'Start Streamlit UI on :8502' },
      { cmd: 'uvicorn zachvev.api.app:app --port 8001', desc: 'Start API on :8001 (ORAKULUM uses :8000)' },
    ]},
  { id: 'rozhovor', name: 'ROZHOVOR', path: `${ROOT}/ROZHOVOR`, port: 8504,
    cmd: 'python', args: ['-m', 'streamlit', 'run', 'ui/app.py', '--server.port', '8504'], tech: 'Streamlit', stack: ['Python', 'Streamlit', 'VibeVoice-ASR', 'Whisper', 'Claude API'],
    desc: 'Audio transcription + AI processing — 8 modes (summary, key points, speakers, Q&A...)',
    commands: [
      { cmd: 'streamlit run ui/app.py --server.port 8504', desc: 'Start transcription UI on :8504' },
    ]},
  { id: 'dane', name: 'DANE', path: `${ROOT}/DANE`, port: 8505,
    cmd: 'python', args: ['-m', 'streamlit', 'run', 'ui/app.py', '--server.port', '8505'], tech: 'Streamlit', stack: ['Python', 'Streamlit', 'Pydantic', 'PyMuPDF', 'Claude API'],
    desc: 'Czech tax calculator — automated 2025 tax return for FO (employees, OSVČ, rental)',
    commands: [
      { cmd: 'streamlit run ui/app.py --server.port 8505', desc: 'Start tax calculator UI on :8505' },
    ]},
  { id: 'biolib', name: 'BIOLIB', path: `${ROOT}/BIOLIB`, port: null,
    cmd: null, args: [], tech: 'Python + SQLite', stack: ['Python', 'SQLite', 'species_names.db', 'termdb.db'],
    desc: 'Biological species database — 747MB terminology DB, used by ADOBE-AUTOMAT and KARTOGRAF',
    commands: [
      { cmd: 'python scraper.py', desc: 'Scrape BioLib species data' },
      { cmd: 'ngm-term lookup "Cervus elaphus"', desc: 'Term lookup (via ngm-terminology)' },
    ]},
  { id: 'sokrates', name: 'SOKRATES', path: `${ROOT}/SOKRATES`, port: 3401,
    cmd: 'node', args: ['--watch', 'server.mjs'], tech: 'Express', stack: ['Node.js', 'Express 5', 'Anthropic SDK', 'SSE'],
    desc: 'Multi-agent Socratic dialogue — 7 philosophers debate events in 4 phases (Aporie → Syntéza)',
    commands: [
      { cmd: 'node server.mjs', desc: 'Start server on :3401' },
      { cmd: 'node --watch server.mjs', desc: 'Start with auto-reload (dev)' },
    ]},
  { id: 'petra', name: 'PETRA', path: `${ROOT}/PETRA`, port: 8506,
    cmd: 'python', args: ['app.py'], tech: 'Flask', stack: ['Python', 'Flask', 'openpyxl', 'Excel VBA'],
    desc: 'Lead time splitter — supplier delivery data processing (AEV, BTL, EATON, SAFIRAL, TYCO)',
    commands: [
      { cmd: 'python app.py', desc: 'Start web UI on :8506' },
      { cmd: 'python split_leadtime.py <input.xlsx>', desc: 'CLI split by supplier' },
      { cmd: 'python create_macro_workbook.py', desc: 'Create VBA macro workbook' },
    ]},
];

// ─── Process Tracking ────────────────────────────────────────────────
const processes = new Map(); // id → { pid, child, log[] }

function spawnProject(proj) {
  const child = spawn(proj.cmd, proj.args, {
    cwd: proj.startCwd || proj.path,
    detached: true,
    stdio: ['ignore', 'pipe', 'pipe'],
    shell: true,
    windowsHide: true,
    env: { ...process.env, PORT: String(proj.port) },
  });
  const log = [];
  const collect = stream => {
    if (!stream) return;
    stream.setEncoding('utf8');
    stream.on('data', chunk => {
      log.push(chunk);
      if (log.length > 50) log.shift();
    });
  };
  collect(child.stdout);
  collect(child.stderr);
  child.on('exit', (code) => {
    log.push(`[process exited with code ${code}]`);
  });
  child.unref();
  processes.set(proj.id, { pid: child.pid, child, log });
  return child;
}

function checkPort(port) {
  return new Promise(resolve => {
    const sock = createConnection({ host: '127.0.0.1', port }, () => {
      sock.destroy();
      resolve(true);
    });
    sock.on('error', () => resolve(false));
    sock.setTimeout(1000, () => { sock.destroy(); resolve(false); });
  });
}

function findPidOnPort(port) {
  try {
    const out = execSync(`netstat -ano | findstr :${port} | findstr LISTENING`,
      { encoding: 'utf-8', ...EXEC_OPTS });
    const lines = out.trim().split('\n');
    for (const line of lines) {
      const parts = line.trim().split(/\s+/);
      const pid = parseInt(parts[parts.length - 1], 10);
      if (pid > 0) return pid;
    }
  } catch { /* no process on port */ }
  return null;
}

function killPid(pid) {
  try {
    execSync(`taskkill /PID ${pid} /T /F`,
      { encoding: 'utf-8', ...EXEC_OPTS, timeout: 10000 });
    return true;
  } catch { return false; }
}

// ─── Express App ─────────────────────────────────────────────────────
const app = express();
app.use(express.json());
app.use(express.static(join(__dirname, 'dashboard/public')));

// GET /api/projects — list all with live status
// Only does TCP port check (no shell commands), PID lookup is lazy
app.get('/api/projects', async (req, res) => {
  const results = await Promise.all(PROJECTS.map(async p => {
    const mainRunning = p.port ? await checkPort(p.port) : false;
    // Check secondary ports too
    let portStatus = null;
    if (p.extraPorts) {
      portStatus = {};
      for (const pp of p.extraPorts) {
        portStatus[pp.label] = await checkPort(pp.port);
      }
    }
    const tracked = processes.get(p.id);
    return { ...p, running: mainRunning, portStatus, pid: tracked?.pid || null };
  }));
  res.json(results);
});

// GET /api/projects/:id/pid — lazy PID lookup (only when needed)
app.get('/api/projects/:id/pid', (req, res) => {
  const proj = PROJECTS.find(p => p.id === req.params.id);
  if (!proj) return res.status(404).json({ error: 'Project not found' });
  const pid = processes.get(proj.id)?.pid || findPidOnPort(proj.port);
  res.json({ pid });
});

// POST /api/projects/:id/start
app.post('/api/projects/:id/start', async (req, res) => {
  const proj = PROJECTS.find(p => p.id === req.params.id);
  if (!proj) return res.status(404).json({ error: 'Project not found' });

  if (!proj.cmd) return res.status(400).json({ error: 'No server command (CLI-only project)' });

  const running = await checkPort(proj.port);
  if (running) return res.status(409).json({ error: 'Already running', port: proj.port });

  try {
    const child = spawnProject(proj);
    res.json({ ok: true, pid: child.pid });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/projects/:id/stop
app.post('/api/projects/:id/stop', async (req, res) => {
  const proj = PROJECTS.find(p => p.id === req.params.id);
  if (!proj) return res.status(404).json({ error: 'Project not found' });

  const tracked = processes.get(proj.id);
  let pid = tracked?.pid || findPidOnPort(proj.port);

  if (!pid) return res.status(404).json({ error: 'No process found' });

  const killed = killPid(pid);
  if (killed) processes.delete(proj.id);
  res.json({ ok: killed, pid });
});

// POST /api/projects/:id/restart
app.post('/api/projects/:id/restart', async (req, res) => {
  const proj = PROJECTS.find(p => p.id === req.params.id);
  if (!proj) return res.status(404).json({ error: 'Project not found' });

  const pid = processes.get(proj.id)?.pid || findPidOnPort(proj.port);
  if (pid) killPid(pid);
  processes.delete(proj.id);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const child = spawnProject(proj);
    res.json({ ok: true, pid: child.pid });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/projects/:id/log — process stdout/stderr
app.get('/api/projects/:id/log', (req, res) => {
  const tracked = processes.get(req.params.id);
  if (!tracked) return res.json({ log: [] });
  res.json({ log: tracked.log.slice(-30) });
});

// GET /api/projects/:id/git-log
app.get('/api/projects/:id/git-log', (req, res) => {
  const proj = PROJECTS.find(p => p.id === req.params.id);
  if (!proj) return res.status(404).json({ error: 'Project not found' });

  try {
    const raw = execSync('git log --oneline -50 --no-color',
      { cwd: proj.path, ...EXEC_OPTS, timeout: 10000 });
    const out = fixEncoding(raw);
    const commits = out.trim().split('\n').filter(Boolean).map(line => {
      const [hash, ...rest] = line.split(' ');
      return { hash, message: rest.join(' ') };
    });
    res.json(commits);
  } catch {
    res.json([]);
  }
});

// GET /api/activity — aggregated git log across all projects (30 days)
app.get('/api/activity', (req, res) => {
  const since = new Date(Date.now() - 30 * 86400000).toISOString().split('T')[0];
  const activity = [];

  for (const proj of PROJECTS) {
    try {
      const raw = execSync(
        `git log --since="${since}" --pretty=format:"%H|%aI|%s" --shortstat --no-color`,
        { cwd: proj.path, ...EXEC_OPTS, timeout: 10000 }
      );
      const out = fixEncoding(raw);
      const lines = out.trim().split('\n');
      let current = null;
      for (const line of lines) {
        if (line.includes('|')) {
          const [hash, date, ...msgParts] = line.split('|');
          const message = msgParts.join('|');
          current = { project: proj.id, name: proj.name, hash, date, message, files: 0, insertions: 0, deletions: 0 };
          activity.push(current);
        } else if (current && line.trim()) {
          const filesMatch = line.match(/(\d+) files? changed/);
          const insMatch = line.match(/(\d+) insertions?/);
          const delMatch = line.match(/(\d+) deletions?/);
          if (filesMatch) current.files = parseInt(filesMatch[1]);
          if (insMatch) current.insertions = parseInt(insMatch[1]);
          if (delMatch) current.deletions = parseInt(delMatch[1]);
        }
      }
    } catch { /* skip projects without git */ }
  }

  activity.sort((a, b) => b.date.localeCompare(a.date));
  res.json(activity);
});

// GET /api/projects/:id/wiki — read CLAUDE.md from project
app.get('/api/projects/:id/wiki', (req, res) => {
  const proj = PROJECTS.find(p => p.id === req.params.id);
  if (!proj) return res.status(404).json({ error: 'Project not found' });

  // Find CLAUDE.md — check project root, then parent (for subprojects like adobe-be/fe)
  const candidates = [
    join(proj.path, 'CLAUDE.md'),
    join(proj.path, '..', 'CLAUDE.md'),
    join(proj.path, 'README.md'),
  ];

  for (const p of candidates) {
    if (existsSync(p)) {
      try {
        const content = readFileSync(p, 'utf8');
        return res.json({ content, source: p });
      } catch { /* try next */ }
    }
  }
  res.json({ content: null, source: null });
});

// ─── Cloud Agents Proxy (:9100) ──────────────────────────────────────

const AGENTS_API = 'http://127.0.0.1:9100';

async function agentProxy(path, req, res) {
  try {
    const url = `${AGENTS_API}${path}`;
    const opts = { method: req.method, headers: { 'Content-Type': 'application/json' } };
    if (req.method === 'POST') opts.body = JSON.stringify(req.body);
    const resp = await fetch(url, opts);
    const data = await resp.json();
    res.status(resp.status).json(data);
  } catch {
    res.status(503).json({ error: 'Agent service not running' });
  }
}

app.get('/api/agents', (req, res) => agentProxy('/api/agents', req, res));
app.get('/api/agents/:name', (req, res) => agentProxy(`/api/agents/${req.params.name}`, req, res));
app.post('/api/agents/:name/run', (req, res) => agentProxy(`/api/agents/${req.params.name}/run`, req, res));
app.get('/api/agents/:name/runs', (req, res) => agentProxy(`/api/agents/${req.params.name}/runs`, req, res));
app.post('/api/agents/:name/toggle', (req, res) => agentProxy(`/api/agents/${req.params.name}/toggle`, req, res));
app.get('/api/costs', (req, res) => agentProxy('/api/costs', req, res));

// ─── Start ───────────────────────────────────────────────────────────
app.listen(PORT, '127.0.0.1', () => {
  console.log(`STOPA Command Center → http://127.0.0.1:${PORT}`);
});
