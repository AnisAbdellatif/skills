#!/usr/bin/env python3
"""Search the Typst Universe `@preview` package index.

  search-packages.py "chart plot"            keyword search (all words must match name/description/keywords/categories)
  search-packages.py --category cv --top 10  filter by category
  search-packages.py --name cetz --versions  show one package, including all versions
  search-packages.py --list-categories
  search-packages.py --refresh ...           re-download the index (cached for 24h in the temp dir)

Output: name  latest-version  [categories]  description   — import as  #import "@preview/name:version"
"""
import json, os, sys, tempfile, time, urllib.request

URL = "https://packages.typst.org/preview/index.json"
CACHE = os.path.join(tempfile.gettempdir(), "typst-universe-index.json")


def load(refresh=False):
    if refresh or not os.path.exists(CACHE) or time.time() - os.path.getmtime(CACHE) > 86400:
        with urllib.request.urlopen(URL, timeout=60) as r:
            data = r.read()
        with open(CACHE, "wb") as f:
            f.write(data)
    with open(CACHE) as f:
        return json.load(f)


def vkey(v):
    return tuple(int(x) for x in v.split(".") if x.isdigit())


def main(argv):
    refresh = "--refresh" in argv
    argv = [a for a in argv if a != "--refresh"]
    versions = "--versions" in argv
    argv = [a for a in argv if a != "--versions"]
    top, category, name, words = 15, None, None, []
    it = iter(argv)
    for a in it:
        if a == "--top":
            top = int(next(it))
        elif a == "--category":
            category = next(it)
        elif a == "--name":
            name = next(it)
        elif a == "--list-categories":
            cats = {}
            latest = latest_by_name(load(refresh))
            for p in latest.values():
                for c in p.get("categories", []):
                    cats[c] = cats.get(c, 0) + 1
            for c, n in sorted(cats.items(), key=lambda kv: -kv[1]):
                print(f"{n:5d}  {c}")
            return
        elif a in ("-h", "--help"):
            print(__doc__)
            return
        else:
            words.extend(a.lower().split())
    data = load(refresh)
    latest = latest_by_name(data)
    if name:
        p = latest.get(name)
        if not p:
            sys.exit(f"no package named {name!r}")
        show(p)
        if versions:
            vs = sorted((x["version"] for x in data if x["name"] == name), key=vkey, reverse=True)
            print("versions:", ", ".join(vs))
        print(f"repository: {p.get('repository', '-')}  license: {p.get('license', '-')}  compiler>={p.get('compiler', '?')}")
        return
    hits = []
    for p in latest.values():
        hay = " ".join([p["name"], p.get("description", ""), " ".join(p.get("keywords", [])), " ".join(p.get("categories", [])), " ".join(p.get("disciplines", []))]).lower()
        if category and category not in p.get("categories", []):
            continue
        if all(w in hay for w in words):
            score = sum(3 for w in words if w in p["name"].lower()) + sum(1 for w in words if w in p.get("description", "").lower())
            hits.append((score, p.get("updatedAt", 0), p))
    hits.sort(key=lambda t: (-t[0], -t[1]))
    for _, _, p in hits[:top]:
        show(p)
    print(f"-- {len(hits)} match(es), showing {min(top, len(hits))}")


def latest_by_name(data):
    best = {}
    for p in data:
        n = p["name"]
        if n not in best or vkey(p["version"]) > vkey(best[n]["version"]):
            best[n] = p
    return best


def show(p):
    cats = ",".join(p.get("categories", []))
    tpl = " [template]" if p.get("template") else ""
    print(f'{p["name"]:28s} {p["version"]:8s} [{cats}]{tpl}  {p.get("description", "")[:100]}')


if __name__ == "__main__":
    main(sys.argv[1:])
