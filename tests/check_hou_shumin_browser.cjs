/* Uses bundled Playwright; external streams are stubbed, not claimed as playback validation. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const http = require('http');
const base = process.env.PREVIEW_URL || 'http://127.0.0.1:8773';
const slugs = ['shumin-fude','shumin-map','shumin-riverside','shumin-jinniang','shumin-belief'];
const report = {layouts:[], taps:[], player:[], touchFallback:[], typography:[], menu:[], errors:[]};
function check(ok, message) { if (!ok) throw Error(message); }
(async () => {
  const site=path.resolve(__dirname,'../02_網站');
  const server=process.env.START_PREVIEW==='1' ? http.createServer((req,res)=>{
    const file=path.resolve(site,'.'+decodeURIComponent(new URL(req.url,base).pathname));
    if(!file.startsWith(site+path.sep)){res.writeHead(403);return res.end();}
    const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.jpg':'image/jpeg','.webp':'image/webp'};
    fs.readFile(file,(error,bytes)=>{res.writeHead(error?404:200,{'Content-Type':types[path.extname(file)]||'application/octet-stream'});res.end(error?'Not found':bytes);});
  }) : null;
  if(server) await new Promise(resolve=>server.listen(Number(new URL(base).port),'127.0.0.1',resolve));
  console.log('Preview root: '+site+'; port: '+new URL(base).port);
  const browser = await chromium.launch({channel:'chrome',headless:true});
  try {
    const context = await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
    await context.route('**/*', async route => {
      const url = new URL(route.request().url());
      if (url.origin !== new URL(base).origin) return route.fulfill({status:200,contentType:'text/html',body:'<p>External preview stub</p>'});
      return route.continue();
    });
    const page = await context.newPage();
    page.on('pageerror', error => report.errors.push(error.message));
    for (const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:900});
      for (const name of ['works', 'shumin', ...slugs]) {
        await page.goto(base+'/'+name+'.html');
        const data = await page.evaluate(() => ({
          overflow:document.documentElement.scrollWidth > innerWidth+1,
          header:document.querySelector('.final-header').getBoundingClientRect().height,
          missing:[...document.querySelectorAll('img')].filter(i => i.complete && !i.naturalWidth).map(i=>i.src),
          badNav:[...document.querySelectorAll('nav')].some(n => n.querySelectorAll('[aria-current="page"]').length>1)
        }));
        check(!data.overflow, name+' overflow '+width);
        check(!data.missing.length, name+' missing images');
        check(!data.badNav, name+' current location');
        check(await page.locator('.drive-viewing-hint:visible').count()===0,name+' mobile hint must be removed');
        check(data.header === (width<=768?56:72), name+' header '+width);
        report.layouts.push({name,width,...data});
      }
    }
    await page.setViewportSize({width:390,height:844});
    for (const slug of ['shumin']) {
      for (const region of ['.card-media','h3','.card-copy p']) {
        await page.goto(base+'/works.html');
        const card=page.locator('article.work-card').filter({has:page.locator('a[href="'+slug+'.html"]')});
        const target=card.locator(region);
        await target.scrollIntoViewIfNeeded();
        const bounds=await target.boundingBox();
        const point={x:bounds.x+bounds.width/2,y:bounds.y+bounds.height/2};
        const destination=await page.evaluate(({x,y})=>document.elementFromPoint(x,y)?.closest('a')?.getAttribute('href'),point);
        check(destination===slug+'.html', slug+' '+region+' hit target: '+destination);
        await page.touchscreen.tap(point.x,point.y);
        await page.waitForURL(base+'/'+slug+'.html');
        report.taps.push({slug,region});
      }
    }
    await page.goto(base+'/shumin.html');
    await page.locator('.site-menu summary').click();
    check(await page.locator('.site-menu').evaluate(n=>n.open), 'menu did not open');
    await page.keyboard.press('Escape');
    check(!(await page.locator('.site-menu').evaluate(n=>n.open)), 'menu did not close');
    report.menu.push('mobile menu opens and Escape closes');
    for(const slug of slugs.slice(0,4)){
      await page.goto(base+'/'+slug+'.html');
      const expected=await page.locator('.player-fallback').getAttribute('href');
      const [popup]=await Promise.all([page.waitForEvent('popup'),page.locator('.video-shell button').click()]);
      await popup.waitForURL(expected);
      check(await page.locator('.video-shell iframe').count()===0,slug+' touch should use direct link');
      report.touchFallback.push({slug,url:popup.url()});
      await popup.close();
    }
    // A viewport resize does not change touch capability: use a real desktop context.
    const desktop=await browser.newPage({viewport:{width:1440,height:1000},hasTouch:false,isMobile:false});
    await desktop.route('**/*',route=>new URL(route.request().url()).origin!==new URL(base).origin
      ? route.fulfill({status:200,contentType:'text/html',body:'<p>External preview stub</p>'}) : route.continue());
    desktop.on('pageerror',error=>report.errors.push(error.message));
    for (const slug of slugs.slice(0,4)) {
      await desktop.goto(base+'/'+slug+'.html');
      await desktop.locator('.video-shell button').click();
      const frame=desktop.locator('.video-shell iframe');
      await frame.waitFor();
      const src=await frame.getAttribute('src');
      check(src.includes('drive.google.com/file/d/') && src.endsWith('/preview'), slug+' player source');
      report.player.push({slug,src,actualStreaming:false});
    }
    const cdp=await desktop.context().newCDPSession(desktop);
    await desktop.goto(base+'/shumin.html');
    const hubIds=await desktop.locator('.video-shell').evaluateAll(nodes=>nodes.map(n=>n.dataset.video));
    check(hubIds.length===4,'hub must contain four video players');
    for(const id of hubIds){
      const shell=desktop.locator('.video-shell[data-video="'+id+'"]');
      await shell.locator('button').click();
      check((await shell.locator('iframe').getAttribute('src')).includes('/'+id+'/preview'),'hub player ID mismatch');
    }
    await cdp.send('DOM.enable');await cdp.send('CSS.enable');
    const selectors=['.article-heading h1','.work-heading .article-lead','.work-author','.work-introduction p'];
    async function typography(){
      await desktop.evaluate(()=>document.fonts.ready);
      return desktop.evaluate(selectors=>selectors.map(selector=>{
        const s=getComputedStyle(document.querySelector(selector));
        return {selector,family:s.fontFamily,weight:s.fontWeight,size:s.fontSize,lineHeight:s.lineHeight};
      }),selectors);
    }
    for(const width of [390,1440]){
      await desktop.setViewportSize({width,height:1000});
      await desktop.goto(base+'/suifen.html');const baseline=await typography();
      await desktop.goto(base+'/shumin.html');
      await desktop.evaluate(()=>document.fonts.ready);
      const hubHeadings=await desktop.evaluate(()=>[...document.querySelectorAll('main .article-heading.work-heading')].map(header=>{
        return ['h1,h2','.article-lead','.work-author'].map(selector=>{
          const s=getComputedStyle(header.querySelector(selector));
          return {family:s.fontFamily,weight:s.fontWeight,size:s.fontSize,lineHeight:s.lineHeight};
        });
      }));
      check(hubHeadings.length===5,'hub must have five work headings');
      const expected=baseline.slice(0,3).map(({selector,...style})=>style);
      for(const [index,heading] of hubHeadings.entries()) check(JSON.stringify(heading)===JSON.stringify(expected),'hub heading '+index+' differs from original at '+width+': '+JSON.stringify(heading));
      for(const slug of slugs){
        await desktop.goto(base+'/'+slug+'.html');const styles=await typography();
        check(JSON.stringify(styles)===JSON.stringify(baseline),slug+' typography differs from original at '+width);
        const {root}=await cdp.send('DOM.getDocument');
        const fonts=[];
        for(const selector of selectors){
          const {nodeId}=await cdp.send('DOM.querySelector',{nodeId:root.nodeId,selector});
          const actual=await cdp.send('CSS.getPlatformFontsForNode',{nodeId});
          check(actual.fonts.every(font=>font.isCustomFont),slug+' system font fallback '+selector+': '+JSON.stringify(actual.fonts));
          fonts.push({selector,fonts:actual.fonts});
        }
        report.typography.push({slug,width,styles,fonts});
      }
    }
    await page.goto(base+'/shumin-belief.html');
    check(await page.locator('.presentation-shell iframe').count()===1,'presentation preview missing');
    // No-JS reading and fallback links remain reachable.
    const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
    await nojs.route('https://**/*',route=>route.abort());
    const simple=await nojs.newPage();
    for(const slug of ['shumin',...slugs]){
      await simple.goto(base+'/'+slug+'.html');
      check(await simple.locator('.work-introduction p').first().isVisible(),slug+' no-JS introduction');
      check(await simple.locator('.player-fallback').first().isVisible(),slug+' no-JS fallback');
      if(slug==='shumin')check(await simple.locator('.player-fallback').count()===5,'hub no-JS fallback count');
    }
    check(!report.errors.length, 'JS errors: '+report.errors.join(','));
    await page.goto(base+'/works.html');
    await page.setViewportSize({width:390,height:844});
    for(const image of await page.locator('img').all()) {await image.scrollIntoViewIfNeeded();await image.evaluate(i=>i.decode());}
    await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
    await page.screenshot({path:path.join(__dirname,'../scratch/hou-shumin-works-mobile.png'),fullPage:true});
    await page.goto(base+'/shumin-fude.html');
    for(const image of await page.locator('img').all()) {if(await image.isVisible()){await image.scrollIntoViewIfNeeded();await image.evaluate(i=>i.decode());}}
    await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
    await page.screenshot({path:path.join(__dirname,'../scratch/hou-shumin-detail-mobile.png'),fullPage:true});
    fs.writeFileSync(path.join(__dirname,'../scratch/hou-shumin-browser.json'),JSON.stringify(report,null,2));
    console.log(JSON.stringify({layouts:report.layouts.length,taps:report.taps.length,players:report.player.length,touchFallback:report.touchFallback.length,typography:report.typography.length,noJS:5,errors:report.errors}));
  } finally {await browser.close(); if(server) await new Promise(resolve=>server.close(resolve));}
})().catch(error => {console.error(error); process.exitCode=1;});
