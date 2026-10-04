const toggle=document.querySelector('.menu-toggle');
const nav=document.querySelector('#nav');
const shade=document.querySelector('.nav-shade');
const header=document.querySelector('.site-header');
function setMenu(open,returnFocus=false){
 toggle.setAttribute('aria-expanded',String(open));
 toggle.setAttribute('aria-label',open?'關閉選單':'開啟選單');
 nav.hidden=!open;shade.hidden=!open;
 document.body.classList.toggle('menu-open',open);
 header.classList.toggle('scrolled',open||window.scrollY>60);
 if(open)nav.querySelector('a')?.focus();
 else if(returnFocus)toggle.focus();
}
toggle.addEventListener('click',()=>setMenu(toggle.getAttribute('aria-expanded')!=='true'));
shade.addEventListener('click',()=>setMenu(false,true));
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));
document.addEventListener('keydown',event=>{
 if(nav.hidden)return;
 if(event.key==='Escape'){setMenu(false,true);return;}
 if(event.key==='Tab'){
  const links=[toggle,...nav.querySelectorAll('a')];
  if(event.shiftKey&&document.activeElement===links[0]){event.preventDefault();links.at(-1).focus();}
  else if(!event.shiftKey&&document.activeElement===links.at(-1)){event.preventDefault();toggle.focus();}
 }
});
function headerTone(){header.classList.toggle('scrolled',window.scrollY>60||!nav.hidden);}
window.addEventListener('scroll',headerTone,{passive:true});headerTone();
document.querySelectorAll('.video-shell').forEach(shell=>{
 shell.querySelector('button')?.addEventListener('click',()=>{
  const frame=document.createElement('iframe');
  frame.src=`https://drive.google.com/file/d/${encodeURIComponent(shell.dataset.video)}/preview`;
  frame.title=shell.querySelector('img').alt.replace('影片封面','');
  frame.allow='autoplay; fullscreen';frame.allowFullscreen=true;
  shell.replaceChildren(frame);
 });
});
