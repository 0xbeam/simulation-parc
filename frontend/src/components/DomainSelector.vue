<template>
  <div class="domain-selector">
    <div class="selector-header">
      <h3 class="selector-title">Select Simulation Domain</h3>
      <p class="selector-subtitle">Choose the type of simulation you want to run</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner-sm"></div>
      <span>Loading domains...</span>
    </div>

    <div v-else-if="error" class="error-state">
      <span>{{ error }}</span>
      <button class="retry-btn" @click="fetchDomains">Retry</button>
    </div>

    <div v-else class="domain-cards">
      <div
        v-for="domain in domains"
        :key="domain.name"
        class="domain-card"
        :class="{ 'selected': selectedDomain === domain.name }"
        @click="selectDomain(domain.name)"
      >
        <div class="card-top">
          <span class="domain-icon">{{ domainIcon(domain.name) }}</span>
          <span class="domain-name">{{ domain.display_name }}</span>
        </div>
        <p class="domain-desc">{{ domain.description }}</p>
        <div class="platform-tags">
          <span
            v-for="platform in domain.platforms"
            :key="platform"
            class="platform-tag"
          >{{ platform }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['select'])

const domains = ref([])
const selectedDomain = ref(null)
const loading = ref(false)
const error = ref(null)

function domainIcon(name) {
  const icons = {
    social_media: '\u{1F4F1}',
    market: '\u{1F4C8}',
    supply_chain: '\u{1F69A}',
  }
  return icons[name] || '\u{1F527}'
}

function selectDomain(name) {
  selectedDomain.value = name
  emit('select', name)
}

async function fetchDomains() {
  loading.value = true
  error.value = null
  try {
    const res = await fetch('/api/domains/')
    const data = await res.json()
    if (data.success) {
      domains.value = data.domains
    } else {
      error.value = data.error || 'Failed to load domains'
    }
  } catch (e) {
    error.value = 'Network error: could not load domains'
  } finally {
    loading.value = false
  }
}

onMounted(fetchDomains)
</script>

<style scoped>
.domain-selector {
  padding: 24px;
  background-color: #FAFAFA;
}

.selector-header {
  margin-bottom: 24px;
}

.selector-title {
  font-size: 18px;
  font-weight: 600;
  color: #111;
  margin: 0 0 6px 0;
}

.selector-subtitle {
  font-size: 13px;
  color: #888;
  margin: 0;
}

.loading-state,
.error-state {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #888;
  padding: 20px 0;
}

.retry-btn {
  background: none;
  border: 1px solid #DDD;
  border-radius: 4px;
  padding: 4px 12px;
  font-size: 12px;
  cursor: pointer;
  color: #555;
}

.retry-btn:hover {
  border-color: #FF5722;
  color: #FF5722;
}

.spinner-sm {
  width: 16px;
  height: 16px;
  border: 2px solid #E0E0E0;
  border-top-color: #FF5722;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.domain-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.domain-card {
  background: #FFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.domain-card:hover {
  border-color: #CCC;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.domain-card.selected {
  border-color: #FF5722;
  box-shadow: 0 4px 12px rgba(255, 87, 34, 0.10);
}

.card-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.domain-icon {
  font-size: 22px;
  line-height: 1;
}

.domain-name {
  font-size: 15px;
  font-weight: 600;
  color: #111;
}

.domain-desc {
  font-size: 12px;
  color: #666;
  line-height: 1.5;
  margin: 0 0 14px 0;
}

.platform-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.platform-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #555;
  background: #F5F5F5;
  border: 1px solid #E8E8E8;
  border-radius: 4px;
  padding: 2px 8px;
}

.domain-card.selected .platform-tag {
  background: #FFF3E0;
  border-color: #FFCCBC;
  color: #E64A19;
}
</style>
