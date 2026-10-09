/* Run with NODE_PATH pointing at the bundled Playwright package directory. */
const { chromium } = require('playwright');
const fs=require('fs'); const path=require('path');
const site=path.join(__dirname,'../02_網站');
const base=process.env.PREVIEW_URL||'http://127.0.0.1:8766';
const pages=fs.readdirSync(site).filter(n=>n.endsWith('.html'));
const widths=[320,360,390,430,768,1024,1440];
const works=['suifen','kuncan','wenjin','yuan','abby'];
const report={layouts:[],taps:[],otherTaps:[],menu:[],failures:[],errors:[],hoverViolations:[]};
function requireCheck(value,label){if(!value)report.failures.push(label);}
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true,deviceScaleFactor:1});
 await context.route('**/*',route=>{
   const u=new URL(route.request().url());
   if(u.origin!==new URL(base).origin)return route.abort();
   if(u.pathname.startsWith('/flying-over-ketagalan/'))return route.continue({url:base+u.pathname.replace('/flying-over-ketagalan','')+u.search});
   return route.continue();
 });
 const page=await context.newPage();
 page.on('pageerror',e=>report.errors.push(e.message));
 for(const width of widths){
  await page.setViewportSize({width,height:900});
  for(const name of pages){
   await page.goto(base+'/'+name,{waitUntil:'domcontentloaded'});
   if(name==='index.html')await page.waitForURL(base+'/intro.html');
   await page.evaluate(()=>document.fonts.ready);
   const data=await page.evaluate(()=>{
    const header=document.querySelector('.final-header'), nav=document.querySelector('.desktop-navigation');
    const bar=document.querySelector('.work-action-bar');
    const visible=getComputedStyle(nav).display!=='none';
    return {width:innerWidth,overflow:document.documentElement.scrollWidth-innerWidth,header:header.getBoundingClientRect().height,navRows:visible?new Set([...nav.children].map(a=>Math.round(a.getBoundingClientRect().top))).size:0,bar:bar&&getComputedStyle(bar).display!=='none'?bar.getBoundingClientRect().height:0,padding:parseFloat(getComputedStyle(document.body).paddingBottom)};
   });
   report.layouts.push({page:name,width,...data});
   if(width===390){
    const violations=await page.evaluate(()=>{
      const result=[];
      function walk(rules,guarded){for(const rule of rules){const g=guarded||(rule.conditionText?.includes('hover: hover')&&rule.conditionText?.includes('pointer: fine'));if(rule.selectorText?.includes(':hover')&&!g)result.push(rule.selectorText);if(rule.cssRules)walk(rule.cssRules,g);}}
      for(const sheet of document.styleSheets){try{walk(sheet.cssRules,false);}catch{}}
      return result;
    });
    report.hoverViolations.push(...violations.map(selector=>({page:name,selector})));
   }
   requireCheck(data.width===width,`${name}/${width}: actual viewport ${data.width}`);
   requireCheck(data.overflow<=1,`${name}/${width}: horizontal overflow ${data.overflow}`);
   requireCheck(Math.abs(data.header-(width<=768?56:72))<1,`${name}/${width}: header height ${data.header}`);
   requireCheck(data.navRows<=1,`${name}/${width}: navigation wraps`);
   if(data.bar)requireCheck(data.padding>=data.bar+15,`${name}/${width}: bottom bar padding`);
  }
 }
 await page.setViewportSize({width:390,height:844});
 for(let i=0;i<works.length;i++)for(const selector of ['img','.poster-play','h3','p']){
  await page.goto(base+'/works.html',{waitUntil:'domcontentloaded'}); await page.evaluate(()=>document.fonts.ready);
  const card=page.locator('.work-card').nth(i), element=card.locator(selector);
  await element.evaluate(el=>el.scrollIntoView({block:'center',behavior:'instant'}));
  const box=await element.boundingBox(); const point={x:box.x+box.width/2,y:box.y+box.height/2};
  const hit=await page.evaluate(p=>{const e=document.elementFromPoint(p.x,p.y);return {tag:e?.tagName,href:e?.closest('a')?.getAttribute('href'),pointer:e?getComputedStyle(e).pointerEvents:null};},point);
  console.log('tap',works[i],selector,JSON.stringify(hit));
  await page.touchscreen.tap(point.x,point.y);
  await page.waitForURL(base+'/'+works[i]+'.html',{waitUntil:'domcontentloaded',timeout:6000}).catch(e=>{throw new Error(`${works[i]}/${selector}: ${page.url()} ${JSON.stringify(hit)} ${e.message}`)});
  const target=new URL(page.url()).pathname.split('/').pop();
  report.taps.push({card:works[i],area:selector,hit,target});
  requireCheck(hit.href===works[i]+'.html'&&target===works[i]+'.html',`${works[i]}/${selector}: tap target`);
 }
 await page.goto(base+'/works.html',{waitUntil:'domcontentloaded'});
 await page.locator('.site-menu summary').click();
 await page.waitForFunction(()=>document.body.style.position==='fixed');
 const opened=await page.evaluate(()=>({focus:document.activeElement.className,expanded:document.querySelector('.site-menu summary').getAttribute('aria-expanded'),heights:[...document.querySelectorAll('.menu-panel nav a')].map(a=>a.getBoundingClientRect().height),inert:document.querySelector('main').inert}));
 requireCheck(opened.focus==='menu-close'&&opened.expanded==='true'&&opened.inert&&opened.heights.every(h=>h>=52),'menu open/focus/lock/row height');
 await page.keyboard.press('Shift+Tab'); requireCheck(await page.locator('.menu-panel nav a').last().evaluate(e=>e===document.activeElement),'menu reverse focus trap');
 await page.keyboard.press('Tab'); requireCheck(await page.locator('.menu-close').evaluate(e=>e===document.activeElement),'menu forward focus trap');
 await page.keyboard.press('Escape');
 requireCheck(await page.locator('.site-menu summary').evaluate(e=>e===document.activeElement&&!e.parentElement.open),'menu Esc restore focus');
 await page.locator('.site-menu summary').click(); await page.waitForFunction(()=>document.body.style.position==='fixed');
 await page.mouse.click(8,100);
 requireCheck(await page.locator('.site-menu').evaluate(e=>!e.open),'menu backdrop closes');
 report.menu.push(opened);
 await page.evaluate(()=>window.scrollTo({top:500,behavior:'instant'}));
 const priorScroll=await page.evaluate(()=>window.scrollY);
 // A locator click can auto-scroll a sticky header before pressing it. Use
 // physical touch coordinates so this checks the user's original scroll position.
 const menuTapBox=await page.locator('.site-menu summary').boundingBox();
 await page.touchscreen.tap(menuTapBox.x+menuTapBox.width/2,menuTapBox.y+menuTapBox.height/2);
 await page.waitForFunction(()=>document.body.style.position==='fixed');
 const scrolledMenu=await page.evaluate(()=>{const h=document.querySelector('header').getBoundingClientRect(),p=document.querySelector('.menu-panel').getBoundingClientRect();return {headerTop:h.top,panelTop:p.top,panelHeight:p.height,expected:innerHeight-h.height};});
 requireCheck(Math.abs(scrolledMenu.headerTop)<1&&Math.abs(scrolledMenu.panelHeight-scrolledMenu.expected)<1,'menu viewport containment after scroll');
 await page.locator('.menu-close').click();
 await page.waitForFunction(y=>Math.abs(window.scrollY-y)<1,priorScroll,{timeout:1000});
 const restoredScroll=await page.evaluate(()=>window.scrollY);
 requireCheck(Math.abs(restoredScroll-priorScroll)<1,`menu restores prior scroll (${priorScroll} -> ${restoredScroll})`);
 await page.locator('.site-menu summary').click(); await page.waitForFunction(()=>document.body.style.position==='fixed');
 await page.locator('.menu-panel nav a').nth(2).click(); await page.waitForURL(base+'/fieldwork.html',{waitUntil:'domcontentloaded'});
 report.menu.push(scrolledMenu);
 for(const [name,selector,targets] of [
   ['intro.html','.intro-method',['teacher.html','fieldwork.html','walks.html','works.html']],
   ['fieldwork.html','.shared-card',['fieldwork-0829.html','fieldwork-0903.html','fieldwork-0905.html','fieldwork-0910.html']]
 ])for(let i=0;i<targets.length;i++){
   await page.goto(base+'/'+name,{waitUntil:'domcontentloaded'}); await page.evaluate(()=>document.fonts.ready);
   const card=page.locator(selector).nth(i); await card.evaluate(e=>e.scrollIntoView({block:'center',behavior:'instant'}));
   if(name==='intro.html'){
     const geometry=await card.evaluate(e=>{const label=e.querySelector('.intro-method-label').getBoundingClientRect(),copy=e.querySelector('.intro-method-copy p').getBoundingClientRect();return {label:label.x,labelBottom:label.bottom,copy:copy.x,copyTop:copy.top,copyWidth:copy.width,heading:getComputedStyle(e.querySelector('h3')).position};});
     requireCheck((geometry.label<geometry.copy||geometry.copyTop>=geometry.labelBottom-1)&&geometry.copyWidth>120&&geometry.heading==='absolute','intro card preserves existing responsive flow '+i);
   }
   const box=await card.boundingBox(); const point={x:box.x+box.width/2,y:box.y+box.height/2};
   const hit=await page.evaluate(p=>document.elementFromPoint(p.x,p.y)?.closest('a')?.getAttribute('href'),point);
   await page.touchscreen.tap(point.x,point.y); await page.waitForURL(base+'/'+targets[i],{waitUntil:'domcontentloaded'});
   report.otherTaps.push({page:name,card:i,hit,target:targets[i]}); requireCheck(hit===targets[i],name+' fullcard hit '+i);
 }
 for(const slug of works){
  await page.goto(base+'/'+slug+'.html',{waitUntil:'domcontentloaded'});
  await page.locator('.work-switcher summary').click();
  const rows=await page.locator('.work-switcher nav a').evaluateAll(es=>es.map(e=>({href:e.getAttribute('href'),height:e.getBoundingClientRect().height})));
  requireCheck(rows.every(r=>r.height>=56),'switcher row height '+slug);
  await page.locator('.work-switcher summary').click();
  await page.evaluate(()=>window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'}));
  const gap=await page.evaluate(()=>document.querySelector('.work-action-bar').getBoundingClientRect().top-document.querySelector('footer').getBoundingClientRect().bottom);
  requireCheck(gap>=15,'footer not covered '+slug);
 }
 requireCheck(report.errors.length===0,'no page JavaScript errors');
 requireCheck(report.hoverViolations.length===0,'hover rules must all require fine pointer');
 await browser.close();
 fs.mkdirSync(path.join(__dirname,'../docs/reports'),{recursive:true});
 fs.writeFileSync(path.join(__dirname,'../docs/reports/2026-10-09-browser-verification.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({layouts:report.layouts.length,taps:report.taps.length,otherTaps:report.otherTaps.length,hoverViolations:report.hoverViolations.length,failures:report.failures,errors:report.errors},null,2));
 process.exitCode=report.failures.length?1:0;
})().catch(e=>{console.error(e);process.exit(1);});
