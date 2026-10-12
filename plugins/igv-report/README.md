# igv-report

Build, inspect and edit self-contained IGV.js genome-browser reports.

An [`igv-reports`](https://github.com/igvteam/igv-reports) page is a single HTML file: a
region table on top, an igv.js browser below, and one gzipped+base64 igv.js session per
table row inlined as `data:` URLs. Nothing is fetched at view time except `igv.min.js`,
so the file can be committed, emailed, served from anything, or embedded in an iframe.

This plugin provides one skill, `igv-report`, covering:

- **Building** a report with `create_report`, including the `--track-config` JSON that
  the defaults get wrong (display modes, splice-junction thresholds).
- **Inspecting** one: `scripts/inspect_report.py` decodes `sessionDictionary` and prints
  the region table plus the full track config per locus.
- **Editing** one without a rebuild: the same script dumps sessions to JSON and
  re-encodes them losslessly, which is what you want when the source BAMs, GTFs and
  genome FASTA live on a cluster rather than the machine you are working on.
- **The standing long-read isoform-comparison track recipe** (bambu discovery, oarfish
  quantification, 10x reference, splice junctions) in
  `skills/igv-report/reference/track-recipe.md`.

The script is stdlib-only Python 3 and does not require `igv-reports` to be installed;
only building a new report does.
