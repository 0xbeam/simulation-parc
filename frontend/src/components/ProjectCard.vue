<template>
  <div class="project-card card-hover" @click="navigateToProject">
    <div class="card-top">
      <h3 class="card-title">{{ project.project_name || project.name || `Project ${project.project_id}` }}</h3>
      <span v-if="domainType" class="card-badge text-eyebrow">{{ domainType }}</span>
    </div>

    <div class="card-status">
      <span class="status-dot" :class="statusClass"></span>
      <span class="status-text">{{ statusLabel }}</span>
    </div>

    <div class="card-meta">
      <span v-if="fileCount !== null" class="meta-item">
        <span class="meta-label">Files</span>
        <span class="meta-value">{{ fileCount }}</span>
      </span>
      <span v-if="lastActivity" class="meta-item">
        <span class="meta-label">Last</span>
        <span class="meta-value">{{ lastActivity }}</span>
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  project: { type: Object, required: true }
})

const router = useRouter()

const domainType = computed(() => {
  return props.project.domain_type || props.project.domain || null
})

const statusLabel = computed(() => {
  const s = props.project.status || 'unknown'
  return s.charAt(0).toUpperCase() + s.slice(1)
})

const statusClass = computed(() => {
  const s = (props.project.status || '').toLowerCase()
  if (s === 'completed' || s === 'done') return 'status-success'
  if (s === 'running' || s === 'processing') return 'status-running'
  if (s === 'error' || s === 'failed') return 'status-error'
  return 'status-idle'
})

const fileCount = computed(() => {
  return props.project.file_count ?? props.project.files?.length ?? null
})

const lastActivity = computed(() => {
  const d = props.project.updated_at || props.project.created_at
  if (!d) return null
  try {
    const date = new Date(d)
    return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
  } catch {
    return d
  }
})

const navigateToProject = () => {
  const id = props.project.project_id || props.project.id
  router.push(`/project/${id}`)
}
</script>

<style scoped>
.project-card {
  min-height: 180px;
  border: 1px solid var(--color-card-border);
  border-radius: 8px;
  padding: 24px;
  background: var(--color-card);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: background 0.2s ease, transform 0.2s var(--ease-smooth), box-shadow 0.2s ease;
}

.project-card:hover {
  background: var(--color-card-hover);
}

.card-top {
  margin-bottom: 12px;
}

.card-title {
  font-family: var(--font-serif);
  font-size: var(--text-lg);
  font-weight: 500;
  letter-spacing: -0.01em;
  color: var(--color-text);
  margin: 0 0 8px 0;
}

.card-badge {
  display: inline-block;
  padding: 2px 8px;
  border: 1px solid var(--color-border);
  border-radius: 3px;
  background: var(--color-bg);
}

.card-status {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 16px;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-success { background: var(--color-success); }
.status-running { background: var(--color-warning); animation: pulse-dot 2s ease-in-out infinite; }
.status-error { background: var(--color-danger); }
.status-idle { background: var(--color-muted); }

.status-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.card-meta {
  display: flex;
  gap: 16px;
  border-top: 1px solid var(--color-border);
  padding-top: 12px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.meta-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-text-faint);
}

.meta-value {
  font-size: var(--text-sm);
  color: var(--color-text);
  font-weight: 500;
}
</style>
