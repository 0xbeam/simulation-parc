<template>
  <aside class="sidebar" :class="{ collapsed }">
    <!-- App brand -->
    <div class="sidebar-brand">
      <router-link to="/" class="brand-link">
        <span class="brand-icon">&#x25C7;</span>
        <span v-if="!collapsed" class="brand-name">MiroFish</span>
      </router-link>
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav">
      <div class="nav-section">
        <span v-if="!collapsed" class="nav-eyebrow">Navigation</span>
        <router-link to="/" class="nav-item" :class="{ active: isActive('/') }">
          <span class="nav-icon">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M2 6l6-4.5L14 6v7.5a1 1 0 01-1 1H3a1 1 0 01-1-1V6z"/>
              <path d="M6 14.5V8h4v6.5"/>
            </svg>
          </span>
          <span v-if="!collapsed" class="nav-label">Dashboard</span>
        </router-link>
      </div>

      <!-- Project steps (only when on a project route) -->
      <div v-if="projectId && !collapsed" class="nav-section">
        <span class="nav-eyebrow">Project Steps</span>
        <router-link
          v-for="step in projectSteps"
          :key="step.path"
          :to="step.path"
          class="nav-item"
          :class="{ active: isActive(step.path) }"
        >
          <span class="nav-step-num">{{ step.num }}</span>
          <span class="nav-label">{{ step.label }}</span>
        </router-link>
      </div>
    </nav>

    <!-- Collapse toggle -->
    <button class="sidebar-toggle" @click="$emit('toggle')">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
        <path v-if="!collapsed" d="M10 3L5 8l5 5" />
        <path v-else d="M6 3l5 5-5 5" />
      </svg>
    </button>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  collapsed: { type: Boolean, default: false }
})

defineEmits(['toggle'])

const route = useRoute()

const projectId = computed(() => {
  return route.params.projectId || route.params.simulationId || route.params.reportId || null
})

const projectSteps = computed(() => {
  const id = projectId.value
  if (!id) return []
  return [
    { num: '01', label: 'Graph Build', path: `/process/${id}` },
    { num: '02', label: 'Simulation', path: `/simulation/${id}` },
    { num: '03', label: 'Run', path: `/simulation/${id}/start` },
    { num: '04', label: 'Report', path: `/report/${id}` },
    { num: '05', label: 'Explore', path: `/interaction/${id}` }
  ]
})

const isActive = (path) => {
  return route.path === path
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 240px;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  z-index: 100;
  transition: width 0.25s var(--ease-smooth);
  font-family: var(--font-body);
}

.sidebar.collapsed {
  width: 56px;
}

/* Brand */
.sidebar-brand {
  height: 48px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-bottom: 1px solid var(--color-border);
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--color-text);
}

.brand-icon {
  font-size: 1.2rem;
  color: var(--color-accent);
}

.brand-name {
  font-family: var(--font-mono);
  font-weight: 500;
  font-size: 0.85rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 12px 8px;
}

.nav-section {
  margin-bottom: 16px;
}

.nav-eyebrow {
  display: block;
  font-family: var(--font-mono);
  font-size: 0.56rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 500;
  color: var(--color-text-secondary);
  padding: 4px 12px 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  text-decoration: none;
  color: var(--color-text-secondary);
  font-size: 0.85rem;
  font-weight: 400;
  transition: all 0.15s ease;
}

.nav-item:hover {
  color: var(--color-text);
  background: var(--color-card-hover);
}

.nav-item.active {
  color: var(--color-accent);
  background: var(--color-accent-light);
  font-weight: 500;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.nav-step-num {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 500;
  width: 20px;
  text-align: center;
  flex-shrink: 0;
  opacity: 0.5;
}

.nav-item.active .nav-step-num {
  opacity: 1;
  color: var(--color-accent);
}

.nav-label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Collapse toggle */
.sidebar-toggle {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  border-top: 1px solid var(--color-border);
}

.sidebar-toggle:hover {
  color: var(--color-text);
  background: var(--color-card-hover);
}
</style>
