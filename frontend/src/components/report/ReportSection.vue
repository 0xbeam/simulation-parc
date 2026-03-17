<template>
  <div class="report-section" :class="{ collapsed: !isExpanded }">
    <div class="section-header" @click="toggle">
      <div class="section-index">{{ String(index + 1).padStart(2, '0') }}</div>
      <h3 class="section-title">{{ title }}</h3>
      <svg
        class="section-chevron"
        :class="{ rotated: isExpanded }"
        viewBox="0 0 24 24"
        width="16"
        height="16"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </div>

    <div class="section-body" v-show="isExpanded">
      <div v-if="isLoading" class="section-loading">
        <div class="loading-bar"></div>
        <span>Generating...</span>
      </div>
      <div v-else-if="renderedContent" class="section-content" v-html="renderedContent"></div>
      <div v-else class="section-empty">No content</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { renderMarkdown } from '../../composables/useMarkdown'

const props = defineProps({
  title: { type: String, required: true },
  content: { type: String, default: '' },
  index: { type: Number, default: 0 },
  isLoading: { type: Boolean, default: false },
  initiallyExpanded: { type: Boolean, default: true }
})

const isExpanded = ref(props.initiallyExpanded)

const toggle = () => {
  isExpanded.value = !isExpanded.value
}

const renderedContent = computed(() => {
  if (!props.content) return ''
  return renderMarkdown(props.content, { stripLeadingH2: true })
})
</script>

<style scoped>
.report-section {
  border: 1px solid var(--color-border, #E8E5E0);
  border-radius: 6px;
  overflow: hidden;
  transition: border-color 0.15s ease;
}

.report-section:hover {
  border-color: var(--color-border-light, #D8D5D0);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  user-select: none;
  transition: background 0.15s ease;
}

.section-header:hover {
  background: var(--color-surface, #F6F5F2);
}

.section-index {
  font-family: var(--font-mono, 'DM Mono', monospace);
  font-size: var(--text-xs, 0.56rem);
  color: var(--color-text-faint, #aaa);
  min-width: 20px;
}

.section-title {
  flex: 1;
  font-family: var(--font-serif, 'Cormorant Garamond', serif);
  font-size: var(--text-lg, 1.2rem);
  font-weight: 600;
  color: var(--color-text, #111);
  margin: 0;
  line-height: 1.3;
}

.section-chevron {
  color: var(--color-text-secondary, #888);
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.section-chevron.rotated {
  transform: rotate(180deg);
}

.section-body {
  padding: 0 16px 16px;
  padding-left: 48px;
}

.section-content {
  font-family: var(--font-body, 'DM Sans', sans-serif);
  font-size: var(--text-base, 0.92rem);
  color: var(--color-text, #111);
  line-height: 1.7;
}

.section-content :deep(h3),
.section-content :deep(h4) {
  font-family: var(--font-serif, 'Cormorant Garamond', serif);
  font-weight: 600;
  margin: 1.5em 0 0.5em;
  color: var(--color-text, #111);
}

.section-content :deep(h3) { font-size: var(--text-lg, 1.2rem); }
.section-content :deep(h4) { font-size: var(--text-base, 1rem); }

.section-content :deep(p) {
  margin: 0.8em 0;
}

.section-content :deep(ul),
.section-content :deep(ol) {
  padding-left: 1.5em;
  margin: 0.5em 0;
}

.section-content :deep(li) {
  margin: 0.3em 0;
}

.section-content :deep(blockquote) {
  border-left: 3px solid var(--color-accent, #2A7A5B);
  padding: 8px 16px;
  margin: 1em 0;
  background: var(--color-surface, #F6F5F2);
  border-radius: 0 4px 4px 0;
}

.section-content :deep(code) {
  font-family: var(--font-mono, 'DM Mono', monospace);
  font-size: 0.9em;
  background: var(--color-surface, #F6F5F2);
  padding: 2px 5px;
  border-radius: 3px;
}

.section-content :deep(pre) {
  background: var(--color-surface, #F6F5F2);
  border: 1px solid var(--color-border, #E8E5E0);
  border-radius: 4px;
  padding: 12px 16px;
  overflow-x: auto;
  margin: 1em 0;
}

.section-content :deep(pre code) {
  background: none;
  padding: 0;
}

.section-content :deep(strong) {
  font-weight: 600;
}

.section-content :deep(hr) {
  border: none;
  border-top: 1px solid var(--color-border, #E8E5E0);
  margin: 1.5em 0;
}

.section-loading {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  color: var(--color-text-secondary, #888);
  font-family: var(--font-mono, monospace);
  font-size: var(--text-sm, 0.78rem);
}

.loading-bar {
  width: 60px;
  height: 3px;
  background: var(--color-border, #E8E5E0);
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}

.loading-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: -60px;
  width: 60px;
  height: 100%;
  background: var(--color-accent, #2A7A5B);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  to { left: 60px; }
}

.section-empty {
  padding: 12px 0;
  color: var(--color-text-faint, #aaa);
  font-family: var(--font-body, 'DM Sans', sans-serif);
  font-size: var(--text-sm, 0.78rem);
}
</style>
