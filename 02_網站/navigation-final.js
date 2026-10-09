/* Navigation-only progressive enhancement. No redirects or player handling. */
(() => {
  'use strict';
  const header=document.querySelector('.final-header');
  const menu=header?.querySelector('.site-menu');
  if (!menu) return;
  const summary=menu.querySelector('summary');
  const panel=menu.querySelector('.menu-panel');
  const wide=window.matchMedia('(min-width:1001px)');
  let locked=false, scrollY=0, bodyStyle='', inertBefore=[];
  function close() { menu.open=false; sync(); }
  function sync() {
    summary.setAttribute('aria-expanded',String(menu.open));
    if (menu.open && !locked) {
      locked=true; scrollY=window.scrollY; bodyStyle=document.body.getAttribute('style');
      document.body.style.position='fixed'; document.body.style.top=`-${scrollY}px`;
      document.body.style.width='100%'; document.body.style.overflow='hidden';
      inertBefore=[...document.querySelectorAll('main,footer,.final-header .brand,.desktop-navigation')].map(node=>[node,node.inert]);
      inertBefore.forEach(([node])=>{node.inert=true;});
      panel.setAttribute('aria-modal','true'); panel.querySelector('.menu-close').focus();
    } else if (!menu.open && locked) {
      locked=false;
      if (bodyStyle===null) document.body.removeAttribute('style'); else document.body.setAttribute('style',bodyStyle);
      inertBefore.forEach(([node,was])=>{node.inert=was;}); inertBefore=[];
      panel.removeAttribute('aria-modal'); window.scrollTo(0,scrollY); summary.focus({preventScroll:true});
    }
  }
  menu.addEventListener('toggle',sync);
  menu.querySelector('.menu-close').addEventListener('click',close);
  menu.querySelector('.menu-backdrop').addEventListener('click',close);
  panel.querySelectorAll('a').forEach(link=>link.addEventListener('click',close));
  document.addEventListener('keydown',event=>{
    if (!menu.open) return;
    if (event.key==='Escape') { event.preventDefault(); close(); return; }
    if (event.key==='Tab') {
      const nodes=[...panel.querySelectorAll('button,a[href]')];
      const first=nodes[0], last=nodes.at(-1), active=document.activeElement;
      if (event.shiftKey && (active===first || !panel.contains(active))) {event.preventDefault();last.focus();}
      else if (!event.shiftKey && (active===last || !panel.contains(active))) {event.preventDefault();first.focus();}
    }
  });
  document.addEventListener('focusin',event=>{
    if (menu.open && locked && !panel.contains(event.target) && event.target!==summary) panel.querySelector('.menu-close').focus();
  });
  function layout() {
    const row=header.querySelector('.final-header-row');
    header.classList.remove('nav-compact');
    if (wide.matches && row.scrollWidth>row.clientWidth+1) header.classList.add('nav-compact');
    if (wide.matches && !header.classList.contains('nav-compact') && menu.open) close();
  }
  window.addEventListener('resize',layout);
  document.fonts?.ready.then(layout); layout();
})();
