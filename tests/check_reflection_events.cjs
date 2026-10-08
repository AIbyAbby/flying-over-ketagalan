// Pure event-logic tests; browser keyboard/layout checks are recorded separately.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const script = fs.readFileSync('02_網站/work-reflection.js', 'utf8');
function run(reduced, hash) {
  const listeners = {};
  let close, focused = false, scrolled, offset;
  const card = {open:false, dataset:{}, style:{setProperty:(k,v)=>{offset=v;}},
    querySelectorAll:()=>[{addEventListener:(event,callback)=>{close=callback;}}],
    querySelector:()=>({focus:options=>{focused=options.preventScroll;}}),
    scrollIntoView:options=>{scrolled=options;}};
  const window = {location:{hash}, matchMedia:()=>({matches:reduced}),
    getComputedStyle:()=>({position:'fixed'}),
    requestAnimationFrame:callback=>callback(),
    addEventListener:(name,callback)=>{listeners[name]=callback;}};
  const document = {readyState:'complete',querySelectorAll:()=>[card],getElementById:()=>card,
    querySelector:()=>({getBoundingClientRect:()=>({height:156})})};
  vm.runInNewContext(script,{window,document});
  if(hash) assert.equal(card.open,true);
  card.open=true;
  close({preventDefault(){}});
  assert.equal(card.open,false);
  assert.equal(focused,true);
  assert.equal(scrolled.behavior,reduced?'instant':'smooth');
  assert.equal(offset,'156px');
  listeners.beforeprint(); assert.equal(card.open,true);
  listeners.beforeprint(); // Repeated print callbacks must not replace original state.
  listeners.afterprint(); assert.equal(card.open,false);
  card.open=true;
  listeners.beforeprint(); listeners.afterprint(); assert.equal(card.open,true);
}
run(false,'#reflection'); run(true,'#reflection'); run(true,'');
console.log('PASS: reduced motion, hash expansion, close focus/header offset, print expansion/restoration.');
