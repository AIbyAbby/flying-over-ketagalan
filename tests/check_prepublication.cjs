const {chromium}=require('playwright');
const fs=require('fs'),path=require('path');
const base='http://127.0.0.1:8766';
const destinations=['intro','teacher','fieldwork','walks','works'];
const report={noJS:[],delayed:[],failures:[]};
function check(ok,label){if(!ok)report.failures.push(label);}
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 for(const mode of ['noJS','delayed']){
  const context=await browser.newContext({javaScriptEnabled:mode!=='noJS',hasTouch:true,isMobile:true,viewport:{width:390,height:844}});
  let release;
  const held=new Promise(resolve=>{release=resolve;});
  await context.route('**/*',async route=>{
   const u=new URL(route.request().url());
   if(u.origin!==base)return route.abort();
   if(mode==='delayed'&&u.pathname.endsWith('/navigation-final.js'))await held;
   return route.continue();
  });
  const page=await context.newPage();
  for(let i=0;i<destinations.length;i++){
   await page.goto(base+'/works.html',{waitUntil:'commit'});
   await page.locator('.site-menu summary').waitFor({state:'visible'});
   await page.locator('.site-menu summary').click();
   const state=await page.evaluate(()=>({open:document.querySelector('.site-menu').open,visible:[...document.querySelectorAll('.menu-panel nav a')].map(e=>({href:e.getAttribute('href'),height:e.getBoundingClientRect().height})),aria:document.querySelector('.site-menu summary').getAttribute('aria-expanded'),locked:document.body.style.position==='fixed'}));
   check(state.open&&state.visible.length===5&&state.visible.every(r=>r.height>=52),mode+' native menu '+i);
   await page.locator('.menu-panel nav a').nth(i).click();
   await page.waitForURL(base+'/'+destinations[i]+'.html',{waitUntil:'commit'});
   report[mode].push({target:destinations[i],...state});
  }
  if(mode==='delayed'){
   await page.goto(base+'/works.html',{waitUntil:'commit'}); await page.locator('.site-menu summary').click();
   const before=await page.evaluate(()=>({open:document.querySelector('.site-menu').open,locked:document.body.style.position==='fixed',aria:document.querySelector('summary').getAttribute('aria-expanded')}));
   release(); await page.waitForLoadState('domcontentloaded');
   const after=await page.evaluate(()=>({open:document.querySelector('.site-menu').open,locked:document.body.style.position==='fixed',aria:document.querySelector('summary').getAttribute('aria-expanded'),focus:document.activeElement.className}));
   report.delayed.push({beforeJS:before,afterJS:after});
   check(after.open&&after.locked&&after.aria==='true'&&after.focus==='menu-close','adopt menu opened before JS loaded');
  }
  release(); await context.close();
 }
 await browser.close();
 const target=path.join(__dirname,'../docs/reports/2026-10-09-prepublication-js.json');fs.writeFileSync(target,JSON.stringify(report,null,2));
 console.log(JSON.stringify(report,null,2));process.exitCode=report.failures.length?1:0;
})().catch(e=>{console.error(e);process.exit(1);});
