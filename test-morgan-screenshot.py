from pathlib import Path
import hashlib,json,re
from datetime import datetime
from PIL import Image
root=Path('dist');html=(root/'index.html').read_text()
card=re.search(r'<article class="feature" id="morgan-project".*?</article>',html,re.S).group()
record=json.loads(Path('morgan-screenshot-provenance.json').read_text())
assert record['source_url']=='https://morgan.aldous.info/?mode=compact&theme=dark'
assert record['placements']==['Morgan project card']
assert record['kind']=='public compact native-workstream screenshot'
assert 0 <= (datetime.fromisoformat(record['captured_at'].replace('Z','+00:00'))-datetime.fromisoformat(record['observed_at'].replace('Z','+00:00'))).total_seconds() < 120
for part in [card]:
 assert 'src="portfolio-assets/morgan-current.jpg"' in part
 assert 'Captured image, not live status.' in part
 assert record['captured_at'] in part and record['observed_at'] in part
 assert f'width="{record["width"]}" height="{record["height"]}"' in part
 assert 'morgan-compact.png' not in part and 'morgan-signals' not in part
image=Image.open(root/'portfolio-assets/morgan-current.jpg')
assert image.size==(record['width'],record['height'])==(850,745) and image.format=='JPEG'
assert hashlib.sha256((root/'portfolio-assets/morgan-current.jpg').read_bytes()).hexdigest()==record['sha256']=='3c4bc0bc4e47131bb840616444aa127f7e0886fd25afa305699309682da3387a'
css=(root/'portfolio.css').read_text()
assert '#morgan-project .feature-image img{object-fit:contain;object-position:center}' in css
assert 'morgan-signals' not in css
print('PASS current unmodified compact public capture, measured freshness, exact provenance, and contain framing.')
