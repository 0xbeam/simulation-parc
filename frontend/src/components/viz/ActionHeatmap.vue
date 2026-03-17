<template>
  <div class="action-heatmap" ref="container">
    <div class="heatmap-header">
      <span class="heatmap-title">Action Frequency</span>
    </div>
    <svg ref="svg"></svg>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  actions: { type: Array, default: () => [] },
  maxRounds: { type: Number, default: 10 }
})

const container = ref(null)
const svg = ref(null)

const render = () => {
  if (!svg.value || !container.value || !props.actions.length) return

  const width = container.value.clientWidth
  const margin = { top: 10, right: 20, bottom: 40, left: 100 }

  const svgEl = d3.select(svg.value)
  svgEl.selectAll('*').remove()

  // Get unique action types and rounds
  const actionTypes = [...new Set(props.actions.map(a => a.action_type || a.type).filter(Boolean))]
  const maxRound = Math.max(props.maxRounds, d3.max(props.actions, d => d.round || 0) || 0)
  const rounds = d3.range(0, maxRound + 1)

  if (!actionTypes.length) return

  const cellSize = Math.max(16, Math.min(28, (width - margin.left - margin.right) / rounds.length))
  const height = margin.top + actionTypes.length * cellSize + margin.bottom

  svgEl.attr('width', width).attr('height', height)

  // Build count matrix
  const counts = d3.rollup(
    props.actions,
    v => v.length,
    d => d.action_type || d.type,
    d => d.round || 0
  )

  const maxCount = d3.max(props.actions, () => {
    let m = 0
    for (const [, byRound] of counts) {
      for (const [, c] of byRound) {
        if (c > m) m = c
      }
    }
    return m
  }) || 1

  // Recompute max properly
  let realMax = 0
  for (const [, byRound] of counts) {
    for (const [, c] of byRound) {
      if (c > realMax) realMax = c
    }
  }

  const colorScale = d3.scaleSequential()
    .domain([0, realMax || 1])
    .interpolator(d3.interpolateGreens)

  const x = d3.scaleBand()
    .domain(rounds)
    .range([margin.left, margin.left + rounds.length * cellSize])
    .padding(0.05)

  const y = d3.scaleBand()
    .domain(actionTypes)
    .range([margin.top, margin.top + actionTypes.length * cellSize])
    .padding(0.05)

  // Draw cells
  for (const actionType of actionTypes) {
    for (const round of rounds) {
      const count = counts.get(actionType)?.get(round) || 0
      svgEl.append('rect')
        .attr('x', x(round))
        .attr('y', y(actionType))
        .attr('width', x.bandwidth())
        .attr('height', y.bandwidth())
        .attr('rx', 2)
        .attr('fill', count > 0 ? colorScale(count) : 'var(--color-surface, #F6F5F2)')
        .attr('stroke', 'var(--color-bg, #fff)')
        .attr('stroke-width', 1)
        .append('title')
        .text(`${actionType} · Round ${round}: ${count}`)
    }
  }

  // Y axis (action types)
  svgEl.append('g')
    .attr('transform', `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).tickSize(0))
    .call(g => g.select('.domain').remove())
    .call(g => g.selectAll('.tick text')
      .attr('fill', 'var(--color-text-secondary, #888)')
      .attr('font-family', 'var(--font-mono, monospace)')
      .attr('font-size', '9px')
      .attr('text-anchor', 'end'))

  // X axis (rounds)
  const xAxis = d3.axisBottom(x).tickSize(0)
    .tickValues(rounds.filter((_, i) => i % Math.max(1, Math.floor(rounds.length / 10)) === 0))
    .tickFormat(d => `R${d}`)

  svgEl.append('g')
    .attr('transform', `translate(0,${margin.top + actionTypes.length * cellSize})`)
    .call(xAxis)
    .call(g => g.select('.domain').remove())
    .call(g => g.selectAll('.tick text')
      .attr('fill', 'var(--color-text-secondary, #888)')
      .attr('font-family', 'var(--font-mono, monospace)')
      .attr('font-size', '9px'))
}

let resizeObserver = null

onMounted(() => {
  nextTick(render)
  resizeObserver = new ResizeObserver(() => render())
  if (container.value) resizeObserver.observe(container.value)
})

onUnmounted(() => {
  if (resizeObserver) resizeObserver.disconnect()
})

watch(() => props.actions, render, { deep: true })
</script>

<style scoped>
.action-heatmap {
  width: 100%;
  background: var(--color-bg, #fff);
  border: 1px solid var(--color-border, #E8E5E0);
  border-radius: 6px;
  overflow: hidden;
}

.heatmap-header {
  padding: 10px 16px;
  border-bottom: 1px solid var(--color-border, #E8E5E0);
}

.heatmap-title {
  font-family: var(--font-mono, monospace);
  font-size: var(--text-xs, 0.6rem);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-secondary, #888);
}

.action-heatmap svg {
  display: block;
  width: 100%;
}
</style>
