# CLI, layout engines, exports, configuration

Contents: [Install](#install) · [Everyday commands](#everyday-commands) · [All flags](#flags) · [d2-config](#d2-config-render-settings-in-the-file) · [Layout engines](#layout-engines) · [Export formats](#export-formats) · [Embedding D2 in other tools](#embedding-d2-in-other-tools) · [Versions](#versions)

## Install

```bash
brew install d2                                       # macOS / Linux Homebrew
curl -fsSL https://d2lang.com/install.sh | sh -s --   # official script (add --dry-run to preview)
curl -fsSL https://d2lang.com/install.sh | sh -s -- --uninstall
```

From source: `go install github.com/d2lang/d2@latest`. Precompiled binaries for every OS: https://github.com/terrastruct/d2/releases (per-OS package-manager instructions: https://github.com/d2lang/d2/blob/master/docs/INSTALL.md). D2 needs no browser and collects no telemetry (it only checks GitHub for new versions occasionally).

Check the version first: behavior differs (see [Versions](#versions)).

## Everyday commands

```bash
d2 in.d2                       # -> in.svg
d2 in.d2 out.png               # format from extension: svg png pdf pptx gif txt
d2 -w in.d2                    # watch + live-reload in browser (PORT/HOST env, --browser 0 for none)
d2 fmt in.d2                   # reformat in place
d2 --check in.d2               # fail if not formatted
d2 validate in.d2              # SYNTAX ONLY; does not catch semantic errors
d2 layout [engine]             # list engines / show an engine's flags
d2 themes                      # list theme ids
d2 play in.d2                  # open in play.d2lang.com
echo 'a -> b' | d2 - out.svg   # stdin
echo 'a -> b' | d2 - -         # stdin to stdout (SVG)
echo 'a -> b' | d2 --stdout-format=png - - > out.png
d2 -l elk -t 4 --pad 40 in.d2 out.svg
```

**Check success with the exit code, never with the existence of the output file**: on errors D2 still writes a partial render so you can keep iterating. **`d2 validate` only parses**; it accepts `a.shape: banana`, `stroke-width: 99`, unsupported layout features, missing imports. Use a full compile (`d2 in.d2 out.svg`) for real validation.

Errors look like `err: failed to compile in.d2: in.d2:3:5: message` (line:column).

## Flags

| flag | env var | meaning |
|---|---|---|
| `-l, --layout` | `D2_LAYOUT` | `dagre` (default), `elk`, `tala` |
| `-t, --theme` | `D2_THEME` | theme id (default 0) |
| `--dark-theme` | `D2_DARK_THEME` | theme used when viewer's OS is dark (default unset = same as light) |
| `-s, --sketch` | `D2_SKETCH` | hand-drawn look |
| `--pad` | `D2_PAD` | pixels around the diagram (default 100) |
| `--center` | `D2_CENTER` | center the SVG in its viewbox |
| `--scale` | | scale output; default fits SVGs to screen, `1` disables fit |
| `-b, --bundle` | `D2_BUNDLE` | bundle assets and layers into the SVG (default true) |
| `--animate-interval` | `D2_ANIMATE_INTERVAL` | ms per board for animated SVG/GIF output of multi-board diagrams |
| `--target` | | board path to render; `''` root only; trailing `*` includes children |
| `--timeout` | `D2_TIMEOUT` | max seconds (default 120): raise it for big diagrams |
| `--salt` | | suffix for element IDs: use when inlining several diagrams in one HTML page |
| `--force-appendix` | `D2_FORCE_APPENDIX` | add tooltip/link appendix to SVG (always present on PNG) |
| `--no-xml-tag` | `D2_NO_XML_TAG` | omit `<?xml?>` so SVG embeds directly in HTML |
| `--omit-version` | `OMIT_VERSION` | drop D2 version from output |
| `--stdout-format` | `D2_STDOUT_FORMAT` | `svg`, `png`, `pdf`, `pptx`, `gif`, `txt`/`ascii` when writing to `-` |
| `--ascii-mode` | `D2_ASCII_MODE` | `extended` (box drawing, default) or `standard` (plain ASCII) |
| `--font-regular/-italic/-bold/-semibold` | `D2_FONT_*` | `.ttf` paths |
| `--font-mono/-mono-italic/-mono-bold/-mono-semibold` | `D2_FONT_MONO*` | `.ttf` paths |
| `--elk-algorithm`, `--elk-*`, `--dagre-nodesep`, `--dagre-edgesep`, `--tala-seeds` | | layout-specific (see `d2 layout <name>`) |
| `-d, --debug` | `DEBUG` | verbose logs |
| `-w, --watch`, `-h/--host`, `-p/--port`, `--browser`, `--img-cache` | | watch mode |

Precedence: **flags and env vars > `vars.d2-config` in the file > defaults**.

## d2-config: render settings in the file

```d2
vars: {
  d2-config: {
    layout-engine: elk
    theme-id: 4
    dark-theme-id: 200     # only if the user wants OS-dark-mode switching
    pad: 40
    center: true
    sketch: false
    theme-overrides: {B1: "#2E7D32"}
    dark-theme-overrides: {B1: "#A5D6A7"}
    data: {
      tala-seeds: [1, 2, 3]
    }
  }
}
a -> b
```

Valid keys: `layout-engine`, `theme-id`, `dark-theme-id`, `theme-overrides`, `dark-theme-overrides`, `pad`, `center`, `sketch`, `data`. Anything else is an error (`"animate-interval" is not a valid config`). `data` is a free-form map for plugins and library consumers; TALA reads `tala-seeds` from it.

Putting settings here makes the `.d2` self-describing, so the same file renders identically in CI, the playground and teammates' machines. Prefer it over remembering flags.

## Layout engines

Check what is installed with `d2 layout`.

| | dagre | elk | tala |
|---|---|---|---|
| default? | yes | | |
| speed | fastest | fast | slower |
| edges | curvy multi-segment | orthogonal, cleanly routed | orthogonal, symmetric |
| containers | works; container-to-descendant edges **error** | best; container-to-container routing native | first-class |
| `width`/`height` on containers | no | yes | yes (may grow to fit) |
| `direction` per container | no, global only | no | **yes** |
| `near: <shape>` and `top`/`left` | no | no | **yes** |
| `sql_table` / `class` row-level edges | no | **yes** | **yes** |
| deterministic | yes | yes | seeded (`tala-seeds`), small edits can reshuffle |
| good for | simple flows, trees, fast iteration | architecture, ERD, nested systems | whiteboard-like software architecture with symmetry |

- ELK algorithms: `--elk-algorithm` = `layered` (default), `force`, `stress`, `mrtree`, `radial` (expects a tree). Tunables: `--elk-nodeNodeBetweenLayers`, `--elk-edgeNodeBetweenLayers`, `--elk-padding`, `--elk-nodeSelfLoop`.
- Dagre tunables: `--dagre-nodesep`, `--dagre-edgesep`.
- TALA is open-source and bundled from v0.9. In older versions it was a paid plugin and `--layout=tala` failed without it.
- ASCII output always uses ELK (or TALA).
- `direction` accepts `up|down|left|right` at the root; fixed per engine as above.

**Rule of thumb**: start with `elk`. Use `dagre` for tiny flowcharts. Try `tala` when the layout looks forced into layers and the diagram is not hierarchical.

## Export formats

| ext | notes |
|---|---|
| `.svg` | default; CSS and fonts embedded; supports links, tooltips, animation; element IDs are base64 classes, with a per-diagram `d2-<hash>` prefix |
| `.png` | built-in renderer in v0.9 (earlier versions needed headless Chromium/Playwright); no interactivity; tooltips/links go in an appendix; up to 32768 px per side |
| `.pdf` | one page per board; links clickable; no animation |
| `.pptx` | one slide per board; opens in PowerPoint and Google Slides |
| `.gif` | animated through boards (`--animate-interval`, default 1000 ms) |
| `.txt` | ASCII art (beta); box-and-arrow diagrams only; many styles ignored; use `--ascii-mode standard` for pure ASCII |

Multi-board diagrams export to directories for SVG/PNG, pages for PDF, slides for PPTX (see `composition.md`).

**Using an SVG on a web page**: inline `<svg>`, `<object>`, `<iframe>` and `<embed>` keep links clickable; `<img>` and CSS backgrounds do not. Embed several diagrams in one HTML page only with distinct `--salt` values.

For quick visual checks while working, render to PNG and open the image.

## Embedding D2 in other tools

- **Markdown renderers**: Goldmark (`FurqanSoftware/goldmark-d2`), MkDocs (`landmaj/mkdocs-d2-plugin`), mdBook (`danieleades/mdbook-d2`), Pandoc filter, Remark, Hexo, Obsidian plugin, Org-mode. Fenced ` ```d2 ` blocks become diagrams.
- **READMEs and wikis**: do not assume ` ```d2 ` blocks render. Commit the rendered `.svg`/`.png`, link it, and keep the `.d2` next to it. A CI step can regenerate: `for f in diagrams/*.d2; do d2 "$f"; done`.
- **Editors**: official VS Code, Vim and Obsidian plugins; community Tree-sitter, Emacs, Zed.
- **JavaScript / browser**: `npm install @d2lang/d2` (D2.js, WebAssembly; `const r = await d2.compile(src); const svg = await d2.render(r.diagram, r.renderOptions)`; imports via an `fs` map of path to content).
- **Go**: the `d2/d2oracle` package creates and edits diagrams programmatically; `d2lib` compiles and renders.
- **Python builder**: `MrBlenny/py-d2`; JS builder: `Kreshnik/d2lang-js`.
- **Playground**: https://play.d2lang.com (shareable links; `sketch=1` URL parameter).

## Versions

Verified against **v0.9.0**. Features by version, so you can reason about older installs:

| version | notable |
|---|---|
| <= 0.6.x | core language: classes, globs, imports, layers/scenarios/steps, sql_table, class, sequence, grid, themes, `d2-config` |
| 0.7.0 | markdown/latex/code as shape labels, `suspend`/`unsuspend`, endpoint glob filters, `&level`, `c4-person`, `d2-legend`, `d2 validate`, connection icons |
| 0.7.1 | ASCII (`.txt`) output, `cross` arrowhead, md/latex/code as edge labels, `border-*` label positions, tooltips with `near` always visible, `--font-mono*` |
| 0.8.2 | GIF with `animate`, reproducible releases, native Go ports of Dagre/ELK/MathJax (faster; layouts shift slightly), `d2ascii` supports tables and classes |
| 0.9.0 | **TALA bundled and open source**, **built-in PNG/GIF/PDF/PPTX renderer (no Chromium)**, much faster rendering, Markdown labels as native SVG |

Because layout engines were swapped in 0.8.x/0.9, regenerate stored SVGs when upgrading; coordinates and edge routes differ.
