// 2BRAIN Knowledge Graph — D3.js Force Layout
function renderGraph(data) {
  const container = document.getElementById('graph-container');
  if (!container) return;

  const width = container.clientWidth;
  const height = container.clientHeight;

  container.innerHTML = '';

  const colors = {
    concept: '#3b82f6',
    person: '#22c55e',
    reasoning: '#f59e0b',
    value: '#ef4444',
    project: '#06b6d4',
    experience: '#a855f7',
    goal: '#ec4899'
  };

  // Convert graph data to D3 format
  const nodeIds = Object.keys(data.nodes);
  const nodes = nodeIds.map(id => ({
    id,
    label: data.nodes[id].label,
    type: data.nodes[id].type,
    wiki: data.nodes[id].wiki,
    r: data.nodes[id].wiki ? 10 : 7
  }));

  const nodeMap = new Map(nodes.map(n => [n.id, n]));

  const links = data.edges
    .filter(e => nodeMap.has(e.from) && nodeMap.has(e.to))
    .map(e => ({
      source: e.from,
      target: e.to,
      rel: e.rel
    }));

  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  // Zoom
  const g = svg.append('g');
  svg.call(d3.zoom()
    .scaleExtent([0.3, 4])
    .on('zoom', (event) => g.attr('transform', event.transform))
  );

  // Simulation
  const sim = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(100))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(d => d.r + 20));

  // Links
  const link = g.append('g')
    .selectAll('line')
    .data(links)
    .join('line')
    .attr('stroke', '#2a2d3a')
    .attr('stroke-width', 1.5)
    .attr('stroke-opacity', 0.6);

  // Edge labels
  const edgeLabel = g.append('g')
    .selectAll('text')
    .data(links)
    .join('text')
    .text(d => d.rel)
    .attr('font-size', 9)
    .attr('fill', '#555')
    .attr('font-family', 'JetBrains Mono')
    .attr('text-anchor', 'middle');

  // Nodes
  const node = g.append('g')
    .selectAll('g')
    .data(nodes)
    .join('g')
    .attr('class', 'graph-node')
    .style('cursor', d => d.wiki ? 'pointer' : 'default')
    .call(d3.drag()
      .on('start', (event, d) => { if (!event.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
      .on('drag', (event, d) => { d.fx = event.x; d.fy = event.y; })
      .on('end', (event, d) => { if (!event.active) sim.alphaTarget(0); d.fx = null; d.fy = null; })
    );

  node.append('circle')
    .attr('r', d => d.r)
    .attr('fill', d => colors[d.type] || '#666')
    .attr('stroke', '#0f1117')
    .attr('stroke-width', 2);

  node.append('text')
    .text(d => d.label)
    .attr('dx', d => d.r + 4)
    .attr('dy', 4)
    .attr('font-size', 11)
    .attr('fill', '#e2e4e9')
    .attr('font-family', 'JetBrains Mono');

  // Click to navigate
  node.on('click', (event, d) => {
    if (d.wiki) {
      const path = d.wiki.replace('.md', '');
      location.hash = `#/wiki/${path}`;
    }
  });

  // Tooltip
  const tooltip = document.getElementById('graph-tooltip');

  node.on('mouseenter', (event, d) => {
    // Highlight connected
    const connected = new Set();
    links.forEach(l => {
      if (l.source.id === d.id) connected.add(l.target.id);
      if (l.target.id === d.id) connected.add(l.source.id);
    });

    node.select('circle').attr('opacity', n =>
      n.id === d.id || connected.has(n.id) ? 1 : 0.2
    );
    node.select('text').attr('opacity', n =>
      n.id === d.id || connected.has(n.id) ? 1 : 0.2
    );
    link.attr('stroke-opacity', l =>
      l.source.id === d.id || l.target.id === d.id ? 0.8 : 0.1
    );

    tooltip.style.display = 'block';
    tooltip.textContent = `${d.label} (${d.type})`;
    tooltip.style.left = event.pageX + 12 + 'px';
    tooltip.style.top = event.pageY - 8 + 'px';
  });

  node.on('mouseleave', () => {
    node.select('circle').attr('opacity', 1);
    node.select('text').attr('opacity', 1);
    link.attr('stroke-opacity', 0.6);
    tooltip.style.display = 'none';
  });

  // Tick
  sim.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);

    edgeLabel
      .attr('x', d => (d.source.x + d.target.x) / 2)
      .attr('y', d => (d.source.y + d.target.y) / 2);

    node.attr('transform', d => `translate(${d.x},${d.y})`);
  });
}
