import {graphSvgs} from './graph-layouts.js?v=41-tools-mobile-zoom';
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
export function viewportLocator(viewBox,graph,viewport){
 const [x,y,w,h]=viewBox,sx=graph.width/w,sy=graph.height/h;
 const left=clamp(x+(viewport.left-graph.left)/sx,x,x+w),top=clamp(y+(viewport.top-graph.top)/sy,y,y+h);
 const right=clamp(x+(viewport.left+viewport.width-graph.left)/sx,x,x+w),bottom=clamp(y+(viewport.top+viewport.height-graph.top)/sy,y,y+h);
 return {x:left,y:top,width:Math.max(0,right-left),height:Math.max(0,bottom-top)};
}
export function mapPoint(viewBox,rect,clientX,clientY){
 const [x,y,w,h]=viewBox,s=Math.min(rect.width/w,rect.height/h),ox=rect.left+(rect.width-w*s)/2,oy=rect.top+(rect.height-h*s)/2;
 return {x:clamp(x+(clientX-ox)/s,x,x+w),y:clamp(y+(clientY-oy)/s,y,y+h)};
}
export function rememberRegions(markup,visited){
 for(const match of markup.matchAll(/data-(actor|handoff|current-node|current-edge)="([^"]+)"/g))visited.add(match[1]+':'+match[2]);
}
export function overviewGraphic(markup,visited=new Set()){
 markup=markup.replace(/<g data-(actor|handoff|current-node|current-edge)="([^"]+)"/g,(_,kind,id)=>`<g data-visited="${visited.has(kind+':'+id)}" data-${kind}="${id}"`);
 return markup.replace(/<text\b[\s\S]*?<\/text>/g,'')
 .replace(/<path\b[^>]*stroke="transparent"[^>]*\/>/g,'')
 .replace(/(<g\b(?=[^>]*data-(?:handoff|current-edge)=)[^>]*>)([\s\S]*?)(<\/g>)/g,(_,a,b,c)=>a+b.replace(/<rect\b[^>]*\/>/g,'')+c)
 .replace(/\s(?:style|role|tabindex|aria-label|data-actor|data-handoff|data-current-node|data-current-edge)="[^"]*"/g,'')
 .replace(/edge-arrow/g,'overview-arrow')
 .replace(/current-arrow/g,'overview-current-arrow')
 .replace(/fill="var\(--(?:edge|active)\)"/g,'fill="context-stroke"')
 .replace('<svg ','<svg aria-hidden="true" preserveAspectRatio="xMidYMid meet" ')
 .replace('</svg>','<rect id="map-viewport" fill="var(--active)" fill-opacity=".12" stroke="var(--active)" stroke-width="2" vector-effect="non-scaling-stroke" pointer-events="none"/></svg>');
}
// Select the largest content-fitting rectangle clear of the overview and view buttons.
export function contentFrame(v,bounds,overlay=null){
 const pad=16,top=v.top+48,base={left:v.left+pad,top,width:v.width-2*pad,height:v.height-48-pad};
 const frames=[base];
 if(overlay&&overlay.right>base.left&&overlay.bottom>base.top){
  const left=Math.max(base.left,overlay.right+pad),below=Math.max(base.top,overlay.bottom+pad);
  frames.splice(0,1,{left,top:base.top,width:v.left+v.width-pad-left,height:base.height},{left:base.left,top:below,width:base.width,height:v.top+v.height-pad-below});
 }
 return frames.filter(r=>r.width>0&&r.height>0).map(r=>({...r,scale:Math.min(r.width/bounds[2],r.height/bounds[3])})).sort((a,b)=>b.scale-a.scale)[0];
}
export function installGraphNavigation({scene,overview,map,zoomIn,zoomOut,fit,readout,onGesture,finalGraphic=graphSvgs.at(-1)}){
 const visited=new Set();let overviewViewBox=finalGraphic.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
 let graph=null,viewBox=null,scale=1,baseWidth=0,baseHeight=0,pinch=null,mapDragging=false;
 const viewport=()=>{const r=scene.getBoundingClientRect();return {left:r.left+scene.clientLeft,top:r.top+scene.clientTop,width:scene.clientWidth,height:scene.clientHeight};};
 const center=()=>{const v=viewport();return {clientX:v.left+v.width/2,clientY:v.top+v.height/2};};
 function update(){
  if(!graph)return;
  const r=viewportLocator(viewBox,graph.getBoundingClientRect(),viewport()),box=map.querySelector('#map-viewport');
  for(const [k,v] of Object.entries(r))box.setAttribute(k,v);
  readout.textContent=Math.round(scale*100)+'%';zoomIn.disabled=scale>=4;zoomOut.disabled=scale<=.1;
 }
 function zoomTo(next,anchor=center()){
  if(!graph)return;next=clamp(next,.1,4);
  const before=graph.getBoundingClientRect(),fx=anchor.fx??(anchor.clientX-before.left)/before.width,fy=anchor.fy??(anchor.clientY-before.top)/before.height;
  scale=next;graph.style.width=baseWidth*scale+'px';graph.style.minWidth=baseWidth*scale+'px';graph.style.height=baseHeight*scale+'px';
  const after=graph.getBoundingClientRect();scene.scrollLeft+=after.left+fx*after.width-anchor.clientX;scene.scrollTop+=after.top+fy*after.height-anchor.clientY;update();
 }
 function contentBounds(){const value=graph?.getAttribute('data-content-bounds');return value?value.split(/\s+/).map(Number):null;}
 function frame(bounds){return contentFrame(viewport(),bounds,overview.getBoundingClientRect?.()??null);}
 function place(bounds,target){
  if(scene.style){scene.style.padding='16px';scene.style.paddingLeft='16px';scene.style.paddingTop='16px';}
  scene.scrollLeft=0;scene.scrollTop=0;
  const r=graph.getBoundingClientRect(),sx=r.width/viewBox[2],sy=r.height/viewBox[3];
  const dx=target.left+target.width/2-(r.left+(bounds[0]+bounds[2]/2-viewBox[0])*sx),dy=target.top+target.height/2-(r.top+(bounds[1]+bounds[3]/2-viewBox[1])*sy);
  if(dx>0&&scene.style)scene.style.paddingLeft=16+dx+'px';else scene.scrollLeft=-dx;
  if(dy>0&&scene.style)scene.style.paddingTop=16+dy+'px';else scene.scrollTop=-dy;
  update();
 }
 function fitAll(){fitBounds(contentBounds());}
 function fitBounds(bounds){
  if(!graph)return;
  if(bounds){const target=frame(bounds);zoomTo(target.scale);place(bounds,target);return;}
  const s=getComputedStyle(scene),px=parseFloat(s.paddingLeft)+parseFloat(s.paddingRight),py=parseFloat(s.paddingTop)+parseFloat(s.paddingBottom);zoomTo(Math.min((scene.clientWidth-px-32)/baseWidth,(scene.clientHeight-py-32)/baseHeight));scene.scrollLeft=0;scene.scrollTop=0;update();
 }
 function reset(index,options={}){
  if(scene.style){scene.style.padding='';scene.style.paddingLeft='';scene.style.paddingTop='';}
  pinch=null;graph=index<0?null:scene.querySelector('svg');overview.hidden=!graph;
  if(!graph)return;
  graph.style.margin='0';
  viewBox=graph.getAttribute('viewBox').split(/\s+/).map(Number);baseWidth=parseFloat(graph.style.width);baseHeight=baseWidth*viewBox[3]/viewBox[2];scale=1;
  const miniature=options.overviewGraphic??finalGraphic;overviewViewBox=miniature.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);rememberRegions(graph.outerHTML,visited);map.innerHTML=overviewGraphic(miniature,visited);graph.style.height=baseHeight+'px';
  if(options.fitAdded){const value=graph.getAttribute('data-introduction-bounds');fitBounds(value?value.split(/\s+/).map(Number):contentBounds());return;}
  if(options.fitContent){fitAll();return;}
  if(options.initialScale)zoomTo(options.initialScale);
  if(options.centerContent){place(contentBounds()??viewBox,viewport());return;}
  const focus=options.focusSelector?graph.querySelector?.(options.focusSelector):null;
  if(focus){const r=focus.getBoundingClientRect(),g=graph.getBoundingClientRect(),bounds=[viewBox[0]+(r.left-g.left)*viewBox[2]/g.width,viewBox[1]+(r.top-g.top)*viewBox[3]/g.height,r.width*viewBox[2]/g.width,r.height*viewBox[3]/g.height];place(bounds,frame(bounds));}
  update();
 }
 zoomIn.onclick=()=>zoomTo(scale*1.25);zoomOut.onclick=()=>zoomTo(scale/1.25);fit.onclick=fitAll;
 scene.addEventListener('scroll',update,{passive:true});addEventListener('resize',update);
 const fingers=touches=>{const [a,b]=touches;return {distance:Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY),clientX:(a.clientX+b.clientX)/2,clientY:(a.clientY+b.clientY)/2};};
 scene.addEventListener('touchstart',e=>{
  if(!graph||e.touches.length!==2)return;e.preventDefault();onGesture();
  const f=fingers(e.touches),r=graph.getBoundingClientRect();pinch={...f,scale,fx:(f.clientX-r.left)/r.width,fy:(f.clientY-r.top)/r.height};
 },{passive:false});
 scene.addEventListener('touchmove',e=>{
  if(!pinch||e.touches.length!==2)return;e.preventDefault();onGesture();const f=fingers(e.touches);
  zoomTo(pinch.scale*f.distance/Math.max(1,pinch.distance),{...f,fx:pinch.fx,fy:pinch.fy});
 },{passive:false});
 const endPinch=e=>{if(pinch){onGesture();if(e.touches.length<2)pinch=null;}};
 scene.addEventListener('touchend',endPinch,{passive:true});scene.addEventListener('touchcancel',endPinch,{passive:true});
 // Trackpad pinch uses ctrl+wheel. Ordinary wheel scrolling remains native.
 scene.addEventListener('wheel',e=>{if(!graph||!e.ctrlKey)return;e.preventDefault();onGesture();zoomTo(scale*Math.exp(-e.deltaY*.01),e);},{passive:false});
 function locate(e){
  if(!graph)return;const p=mapPoint(overviewViewBox,map.querySelector('svg').getBoundingClientRect(),e.clientX,e.clientY),r=graph.getBoundingClientRect(),v=viewport();
  scene.scrollLeft+=r.left+(p.x-viewBox[0])*r.width/viewBox[2]-(v.left+v.width/2);
  scene.scrollTop+=r.top+(p.y-viewBox[1])*r.height/viewBox[3]-(v.top+v.height/2);update();
 }
 map.onpointerdown=e=>{e.preventDefault();mapDragging=true;map.setPointerCapture(e.pointerId);locate(e);};
 map.onpointermove=e=>{if(mapDragging)locate(e);};map.onpointerup=()=>{mapDragging=false;};map.onpointercancel=()=>{mapDragging=false;};
 return {reset,update,zoomTo,fitAll,getScale:()=>scale};
}
