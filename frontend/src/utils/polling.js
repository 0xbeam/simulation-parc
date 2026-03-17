/**
 * Poll a function with timeout and exponential backoff on errors.
 *
 * @param {Function} fn - Async function to call. Should return truthy to stop.
 * @param {object} opts
 * @param {number} opts.interval - Base polling interval (ms), default 2000
 * @param {number} opts.maxAttempts - Max polls before timeout, default 300
 * @param {Function} opts.onTimeout - Called when max attempts reached
 * @param {Function} opts.onError - Called on error (receives error object)
 * @returns {{ stop: Function }} Control handle
 */
export function pollWithTimeout(fn, opts = {}) {
  const interval = opts.interval || 2000
  const maxAttempts = opts.maxAttempts || 300
  const onTimeout = opts.onTimeout || (() => {})
  const onError = opts.onError || (() => {})

  let count = 0
  let timer = null
  let stopped = false

  const tick = async () => {
    if (stopped) return

    count++
    if (count > maxAttempts) {
      onTimeout()
      return
    }

    try {
      const done = await fn()
      if (done || stopped) return
    } catch (e) {
      onError(e)
    }

    if (!stopped) {
      timer = setTimeout(tick, interval)
    }
  }

  timer = setTimeout(tick, 0)

  return {
    stop() {
      stopped = true
      if (timer) clearTimeout(timer)
    }
  }
}
