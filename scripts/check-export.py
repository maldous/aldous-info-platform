"""Check runtime completeness, source parity, and local module/asset references."""
from pathlib import Path
import hashlib
import json
import re
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

root = Path(__file__).resolve().parent.parent
dist = root / "dist"
expected = json.loads((root / "docs/published-assets.sha256.json").read_text())
actual = {str(p.relative_to(dist)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(dist.rglob("*")) if p.is_file()}
assert actual == expected, "Runtime bytes differ from the published snapshot; review and update provenance for intentional edits"

def check_reference(base, value):
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("data:"):
        return
    local = (dist if parsed.path.startswith("/") else base) / unquote(parsed.path.lstrip("/"))
    assert local.resolve().is_relative_to(dist.resolve()), value
    assert local.exists(), str(local.relative_to(dist))

class Assets(HTMLParser):
    def __init__(self, base):
        super().__init__(); self.base = base
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("src", "href") and value:
                check_reference(self.base, value)

for path in dist.rglob("*.html"):
    Assets(path.parent).feed(path.read_text())
for path in list(dist.rglob("*.js")) + list(dist.rglob("*.mjs")):
    for value in re.findall(r"(?:from\s*|import\s*)['\"]([^'\"]+)['\"]", path.read_text()):
        check_reference(path.parent, value)
for path in dist.rglob("*.css"):
    for value in re.findall(r"url\(['\"]?([^)'\"]+)", path.read_text()):
        check_reference(path.parent, value)
print(f"PASS: {len(actual)} published runtime files byte-identical; local asset/module references resolve")
