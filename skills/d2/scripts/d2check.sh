#!/usr/bin/env bash
# Format, compile and render a D2 file; print errors with line numbers.
# Usage: d2check.sh <file.d2> [outdir] [extra formats...]
#   renders <outdir>/<name>.svg and a PNG preview in <outdir>/preview/ (look at the PNG).
#   extra formats: pdf pptx gif txt, e.g.  d2check.sh a.d2 out pdf
#   d2check.sh --version
# Multi-board files (layers/scenarios/steps) make SVG and PNG outputs DIRECTORIES (<name>/index.svg,
# <name>/layers/x.svg ...), which is why PNG previews live in their own preview/ folder: rendering
# both formats to the same name would overwrite one with the other.
# Exit code is d2's: 0 only if the diagram fully compiled (a partial render may still be written on error).
set -u
if ! command -v d2 >/dev/null 2>&1; then
  echo "d2 is not installed. Ask the user, then: brew install d2   (or: curl -fsSL https://d2lang.com/install.sh | sh -s --)" >&2
  exit 127
fi
if [ "${1:-}" = "--version" ]; then d2 --version; exit 0; fi
[ $# -ge 1 ] || { echo "usage: $0 <file.d2> [outdir] [pdf|pptx|gif|txt ...]" >&2; exit 2; }
src=$1
out=${2:-$(dirname "$src")}
shift; [ $# -ge 1 ] && shift
base=$(basename "${src%.d2}")
[ -f "$src" ] || { echo "no such file: $src" >&2; exit 2; }
mkdir -p "$out/preview"

d2 fmt "$src" >/dev/null 2>&1 || echo "note: d2 fmt could not format $src (syntax error?); continuing to compile for the real error"

status=0
render() {  # render <target>
  d2 "$src" "$1" 2>&1 | grep -v '^success:'
  local rc=${PIPESTATUS[0]}
  [ "$rc" -ne 0 ] && status=$rc
  return $rc
}
# PNG is only a preview; skipped if the SVG compile already failed (it would repeat the same error)
render "$out/$base.svg" && render "$out/preview/$base.png"
for ext in "$@"; do [ $status -eq 0 ] && render "$out/$base.$ext"; done

if [ $status -eq 0 ]; then
  echo "OK: $out/$base.svg  preview: $out/preview/$base.png${*:+  extra: $*}"
  [ -d "$out/$base" ] && echo "multi-board: boards written under $out/$base/ (svg) and $out/preview/$base/ (png); PDF/PPTX keep one page/slide per board"
else
  echo "FAILED (exit $status). Fix the first error above, then re-run." >&2
fi
exit $status
