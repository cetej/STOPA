import express from 'express';
import { readFile, readdir, appendFile, stat } from 'fs/promises';
import { join, relative, basename, extname } from 'path';
import { marked } from 'marked';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3333;

// Brain data directory
const BRAIN = join(__dirname, '..', '.claude', 'memory', 'brain');
const WIKI = join(BRAIN, 'wiki');

app.use(express.json());
app.use(express.static(join(__dirname, 'public')));

// --- API Routes ---

// List all wiki articles (parsed from filesystem)
app.get('/api/wiki', async (req, res) => {
  try {
    const categories = ['concepts', 'people', 'reasoning', 'projects'];
    const articles = [];

    for (const cat of categories) {
      const dir = join(WIKI, cat);
      try {
        const files = await readdir(dir);
        for (const f of files) {
          if (!f.endsWith('.md')) continue;
          const slug = f.replace('.md', '');
          const content = await readFile(join(dir, f), 'utf-8');
          const title = content.match(/^#\s+(.+)/m)?.[1] || slug;
          const tags = content.match(/\*\*Tags?:\*\*\s*(.+)/i)?.[1]
            || content.match(/^Tags?:\s*(.+)/mi)?.[1] || '';
          articles.push({ slug, category: cat, title, tags, path: `${cat}/${slug}` });
        }
      } catch { /* directory doesn't exist yet */ }
    }

    res.json(articles);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get single wiki article as HTML
app.get('/api/wiki/:category/:slug', async (req, res) => {
  try {
    const { category, slug } = req.params;
    const filePath = join(WIKI, category, `${slug}.md`);
    const md = await readFile(filePath, 'utf-8');

    // Convert [[wikilinks]] to clickable links — resolve to full category/slug path
    const allArticles = [];
    for (const cat of ['concepts', 'people', 'reasoning', 'projects']) {
      try {
        const files = await readdir(join(WIKI, cat));
        for (const f of files) {
          if (!f.endsWith('.md')) continue;
          const s = f.replace('.md', '');
          const content = await readFile(join(WIKI, cat, f), 'utf-8');
          const title = content.match(/^#\s+(.+)/m)?.[1] || s;
          allArticles.push({ slug: s, category: cat, title });
        }
      } catch { /* skip */ }
    }

    const linkedMd = md.replace(/\[\[([^\]]+)\]\]/g, (_, name) => {
      const needle = name.toLowerCase().replace(/\s+/g, '-');
      const match = allArticles.find(a => a.slug === needle)
        || allArticles.find(a => a.title.toLowerCase() === name.toLowerCase())
        || allArticles.find(a => a.slug.includes(needle) || needle.includes(a.slug));
      if (match) {
        return `[${name}](#/wiki/${match.category}/${match.slug})`;
      }
      return `[${name}](#/wiki/${needle})`;
    });

    const html = marked(linkedMd);
    res.json({ slug, category, markdown: md, html });
  } catch (err) {
    if (err.code === 'ENOENT') return res.status(404).json({ error: 'Article not found' });
    res.status(500).json({ error: err.message });
  }
});

// Knowledge graph
app.get('/api/graph', async (req, res) => {
  try {
    const data = await readFile(join(BRAIN, 'knowledge-graph.json'), 'utf-8');
    res.json(JSON.parse(data));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Timeline
app.get('/api/timeline', async (req, res) => {
  try {
    const md = await readFile(join(BRAIN, 'timeline.md'), 'utf-8');
    const lines = md.split('\n').filter(l => l.startsWith('|') && !l.includes('---') && !l.includes('Date'));
    const events = lines.map(line => {
      const cols = line.split('|').map(c => c.trim()).filter(Boolean);
      if (cols.length >= 4) {
        return { date: cols[0], type: cols[1], entity: cols[2], event: cols[3], learning: cols[4] || '' };
      }
      return null;
    }).filter(Boolean);
    res.json(events);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Inbox — read queue
app.get('/api/inbox', async (req, res) => {
  try {
    const md = await readFile(join(BRAIN, 'inbox.md'), 'utf-8');
    const queueMatch = md.match(/## Queue\n([\s\S]*?)## Processed/);
    const items = [];
    if (queueMatch) {
      const lines = queueMatch[1].split('\n').filter(l => l.match(/^(URL|IDEA|WATCH):/));
      for (const line of lines) {
        const match = line.match(/^(URL|IDEA|WATCH):\s*(.+?)(?:\s*<!--.*-->)?$/);
        if (match) items.push({ type: match[1], content: match[2].trim() });
      }
    }
    res.json(items);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Inbox — add item
app.post('/api/inbox', async (req, res) => {
  try {
    const { type, content } = req.body;
    if (!type || !content) return res.status(400).json({ error: 'type and content required' });
    if (!['URL', 'IDEA', 'WATCH'].includes(type)) return res.status(400).json({ error: 'type must be URL, IDEA, or WATCH' });

    const inboxPath = join(BRAIN, 'inbox.md');
    const md = await readFile(inboxPath, 'utf-8');
    const now = new Date().toISOString().slice(0, 16).replace('T', ' ');
    const entry = `${type}: ${content}  <!-- ui ${now} -->`;

    // Insert after ## Queue
    const updated = md.replace('## Queue\n', `## Queue\n${entry}\n`);
    const { writeFile } = await import('fs/promises');
    await writeFile(inboxPath, updated, 'utf-8');

    res.json({ ok: true, entry });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Search across wiki
app.get('/api/search', async (req, res) => {
  try {
    const q = (req.query.q || '').toLowerCase();
    if (!q || q.length < 2) return res.json([]);

    const categories = ['concepts', 'people', 'reasoning', 'projects'];
    const results = [];

    for (const cat of categories) {
      const dir = join(WIKI, cat);
      try {
        const files = await readdir(dir);
        for (const f of files) {
          if (!f.endsWith('.md')) continue;
          const content = await readFile(join(dir, f), 'utf-8');
          if (content.toLowerCase().includes(q)) {
            const slug = f.replace('.md', '');
            const title = content.match(/^#\s+(.+)/m)?.[1] || slug;
            // Find matching lines for snippet
            const lines = content.split('\n');
            const matchLine = lines.find(l => l.toLowerCase().includes(q) && !l.startsWith('#')) || '';
            results.push({ slug, category: cat, title, path: `${cat}/${slug}`, snippet: matchLine.slice(0, 150) });
          }
        }
      } catch { /* skip */ }
    }

    res.json(results);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Stats
app.get('/api/stats', async (req, res) => {
  try {
    const graph = JSON.parse(await readFile(join(BRAIN, 'knowledge-graph.json'), 'utf-8'));
    const nodeCount = Object.keys(graph.nodes).length;
    const edgeCount = graph.edges.length;

    let articleCount = 0;
    for (const cat of ['concepts', 'people', 'reasoning', 'projects']) {
      try {
        const files = await readdir(join(WIKI, cat));
        articleCount += files.filter(f => f.endsWith('.md')).length;
      } catch { /* skip */ }
    }

    res.json({ articles: articleCount, nodes: nodeCount, edges: edgeCount });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// --- Growth Triggers ---
// Checks brain size against thresholds and returns upgrade recommendations

const GROWTH_TIERS = [
  {
    id: 'sidebar-collapse',
    metric: 'articles',
    threshold: 50,
    severity: 'warn',
    title: 'Sidebar needs categories',
    description: 'At 50+ articles, flat sidebar becomes unusable. Add collapsible category groups or switch to search-first navigation.',
    upgrade: 'Add accordion sidebar with category collapse + article count badges'
  },
  {
    id: 'graph-canvas',
    metric: 'nodes',
    threshold: 200,
    severity: 'warn',
    title: 'Graph renderer upgrade',
    description: 'D3 SVG force layout lags above 200 nodes. Switch to Canvas or WebGL renderer (sigma.js, d3-force + canvas).',
    upgrade: 'Replace SVG renderer with Canvas-based force layout or sigma.js'
  },
  {
    id: 'graph-clustering',
    metric: 'nodes',
    threshold: 100,
    severity: 'info',
    title: 'Graph clustering available',
    description: 'With 100+ nodes, visual clustering by type improves readability. Group nodes by category with force boundaries.',
    upgrade: 'Add force-cluster by node type + toggle for flat/clustered view'
  },
  {
    id: 'search-bm25',
    metric: 'articles',
    threshold: 80,
    severity: 'warn',
    title: 'Search needs ranking',
    description: 'Substring grep degrades at 80+ articles. Implement BM25 or TF-IDF scoring for relevance-ranked results.',
    upgrade: 'Add server-side BM25 scoring (e.g. minisearch or lunr.js)'
  },
  {
    id: 'context-selective',
    metric: 'totalBytes',
    threshold: 500_000,
    severity: 'critical',
    title: 'Selective context loading needed',
    description: 'Brain data exceeds 500KB (~125K tokens). LLM operations (/ingest, /compile) should load only relevant wiki subset, not entire brain.',
    upgrade: 'Implement topic-scoped context: query graph neighbors + top-K BM25 articles instead of full brain'
  },
  {
    id: 'graph-json-cache',
    metric: 'graphBytes',
    threshold: 50_000,
    severity: 'info',
    title: 'Graph API caching',
    description: 'knowledge-graph.json over 50KB. Add ETag/Last-Modified caching to avoid re-sending on every page load.',
    upgrade: 'Add Cache-Control + ETag header to /api/graph'
  },
  {
    id: 'inbox-overflow',
    metric: 'inboxItems',
    threshold: 30,
    severity: 'warn',
    title: 'Inbox backlog growing',
    description: 'Over 30 unprocessed inbox items. Consider batch ingest or auto-triage by type.',
    upgrade: 'Add batch ingest button + auto-priority sorting (URL > IDEA > WATCH)'
  },
  {
    id: 'wiki-pagination',
    metric: 'articles',
    threshold: 150,
    severity: 'critical',
    title: 'API pagination required',
    description: 'At 150+ articles, /api/wiki loads all content into memory. Add pagination or lazy loading.',
    upgrade: 'Paginate /api/wiki (return metadata only, load content on demand)'
  },
  {
    id: 'category-rebalance',
    metric: 'maxCategorySize',
    threshold: 30,
    severity: 'info',
    title: 'Category rebalancing',
    description: 'One category has 30+ articles while others are small. Consider splitting into subcategories.',
    upgrade: 'Add subcategory support (e.g. concepts/ai/, concepts/psychology/)'
  }
];

async function measureBrain() {
  const categories = ['concepts', 'people', 'reasoning', 'projects'];
  let articles = 0;
  let totalBytes = 0;
  const catSizes = {};

  for (const cat of categories) {
    const dir = join(WIKI, cat);
    let count = 0;
    try {
      const files = await readdir(dir);
      for (const f of files) {
        if (!f.endsWith('.md')) continue;
        count++;
        const s = await stat(join(dir, f));
        totalBytes += s.size;
      }
    } catch { /* skip */ }
    catSizes[cat] = count;
    articles += count;
  }

  let nodes = 0, edges = 0, graphBytes = 0;
  try {
    const graphStat = await stat(join(BRAIN, 'knowledge-graph.json'));
    graphBytes = graphStat.size;
    totalBytes += graphBytes;
    const graph = JSON.parse(await readFile(join(BRAIN, 'knowledge-graph.json'), 'utf-8'));
    nodes = Object.keys(graph.nodes).length;
    edges = graph.edges.length;
  } catch { /* skip */ }

  let inboxItems = 0;
  try {
    const md = await readFile(join(BRAIN, 'inbox.md'), 'utf-8');
    const queueMatch = md.match(/## Queue\n([\s\S]*?)## Processed/);
    if (queueMatch) {
      inboxItems = queueMatch[1].split('\n').filter(l => l.match(/^(URL|IDEA|WATCH):/)).length;
    }
  } catch { /* skip */ }

  const maxCategorySize = Math.max(...Object.values(catSizes), 0);

  return { articles, nodes, edges, totalBytes, graphBytes, inboxItems, maxCategorySize, catSizes };
}

app.get('/api/health', async (req, res) => {
  try {
    const metrics = await measureBrain();
    const triggered = [];
    const upcoming = [];

    for (const tier of GROWTH_TIERS) {
      const value = metrics[tier.metric];
      const pct = value / tier.threshold;

      if (pct >= 1.0) {
        triggered.push({ ...tier, value, pct: Math.round(pct * 100) });
      } else if (pct >= 0.7) {
        upcoming.push({ ...tier, value, pct: Math.round(pct * 100) });
      }
    }

    const overallStatus = triggered.some(t => t.severity === 'critical') ? 'critical'
      : triggered.some(t => t.severity === 'warn') ? 'warn'
      : upcoming.length > 0 ? 'growing'
      : 'healthy';

    res.json({
      status: overallStatus,
      metrics,
      triggered,
      upcoming,
      tokenEstimate: Math.round(metrics.totalBytes / 4),
      costPerIngest: metrics.totalBytes < 200_000 ? '$0.03-0.06' : metrics.totalBytes < 500_000 ? '$0.10-0.20' : '$0.30-0.50'
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// SPA fallback (Express 5 syntax)
app.get('/{*path}', (req, res) => {
  res.sendFile(join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`2BRAIN UI running at http://localhost:${PORT}`);
  console.log(`Reading brain data from: ${BRAIN}`);
});
