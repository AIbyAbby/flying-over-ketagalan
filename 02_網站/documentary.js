const header=document.querySelector('.site-header');
const toggle=document.querySelector('.air-toggle');
const panel=document.querySelector('#air-subnav');
const nav=document.querySelector('.top-nav');
function setAirMenu(open,returnFocus=false){
 if(!toggle||!panel)return;
 toggle.setAttribute('aria-expanded',String(open));
 toggle.setAttribute('aria-label',open?'收合空拍紀錄子選單':'展開空拍紀錄子選單');
 panel.hidden=!open;
 if(returnFocus)toggle.focus();
}
if(toggle&&panel){
 const links=[...panel.querySelectorAll('a')];
 toggle.addEventListener('click',()=>setAirMenu(panel.hidden));
 toggle.addEventListener('keydown',event=>{
  if(event.key==='ArrowDown'||event.key==='ArrowUp'){
   event.preventDefault();setAirMenu(true);
   (event.key==='ArrowDown'?links[0]:links.at(-1))?.focus();
  }
 });
 panel.addEventListener('keydown',event=>{
  const index=links.indexOf(document.activeElement);
  if(event.key==='ArrowDown'||event.key==='ArrowUp'){
   event.preventDefault();links[(index+(event.key==='ArrowDown'?1:-1)+links.length)%links.length]?.focus();
  }
  if(event.key==='Home'||event.key==='End'){
   event.preventDefault();(event.key==='Home'?links[0]:links.at(-1))?.focus();
  }
 });
 document.addEventListener('keydown',event=>{
  if(event.key==='Escape'&&!panel.hidden){event.preventDefault();setAirMenu(false,true);}
 });
 document.addEventListener('click',event=>{
  if(!toggle.contains(event.target)&&!panel.contains(event.target))setAirMenu(false);
 });
 document.addEventListener('focusin',event=>{
  if(!toggle.contains(event.target)&&!panel.contains(event.target))setAirMenu(false);
 });
 links.forEach(link=>link.addEventListener('click',()=>setAirMenu(false)));
}
if(nav){
 const shell=nav.closest('.nav-scroll-shell');
 function scrollHint(){
  shell.dataset.canScroll=String(nav.scrollWidth-nav.clientWidth-nav.scrollLeft>2);
  shell.dataset.scrolled=String(nav.scrollLeft>2);
 }
 function revealCurrent(){
  const current=nav.querySelector('[aria-current="page"]');
  if(!current)return;
  const bounds=nav.getBoundingClientRect(),link=current.getBoundingClientRect();
  if(link.right>bounds.right)nav.scrollLeft+=link.right-bounds.right+4;
  else if(link.left<bounds.left)nav.scrollLeft-=bounds.left-link.left+4;
 }
 nav.addEventListener('scroll',scrollHint,{passive:true});
 window.addEventListener('resize',scrollHint);
 if(window.ResizeObserver)new ResizeObserver(scrollHint).observe(nav);
 document.fonts?.ready.then(()=>{revealCurrent();scrollHint();});
 revealCurrent();
 scrollHint();
}
function headerTone(){header?.classList.toggle('scrolled',window.scrollY>60);}
window.addEventListener('scroll',headerTone,{passive:true});headerTone();
document.querySelectorAll('.video-shell').forEach(shell=>{
 shell.querySelector('button')?.addEventListener('click',()=>{
  const frame=document.createElement('iframe');
  if(shell.dataset.youtube){
   frame.src=`https://www.youtube-nocookie.com/embed/${encodeURIComponent(shell.dataset.youtube)}?autoplay=1&rel=0`;
   frame.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
  }else{
   frame.src=`https://drive.google.com/file/d/${encodeURIComponent(shell.dataset.video)}/preview`;
   frame.allow='autoplay; fullscreen';
  }
  frame.title=shell.dataset.title||shell.querySelector('button')?.getAttribute('aria-label')?.replace(/^播放作品[：:]\s*/,'')||shell.querySelector('img')?.alt.replace('影片封面','')||'影片播放器';
  frame.tabIndex=0;
  frame.allowFullscreen=true;
  shell.replaceChildren(frame);
  frame.focus({preventScroll:true});
 });
});
