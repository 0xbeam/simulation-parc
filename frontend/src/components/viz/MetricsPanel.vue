<template>
  <div class="metrics-panel">
    <div class="metric-card" v-for="metric in metrics" :key="metric.label">
      <div class="metric-value">{{ formatValue(metric.value) }}</div>
      <div class="metric-label">{{ metric.label }}</div>
      <div class="metric-delta" v-if="metric.delta" :class="metric.delta > 0 ? 'positive' : 'negative'">
        {{ metric.delta > 0 ? '+' : '' }}{{ metric.delta }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  totalAgents: { type: Number, default: 0 },
  totalActions: { type: Number, default: 0 },
  currentRound: { type: Number, default: 0 },
  maxRounds: { type: Number, default: 0 },
  elapsedTime: { type: String, default: '0:00' },
  platformStats: { type: Object, default: () => ({}) }
})

const metrics = computed(() => [
  { label: 'AGENTS', value: props.totalAgents },
  { label: 'ACTIONS', value: props.totalActions },
  { label: 'ROUND', value: `${props.currentRound}/${props.maxRounds}` },
  { label: 'ELAPSED', value: props.elapsedTime },
  ...Object.entries(props.platformStats).map(([platform, count]) => ({
    label: platform.toUpperCase(),
    value: count
  }))
])

const formatValue = (val) => {
  if (typeof val === 'number' && val >= 1000) {
    return (val / 1000).toFixed(1) + 'k'
  }
  return val
}
</script>

<style scoped>
.metrics-panel {
  display: flex;
  gap: 1px;
  background: var(--color-border, #E8E5E0);
  border: 1px solid var(--color-border, #E8E5E0);
  border-radius: 6px;
  overflow: hidden;
}

.metric-card {
  flex: 1;
  min-width: 80px;
  padding: 12px 16px;
  background: var(--color-bg, #fff);
  text-align: center;
}

.metric-value {
  font-family: var(--font-mono, 'DM Mono', monospace);
  font-size: var(--text-lg, 1.2rem);
  font-weight: 500;
  color: var(--color-text, #111);
  line-height: 1.2;
}

.metric-label {
  font-family: var(--font-mono, 'DM Mono', monospace);
  font-size: var(--text-xs, 0.6rem);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-secondary, #888);
  margin-top: 4px;
}

.metric-delta {
  font-family: var(--font-mono, 'DM Mono', monospace);
  font-size: var(--text-xs, 0.6rem);
  margin-top: 2px;
}

.metric-delta.positive { color: var(--color-success, #2A7A5B); }
.metric-delta.negative { color: var(--color-danger, #C0392B); }
</style>
