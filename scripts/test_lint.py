"""Synthetic parser and tracked-source enumeration contracts only."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("syntax_lint", Path(__file__).with_name("lint.py"))
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)


class SyntaxLintContracts(unittest.TestCase):
    def test_python_and_json_accept_valid_reject_invalid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for suffix, valid, invalid in [(".py", "value = 1\n", "value =\n"),
                                           (".json", '{"value":1}', '{"value":NaN}')]:
                path = root / ("fixture" + suffix)
                path.write_text(valid)
                self.assertTrue(LINT.check_syntax(path, "unused"))
                path.write_text(invalid)
                self.assertFalse(LINT.check_syntax(path, "unused"))

    def test_node_parser_does_not_execute_source(self):
        node = shutil.which("node")
        self.assertIsNotNone(node)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.mjs"
            path.write_text("throw new Error('must never execute');\n")
            self.assertTrue(LINT.check_syntax(path, node))
            path.write_text("export const = ;\n")
            self.assertFalse(LINT.check_syntax(path, node))

    def test_untracked_files_are_excluded_and_symlinks_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            tracked = root / "tracked.py"
            tracked.write_text("value = 1\n")
            (root / "untracked.py").write_text("invalid =\n")
            subprocess.run(["git", "-C", str(root), "add", "tracked.py"], check=True)
            self.assertEqual([tracked], LINT.tracked_paths(root))
            tracked.unlink()
            tracked.symlink_to(root / "untracked.py")
            with self.assertRaises(ValueError):
                LINT.tracked_paths(root)


if __name__ == "__main__":
    unittest.main()
