# skills
Personal [Claude Code](https://claude.com/claude-code) agent skills.

| skill | what |
|---|---|
| `typst` | write, debug, compile and package [Typst](https://typst.app) documents (verified against Typst 0.15.1) |
| `d2` | write, style and render [D2](https://d2lang.com) diagrams |

## Install
```
npx skills add AnisAbdellatif/skills --skill typst -g -y
npx skills add AnisAbdellatif/skills --skill d2 -g -y
```
Or symlink: `ln -s "$PWD/skills/typst" ~/.claude/skills/typst`.

Binaries needed to compile/render: `brew install typst d2`.

`tools/` holds maintainer scripts (not part of the skills).
