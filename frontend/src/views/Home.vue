<template>
  <div class="home-container">
    <!-- Top navigation -->
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-icon">&#x25C7;</span>
          MIROFISH
        </router-link>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Dashboard</router-link>
        <a href="https://github.com/666ghj/MiroFish" target="_blank" class="github-link">
          Github <span class="arrow">&#x2197;</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- Hero section -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="accent-tag">Swarm Intelligence Engine</span>
            <span class="version-text">/ v0.1-preview</span>
          </div>

          <h1 class="main-title">
            Upload Any Report<br>
            <span class="gradient-text">Simulate the Future</span>
          </h1>

          <div class="hero-desc">
            <p>
              Even from a single paragraph, <span class="highlight-bold">MiroFish</span> extracts real-world seeds to auto-generate parallel worlds with up to <span class="highlight-accent">1M+ Agents</span>. Inject variables from a god's-eye view and find <span class="highlight-code">"local optima"</span> in complex group interactions.
            </p>
            <p class="slogan-text">
              Let the future rehearse among agents, let decisions emerge from battle-tested simulations<span class="blinking-cursor">_</span>
            </p>
          </div>

          <div class="decoration-square"></div>
        </div>

        <div class="hero-right">
          <!-- Logo area -->
          <div class="logo-container">
            <img src="../assets/logo/MiroFish_logo_left.jpeg" alt="MiroFish Logo" class="hero-logo" />
          </div>

          <button class="scroll-down-btn" @click="scrollToBottom">
            &#x2193;
          </button>
        </div>
      </section>

      <!-- Dashboard two-column layout -->
      <section class="dashboard-section">
        <!-- Left panel: status & steps -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">&#x25A0;</span> System Status
          </div>

          <h2 class="section-title">Ready</h2>
          <p class="section-desc">
            Prediction engine standing by. Upload unstructured data to initialize simulation sequences.
          </p>

          <!-- Metric cards -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">Low Cost</div>
              <div class="metric-label">Avg $5/simulation</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">High Scale</div>
              <div class="metric-label">Up to 1M+ agents</div>
            </div>
          </div>

          <!-- Workflow steps -->
          <div class="steps-container">
            <div class="steps-header">
               <span class="diamond-icon">&#x25C7;</span> Workflow Sequence
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <span class="step-num">01</span>
                <div class="step-info">
                  <div class="step-title">Graph Build</div>
                  <div class="step-desc">Seed extraction, memory injection, and GraphRAG construction</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">02</span>
                <div class="step-info">
                  <div class="step-title">Environment Setup</div>
                  <div class="step-desc">Entity extraction, persona generation, and parameter injection</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">03</span>
                <div class="step-info">
                  <div class="step-title">Start Simulation</div>
                  <div class="step-desc">Dual-platform parallel simulation with dynamic temporal memory</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">04</span>
                <div class="step-info">
                  <div class="step-title">Report Generation</div>
                  <div class="step-desc">ReportAgent deep interaction with post-simulation environment</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">05</span>
                <div class="step-info">
                  <div class="step-title">Deep Interaction</div>
                  <div class="step-desc">Converse with any agent or the ReportAgent</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right panel: interactive console -->
        <div class="right-panel">
          <div class="console-box">
            <!-- Upload area -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">01 / Real-World Seeds</span>
                <span class="console-meta">Formats: PDF, MD, TXT</span>
              </div>

              <div
                class="upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />

                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">&#x2191;</div>
                  <div class="upload-title">Drag files to upload</div>
                  <div class="upload-hint">or click to browse</div>
                </div>

                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">&#x1F4C4;</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">&times;</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Divider -->
            <div class="console-divider">
              <span>Parameters</span>
            </div>

            <!-- Input area -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">>_ 02 / Simulation Prompt</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  placeholder="// Describe your simulation goal in natural language..."
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">Engine: MiroFish-V1.0</div>
              </div>
            </div>

            <!-- Start button -->
            <div class="console-section btn-section">
              <button
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!loading">Start Engine</span>
                <span v-else>Initializing...</span>
                <span class="btn-arrow">&rarr;</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- History database -->
      <HistoryDatabase />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'

const router = useRouter()

// Form data
const formData = ref({
  simulationRequirement: ''
})

// File list
const files = ref([])

// State
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)

// File input ref
const fileInput = ref(null)

// Can submit?
const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== '' && files.value.length > 0
})

// Trigger file input
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// Handle file select
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// Drag handlers
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return

  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// Add files
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// Remove file
const removeFile = (index) => {
  files.value.splice(index, 1)
}

// Scroll to bottom
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// Start simulation - navigate immediately, API call happens in Process page
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return

  // Store pending upload data
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(files.value, formData.value.simulationRequirement)

    // Navigate to Process page (use special ID for new project)
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  })
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: var(--color-bg);
  font-family: var(--font-body);
  color: var(--color-text);
}

/* Top navigation */
.navbar {
  height: 60px;
  background: var(--color-gray-900);
  color: var(--color-bg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  display: flex;
  align-items: center;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--color-bg);
  font-family: var(--font-mono);
  font-weight: 500;
  letter-spacing: 0.04em;
  font-size: 0.9rem;
}

.brand-icon {
  color: var(--color-accent);
  font-size: 1.1rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: var(--color-gray-400);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 400;
  letter-spacing: 0.02em;
}

.nav-link:hover {
  color: var(--color-bg);
}

.github-link {
  color: var(--color-gray-400);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 400;
  display: flex;
  align-items: center;
  gap: 4px;
}

.github-link:hover {
  color: var(--color-bg);
}

.arrow {
  font-family: sans-serif;
}

/* Main content */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Hero section */
.hero-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 80px;
  position: relative;
}

.hero-left {
  flex: 1;
  padding-right: 60px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.accent-tag {
  background: var(--color-accent);
  color: #fff;
  padding: 4px 10px;
  font-weight: 500;
  letter-spacing: 0.04em;
  font-size: 0.7rem;
  text-transform: uppercase;
}

.version-text {
  color: var(--color-text-secondary);
  font-weight: 400;
  letter-spacing: 0.5px;
}

.main-title {
  font-family: var(--font-serif);
  font-size: 4rem;
  line-height: 1.15;
  font-weight: 400;
  margin: 0 0 40px 0;
  letter-spacing: -0.02em;
  color: var(--color-text);
}

.gradient-text {
  background: linear-gradient(90deg, var(--color-accent) 0%, var(--color-teal-300) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: var(--text-base);
  line-height: 1.8;
  color: var(--color-text-secondary);
  max-width: 640px;
  margin-bottom: 50px;
  font-weight: 400;
  text-align: justify;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: var(--color-text);
  font-weight: 600;
}

.highlight-accent {
  color: var(--color-accent);
  font-weight: 600;
  font-family: var(--font-mono);
}

.highlight-code {
  background: var(--color-surface);
  padding: 2px 6px;
  border-radius: 3px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--color-text);
  font-weight: 500;
  border: 1px solid var(--color-border);
}

.slogan-text {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--color-text);
  letter-spacing: 0.01em;
  border-left: 3px solid var(--color-accent);
  padding-left: 15px;
  margin-top: 20px;
}

.blinking-cursor {
  color: var(--color-accent);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: var(--color-accent);
}

.hero-right {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}

.logo-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding-right: 40px;
}

.hero-logo {
  max-width: 500px;
  width: 100%;
  border-radius: 8px;
}

.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-accent);
  font-size: 1.2rem;
}

.scroll-down-btn:hover {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
}

/* Dashboard two-column layout */
.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid var(--color-border);
  padding-top: 60px;
  align-items: flex-start;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}

/* Left panel */
.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.status-dot {
  color: var(--color-accent);
  font-size: 0.7rem;
}

.section-title {
  font-family: var(--font-serif);
  font-size: var(--text-2xl);
  font-weight: 400;
  margin: 0 0 15px 0;
  letter-spacing: -0.01em;
}

.section-desc {
  color: var(--color-text-secondary);
  margin-bottom: 25px;
  line-height: 1.6;
  font-size: var(--text-base);
}

.metrics-row {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.metric-card {
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 20px 28px;
  min-width: 150px;
  background: var(--color-surface);
}

.metric-value {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 4px;
  color: var(--color-text);
}

.metric-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* Workflow steps */
.steps-container {
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 28px;
  background: var(--color-surface);
}

.steps-header {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--color-text-secondary);
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.diamond-icon {
  font-size: 1.1rem;
  line-height: 1;
  color: var(--color-accent);
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 18px;
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 500;
  color: var(--color-text);
  opacity: 0.25;
  font-size: 0.85rem;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 500;
  font-size: var(--text-base);
  margin-bottom: 3px;
  color: var(--color-text);
}

.step-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: 1.5;
}

/* Right panel: interactive console */
.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 6px;
  background: var(--color-bg);
}

.console-section {
  padding: 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 14px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.upload-zone {
  border: 1px dashed var(--color-border);
  border-radius: 6px;
  height: 200px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.25s var(--ease-smooth);
  background: var(--color-surface);
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  background: var(--color-card-hover);
  border-color: var(--color-border-light);
}

.upload-zone.drag-over {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 40px;
  height: 40px;
  border: 1px solid var(--color-border);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
  color: var(--color-text-faint);
  font-size: 1.1rem;
}

.upload-title {
  font-weight: 500;
  font-size: var(--text-base);
  margin-bottom: 4px;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-text-faint);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.file-list {
  width: 100%;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-item {
  display: flex;
  align-items: center;
  background: var(--color-bg);
  padding: 8px 12px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.82rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
  color: var(--color-text);
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: var(--color-text-faint);
  padding: 0 4px;
}

.remove-btn:hover {
  color: var(--color-danger);
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 8px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-border);
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.6rem;
  color: var(--color-text-faint);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.input-wrapper {
  position: relative;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-surface);
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 18px 20px;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 150px;
  color: var(--color-text);
}

.code-input::placeholder {
  color: var(--color-text-faint);
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: var(--font-mono);
  font-size: 0.6rem;
  color: var(--color-text-faint);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.start-engine-btn {
  width: 100%;
  background: var(--color-accent);
  color: #fff;
  border: none;
  padding: 18px 24px;
  font-family: var(--font-mono);
  font-weight: 500;
  font-size: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.25s var(--ease-smooth);
  letter-spacing: 0.04em;
  border-radius: 6px;
  position: relative;
  overflow: hidden;
}

.start-engine-btn:not(:disabled) {
  animation: pulse-accent 2s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: var(--color-teal-700);
  transform: translateY(-1px);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(0);
}

.start-engine-btn:disabled {
  background: var(--color-gray-200);
  color: var(--color-text-faint);
  cursor: not-allowed;
  transform: none;
}

@keyframes pulse-accent {
  0% { box-shadow: 0 0 0 0 rgba(42, 122, 91, 0.25); }
  70% { box-shadow: 0 0 0 6px rgba(42, 122, 91, 0); }
  100% { box-shadow: 0 0 0 0 rgba(42, 122, 91, 0); }
}

/* Responsive */
@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }

  .hero-section {
    flex-direction: column;
  }

  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }

  .hero-logo {
    max-width: 200px;
    margin-bottom: 20px;
  }
}
</style>
