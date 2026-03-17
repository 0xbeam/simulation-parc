<template>
  <header class="topbar">
    <nav class="topbar-breadcrumb">
      <router-link to="/" class="breadcrumb-item">Dashboard</router-link>
      <template v-if="projectName">
        <span class="breadcrumb-sep">/</span>
        <span class="breadcrumb-item current">{{ projectName }}</span>
      </template>
      <template v-if="currentStep">
        <span class="breadcrumb-sep">/</span>
        <span class="breadcrumb-item current">{{ currentStep }}</span>
      </template>
    </nav>

    <div class="topbar-actions">
      <button class="topbar-icon-btn" title="Settings">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="8" cy="8" r="2.5"/>
          <path d="M13.5 8a5.5 5.5 0 01-.3 1.8l1.3.8-.9 1.5-1.3-.7a5.5 5.5 0 01-1.5 1l.1 1.5h-1.8l.1-1.5a5.5 5.5 0 01-1.5-1l-1.3.7-.9-1.5 1.3-.8A5.5 5.5 0 012.5 8a5.5 5.5 0 01.3-1.8l-1.3-.8.9-1.5 1.3.7a5.5 5.5 0 011.5-1L5.1 2.1h1.8l-.1 1.5a5.5 5.5 0 011.5 1l1.3-.7.9 1.5-1.3.8A5.5 5.5 0 0113.5 8z"/>
        </svg>
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const projectName = computed(() => {
  const id = route.params.projectId || route.params.simulationId || route.params.reportId
  if (!id) return null
  return `Project ${id}`
})

const currentStep = computed(() => {
  const path = route.path
  if (path.includes('/process/')) return 'Graph Build'
  if (path.includes('/simulation/') && path.endsWith('/start')) return 'Run'
  if (path.includes('/simulation/')) return 'Simulation'
  if (path.includes('/report/')) return 'Report'
  if (path.includes('/interaction/')) return 'Explore'
  return null
})
</script>

<style scoped>
.topbar {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-bg);
  flex-shrink: 0;
}

.topbar-breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.82rem;
}

.breadcrumb-item {
  text-decoration: none;
  color: var(--color-text-secondary);
  transition: color 0.15s ease;
}

a.breadcrumb-item:hover {
  color: var(--color-accent);
}

.breadcrumb-item.current {
  color: var(--color-text);
  font-weight: 500;
}

.breadcrumb-sep {
  color: var(--color-text-faint);
  font-size: 0.75rem;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.topbar-icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  border-radius: 6px;
  cursor: pointer;
}

.topbar-icon-btn:hover {
  color: var(--color-text);
  background: var(--color-surface);
}
</style>
