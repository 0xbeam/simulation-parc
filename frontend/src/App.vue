<template>
  <router-view />
</template>

<script setup>
// Vue Router manages pages
</script>

<style>
/* Global reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--color-text);
  background-color: var(--color-bg);
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(17, 17, 20, 0.15);
  border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(17, 17, 20, 0.3);
}

/* Global button style */
button {
  font-family: inherit;
}
</style>
