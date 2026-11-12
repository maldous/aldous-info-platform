"""Regenerate current recruiter and architecture outputs from retained inputs."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
(root / "review" / "graphical").mkdir(parents=True, exist_ok=True)
for script in ("build-recruiters.py", "generate-graphs.py", "generate-current-architecture.py"):
    subprocess.run([sys.executable, str(root / script)], cwd=root, check=True)
