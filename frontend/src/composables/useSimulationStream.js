import { ref, onUnmounted } from 'vue'

/**
 * Composable for streaming real-time simulation data via SSE or polling fallback.
 *
 * @param {string} simulationId
 * @param {object} options - { interval: polling interval ms, onAction, onStatus }
 */
export function useSimulationStream(simulationId, options = {}) {
  const actions = ref([])
  const status = ref(null)
  const isConnected = ref(false)
  const error = ref(null)

  const interval = options.interval || 2000
  let pollTimer = null
  let lastActionIndex = 0

  const baseUrl = import.meta.env.VITE_API_BASE_URL || ''

  // Try SSE first, fall back to polling
  let eventSource = null

  const startSSE = () => {
    const url = `${baseUrl}/api/simulation/${simulationId}/stream`
    try {
      eventSource = new EventSource(url)
      isConnected.value = true

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          if (data.type === 'action') {
            actions.value.push(data.payload)
            options.onAction?.(data.payload)
          } else if (data.type === 'status') {
            status.value = data.payload
            options.onStatus?.(data.payload)
          }
        } catch (e) {
          console.warn('SSE parse error:', e)
        }
      }

      eventSource.onerror = () => {
        // SSE not available, fall back to polling
        eventSource.close()
        eventSource = null
        isConnected.value = false
        startPolling()
      }
    } catch {
      startPolling()
    }
  }

  const startPolling = () => {
    if (pollTimer) return

    const poll = async () => {
      try {
        // Fetch status
        const statusRes = await fetch(`${baseUrl}/api/simulation/${simulationId}/run-status`)
        if (statusRes.ok) {
          const statusData = await statusRes.json()
          if (statusData.success) {
            status.value = statusData.data
            options.onStatus?.(statusData.data)
          }
        }

        // Fetch new actions (incremental)
        const actionsRes = await fetch(
          `${baseUrl}/api/simulation/${simulationId}/actions?offset=${lastActionIndex}&limit=50`
        )
        if (actionsRes.ok) {
          const actionsData = await actionsRes.json()
          if (actionsData.success && actionsData.data?.actions?.length > 0) {
            const newActions = actionsData.data.actions
            actions.value.push(...newActions)
            lastActionIndex += newActions.length
            newActions.forEach(a => options.onAction?.(a))
          }
        }

        isConnected.value = true
        error.value = null
      } catch (e) {
        error.value = e.message
        isConnected.value = false
      }
    }

    poll()
    pollTimer = setInterval(poll, interval)
  }

  const stop = () => {
    if (eventSource) {
      eventSource.close()
      eventSource = null
    }
    if (pollTimer) {
      clearInterval(pollTimer)
      pollTimer = null
    }
    isConnected.value = false
  }

  const start = () => {
    stop()
    actions.value = []
    lastActionIndex = 0
    startSSE()
  }

  onUnmounted(stop)

  return {
    actions,
    status,
    isConnected,
    error,
    start,
    stop
  }
}
