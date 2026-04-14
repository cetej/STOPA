// 2BRAIN SPA — Wiki Browser, Timeline, Inbox
(function () {
  let articles = [];
  let graphData = null;
  let currentView = 'wiki';
  let currentArticle = null;

  // --- Init ---
  async function init() {
    articles = await fetchJSON('/api/wiki');
    graphData = await fetchJSON('/api/graph');
    loadStats();
    renderSidebar();
    handleRoute();
    window.addEventListener('hashchange', handleRoute);
    initSearch();
  }

  async function fetchJSON(url) {
    const res = await fetch(url);
    return res.json();
  }

  async function loadStats() {
    const stats = await fetchJSON('/api/stats');
    document.getElementById('stats').textContent =
      `${stats.articles} articles \u00b7 ${stats.nodes} nodes \u00b7 ${stats.edges} edges`;
  }

  // --- Routing ---
  function handleRoute() {
    const hash = location.hash || '#/';
    const navLinks = document.querySelectorAll('.topbar nav a');
    navLinks.forEach(a => a.classList.remove('active'));

    if (hash.startsWith('#/wiki/')) {
      const path = hash.slice(7); // remove #/wiki/
      setActiveNav('wiki');
      loadArticleByPath(path);
    } else if (hash === '#/graph') {
      setActiveNav('graph');
      showGraph();
    } else if (hash === '#/timeline') {
      setActiveNav('timeline');
      showTimeline();
    } else if (hash === '#/inbox') {
      setActiveNav('inbox');
      showInbox();
    } else {
      setActiveNav('wiki');
      showWelcome();
    }
  }

  function setActiveNav(view) {
    currentView = view;
    document.querySelectorAll('.topbar nav a').forEach(a => {
      a.classList.toggle('active', a.dataset.view === view);
    });
    // Show/hide sidebar
    document.getElementById('sidebar').style.display =
      (view === 'graph') ? 'none' : '';
    document.querySelector('.app').style.gridTemplateColumns =
      (view === 'graph') ? '1fr' : 'var(--sidebar-w) 1fr';
  }

  // --- Sidebar ---
  function renderSidebar() {
    const sidebar = document.getElementById('sidebar');
    const grouped = {};
    for (const a of articles) {
      if (!grouped[a.category]) grouped[a.category] = [];
      grouped[a.category].push(a);
    }

    const order = ['concepts', 'reasoning', 'people', 'projects'];
    const labels = { concepts: 'Concepts', reasoning: 'Reasoning', people: 'People', projects: 'Projects' };

    let html = '';
    for (const cat of order) {
      const items = grouped[cat] || [];
      if (items.length === 0) continue;
      html += `<h3>${labels[cat]}</h3>`;
      for (const item of items) {
        html += `<a href="#/wiki/${item.path}" data-path="${item.path}">
          <span class="dot ${cat}"></span>${item.title}
        </a>`;
      }
    }
    sidebar.innerHTML = html;
  }

  function highlightSidebar(path) {
    document.querySelectorAll('.sidebar a').forEach(a => {
      a.classList.toggle('active', a.dataset.path === path);
    });
  }

  // --- Wiki Article ---
  async function loadArticleByPath(path) {
    const main = document.getElementById('main');
    try {
      const parts = path.split('/');
      if (parts.length < 2) {
        // Try to find article by slug across categories
        const found = articles.find(a => a.slug === parts[0]);
        if (found) {
          location.hash = `#/wiki/${found.path}`;
          return;
        }
        main.innerHTML = '<p>Article not found.</p>';
        return;
      }

      const data = await fetchJSON(`/api/wiki/${parts[0]}/${parts[1]}`);
      highlightSidebar(path);

      // Find related from graph
      const related = findRelated(parts[1]);

      let html = `<div class="article">${data.html}</div>`;

      if (related.length > 0) {
        html += `<div class="related"><h4>Related in Knowledge Graph</h4><div class="related-links">`;
        for (const r of related) {
          const article = articles.find(a => a.slug === r.slug);
          if (article) {
            html += `<a href="#/wiki/${article.path}">${r.label} <span style="color:var(--text-dim)">(${r.rel})</span></a>`;
          } else {
            html += `<span class="related-links" style="opacity:0.5">${r.label}</span>`;
          }
        }
        html += '</div></div>';
      }

      main.innerHTML = html;
    } catch (err) {
      main.innerHTML = `<p>Error loading article: ${err.message}</p>`;
    }
  }

  function findRelated(slug) {
    if (!graphData) return [];
    const related = [];
    for (const edge of graphData.edges) {
      if (edge.from === slug) {
        const node = graphData.nodes[edge.to];
        if (node) related.push({ slug: edge.to, label: node.label, rel: edge.rel });
      }
      if (edge.to === slug) {
        const node = graphData.nodes[edge.from];
        if (node) related.push({ slug: edge.from, label: node.label, rel: edge.rel });
      }
    }
    return related;
  }

  // --- Welcome ---
  async function showWelcome() {
    const main = document.getElementById('main');
    const [stats, health] = await Promise.all([
      fetchJSON('/api/stats'),
      fetchJSON('/api/health')
    ]);

    const statusColors = { healthy: '#22c55e', growing: '#3b82f6', warn: '#f59e0b', critical: '#ef4444' };
    const statusLabels = { healthy: 'Healthy', growing: 'Growing', warn: 'Needs attention', critical: 'Upgrade needed' };
    const statusColor = statusColors[health.status] || '#666';

    let healthHtml = '';

    if (health.triggered.length > 0) {
      healthHtml += '<div class="health-triggers">';
      for (const t of health.triggered) {
        const sevColors = { critical: '#ef4444', warn: '#f59e0b', info: '#3b82f6' };
        healthHtml += `<div class="health-trigger" style="border-left:3px solid ${sevColors[t.severity]}">
          <div class="trigger-header">
            <strong>${t.title}</strong>
            <span class="trigger-pct" style="color:${sevColors[t.severity]}">${t.pct}%</span>
          </div>
          <p>${t.description}</p>
          <div class="trigger-upgrade">${t.upgrade}</div>
        </div>`;
      }
      healthHtml += '</div>';
    }

    if (health.upcoming.length > 0) {
      healthHtml += '<div class="health-upcoming"><h4>Approaching thresholds</h4>';
      for (const t of health.upcoming) {
        healthHtml += `<div class="health-upcoming-item">
          <span class="upcoming-bar"><span class="upcoming-fill" style="width:${t.pct}%"></span></span>
          <span class="upcoming-label">${t.title}</span>
          <span class="upcoming-pct">${t.pct}%</span>
        </div>`;
      }
      healthHtml += '</div>';
    }

    main.innerHTML = `
      <div class="welcome">
        <h2>2BRAIN</h2>
        <p style="color:var(--text-dim)">Personal knowledge wiki powered by LLM compilation. Click an article in the sidebar or explore the knowledge graph.</p>
        <div class="stat-grid">
          <div class="stat-card"><div class="number">${stats.articles}</div><div class="label">Wiki Articles</div></div>
          <div class="stat-card"><div class="number">${stats.nodes}</div><div class="label">Graph Nodes</div></div>
          <div class="stat-card"><div class="number">${stats.edges}</div><div class="label">Connections</div></div>
        </div>
        <div class="health-summary">
          <div class="health-status-row">
            <span class="health-dot" style="background:${statusColor}"></span>
            <span>System: <strong style="color:${statusColor}">${statusLabels[health.status]}</strong></span>
            <span style="color:var(--text-dim);margin-left:auto">~${health.tokenEstimate.toLocaleString()} tokens &middot; ${health.costPerIngest}/ingest</span>
          </div>
          ${healthHtml}
        </div>
      </div>
    `;
  }

  // --- Graph ---
  function showGraph() {
    const main = document.getElementById('main');
    main.innerHTML = '<div id="graph-container"></div>';
    if (graphData) renderGraph(graphData);
  }

  // --- Timeline ---
  async function showTimeline() {
    const main = document.getElementById('main');
    const events = await fetchJSON('/api/timeline');
    let html = '<h2 style="font-family:DM Sans;margin-bottom:16px">Timeline</h2>';
    for (const e of events.reverse()) {
      html += `<div class="timeline-event">
        <span class="date">${e.date}</span>
        <span class="type type-${e.type}">${e.type}</span>
        <span>${e.event}</span>
      </div>`;
    }
    main.innerHTML = html;
  }

  // --- Inbox ---
  async function showInbox() {
    const main = document.getElementById('main');
    const items = await fetchJSON('/api/inbox');

    let html = `
      <h2 style="font-family:DM Sans;margin-bottom:16px">Inbox</h2>
      <div class="inbox-form">
        <select id="inbox-type">
          <option value="URL">URL</option>
          <option value="IDEA">IDEA</option>
          <option value="WATCH">WATCH</option>
        </select>
        <input type="text" id="inbox-content" placeholder="URL or idea text...">
        <button id="inbox-submit">Capture</button>
      </div>
      <div id="inbox-list">
    `;

    if (items.length === 0) {
      html += '<p style="color:var(--text-dim)">Inbox is empty. Add URLs or ideas above, or send them via Telegram.</p>';
    } else {
      for (const item of items) {
        html += `<div class="inbox-item">
          <span class="badge badge-${item.type}">${item.type}</span>
          <span>${item.content}</span>
        </div>`;
      }
    }

    html += '</div>';
    main.innerHTML = html;

    // Bind form
    document.getElementById('inbox-submit').addEventListener('click', async () => {
      const type = document.getElementById('inbox-type').value;
      const content = document.getElementById('inbox-content').value.trim();
      if (!content) return;

      await fetch('/api/inbox', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, content })
      });

      document.getElementById('inbox-content').value = '';
      showInbox(); // refresh
    });

    // Enter key
    document.getElementById('inbox-content').addEventListener('keydown', (e) => {
      if (e.key === 'Enter') document.getElementById('inbox-submit').click();
    });
  }

  // --- Search ---
  function initSearch() {
    const input = document.getElementById('search-input');
    const results = document.getElementById('search-results');
    let timeout;

    input.addEventListener('input', () => {
      clearTimeout(timeout);
      const q = input.value.trim();
      if (q.length < 2) { results.classList.remove('visible'); return; }

      timeout = setTimeout(async () => {
        const data = await fetchJSON(`/api/search?q=${encodeURIComponent(q)}`);
        if (data.length === 0) {
          results.innerHTML = '<div class="search-result"><span class="title">No results</span></div>';
        } else {
          results.innerHTML = data.map(r => `
            <div class="search-result" data-path="${r.path}">
              <div class="title">${r.title}</div>
              <div class="snippet">${r.snippet}</div>
            </div>
          `).join('');
        }
        results.classList.add('visible');

        results.querySelectorAll('.search-result[data-path]').forEach(el => {
          el.addEventListener('click', () => {
            location.hash = `#/wiki/${el.dataset.path}`;
            results.classList.remove('visible');
            input.value = '';
          });
        });
      }, 200);
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.search-box')) results.classList.remove('visible');
    });
  }

  // Start
  init();
})();
