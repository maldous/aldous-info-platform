import assert from 'node:assert/strict';
import fs from 'node:fs';
import {viewportLocator,mapPoint,contentFrame,overviewGraphic,rememberRegions,installGraphNavigation} from './dist/graph-navigation.js';
assert.deepEqual(viewportLocator([100,200,1000,800],{left:-100,top:-50,width:2000,height:1600},{left:100,top:50,width:400,height:300}),{x:200,y:250,width:200,height:150});
assert.deepEqual(viewportLocator([100,200,1000,800],{left:100,top:100,width:200,height:160},{left:0,top:0,width:400,height:400}),{x:100,y:200,width:1000,height:800});
assert.deepEqual(mapPoint([100,200,1000,500],{left:0,top:0,width:100,height:100},50,50),{x:600,y:450});
assert.deepEqual(mapPoint([100,200,1000,500],{left:0,top:0,width:100,height:100},200,0),{x:1100,y:200});
const original=fs.readFileSync('review/graphical/stage-7.svg','utf8'),overview=overviewGraphic(original);
assert(!/data-actor=|data-handoff=|tabindex=|role="button"|<text\b/.test(overview));assert(overview.includes('id="map-viewport"'));assert(overview.includes('overview-current-arrow'));assert(!overview.includes('id="edge-arrow"'));
// A geometry-aware DOM substitute exercises the actual event handlers without browser state injection.
globalThis.getComputedStyle=()=>({paddingLeft:'0px',paddingRight:'0px',paddingTop:'0px',paddingBottom:'0px'});
let left=0,top=0;const handlers={},viewportEvents={};globalThis.addEventListener=(n,f)=>viewportEvents[n]=f;
const box={attributes:{},setAttribute(k,v){this.attributes[k]=v;}};
const graph={style:{width:'1000px',height:'800px'},outerHTML:original,getAttribute:n=>n==='viewBox'?'0 0 1000 800':null,getBoundingClientRect(){const w=parseFloat(this.style.width),h=parseFloat(this.style.height);return {left:20+Math.max(0,(400-w)/2)-left,top:30+Math.max(0,(300-h)/2)-top,width:w,height:h};}};
const scene={clientLeft:0,clientTop:0,clientWidth:400,clientHeight:300,querySelector:()=>graph,getBoundingClientRect:()=>({left:20,top:30}),addEventListener(n,f,opts){handlers[n]=f;if(n==='touchmove'||n==='touchstart')assert.equal(opts.passive,false);},get scrollLeft(){return left;},set scrollLeft(n){left=Math.max(0,Math.min(n,parseFloat(graph.style.width)-400));},get scrollTop(){return top;},set scrollTop(n){top=Math.max(0,Math.min(n,parseFloat(graph.style.height)-300));}};
const map={querySelector:s=>s==='#map-viewport'?box:{getBoundingClientRect:()=>({left:0,top:0,width:150,height:100})},setPointerCapture(){}};
const overviewBox={},zoomIn={},zoomOut={},fit={},readout={};let gestures=0;
const nav=installGraphNavigation({scene,overview:overviewBox,map,zoomIn,zoomOut,fit,readout,onGesture:()=>gestures++,finalGraphic:original.replace(/viewBox="[^"]+"/,'viewBox="0 0 1000 800"')});nav.reset(0);assert.equal(overviewBox.hidden,false);assert.equal(nav.getScale(),1);
const touch=(points)=>({touches:points.map(([clientX,clientY])=>({clientX,clientY})),preventDefault(){this.prevented=true;}});
const one=touch([[200,200]]);handlers.touchstart(one);assert(!one.prevented,'one-finger pan must remain native');
const start=touch([[170,170],[270,170]]);handlers.touchstart(start);assert(start.prevented);
const doubled=touch([[120,170],[320,170]]);handlers.touchmove(doubled);assert.equal(nav.getScale(),2);assert.equal(left,200);assert.equal(top,140);assert.equal(readout.textContent,'200%');
assert.deepEqual(box.attributes,{x:100,y:70,width:200,height:150});
handlers.touchmove(touch([[140,160],[340,160]]));assert.equal(left,180);assert.equal(top,150,'moving pinch midpoint must pan without changing the anchored graph point');
handlers.touchend(touch([]));assert(gestures>=3);
const oldScale=nav.getScale();handlers.touchmove(touch([[0,0],[300,0]]));assert.equal(nav.getScale(),oldScale,'released pinch cannot continue');
nav.zoomTo(100);assert.equal(nav.getScale(),4);nav.zoomTo(0);assert.equal(nav.getScale(),.1);
fit.onclick();assert(Math.abs(nav.getScale()-.335)<1e-10);assert.equal(left,0);assert.equal(top,0);assert.equal(box.attributes.width,1000);assert.equal(box.attributes.height,800);
const plainWheel={ctrlKey:false,preventDefault(){throw Error('ordinary scroll was blocked');}};handlers.wheel(plainWheel);
zoomIn.onclick();assert(nav.getScale()>.335);zoomOut.onclick();assert(Math.abs(nav.getScale()-.335)<1e-10);
nav.zoomTo(1);map.onpointerdown({pointerId:1,clientX:150,clientY:100,preventDefault(){}});assert.equal(left,600);assert.equal(top,500);map.onpointerup();
left=200;top=100;handlers.scroll();assert.equal(box.attributes.x,200);assert.equal(box.attributes.y,100);
nav.reset(-1);assert.equal(overviewBox.hidden,true);
console.log('PASS actual pinch event handlers: zoom both directions, moving midpoint anchor, limits, native one-finger/ordinary scroll, fit, buttons, minimap location and viewport tracking, hidden landing overview.');

nav.reset(0);globalThis.getComputedStyle=()=>({paddingLeft:'20px',paddingRight:'20px',paddingTop:'20px',paddingBottom:'20px'});nav.fitAll();assert(Math.abs(nav.getScale()-.285)<1e-10);console.log('PASS fit accounts for viewport padding; miniature outlines remain readable independently of graph scale.');

graph.style.width='1000px';graph.style.height='800px';left=0;top=0;graph.querySelector=()=>({getBoundingClientRect(){const g=graph.getBoundingClientRect();return {left:g.left+800,top:g.top+200,width:0,height:0};}});nav.reset(0,{focusSelector:'[data-current-node]'});assert.equal(left,600);console.log('PASS page admission centers the new-node region instead of an empty graph margin.');

// The locator keeps the final topology while actual stage visits accumulate.
const visited=new Set(),first=fs.readFileSync('review/graphical/stage-1.svg','utf8');
rememberRegions(first,visited);
const firstOverview=overviewGraphic(original,visited);
assert.equal((firstOverview.match(/data-visited="true"/g)||[]).length,3);
assert.equal((firstOverview.match(/data-visited="false"/g)||[]).length,77);
assert(firstOverview.includes(original.match(/viewBox="[^"]+"/)[0]),'overview must preserve the final graph bounds');
rememberRegions(original,visited);rememberRegions(first,visited);
const revisited=overviewGraphic(original,visited);
assert.equal((revisited.match(/data-visited="true"/g)||[]).length,80);
assert(!revisited.includes('data-visited="false"'));
assert.equal((firstOverview.match(/data-visited=/g)||[]).length,(revisited.match(/data-visited=/g)||[]).length);
console.log('PASS final map stays complete; future nodes and edges are grey; visited regions remain highlighted when returning to an earlier stage.');

const {currentArchitectureSvg,currentArchitecture}=await import('./dist/current-architecture.js');
const currentVisited=new Set();rememberRegions(currentArchitectureSvg,currentVisited);const currentMini=overviewGraphic(currentArchitectureSvg,currentVisited);
assert.equal(currentVisited.size,currentArchitecture.nodes.length+currentArchitecture.edges.length);assert.equal((currentMini.match(/data-visited="true"/g)||[]).length,currentArchitecture.nodes.length+currentArchitecture.edges.length);
assert(!/data-current-node=|data-current-edge=|id="current-arrow"/.test(currentMini));
assert.equal((currentMini.match(/<rect /g)||[]).length,currentArchitecture.nodes.length+1,'minimap retains node rectangles and viewport, not blank edge labels');
console.log('PASS current overview identities, complete final map, unique markers and no empty label patches.');

// Framing must leave room for the locator and use actual content bounds.
for(const v of [{left:0,top:153,width:390,height:531},{left:0,top:141,width:1280,height:454}]){
 const b=[100,100,2520,2140],o={right:160,bottom:v.top+150};const f=contentFrame(v,b,o);
 assert(f.left>=o.right||f.top>=o.bottom);assert(f.width>=b[2]*f.scale-1e-8&&f.height>=b[3]*f.scale-1e-8);
}
graph.style.width='1000px';nav.reset(0,{initialScale:.5});assert.equal(nav.getScale(),.5);
console.log('PASS exact50% admission and chapter framing clear of the locator.');

// Full Map must center the complete diagram at its chosen scale, not a node.
graph.style.width='1000px';graph.style.height='800px';left=top=0;
nav.reset(0,{initialScale:.5,centerContent:true});
assert.equal(nav.getScale(),.5);assert.equal(left,50);assert.equal(top,50);
const centered=graph.getBoundingClientRect();assert.equal(centered.left+centered.width/2,220);assert.equal(centered.top+centered.height/2,180);
console.log('PASS Full Map at50% centers the whole diagram on both axes.');

// Introduction framing uses the added region rather than the cumulative canvas.
graph.getAttribute=name=>name==='viewBox'?'0 0 1000 800':name==='data-introduction-bounds'?'100 100 200 100':name==='data-content-bounds'?'0 0 1000 800':null;
graph.style.width='1000px';graph.style.height='800px';left=top=0;
nav.reset(2,{fitAdded:true});assert.equal(nav.getScale(),1.84);
console.log('PASS chapter opening zooms to its added region rather than the whole accumulated map.');
