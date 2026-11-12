"""Stage the buildless, editable published application without changing its bytes."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
source = root / "dist"
target = root / "build"
if target.is_symlink():
    raise SystemExit("Refusing a symlinked build directory")
if target.exists():
    shutil.rmtree(target)
shutil.copytree(source, target)
print(f"Built {sum(p.is_file() for p in target.rglob('*'))} static files into build/")
