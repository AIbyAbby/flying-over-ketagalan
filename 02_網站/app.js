const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#nav');
toggle?.addEventListener('click', () => {
  const expanded = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(expanded));
  toggle.setAttribute('aria-label', expanded ? '關閉選單' : '開啟選單');
  nav.classList.toggle('open', expanded);
});
function closeMenu() {
  toggle?.setAttribute('aria-expanded', 'false');
  toggle?.setAttribute('aria-label', '開啟選單');
  nav?.classList.remove('open');
}
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && nav?.classList.contains('open')) {
    closeMenu();
    toggle?.focus();
  }
});
document.addEventListener('click', event => {
  if (nav?.classList.contains('open') && !nav.contains(event.target) && !toggle.contains(event.target)) closeMenu();
});
document.querySelectorAll('.video-shell').forEach(shell => {
  shell.querySelector('button')?.addEventListener('click', () => {
    const frame = document.createElement('iframe');
    frame.src = `https://drive.google.com/file/d/${encodeURIComponent(shell.dataset.video)}/preview`;
    frame.title = shell.querySelector('img').alt;
    frame.allow = 'autoplay; fullscreen';
    frame.allowFullscreen = true;
    shell.replaceChildren(frame);
  });
});
document.querySelectorAll('.pdf-detail').forEach(details => {
  details.addEventListener('toggle', () => {
    if (!details.open) return;
    const frame = details.querySelector('iframe');
    if (!frame.getAttribute('src')) frame.src = frame.dataset.src;
  });
});
