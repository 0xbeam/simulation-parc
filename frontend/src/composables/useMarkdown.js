import { marked } from 'marked'
import DOMPurify from 'dompurify'

// Configure marked for safe, consistent rendering
marked.setOptions({
  breaks: true,
  gfm: true
})

// Configure DOMPurify to allow standard markdown HTML
const PURIFY_CONFIG = {
  ALLOWED_TAGS: [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'hr',
    'ul', 'ol', 'li',
    'blockquote', 'pre', 'code',
    'strong', 'em', 'del', 's',
    'a', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'div', 'span', 'sup', 'sub'
  ],
  ALLOWED_ATTR: ['href', 'target', 'rel', 'class', 'start'],
  ALLOW_DATA_ATTR: false
}

/**
 * Render markdown to sanitized HTML.
 * @param {string} content - Raw markdown string
 * @param {object} options - { stripLeadingH2: bool }
 * @returns {string} Sanitized HTML
 */
export function renderMarkdown(content, options = {}) {
  if (!content) return ''

  let processed = content

  // Strip leading h2 when section title is already shown externally
  if (options.stripLeadingH2) {
    processed = processed.replace(/^##\s+.+\n+/, '')
  }

  const rawHtml = marked.parse(processed)
  return DOMPurify.sanitize(rawHtml, PURIFY_CONFIG)
}

/**
 * Composable that returns the renderMarkdown function for use in Vue components.
 */
export function useMarkdown() {
  return { renderMarkdown }
}
