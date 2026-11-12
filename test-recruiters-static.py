from pathlib import Path
from html.parser import HTMLParser
import json,re
root=Path('dist')
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.assets=[];self.scripts=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a':self.links.append(a.get('href',''))
  if tag=='script':self.scripts.append(a.get('src',''))
  for key in ['src','href']:
   if a.get(key) and not a[key].startswith(('http','mailto:','#','./#')):self.assets.append(a[key])
p=Parser();s=(root/'recruiters.html').read_text();p.feed(s)
assert len(p.ids)==len(set(p.ids))
for href in p.links:
 if href.startswith('#'):assert href[1:] in p.ids or href=='#results-heading',href
for asset in p.assets:assert (root/asset.split('?')[0].split('#')[0]).exists(),asset
assert p.scripts==['theme-init.js','recruiters.mjs?v=45']
assert len(re.findall('class="recruiter-skill"',s))==94
assert len(re.findall('class="career-group"',s))==5
for company in ['paperly','citoplus','lexer','lynkstate','subspace','telstra']:
 m=re.search(r'id="career-'+company+r'"><time>(.*?)</time><h5>(.*?)</h5>',s);assert m and m.group(2).lower()==company
c=json.loads((root/'recruiter-evidence.json').read_text());assert c==json.loads(Path('recruiter-data/evidence.json').read_text())
for skill in c['skills']:
 assert 'skill-'+skill['id'] in p.ids
 for evidence in skill['evidence']:
  assert evidence['quote'] in __import__('html').unescape(s)
  if evidence.get('contextUrl','').startswith('#'):assert evidence['contextUrl'][1:] in p.ids
  assert evidence['url'].startswith(('https://aldous.info/Matthew-Aldous-Resume-2026.pdf#page=','https://github.com/maldous/','https://aldous.info/recruiters.html#languages'))
  if evidence['kind']=='project':assert re.search('/blob/[a-f0-9]{40}/README.md$',evidence['url']) and evidence['limitation']
script=(root/'recruiters.mjs').read_text()
assert script.count('fetch(')==1 and "fetch('./recruiter-evidence.json?v=45')" in script
for bad in ['innerHTML','outerHTML','insertAdjacentHTML','sendBeacon','localStorage','sessionStorage','XMLHttpRequest','WebSocket','location.search','pushState','replaceState']:
 assert bad not in script,bad
assert 'textContent=text' in script
assert 'maxlength="30000"' in s and 'role="status"' in s and 'aria-describedby="input-help input-privacy"' in s
assert 'id="jump-results"' in s
assert not re.search(r'/home/|/workspace/|libfile_|file_0000|BEGIN PRIVATE KEY',s)
assert '<link rel="canonical" href="https://aldous.info/recruiters.html">' in s
print('PASS static evidence, references, assets, career anchors, source permission surface, input privacy and accessible form contracts.')
