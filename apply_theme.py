#!/usr/bin/env python3
"""Copy a CSS file into notebooks' RISE overlay metadata.

usage: python apply_theme.py theme.css wk2/MY470_wk2_lecture.ipynb [more.ipynb ...]
"""
import json
import sys
from pathlib import Path


def apply(css: str, nb_path: Path) -> None:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    nb["metadata"].setdefault("rise", {})["overlay"] = f"<style>\n{css}</style>"
    nb_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"styled {nb_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    css = Path(sys.argv[1]).read_text(encoding="utf-8")
    for arg in sys.argv[2:]:
        apply(css, Path(arg))
