# bioinf-plugins

A Claude Code plugin marketplace for bioinformatics workflow tooling.

## Plugins

| Plugin | What it does |
|---|---|
| [`igv-report`](plugins/igv-report) | Build, inspect and edit self-contained IGV.js genome-browser reports (`igv-reports` HTML). |

## Install

```bash
claude plugin marketplace add https://github.com/dhoanghiep/bioinf-plugins.git
claude plugin install igv-report@bioinf-plugins
```

To develop against a local checkout instead, point the marketplace at the directory:

```bash
claude plugin marketplace add /path/to/bioinf-plugins
```

An install is pinned to a commit, so after editing the source run
`claude plugin update igv-report@bioinf-plugins` to pick the change up.

Then start a new Claude Code session; the plugin's skills are picked up automatically.

## Layout

```
.claude-plugin/marketplace.json     # marketplace manifest, one entry per plugin
plugins/<plugin>/
├── .claude-plugin/plugin.json      # plugin manifest
└── skills/<skill>/SKILL.md         # the skill, plus any reference/ and scripts/
```
