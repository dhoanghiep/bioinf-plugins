---
name: igv-report
description: Build, inspect or edit a self-contained IGV.js genome-browser report (an igv-reports HTML page with an inlined region table and one session per locus). Use when asked to make or change an IGV view, a locus or region browser, a read-coverage panel, a splice-junction panel, or a transcript-structure comparison, or when working with a file that looks like igv-reports output. Covers the create_report build, the track-config JSON that the defaults get wrong, a decode/patch script for editing a report without regenerating it, and the standing long-read isoform-comparison track recipe.
---

# Self-contained IGV reports

An [`igv-reports`](https://github.com/igvteam/igv-reports) page is **one HTML file** with
a region table on top, an igv.js browser below, and one gzipped+base64 igv.js session per
table row inlined in a `const sessionDictionary = {...}` literal. Everything the view
needs, reference sequence included, is baked in as `data:` URLs. The only network fetch
at view time is `igv.min.js` from jsDelivr.

That self-containment is the whole value: the file can be emailed, committed, served from
anything, or embedded in an iframe, and it still works. **Protect it.** If a build emits a
sidecar data directory next to the HTML, the report is not self-contained and will break
wherever it gets moved.

## Inspect before you change

Never edit a report blind. `scripts/inspect_report.py`, bundled with this skill,
decodes the sessions:

```bash
python3 scripts/inspect_report.py REPORT.html
```

The script path is relative to this skill's own directory. If the relative path does not
resolve, run it by absolute path, i.e.
`/absolute/path/to/igv-report/skills/igv-report/scripts/inspect_report.py`.

The script is stdlib-only, any Python 3 will run it. Use whichever interpreter the
project mandates: some setups pin a specific conda env rather than bare `python3`.

It prints the region table and the full track config per session, with long `data:` URLs
elided. Use it to see what a report actually carries, and to check that a new report
matches an existing one.

## Edit without regenerating

The source data for these reports (BAMs, GTFs, genome FASTA) usually lives on a cluster,
not on this machine, so a full rebuild is often not available. For a small change (drop a
track, retitle, reorder or drop loci, change a display mode or threshold) round-trip the
sessions instead:

```bash
PY=python3                           # or the interpreter this project mandates
S=scripts/inspect_report.py          # relative to this skill's directory

$PY $S REPORT.html --sessions-out /tmp/sess     # one session_<id>.json per table row
# edit the JSON files
$PY $S REPORT.html --patch /tmp/sess --out NEW.html
```

The round-trip is lossless: bytes outside `sessionDictionary` are untouched, and
re-encoding unmodified sessions reproduces them exactly. `--patch` needs one file per
session and will refuse a partial directory rather than silently drop a locus. Note that
dropping a *locus* also means editing the `tableJson` literal by hand, the script only
rewrites sessions.

## Building a new report

```bash
pip install igv-reports          # provides create_report

create_report regions.bed \
  --fasta <genome.fa> \
  --tracks <track files...> \
  --track-config tracks.json \
  --info-columns name \
  --title "<short title>" \
  --output igv_<slug>.html
```

- `regions.bed` drives the table, one row per locus: `chrom start end name`. **Row order
  is presentation order**, the first row loads on open and arrow keys step down the table.
- **Always pass `--track-config`.** The defaults get display modes and the
  splice-junction thresholds wrong for this kind of comparison. See
  `reference/track-recipe.md`.
- Name the output for what it shows, not for the run that made it.

## Gotchas

- **Arrow keys are claimed.** Every report binds `ArrowLeft`/`ArrowRight` to step through
  its region table. If the report is embedded in a page that also uses arrow keys, focus
  decides which one responds. Worth warning anyone presenting a multi-locus report.
- **The table is labelled "Variants"** by igv-reports whatever the rows actually are:
  genes, splice forms, loci. Cosmetic, usually leave it.
- Reports set `showChromosomeWidget: false` and `search: false` because each session
  carries reference sequence for its own locus only. Re-enabling either looks broken.
- The igv.js version is pinned in the generated HTML (`igv@3.5.2` in the reports built so
  far). Keep a set of related reports on one version so they behave identically.
- Expect 100KB to 300KB per report with inlined coverage. That is normal, not a bug to
  optimise. A BAM alignment track instead of a bedgraph would blow that up by orders of
  magnitude, so treat adding one as a real decision.

## Embedding a report in a slide deck

A report is self-contained, so a slide deck or web page can embed it in an iframe
directly. Where reports live, how they are referenced and how a slide is verified are
deck conventions, not report ones: check for a project-level skill covering that (in the
`isoform_compare` deck it is `igv-slide-report`) and follow it for placement, captions
and verification. This skill covers only the report itself.
