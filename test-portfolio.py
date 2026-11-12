from pathlib import Path
from html.parser import HTMLParser
import re
root=Path('dist')
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.assets=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a':self.links.append(a.get('href',''))
  for key in ['src','href']:
   if a.get(key) and not a[key].startswith(('http','mailto:','#')):self.assets.append(a[key])
p=Parser();p.feed(root.joinpath('index.html').read_text())
assert len(p.ids)==len(set(p.ids)), 'Duplicate IDs'
for href in p.links:
 if href.startswith('#'):assert href[1:] in p.ids,href
for asset in p.assets:
 path=asset.split('?')[0].split('#')[0]
 assert (root/path).exists(),path
text=root.joinpath('index.html').read_text()
for subject in ['OffMenu','ANQR','UIF / USF','Morgan','Circular Quay','Lixit','Colour Index','CADLE','NEEG','Bayesian Bot','GANN','ANNYWAY','MILC','Solution Leaflet']:assert subject in text,subject
assert 'Sample dashboard view · values shown are illustrative.' not in text
assert 'Decorative Morgan project diagram, not live monitoring data.' not in text
assert text.count('Morgan compact native-workstream snapshot captured')==1
assert text.count('Captured image, not live status.')==1
assert 'Products you can try.' not in text
assert 'Interface concept' not in text
assert len(re.findall('class="career-group"',text))==5
assert len(re.findall('<time>',text))==12
assert 'career-rail' not in text and 'data-scroll' not in text
assert len(re.findall('class="feature"',text))==11
assert 'Engineering ideas.' not in text
assert 'Ideas with a longer history.' not in text
assert 'Original archival illustrations from my historical CV' not in text
assert '<h2>Other</h2>' in text
assert 'I’m Matthew, a Melbourne-based engineer. I connect architecture with practical delivery and am available for fully remote work.' in text
assert text.count('matthew.aldous@gmail.com</a></h')==2
assert 'aria-label="Colour theme"' not in text # label is provided as a real label
assert '<label class="sr-only" for="portfolio-theme">Colour theme</label>' in text
assert 'id="scene"' in root.joinpath('architecture.html').read_text()
assert not re.search(r'/home/|/workspace/|libfile_|file_0000|sk_live|BEGIN PRIVATE KEY',text)
print('PASS portfolio anchors, unique IDs, all local assets, project/archive coverage, career timeline, theme label, retained architecture and public-content hygiene.')

assert re.findall(r"<h4>(.*?)</h4>", text)==["Australia (Academia)","Europe (Enterprise)","Australia (Enterprise)","USA (Startup)","Australia (Startup)"]

assert 'class="project-row"' not in text
assert 'href="#research"' not in text
assert text.count('<h3>Morgan monitoring</h3>') == 1
assert text.count('<h3>Circular Quay</h3>') == 1
assert 'anqr-i18n' in text and 'colour-index-compression' in text and 'usf-v3' in text

assert 'class="section-toolbar"' not in text
assert 'class="hero-index"' not in text
header = re.search(r'<header.*?</header>', text).group()
for destination in ['#work', 'recruiters.html', '#about', 'recruiters.html#technical-experience', '#other', '#contact']:
 assert f'href="{destination}"' in header
assert header.count('<nav ') == 1
assert 'Matthew Aldous<span>.</span>' not in header
assert 'class="theme-icon"' in header
assert 'title="Colour theme"' in header
for choice in ['system', 'light', 'dark']: assert f'value="{choice}"' in header

assert "<h2>Projects</h2>" in text
assert '<h3>Robox Gaming</h3>' in text
assert 'Proof-of-concept adventure-world games built in Roblox.' in text
assert text.index('<h3>Solution Leaflet</h3>') < text.index('<h3>Robox Gaming</h3>')

assert 'View projects' not in text
hero_actions=re.search(r'<div class="hero-actions">.*?</div>',text).group()
assert '<a class="button" href="Matthew-Aldous-Resume-2026.pdf">Résumé' in hero_actions
recruiters=root.joinpath('recruiters.html').read_text()
assert recruiters.count('class="technical-group"') == 6
assert text.count('id="technical-experience"') == 0
assert recruiters.count('id="technical-experience"') == 1
assert 'ISO 27001-aligned' in recruiters and '250+ schools' in recruiters
assert 'Full technology background, including earlier platforms' in recruiters
assert 'Authored the primary data analysis for network location and coverage maps.' in recruiters
assert 'Start with the requirements.' not in recruiters

footer=re.search(r'<footer.*?</footer>',text,re.S).group()
badges=__import__('json').loads((root.parent/'recruiter-data'/'footer-badges.json').read_text())
assert footer.count('https://img.shields.io/badge/') == len(badges)
assert len(badges) >= 261
assert 'footer-badges-label' not in footer
assert 'class="skill-badges"' in footer
assert 'class="technical-experience"' not in text

# Complete profile wall and precisely three supported badges per project.
profile=__import__('json').loads((root.parent/'recruiter-data'/'footer-badges.json').read_text())
projects=__import__('json').loads((root.parent/'recruiter-data'/'project-badges.json').read_text())
assert len(profile)==273 and len({b['url'] for b in profile})==273
for project in projects:
    article=re.search(r'<article\b[^>]*id="'+re.escape(project['id'])+r'"[^>]*>.*?</article>',text,re.S).group()
    strip=re.search(r'<div class="project-badges".*?</div>',article,re.S).group()
    assert strip.count('<img ')==3, project['id']
    assert article.count('class="project-badges"')==1, project['id']
    assert len(project['badges'])==3
    for badge in project['badges']:
        assert badge['url'] in {b['url'] for b in profile}
    assert article.index('project-badges') > article.index('</p>')
    if 'class="text-link"' in article:
        assert article.index('project-badges') < article.index('class="text-link"')
assert len(projects)==18
print('PASS complete 273-badge profile wall and three source-backed badges for all 18 projects.')
# Generic badges must be coloured individually, not merge into one grey text field.
assert all(b['color'].lower() != '#475569' for b in profile)
assert '-475569?' not in footer
palette=['1D4ED8','0F766E','7E22CE','B45309','BE123C','0369A1','4D7C0F','A21CAF','4338CA','C2410C']
for color in palette:
    rgb=[int(color[i:i+2],16)/255 for i in (0,2,4)]
    linear=[c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in rgb]
    luminance=sum(c*w for c,w in zip(linear,[.2126,.7152,.0722]))
    assert 1.05/(luminance+.05) >= 4.5, color
print('PASS individually coloured generic badges with white-text contrast >=4.5:1.')

# Linked research asset, not a reproduction of the article.
article=re.search(r'<article[^>]+id="navigating-digital-pathways".*?</article>',text,re.S).group()
assert 'data-category="research"' in article
assert 'https://www.linkedin.com/pulse/navigating-digital-pathways-illuminating-network-ai-nlp-aldous' in article
assert 'AI research &amp; development' in article
assert len(re.sub(r"<[^>]+>", "", article).split()) < 110

assert article.count('class="feature-image"') == 1
assert article.count('https://img.shields.io/badge/') == 3
for label in ["IP embeddings", "Network topology", "NLP summaries"]:
    assert text.count('alt="'+label+'"') == 1

feature=re.search(r'<section class="section morgan".*?</section>',text,re.S).group()
assert 'id="network-intelligence"' in feature
assert "Navigating Digital Pathways" in feature and "retrieval-augmented generation (RAG)" in feature
assert "Directions for extending this work" in feature
assert "morgan-current.jpg" not in feature

assert "ip-geolocation-map.jpg" in feature
assert "ip-network-embeddings.jpg" in article
assert "ip-network-embeddings.jpg" not in feature
assert (root/"portfolio-assets/ip-geolocation-map.jpg").read_bytes() != (root/"portfolio-assets/ip-network-embeddings.jpg").read_bytes()
