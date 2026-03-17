<template>
  <div class="network-graph" ref="container">
    <svg ref="svg"></svg>
    <div class="graph-controls">
      <button @click="resetZoom" title="Reset zoom">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
          <path d="M3 3v5h5"/>
        </svg>
      </button>
    </div>
    <div class="graph-legend" v-if="platforms.length > 0">
      <span v-for="p in platforms" :key="p" class="legend-item">
        <span class="legend-dot" :style="{ background: platformColor(p) }"></span>
        {{ p }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  nodes: { type: Array, default: () => [] },
  edges: { type: Array, default: () => [] },
  highlightAgent: { type: String, default: null }
})

const container = ref(null)
const svg = ref(null)
let simulation = null
let zoomBehavior = null

const platforms = ref([])

const COLORS = {
  twitter: 'var(--color-accent, #2A7A5B)',
  reddit: '#B8860B',
  exchange: '#4A6FA5',
  logistics: '#8B5E3C',
  default: 'var(--color-text-secondary, #888)'
}

const platformColor = (platform) => COLORS[platform?.toLowerCase()] || COLORS.default

const resetZoom = () => {
  if (!svg.value || !zoomBehavior) return
  d3.select(svg.value).transition().duration(300).call(zoomBehavior.transform, d3.zoomIdentity)
}

const render = () => {
  if (!svg.value || !container.value) return
  if (!props.nodes.length) return

  const width = container.value.clientWidth
  const height = container.value.clientHeight || 400

  const svgEl = d3.select(svg.value)
  svgEl.selectAll('*').remove()
  svgEl.attr('width', width).attr('height', height)

  // Extract unique platforms
  const uniquePlatforms = [...new Set(props.nodes.map(n => n.platform).filter(Boolean))]
  platforms.value = uniquePlatforms

  // Create zoom group
  const g = svgEl.append('g')

  zoomBehavior = d3.zoom()
    .scaleExtent([0.2, 4])
    .on('zoom', (event) => g.attr('transform', event.transform))

  svgEl.call(zoomBehavior)

  // Build node/edge maps
  const nodeMap = new Map(props.nodes.map(n => [n.id, { ...n }]))
  const links = props.edges
    .filter(e => nodeMap.has(e.source) && nodeMap.has(e.target))
    .map(e => ({ ...e, source: e.source, target: e.target }))

  // Force simulation
  simulation = d3.forceSimulation(Array.from(nodeMap.values()))
    .force('link', d3.forceLink(links).id(d => d.id).distance(80))
    .force('charge', d3.forceManyBody().strength(-200))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(20))

  // Draw edges
  const link = g.append('g')
    .selectAll('line')
    .data(links)
    .join('line')
    .attr('stroke', 'var(--color-border, #E8E5E0)')
    .attr('stroke-width', d => Math.max(1, Math.min(3, d.weight || 1)))
    .attr('stroke-opacity', 0.6)

  // Draw nodes
  const node = g.append('g')
    .selectAll('circle')
    .data(Array.from(nodeMap.values()))
    .join('circle')
    .attr('r', d => d.id === props.highlightAgent ? 10 : 6)
    .attr('fill', d => platformColor(d.platform))
    .attr('stroke', d => d.id === props.highlightAgent ? 'var(--color-text, #111)' : 'var(--color-bg, #fff)')
    .attr('stroke-width', d => d.id === props.highlightAgent ? 2 : 1.5)
    .style('cursor', 'pointer')
    .call(drag(simulation))

  // Labels
  const label = g.append('g')
    .selectAll('text')
    .data(Array.from(nodeMap.values()))
    .join('text')
    .text(d => d.name || d.username || d.id)
    .attr('font-size', 'var(--text-xs, 10px)')
    .attr('font-family', 'var(--font-mono, monospace)')
    .attr('fill', 'var(--color-text-secondary, #888)')
    .attr('dx', 10)
    .attr('dy', 3)

  // Tooltip on hover
  node.append('title').text(d => `${d.name || d.id}\n${d.platform || ''}\n${d.profession || ''}`)

  // Tick
  simulation.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)
    node
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
    label
      .attr('x', d => d.x)
      .attr('y', d => d.y)
  })
}

function drag(sim) {
  return d3.drag()
    .on('start', (event, d) => {
      if (!event.active) sim.alphaTarget(0.3).restart()
      d.fx = d.x
      d.fy = d.y
    })
    .on('drag', (event, d) => {
      d.fx = event.x
      d.fy = event.y
    })
    .on('end', (event, d) => {
      if (!event.active) sim.alphaTarget(0)
      d.fx = null
      d.fy = null
    })
}

let resizeObserver = null

onMounted(() => {
  nextTick(render)
  resizeObserver = new ResizeObserver(() => render())
  if (container.value) resizeObserver.observe(container.value)
})

onUnmounted(() => {
  if (simulation) simulation.stop()
  if (resizeObserver) resizeObserver.disconnect()
})

watch(() => [props.nodes, props.edges, props.highlightAgent], render, { deep: true })
</script>

<style scoped>
.network-graph {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
  background: var(--color-bg, #fff);
  border: 1px solid var(--color-border, #E8E5E0);
  border-radius: 6px;
  overflow: hidden;
}

.network-graph svg {
  display: block;
  width: 100%;
  height: 100%;
}

.graph-controls {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 4px;
}

.graph-controls button {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-surface, #F6F5F2);
  border: 1px solid var(--color-border, #E8E5E0);
  border-radius: 4px;
  cursor: pointer;
  color: var(--color-text-secondary, #888);
  transition: all 0.15s ease;
}

.graph-controls button:hover {
  color: var(--color-text, #111);
  border-color: var(--color-text-secondary, #888);
}

.graph-legend {
  position: absolute;
  bottom: 8px;
  left: 8px;
  display: flex;
  gap: 12px;
  padding: 4px 8px;
  background: var(--color-bg, #fff);
  border: 1px solid var(--color-border, #E8E5E0);
  border-radius: 4px;
  font-family: var(--font-mono, monospace);
  font-size: var(--text-xs, 0.6rem);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-text-secondary, #888);
}

.legend-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 4px;
  vertical-align: middle;
}
</style>
