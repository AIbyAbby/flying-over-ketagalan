/* Touch-only launch through the existing fallback anchor; player code stays intact. */
(() => {
  'use strict';
  let userAgent;
  try { userAgent = globalThis.navigator?.userAgent; } catch { userAgent = ''; }
  if (typeof userAgent === 'string' && userAgent.includes('Line/')) {
    document.querySelectorAll('.drive-viewing-hint').forEach(hint => {
      hint.dataset.line = 'true';
      hint.querySelector('.drive-hint-standard')?.setAttribute('aria-hidden', 'true');
      hint.querySelector('.drive-hint-line')?.removeAttribute('aria-hidden');
    });
  }
  if (typeof globalThis.matchMedia !== 'function') return;
  const touch = matchMedia('(hover: none) and (pointer: coarse)');
  const bindings = [];
  function fallback(binding) {
    const link = binding.hint.nextElementSibling?.querySelector('a.player-fallback');
    if (!link?.isConnected || link.target !== '_blank' ||
        !link.relList.contains('noopener')) return null;
    try {
      const url = new URL(link.href);
      const id = url.pathname.match(/^\/file\/d\/([^/]+)\/(?:view|preview)\/?$/)?.[1];
      return url.protocol === 'https:' && url.hostname === 'drive.google.com' &&
        decodeURIComponent(id || '') === binding.shell.dataset.video ? link : null;
    } catch { return null; }
  }
  document.querySelectorAll('.drive-viewing-hint').forEach(hint => {
    const shell = hint.previousElementSibling;
    const button = shell?.querySelector('button.play-button');
    if (!shell?.matches('.video-shell[data-video]') || !button) return;
    bindings.push({hint, shell, button, originalLabel:button.getAttribute('aria-label')});
  });
  function label(binding) {
    if (touch.matches && fallback(binding)) {
      binding.button.setAttribute('aria-label', '另開新視窗觀看影片');
    } else if (binding.originalLabel === null) {
      binding.button.removeAttribute('aria-label');
    } else {
      binding.button.setAttribute('aria-label', binding.originalLabel);
    }
  }
  bindings.forEach(label);
  touch.addEventListener?.('change', () => bindings.forEach(label));
  document.addEventListener('click', event => {
    if (!touch.matches || event.defaultPrevented) return;
    const binding = bindings.find(item => item.shell.contains(event.target));
    if (!binding || !binding.shell.contains(binding.button)) return;
    const link = fallback(binding);
    if (!link) { label(binding); return; }
    // Synchronous anchor activation preserves the original user's gesture.
    // If activation throws, leave the original button handler available.
    try { link.click(); } catch { return; }
    event.preventDefault();
    event.stopImmediatePropagation();
  }, true);
})();
