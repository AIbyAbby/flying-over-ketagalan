/** Progressive enhancement for native creation-reflection disclosures only. */
(function () {
  'use strict';
  function initReflectionCards() {
    const cards = [...document.querySelectorAll('details.reflection-card')];
    if (!cards.length) return;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let printState;
    function scrollToCard(card) {
      const header = document.querySelector('.site-header, .topbar, header.header');
      if (header) {
        const style = window.getComputedStyle(header);
        if (style.position === 'fixed' || style.position === 'sticky') {
          card.style.setProperty('--reflection-header-height', header.getBoundingClientRect().height + 'px');
        }
      }
      card.scrollIntoView({behavior: reduceMotion.matches ? 'instant' : 'smooth', block: 'start'});
    }
    function checkHashAnchor() {
      const hash = window.location.hash;
      if (!['#reflection', '#creator-note-title', '#creator-note'].includes(hash)) return;
      const card = document.getElementById('reflection') || cards[0];
      card.open = true;
      window.requestAnimationFrame(() => scrollToCard(card));
    }
    cards.forEach(card => {
      card.dataset.reflectionReady = 'true';
      card.querySelectorAll('.reflection-close-btn').forEach(button => {
        button.addEventListener('click', event => {
          event.preventDefault();
          card.open = false;
          card.querySelector('summary').focus({preventScroll: true});
          scrollToCard(card);
        });
      });
    });
    window.addEventListener('beforeprint', () => {
      if (!printState) printState = cards.map(card => card.open);
      cards.forEach(card => { card.open = true; });
    });
    window.addEventListener('afterprint', () => {
      if (!printState) return;
      cards.forEach((card, index) => { card.open = printState[index]; });
      printState = undefined;
    });
    checkHashAnchor();
    window.addEventListener('hashchange', checkHashAnchor);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initReflectionCards);
  } else {
    initReflectionCards();
  }
})();
