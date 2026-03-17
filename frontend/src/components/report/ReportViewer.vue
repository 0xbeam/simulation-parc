<template>
  <div class="report-viewer">
    <!-- Table of Contents sidebar -->
    <aside class="report-toc" v-if="sections.length > 0">
      <div class="toc-header">Contents</div>
      <nav class="toc-nav">
        <a
          v-for="(section, idx) in sections"
          :key="idx"
          :class="['toc-item', { active: activeSection === idx }]"
          @click="scrollToSection(idx)"
        >
          <span class="toc-number">{{ String(idx + 1).padStart(2, '0') }}</span>
          <span class="toc-title">{{ section.title }}</span>
        </a>
      </nav>
    </aside>

    <!-- Report content -->
    <main class="report-content" ref="contentRef">
      <header class="report-header" v-if="title">
        <h1 class="report-title">{{ title }}</h1>
        <p class="report-summary" v-if="summary">{{ summary }}</p>
        <div class="report-meta" v-if="meta">
          <span v-for="(val, key) in meta" :key="key" class="meta-item">
            <span class="meta-key">{{ key }}</span>
            <span class="meta-val">{{ val }}</span>
          </span>
        </div>
      </header>

      <div
        v-for="(section, idx) in sections"
        :key="idx"
        :ref="el => { if (el) sectionRefs[idx] = el }"
        class="report-section"
      >
        <ReportSection
          :title="section.title"
          :content="section.content"
          :index="idx"
          :is-loading="section.isLoading"
          :initially-expanded="idx < 3"
        />
      </div>

      <div v-if="sections.length === 0" class="report-empty">
        <p>No report content yet.</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import ReportSection from './ReportSection.vue'

const props = defineProps({
  title: { type: String, default: '' },
  summary: { type: String, default: '' },
  sections: { type: Array, default: () => [] },
  meta: { type: Object, default: null }
})

const activeSection = ref(0)
const contentRef = ref(null)
const sectionRefs = ref({})

const scrollToSection = (idx) => {
  activeSection.value = idx
  const el = sectionRefs.value[idx]
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

// Track active section on scroll
const onScroll = () => {
  if (!contentRef.value) return
  const scrollTop = contentRef.value.scrollTop
  let current = 0

  for (const [idx, el] of Object.entries(sectionRefs.value)) {
    if (el && el.offsetTop <= scrollTop + 100) {
      current = parseInt(idx)
    }
  }
  activeSection.value = current
}

watch(contentRef, (el) => {
  if (el) el.addEventListener('scroll', onScroll, { passive: true })
})
</script>

<style scoped>
.report-viewer {
  display: flex;
  height: 100%;
  background: var(--color-bg, #fff);
}

.report-toc {
  width: 220px;
  min-width: 220px;
  border-right: 1px solid var(--color-border, #E8E5E0);
  overflow-y: auto;
  padding: 20px 0;
}

.toc-header {
  font-family: var(--font-mono, 'DM Mono', monospace);
  font-size: var(--text-xs, 0.56rem);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-secondary, #888);
  padding: 0 16px 12px;
}

.toc-nav {
  display: flex;
  flex-direction: column;
}

.toc-item {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 6px 16px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
  border-left: 2px solid transparent;
}

.toc-item:hover {
  background: var(--color-surface, #F6F5F2);
}

.toc-item.active {
  border-left-color: var(--color-accent, #2A7A5B);
  background: var(--color-accent-light, #E8F5EE);
}

.toc-number {
  font-family: var(--font-mono, 'DM Mono', monospace);
  font-size: var(--text-xs, 0.56rem);
  color: var(--color-text-faint, #aaa);
  min-width: 18px;
}

.toc-title {
  font-family: var(--font-body, 'DM Sans', sans-serif);
  font-size: var(--text-sm, 0.78rem);
  color: var(--color-text, #111);
  line-height: 1.4;
}

.toc-item.active .toc-title {
  color: var(--color-accent, #2A7A5B);
  font-weight: 500;
}

.report-content {
  flex: 1;
  overflow-y: auto;
  padding: 32px 40px;
  scroll-padding-top: 20px;
}

.report-header {
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--color-border, #E8E5E0);
}

.report-title {
  font-family: var(--font-serif, 'Cormorant Garamond', serif);
  font-size: var(--text-2xl, 2rem);
  font-weight: 600;
  color: var(--color-text, #111);
  line-height: 1.2;
  letter-spacing: -0.02em;
  margin: 0 0 12px;
}

.report-summary {
  font-family: var(--font-body, 'DM Sans', sans-serif);
  font-size: var(--text-base, 1rem);
  color: var(--color-text-secondary, #888);
  line-height: 1.6;
  margin: 0;
}

.report-meta {
  display: flex;
  gap: 20px;
  margin-top: 16px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.meta-key {
  font-family: var(--font-mono, 'DM Mono', monospace);
  font-size: var(--text-xs, 0.56rem);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-faint, #aaa);
}

.meta-val {
  font-family: var(--font-mono, 'DM Mono', monospace);
  font-size: var(--text-sm, 0.78rem);
  color: var(--color-text, #111);
}

.report-section {
  margin-bottom: 8px;
}

.report-empty {
  text-align: center;
  padding: 60px 0;
  color: var(--color-text-faint, #aaa);
  font-family: var(--font-body, 'DM Sans', sans-serif);
}

@media (max-width: 768px) {
  .report-toc { display: none; }
  .report-content { padding: 20px 16px; }
}
</style>
