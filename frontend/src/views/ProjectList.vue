<template>
  <div class="project-list">
    <div class="project-list-header">
      <div>
        <h1 class="project-list-title">Simulations</h1>
        <p class="project-list-subtitle">All MiroFish simulation projects</p>
      </div>
    </div>

    <div v-if="loading" class="project-grid">
      <div v-for="i in 4" :key="i" class="skeleton-card">
        <div class="skeleton-line skeleton-shimmer" style="width: 60%; height: 18px; margin-bottom: 12px;"></div>
        <div class="skeleton-line skeleton-shimmer" style="width: 40%; height: 12px; margin-bottom: 20px;"></div>
        <div class="skeleton-line skeleton-shimmer" style="width: 80%; height: 12px;"></div>
      </div>
    </div>

    <div v-else class="project-grid">
      <!-- New project card -->
      <button class="new-project-card" @click="$router.push('/')">
        <div class="new-project-icon">+</div>
        <div class="new-project-label">New Simulation</div>
        <div class="new-project-hint">Upload files to begin</div>
      </button>

      <!-- Project cards -->
      <ProjectCard
        v-for="project in projects"
        :key="project.project_id"
        :project="project"
      />
    </div>

    <div v-if="error" class="project-error">
      <p>{{ error }}</p>
      <button class="retry-btn" @click="fetchProjects">Retry</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ProjectCard from '../components/ProjectCard.vue'

const projects = ref([])
const loading = ref(true)
const error = ref('')

const fetchProjects = async () => {
  loading.value = true
  error.value = ''
  try {
    const resp = await axios.get('/api/graph/project/list')
    projects.value = resp.data.projects || resp.data || []
  } catch (e) {
    error.value = 'Failed to load projects. The API may be unavailable.'
    projects.value = []
  } finally {
    loading.value = false
  }
}

onMounted(fetchProjects)
</script>

<style scoped>
.project-list {
  max-width: 1100px;
  margin: 0 auto;
}

.project-list-header {
  margin-bottom: 32px;
}

.project-list-title {
  font-family: var(--font-serif);
  font-size: var(--text-3xl);
  font-weight: 400;
  letter-spacing: -0.02em;
  color: var(--color-text);
  margin: 0 0 4px 0;
}

.project-list-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin: 0;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

/* New project card */
.new-project-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 180px;
  border: 1px dashed var(--color-border);
  border-radius: 8px;
  background: transparent;
  cursor: pointer;
  padding: 24px;
  transition: all 0.2s var(--ease-smooth);
}

.new-project-card:hover {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
}

.new-project-icon {
  font-size: 1.5rem;
  color: var(--color-text-faint);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  transition: all 0.2s ease;
}

.new-project-card:hover .new-project-icon {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.new-project-label {
  font-weight: 500;
  font-size: var(--text-base);
  color: var(--color-text);
  margin-bottom: 4px;
}

.new-project-hint {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-text-faint);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* Skeleton */
.skeleton-card {
  min-height: 180px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 24px;
  background: var(--color-surface);
}

.skeleton-line {
  border-radius: 4px;
}

/* Error */
.project-error {
  text-align: center;
  padding: 40px 20px;
  color: var(--color-text-secondary);
}

.retry-btn {
  margin-top: 12px;
  padding: 8px 20px;
  background: var(--color-accent);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-family: var(--font-body);
  font-size: var(--text-sm);
  cursor: pointer;
}

.retry-btn:hover {
  opacity: 0.9;
}
</style>
