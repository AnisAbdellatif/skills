#!/usr/bin/env python3
"""Compile every ```typ fenced block in the given Markdown files with the local typst CLI.

Fence tags:
  ```typ     self-contained snippet, must compile without errors  (checked)
  ```typ-x   illustrative / intentionally failing / needs context  (skipped)
Blocks importing @preview packages are skipped unless --packages is given.

Usage: check-snippets.py [--packages] [--keep] FILE.md [FILE.md ...]
"""
import re, subprocess, sys, tempfile, pathlib
from concurrent.futures import ThreadPoolExecutor

args = [a for a in sys.argv[1:] if not a.startswith("--")]
packages = "--packages" in sys.argv
keep = "--keep" in sys.argv
if not args:
    sys.exit(__doc__)

FENCE = re.compile(r"^```typ\n(.*?)^```", re.S | re.M)
jobs = []
for f in args:
    text = pathlib.Path(f).read_text()
    for m in FENCE.finditer(text):
        line = text[: m.start()].count("\n") + 2
        src = m.group(1)
        if "@preview" in src and not packages:
            continue
        jobs.append((f, line, src))

tmp = pathlib.Path(tempfile.mkdtemp(prefix="typst-snippets-"))
(tmp / "data.csv").write_text("name,score\nAnn,3\nBo,5\n")
(tmp / "data.json").write_text('{"title": "T", "items": [1, 2, 3]}')
(tmp / "refs.bib").write_text("@book{knuth, author={Donald Knuth}, title={TAOCP}, year={1968}, publisher={AW}}\n")
(tmp / "refs.yml").write_text("knuth:\n  type: book\n  title: TAOCP\n  author: Knuth, Donald\n  date: 1968\n")
(tmp / "chapter.typ").write_text("= Chapter\nHello.\n#let secret = 42\n")
(tmp / "a.png").write_bytes(subprocess.run(["typst", "compile", "-", "-", "-f", "png"], input=b"#set page(width: 40pt, height: 40pt, margin: 0pt)\n#rect(width: 100%, height: 100%, fill: red)", capture_output=True).stdout)

def run(job):
    i, (f, line, src) = job
    p = tmp / f"s{i}.typ"
    p.write_text(src)
    r = subprocess.run(["typst", "compile", "--root", str(tmp), str(p), str(tmp / f"s{i}.pdf")], capture_output=True, text=True)
    return f, line, r.returncode, r.stderr

bad = 0
with ThreadPoolExecutor(4) as ex:
    for f, line, rc, err in ex.map(run, list(enumerate(jobs))):
        if rc != 0:
            bad += 1
            print(f"FAIL {f}:{line}\n{err.strip()[:600]}\n")
print(f"{len(jobs) - bad}/{len(jobs)} snippets compiled")
if not keep:
    import shutil; shutil.rmtree(tmp, ignore_errors=True)
sys.exit(1 if bad else 0)
