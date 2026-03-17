<template>
  <div class="activity-timeline" ref="container">
    <div class="timeline-header">
      <span class="timeline-title">Activity Timeline</span>
      <div class="timeline-filters">
        <button
          v-for="p in availablePlatforms"
          :key="p"
          :class="['filter-btn', { active: activePlatforms.has(p) }]"
          @click="togglePlatform(p)"
        >{{ p }}</button>
      </div>
    </div>
    <svg ref="svg"></svg>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick, computed } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  actions: { type: Array, default: () => [] },
  roundMinutes: { type: Number, default: 60 }
})

const container = ref(null)
const svg = ref(null)
const activePlatforms = ref(new Set())

const availablePlatforms = computed(() => {
  return [...new Set(props.actions.map(a => a.platform).filter(Boolean))]
})

const togglePlatform = (p) => {
  const s = new Set(activePlatforms.value)
  if (s.has(p)) s.delete(p)
  else s.add(p)
  activePlatforms.value = s
}

const PLATFORM_COLORS = {
  twitter: 'var(--color-accent, #2A7A5B)',
  reddit: '#B8860B',
  exchange: '#4A6FA5',
  logistics: '#8B5E3C'
}

const render = () => {
  if (!svg.value || !container.value || !props.actions.length) return

  const width = container.value.clientWidth
  const height = 200
  const margin = { top: 20, right: 20, bottom: 30, left: 50 }

  const svgEl = d3.select(svg.value)
  svgEl.selectAll('*').remove()
  svgEl.attr('width', width).attr('height', height)

  // Filter by active platforms
  const filtered = activePlatforms.value.size > 0
    ? props.actions.filter(a => activePlatforms.value.has(a.platform))
    : props.actions

  // Group actions by round
  const byRound = d3.rollup(filtered, v => v.length, d => d.round || 0)
  const data = Array.from(byRound, ([round, count]) => ({ round, count }))
    .sort((a, b) => a.round - b.round)

  if (!data.length) return

  const x = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.round)])
    .range([margin.left, width - margin.right])

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.count)])
    .nice()
    .range([height - margin.bottom, margin.top])

  // Area + line
  const area = d3.area()
    .x(d => x(d.round))
    .y0(y(0))
    .y1(d => y(d.count))
    .curve(d3.curveMonotoneX)

  const line = d3.line()
    .x(d => x(d.round))
    .y(d => y(d.count))
    .curve(d3.curveMonotoneX)

  svgEl.append('path')
    .datum(data)
    .attr('d', area)
    .attr('fill', 'var(--color-accent-light, #E8F5EE)')
    .attr('opacity', 0.5)

  svgEl.append('path')
    .datum(data)
    .attr('d', line)
    .attr('fill', 'none')
    .attr('stroke', 'var(--color-accent, #2A7A5B)')
    .attr('stroke-width', 1.5)

  // X axis
  svgEl.append('g')
    .attr('transform', `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(Math.min(data.length, 10)).tickFormat(d => `R${d}`))
    .call(g => g.select('.domain').attr('stroke', 'var(--color-border, #E8E5E0)'))
    .call(g => g.selectAll('.tick text')
      .attr('fill', 'var(--color-text-secondary, #888)')
      .attr('font-family', 'var(--font-mono, monospace)')
      .attr('font-size', '10px'))
    .call(g => g.selectAll('.tick line').attr('stroke', 'var(--color-border, #E8E5E0)'))

  // Y axis
  svgEl.append('g')
    .attr('transform', `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5))
    .call(g => g.select('.domain').remove())
    .call(g => g.selectAll('.tick text')
      .attr('fill', 'var(--color-text-secondary, #888)')
      .attr('font-family', 'var(--font-mono, monospace)')
      .attr('font-size', '10px'))
    .call(g => g.selectAll('.tick line')
      .attr('stroke', 'var(--color-border, #E8E5E0)')
      .attr('stroke-dasharray', '2,2')
      .attr('x2', width - margin.left - margin.right))
}

let resizeObserver = null

onMounted(() => {
  // Init all platforms as active
  activePlatforms.value = new Set(availablePlatforms.value)
  nextTick(render)
  resizeObserver = new ResizeObserver(() => render())
  if (container.value) resizeObserver.observe(container.value)
})

onUnmounted(() => {
  if (resizeObserver) resizeObserver.disconnect()
})

watch(() => props.actions, () => {
  if (activePlatforms.value.size === 0) {
    activePlatforms.value = new Set(availablePlatforms.value)
  }
  render()
}, { deep: true })

watch(activePlatforms, render, { deep: true })
</script>

<style scoped>
.activity-timeline {
  width: 100%;
  background: var(--color-bg, #fff);
  border: 1px solid var(--color-border, #E8E5E0);
  border-radius: 6px;
  overflow: hidden;
}

.timeline-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  border-bottom: 1px solid var(--color-border, #E8E5E0);
}

.timeline-title {
  font-family: var(--font-mono, monospace);
  font-size: var(--text-xs, 0.6rem);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-secondary, #888);
}

.timeline-filters {
  display: flex;
  gap: 4px;
}

.filter-btn {
  font-family: var(--font-mono, monospace);
  font-size: var(--text-xs, 0.56rem);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 2px 8px;
  border: 1px solid var(--color-border, #E8E5E0);
  border-radius: 3px;
  background: transparent;
  color: var(--color-text-secondary, #888);
  cursor: pointer;
  transition: all 0.15s ease;
}

.filter-btn.active {
  background: var(--color-accent, #2A7A5B);
  color: #fff;
  border-color: var(--color-accent, #2A7A5B);
}

.activity-timeline svg {
  display: block;
  width: 100%;
}
</style>
