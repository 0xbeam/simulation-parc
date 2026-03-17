<template>
  <div class="app-shell" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <Sidebar
      :collapsed="isSidebarCollapsed"
      @toggle="isSidebarCollapsed = !isSidebarCollapsed"
    />
    <div class="app-shell-main">
      <TopBar />
      <div class="app-shell-content">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './Sidebar.vue'
import TopBar from './TopBar.vue'

const isSidebarCollapsed = ref(false)
</script>

<style scoped>
.app-shell {
  display: flex;
  min-height: 100vh;
  background: var(--color-bg);
  font-family: var(--font-body);
}

.app-shell-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  margin-left: 240px;
  transition: margin-left 0.25s var(--ease-smooth);
}

.sidebar-collapsed .app-shell-main {
  margin-left: 56px;
}

.app-shell-content {
  flex: 1;
  padding: 24px 32px;
  overflow-y: auto;
}
</style>
