# bioinf-plugins

A Claude Code plugin marketplace for bioinformatics workflow tooling.

## Plugins

| Plugin | What it does |
|---|---|
| [`igv-report`](plugins/igv-report) | Build, inspect and edit self-contained IGV.js genome-browser reports (`igv-reports` HTML). |

## Install

```bash
claude plugin marketplace add /path/to/bioinf-plugins     # or the git URL once pushed
claude plugin install igv-report@bioinf-plugins
```

Then start a new Claude Code session; the plugin's skills are picked up automatically.

## Layout

```
.claude-plugin/marketplace.json     # marketplace manifest, one entry per plugin
plugins/<plugin>/
├── .claude-plugin/plugin.json      # plugin manifest
└── skills/<skill>/SKILL.md         # the skill, plus any reference/ and scripts/
```
