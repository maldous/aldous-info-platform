import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {createServer} from 'node:net';

const probe=createServer();probe.listen(0,'127.0.0.1');await once(probe,'listening');
const port=probe.address().port;await new Promise(resolve=>probe.close(resolve));
const server=spawn('python3',['-m','http.server',String(port),'--bind','127.0.0.1','--directory','build'],{stdio:'ignore'});
const base=`http://127.0.0.1:${port}/`;
let browser;
try {
  for(let i=0;i<50;i++) {try {if((await fetch(base)).ok)break;}catch{} await new Promise(r=>setTimeout(r,100));}
  browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});
  const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  const page=await context.newPage(),errors=[],requests=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>requests.push(r.url()));
  await page.goto(base);assert.equal(await page.title(),'Matthew Aldous · Engineering, architecture & independent projects');
  assert.equal(await page.locator('[data-category]').count(),11);
  await page.locator('[data-filter="research"]').click();assert.equal(await page.locator('[data-category]:visible').count(),6);
  await page.locator('[data-filter="all"]').click();assert.equal(await page.locator('[data-category]:visible').count(),11);
  for(const width of [320,390,768,1440]){await page.setViewportSize({width,height:1000});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
  await page.goto(base+'recruiters.html');await page.waitForFunction(()=>!document.querySelector('#recruiter-submit').disabled);
  assert.equal(await page.locator('.recruiter-skill').count(),94);
  for(const width of [320,390,768,1440]){await page.setViewportSize({width,height:1000});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
  await page.waitForLoadState('networkidle');requests.length=0;
  await page.locator('#requirements').fill('Kubernetes and TypeScript\nzzznomatchzzz\n<img src=x onerror=alert(1)>');
  await page.locator('#recruiter-submit').click();assert.equal(await page.locator('.recruiter-result').count(),3);
  assert.equal(await page.locator('#recruiter-results img').count(),0);assert((await page.locator('#recruiter-results').innerText()).includes('Kubernetes'));
  assert((await page.locator('#recruiter-results').innerText()).includes('No recognized terms'));
  await page.waitForTimeout(100);assert.deepEqual(requests,[], 'Search must not transmit pasted requirements');
  await page.locator('#recruiter-clear').click();assert.equal(await page.locator('#requirements').inputValue(),'');
  await page.locator('#requirements').fill(Array(121).fill('Python').join('\n'));await page.locator('#recruiter-submit').click();
  assert.equal(await page.locator('.recruiter-result').count(),50);await page.getByRole('button',{name:'Show next 50 requirements'}).click();
  assert.equal(await page.locator('.recruiter-result').count(),100);await page.getByRole('button',{name:'Show next 21 requirements'}).click();
  assert.equal(await page.locator('.recruiter-result').count(),121);
  await page.locator('#portfolio-theme').selectOption('dark');assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
  await page.goto(base+'architecture.html');await page.waitForSelector('#scene');
  assert.deepEqual(errors,[]);
  console.log(JSON.stringify({result:'PASS',browser:browser.version(),pages:3,widths:[320,390,768,1440],projectCards:11,evidenceSkills:94,paginationRows:121,searchNetworkRequests:0,checks:['project filters','responsive layout','search','unknown input','XSS-safe text','clear','pagination','theme','architecture load']}));
} finally {if(browser)await browser.close();server.kill();}
