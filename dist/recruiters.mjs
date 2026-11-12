import {initTheme} from './theme.js';
import {compile,searchRequirements} from './recruiter-matcher.mjs?v=45';
const theme=initTheme(), select=document.querySelector('#portfolio-theme');
select.value=theme.preference;select.addEventListener('change',()=>theme.setPreference(select.value));
const menu=document.querySelector('#menu-toggle'),nav=document.querySelector('#primary-nav');
function closeMenu(){menu.setAttribute('aria-expanded','false');nav.classList.remove('open');}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);});
nav.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus();}});
const input=document.querySelector('#requirements'),results=document.querySelector('#recruiter-results'),status=document.querySelector('#recruiter-status'),submit=document.querySelector('#recruiter-submit');
let catalog;
try{
 const response=await fetch('./recruiter-evidence.json?v=45');
 if(!response.ok)throw new Error('Evidence unavailable');
 catalog=compile(await response.json());submit.disabled=false;input.disabled=false;
 status.textContent='Search a skill or paste requirements to begin.';
}catch{status.textContent='Search could not load. Browse all skills and sources below, or reload to try again.';}
const node=(tag,text,className)=>{const n=document.createElement(tag);n.textContent=text;if(className)n.className=className;return n;};
const labels={'profile-listed':'Listed in GitHub profile','self-reported':'Confirmed by Matthew','education':'Education','cv-role':'Role evidence','cv-listed':'Listed in résumé','project':'Project source'};
function citation(evidence){
 const block=node('div','');block.append(node('p',labels[evidence.kind],'evidence-label'),node('p',evidence.quote));
 const link=node('a',evidence.section,'recruiter-citation');link.href=evidence.url;block.append(link);if(evidence.contextUrl){const p=node('p','');const context=node('a',evidence.contextLabel,'recruiter-citation');context.href=evidence.contextUrl;p.append(context);block.append(p);}if(evidence.limitation)block.append(node('p',evidence.limitation,'recruiter-footnote'));return block;
}
function search(){
 results.replaceChildren();document.querySelector('#jump-results').hidden=true;if(!catalog)return;
 let report;
 try{report=searchRequirements(input.value,catalog);}catch(error){status.textContent=error.message;return;}
 if(!report.lines.length){status.textContent='Enter a skill or requirement, or browse the evidence below.';input.focus();return;}
 document.querySelector('#jump-results').hidden=false;
 const heading=node('div','','recruiter-result-head');const title=node('h2','Requirements and evidence');title.id='results-heading';title.tabIndex=-1;heading.append(title);
 const browse=node('a','Browse all skills','text-link');browse.href='#skills';heading.append(browse);results.append(heading,node('p',report.disclaimer,'recruiter-help'));
 let shown=0;const more=node('button','Show next 50 requirements','button recruiter-secondary');more.type='button';
 const renderBatch=()=>{
 const batch=report.lines.slice(shown,shown+50);
 for(const [offset,line] of batch.entries()){const index=shown+offset;
  const row=node('article','','recruiter-result');row.append(node('h3',`Requirement ${index+1}`),node('p',line.text,'recruiter-input-line'));
  if(!line.matches.length)row.append(node('p','No recognized terms in this evidence index. That does not mean the experience is absent. Review the résumé or ask Matthew.','recruiter-help'));
  else{
   row.append(node('p','Evidence for recognized terms. Other parts of this requirement may not have been recognized.','recruiter-help'));
   const list=node('ul','');
   for(const match of line.matches){
    const item=node('li',''),title=node('a',match.label,'text-link');title.href=`#skill-${match.id}`;item.append(title,citation(match.evidence[0]));
    if(match.evidence.length>1){const details=node('details','');details.append(node('summary',`${match.evidence.length-1} more source${match.evidence.length>2?'s':''}`));for(const e of match.evidence.slice(1))details.append(citation(e));item.append(details);}
    list.append(item);
   }row.append(list);
  }if(more.parentNode)results.insertBefore(row,more);else results.append(row);
 }
 shown+=batch.length;more.hidden=shown>=report.lines.length;more.textContent=`Show next ${Math.min(50,report.lines.length-shown)} requirements`;
 };
 renderBatch();more.addEventListener('click',()=>{renderBatch();status.textContent=`Showing ${shown} of ${report.lines.length} requirements.`;if(more.hidden){const final=results.querySelector('.recruiter-result:last-of-type');if(final){final.tabIndex=-1;final.focus();}}});results.append(more);
 status.textContent=`${report.lines.length} text line${report.lines.length===1?'':'s'} reviewed. Evidence found for ${report.matchedSkills.length} distinct indexed term${report.matchedSkills.length===1?'':'s'}. Results are below${report.lines.length>50?`; showing the first 50, with more available`:''}.`;
}
document.querySelector('#recruiter-search').addEventListener('submit',event=>{event.preventDefault();search();});
document.querySelector('#recruiter-clear').addEventListener('click',()=>{input.value='';results.replaceChildren();document.querySelector('#jump-results').hidden=true;status.textContent='Text and results cleared.';input.focus();});
for(const button of document.querySelectorAll('[data-example]'))button.addEventListener('click',()=>{
 if(!catalog)return;
 const next=[input.value.trim(),button.dataset.example].filter(Boolean).join('\n');
 if(next.length>30000){status.textContent='This example would exceed 30,000 characters. Shorten the text first.';return;}
 input.value=next;search();
});
function reveal(){const hash=location.hash.slice(1);if(!hash.startsWith('skill-'))return;const target=document.getElementById(hash);if(target?.tagName==='DETAILS')target.open=true;}
window.addEventListener('hashchange',reveal);reveal();
// A citation to an already-selected hash must reopen its details after manual closure.
document.addEventListener('click',event=>{const link=event.target.closest('a[href^="#skill-"]');if(link){const target=document.getElementById(link.hash.slice(1));if(target?.tagName==='DETAILS')target.open=true;}});

document.querySelector('#jump-results').addEventListener('click',()=>document.querySelector('#results-heading')?.focus());
