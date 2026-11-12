import {graphSvgs} from './graph-layouts.js?v=41-tools-mobile-zoom';
export const capabilities=[
{id:'local',title:'Compute',products:'Compute runs your code',responsibility:'Try ideas and get quick feedback.',resources:['node-runner','node-code']},
{id:'engineering',title:'Review',products:'GitHub keeps changes reviewable',responsibility:'Share, discuss and accept changes.',resources:['node-workspace','node-github','node-pr','node-review','node-policy']},
{id:'agents',title:'Coding',products:'Codex / Claude helps with coding',responsibility:'Turn a clear request into a proposed change.',resources:['node-isolated','node-provider','node-tools']},
{id:'workflow',title:'Memory',products:'LangGraph remembers progress',responsibility:'See where a task stopped and how to continue.',resources:['node-delivery','node-langgraph','node-sqlite']},
{id:'ownership',title:'Coordination',products:'Sokolovski coordinates AI work',responsibility:'Connect tasks, workers and review feedback.',resources:['node-stokowski','node-supervisor','node-journal','node-linear']},
{id:'execution',title:'Jobs',products:'Windmill runs background jobs',responsibility:'Run checks on compute and bring back results.',resources:['node-windmill','node-adapter','node-bridge','node-integration']},
{id:'autonomy',title:'Automation',products:'The layers work together',responsibility:'Confirm the result before moving to the next task.',resources:['node-durable','node-threads','node-wm_mcp']}];
export function buildCoverage(catalog){const nodeStage=new Map();capabilities.forEach((c,i)=>c.resources.forEach(id=>{if(nodeStage.has(id))throw Error('Duplicate resource');nodeStage.set(id,i);}));if(catalog.resources.some(r=>!nodeStage.has(r.id))||nodeStage.size!==catalog.resources.length)throw Error('Every resource needs a capability stage');const edges=catalog.relationships.map(e=>{if(!nodeStage.has(e.source)||!nodeStage.has(e.target)||!e.protocol||!e.payload||!e.purpose)throw Error('Every communication needs endpoints, protocol, exchange and purpose');return{id:e.id,stage:Math.max(nodeStage.get(e.source),nodeStage.get(e.target))};});if(new Set(edges.map(e=>e.id)).size!==edges.length)throw Error('Duplicate communication');return{catalog,resources:[...nodeStage].map(([id,stage])=>({id,stage})),relationships:edges};}
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
export function wrap(s,n){let row='';const a=[];for(const w of s.split(/\s+/)){if(row.length+w.length>n){a.push(row);row='';}row+=(row?' ':'')+w;}if(row)a.push(row);return a;}
const text=(s,x,y,size=20,max=24,color='var(--text)')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}">${wrap(s,max).map((v,i)=>`<tspan x="${x}" dy="${i?size*1.25:0}">${esc(v)}</tspan>`).join('')}</text>`;
export function capabilityGraphic(index,coverage,compact=false){
 if(index<0){
  const w=compact?360:1040,h=compact?560:660;
  const layerTitles=["Compute", "Review", "Coding", "Memory", "Coordination", "Jobs", "Automation"];
  const descriptions=['Compute runs your code','GitHub shares and reviews changes','Codex / Claude helps with coding','LangGraph remembers progress','Sokolovski coordinates AI work','Windmill runs background jobs','Connect the full delivery loop'];
  const baseX=compact?20:460,baseW=compact?320:540,top=compact?132:54,gap=compact?54:76,layerH=compact?48:66;
  const foundationY=top+5*gap-6;
  return `<svg xmlns="http://www.w3.org/2000/svg" class="foundation-stack" viewBox="0 0 ${w} ${h}" role="group" aria-label="OffMenu capability stack, built from Compute at the bottom to Automation at the top">
  ${text('BUILT FROM THE BOTTOM UP',compact?20:40,compact?27:88,12,50,'var(--subtle)')}
  ${text('Every layer builds on the foundations.',compact?20:40,compact?61:142,compact?24:36,compact?29:20)}
  ${text(compact?'Start at the base. Select a layer to explore.':'Start with local compute and GitHub. Then add capabilities, one layer at a time.',compact?20:40,compact?112:290,compact?12:18,compact?60:33,'var(--subtle)')}
  ${!compact?text('Explore the connections after the stack.',40,422,16,35,'var(--subtle)'):''}
  <rect x="${baseX-8}" y="${foundationY}" width="${baseW+16}" height="${gap+layerH+12}" rx="12" fill="var(--group-fill)"/>
  ${capabilities.map((c,i)=>{
   const x=baseX+i*(compact?6:10),y=top+(6-i)*gap,width=baseW-i*(compact?12:20);
   return `<g data-stage="${i}" tabindex="0" role="button" aria-label="Open ${c.title}">
    <rect x="${x}" y="${y}" width="${width}" height="${layerH}" rx="6" fill="var(--panel)" stroke="${i<2?'var(--edge)':'var(--active)'}" stroke-width="1.5"/>
    <text x="${x+18}" y="${y+(compact?28:39)}" font-size="${compact?13:16}" fill="var(--subtle)">${String(i+1).padStart(2,'0')}</text>
    ${text(layerTitles[i],x+(compact?47:56),y+(compact?19:27),compact?16:21,40)}
    ${text(descriptions[i],x+(compact?47:56),y+(compact?37:49),compact?11:14,60,'var(--subtle)')}
   </g>`;
  }).join('')}
  ${text('TRADITIONAL DEVELOPMENT FOUNDATION',compact?20:460,compact?540:622,compact?10:12,60,'var(--subtle)')}
  </svg>`;
 }
 const width=Math.max(340,Number(graphSvgs[index].match(/viewBox="[^"]*"/)[0].split(' ')[2]));return graphSvgs[index].replace('<svg ',`<svg style="width:${width}px;min-width:${width}px;max-height:none;height:auto;margin:auto" `);
}
