import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
import {compile,searchRequirements} from './dist/recruiter-matcher.mjs';
const corpus=JSON.parse(fs.readFileSync('dist/recruiter-evidence.json'));
let focused;
class E{
 constructor(tag='div'){this.tagName=tag.toUpperCase();this.children=[];this.events={};this.attrs={};this.dataset={};this.hidden=false;this.value='';this.disabled=true;this._text='';this.classes=new Set();this.classList={toggle:(x,b)=>b?this.classes.add(x):this.classes.delete(x),remove:x=>this.classes.delete(x)};}
 set textContent(x){this._text=x;this.children=[];}get textContent(){return this._text+this.children.map(x=>x.textContent).join('');}
 append(...children){for(const c of children){c.parentNode=this;this.children.push(c);}}
 replaceChildren(){for(const c of this.children)c.parentNode=null;this.children=[];this._text='';}
 insertBefore(child,before){child.parentNode=this;this.children.splice(this.children.indexOf(before),0,child);}
 addEventListener(k,v){this.events[k]=v;}setAttribute(k,v){this.attrs[k]=v;}getAttribute(k){return this.attrs[k];}focus(){focused=this;}
 get hash(){return this.href?.includes('#')?'#'+this.href.split('#')[1]:'';}
 all(predicate){return this.children.flatMap(c=>[...(predicate(c)?[c]:[]),...c.all(predicate)]);}
 querySelector(s){if(s==='.recruiter-result:last-of-type')return this.all(c=>c.className==='recruiter-result').at(-1);return null;}
}
async function harness(fail=false){
 const elements={};for(const id of ['portfolio-theme','menu-toggle','primary-nav','requirements','recruiter-results','recruiter-status','recruiter-submit','recruiter-search','recruiter-clear','jump-results'])elements[id]=new E();
 const example=new E('button');example.dataset.example='Kubernetes, AWS and release automation';
 const doc={querySelector:s=>elements[s.slice(1)],querySelectorAll:()=>[example],createElement:t=>new E(t),addEventListener(){},getElementById:id=>elements[id]||elements['recruiter-results'].all(e=>e.id===id)[0]};
 const requests=[];const source=fs.readFileSync('dist/recruiters.mjs','utf8').replace(/^import .*;\n/gm,'');
 const context=vm.createContext({document:doc,window:{addEventListener(){}},location:{hash:''},initTheme:()=>({preference:'system',setPreference(){}}),compile,searchRequirements,fetch:async url=>{requests.push(url);if(fail)throw Error('blocked');return{ok:true,json:async()=>corpus};}});
 await vm.runInContext('(async()=>{'+source+'})()',context);
 return {elements,example,requests};
}
const {elements:e,example,requests}=await harness();
assert(!e['requirements'].disabled);assert(!e['recruiter-submit'].disabled);
const run=()=>e['recruiter-search'].events.submit({preventDefault(){}});
const rows=()=>e['recruiter-results'].all(x=>x.className==='recruiter-result');
e.requirements.value='Kubernetes\nRust\n<script>alert(1)</script>';run();assert.equal(rows().length,3);assert(e['recruiter-results'].textContent.includes('<script>alert(1)</script>'));assert(e['recruiter-results'].textContent.includes('No recognized terms'));assert(!e['jump-results'].hidden);
e['recruiter-clear'].events.click();assert.equal(e.requirements.value,'');assert.equal(rows().length,0);assert(e['jump-results'].hidden);assert.equal(focused,e.requirements);
run();assert(e['recruiter-status'].textContent.includes('Enter a skill'));
example.events.click();assert.equal(rows().length,1);example.events.click();assert.equal(rows().length,2);
e.requirements.value=Array.from({length:121},(_,i)=>`Python requirement ${i}`).join('\n');run();assert.equal(rows().length,50);const more=e['recruiter-results'].children.at(-1);assert(!more.hidden);more.events.click();assert.equal(rows().length,100);more.events.click();assert.equal(rows().length,121);assert(more.hidden);assert.equal(focused,rows().at(-1));assert(rows().at(-1).textContent.includes('Requirement 121'));
e.requirements.value='TypeScript';run();assert(e['recruiter-results'].textContent.includes('not a standalone deployment'));assert(e['recruiter-results'].all(x=>x.href==='./#anqr').length);
e.requirements.value='Kubernetes';run();assert(e['recruiter-results'].all(x=>x.href==='#career-paperly').length);
assert.deepEqual(requests,['./recruiter-evidence.json?v=45']);
const failed=await harness(true);assert(failed.elements.requirements.disabled);assert(failed.elements['recruiter-status'].textContent.includes('could not load'));
console.log('PASS DOM harness: initialization, search, unknown terms, safe text, clear/focus, examples, all 121 paginated results, citations, internal project/company links, single static fetch, load failure. Not browser/layout verification.');
