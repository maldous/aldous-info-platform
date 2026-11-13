import {initTheme} from './theme.js';
const theme=initTheme();
const select=document.querySelector('#portfolio-theme');
function updateToggle(){const dark=document.documentElement.dataset.theme==='dark';select.setAttribute('aria-checked',String(dark));select.title=`Switch to ${dark?'light':'dark'} theme`;}
updateToggle();
select.addEventListener('click',()=>{theme.setPreference(document.documentElement.dataset.theme==='dark'?'light':'dark');updateToggle();});
new MutationObserver(updateToggle).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
const filters=[...document.querySelectorAll('[data-filter]')];
const projects=[...document.querySelectorAll('[data-category]')];
const count=document.querySelector('#project-count');
for(const button of filters)button.addEventListener('click',()=>{
 const category=button.dataset.filter;
 for(const b of filters)b.setAttribute('aria-pressed',String(b===button));
 for(const project of projects)project.hidden=category!=='all'&&!project.dataset.category.split(' ').includes(category);
 count.textContent=`${projects.filter(p=>!p.hidden).length} projects shown`;
});
const menu=document.querySelector('#menu-toggle'),nav=document.querySelector('#primary-nav');
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);});
nav.addEventListener('click',e=>{if(e.target.closest('a')){menu.setAttribute('aria-expanded','false');nav.classList.remove('open');}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){menu.setAttribute('aria-expanded','false');nav.classList.remove('open');menu.focus?.();}});

