#!/usr/bin/env python3
"""Compile every ```d2 fenced block in the skill's markdown files and every
assets/templates/*.d2 file with the real d2 binary. ```d2-fragment blocks are skipped.

Usage: python3 -I tools/check_examples.py [skill_dir]
"""
import re, subprocess, sys, tempfile, pathlib, os

skill = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "d2").resolve()
fence = re.compile(r"^```d2[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)
jobs = []
for md in sorted(skill.rglob("*.md")):
    text = md.read_text()
    for m in fence.finditer(text):
        line = text[: m.start()].count("\n") + 2
        jobs.append((f"{md.relative_to(skill)}:{line}", m.group(1)))
for f in sorted((skill / "assets").rglob("*.d2")):
    jobs.append((str(f.relative_to(skill)), f.read_text()))

bad = 0
with tempfile.TemporaryDirectory() as td:
    for i, (name, src) in enumerate(jobs):
        p = pathlib.Path(td) / f"b{i}.d2"
        p.write_text(src)
        r = subprocess.run(["d2", str(p), str(p.with_suffix(".svg"))], capture_output=True, text=True, timeout=180)
        if r.returncode:
            bad += 1
            err = [l for l in r.stderr.splitlines() if "err" in l]
            print(f"FAIL {name}: {(err[0] if err else r.stderr.strip())[-230:]}")
print(f"{len(jobs) - bad}/{len(jobs)} blocks compiled")
sys.exit(1 if bad else 0)
