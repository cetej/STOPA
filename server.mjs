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
  { id: 'adobe', name: 'ADOBE-AUTOMAT', path: `${ROOT}/ADOBE-AUTOMAT`, port: 8100,
    extraPorts: [{ port: 5173, label: 'UI' }],
    cmd: 'uvicorn', args: ['main:app', '--host', '127.0.0.1', '--port', '8100'],
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
    cmd: 'uvicorn', args: ['grafik.api.app:app', '--port', '8300', '--host', '127.0.0.1'],
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
    cmd: 'uvicorn', args: ['orakulum.serve.app:create_app', '--factory', '--port', '8000'], tech: 'FastAPI', stack: ['Python', 'FastAPI', 'scikit-learn', 'Tigramite'],
    desc: 'Prediction & correlation engine — anomaly detection, causal inference, shared by MONITOR/POLYBOT',
    commands: [
      { cmd: 'uvicorn orakulum.serve.app:create_app --factory --port 8000', desc: 'Start API on :8000' },
      { cmd: 'orakulum', desc: 'CLI interface' },
    ]},
  { id: 'zachvev', name: 'ZACHVEV', path: `${ROOT}/ZACHVEV`, port: 8502,
    extraPorts: [{ port: 8001, label: 'API' }],
    cmd: 'streamlit', args: ['run', 'ui/app.py', '--server.port', '8502'], tech: 'Streamlit + FastAPI', stack: ['Python', 'Streamlit', 'FastAPI', 'DistilBERT', 'HDBSCAN'],
    desc: 'Opinion avalanche detection — Reddit narrative cascades, EWS, CRI index, embedding clustering',
    commands: [
      { cmd: 'streamlit run ui/app.py --server.port 8502', desc: 'Start Streamlit UI on :8502' },
      { cmd: 'uvicorn zachvev.api.app:app --port 8001', desc: 'Start API on :8001 (ORAKULUM uses :8000)' },
    ]},
  { id: 'rozhovor', name: 'ROZHOVOR', path: `${ROOT}/ROZHOVOR`, port: 8504,
    cmd: 'streamlit', args: ['run', 'ui/app.py', '--server.port', '8504'], tech: 'Streamlit', stack: ['Python', 'Streamlit', 'VibeVoice-ASR', 'Whisper', 'Claude API'],
    desc: 'Audio transcription + AI processing — 8 modes (summary, key points, speakers, Q&A...)',
    commands: [
      { cmd: 'streamlit run ui/app.py --server.port 8504', desc: 'Start transcription UI on :8504' },
    ]},
  { id: 'dane', name: 'DANE', path: `${ROOT}/DANE`, port: 8505,
    cmd: 'streamlit', args: ['run', 'ui/app.py', '--server.port', '8505'], tech: 'Streamlit', stack: ['Python', 'Streamlit', 'Pydantic', 'PyMuPDF', 'Claude API'],
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
];

// ─── Process Tracking ────────────────────────────────────────────────
const processes = new Map(); // id → { pid, child }

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
    const child = spawn(proj.cmd, proj.args, {
      cwd: proj.startCwd || proj.path,
      detached: true,
      stdio: 'ignore',
      shell: true,
      windowsHide: true,
      env: { ...process.env, PORT: String(proj.port) },
    });
    child.unref();
    processes.set(proj.id, { pid: child.pid, child });
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
    const child = spawn(proj.cmd, proj.args, {
      cwd: proj.startCwd || proj.path,
      detached: true,
      stdio: 'ignore',
      shell: true,
      windowsHide: true,
      env: { ...process.env, PORT: String(proj.port) },
    });
    child.unref();
    processes.set(proj.id, { pid: child.pid, child });
    res.json({ ok: true, pid: child.pid });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
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

// ─── Start ───────────────────────────────────────────────────────────
app.listen(PORT, '127.0.0.1', () => {
  console.log(`STOPA Command Center → http://127.0.0.1:${PORT}`);
});
