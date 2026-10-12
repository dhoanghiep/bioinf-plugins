# Long-read isoform-comparison track recipe

The standing track stacks for comparing isoform calls (bambu discovery, oarfish
quantification, 10x reference) against read evidence. Decoded with
`scripts/inspect_report.py` from the reports built for the `isoform_compare` talk, so
these are configs that shipped, not defaults. Pass them via `create_report
--track-config`; the defaults differ on display mode and on every splice-junction option.

## Full stack (6 tracks)

For "which call is right here" slides: the stack walks from evidence, to reference, to
each way of calling, to the junction evidence that arbitrates.

```json
[
  {"name": "coverage",
   "type": "wig", "format": "bedgraph", "order": 1},

  {"name": "10x reference genes",
   "type": "annotation", "format": "gtf", "displayMode": "EXPANDED", "order": 2},

  {"name": "unfiltered (oarfish UMI)",
   "type": "annotation", "format": "gtf", "displayMode": "EXPANDED", "order": 3},

  {"name": "filtered (oarfish UMI)",
   "type": "annotation", "format": "gtf", "displayMode": "EXPANDED", "order": 4},

  {"name": "per-sample (donor) unfiltered",
   "type": "annotation", "format": "gtf", "displayMode": "EXPANDED", "order": 5},

  {"name": "splice junctions",
   "type": "spliceJunctions", "format": "bed",
   "colorBy": "strand",
   "thicknessBasedOn": "numUniqueReads",
   "bounceHeightBasedOn": "distance",
   "labelUniqueReadCount": true,
   "minUniquelyMappedReads": 2,
   "order": 6}
]
```

Details that are easy to lose:

- **`minUniquelyMappedReads: 2`** is the point of the junction track here. It hides
  single-read junctions so only junctions worth arbitrating on are drawn. Do not drop it.
- Coverage is a **bedgraph wig track, not a BAM**. These reports carry no alignment track
  at all, which is what keeps them embeddable. Needing individual reads is a new
  decision, not a tweak.
- Every annotation track is `EXPANDED`. `COLLAPSED` stacks overlapping isoforms onto one
  row and destroys the comparison the slide exists to make.
- No explicit `color` on this stack: igv.js assigns per track and the names carry the
  meaning.

## Structures-only stack (2 tracks)

For "do these structures agree" slides. Drop coverage and junctions entirely.

```json
[
  {"name": "merged splice forms (batch1,batch2,paper1,paper2)",
   "type": "annotation", "format": "gtf", "displayMode": "EXPANDED",
   "color": "#2c3e50", "order": 1},

  {"name": "10x reference genes",
   "type": "annotation", "format": "gtf", "displayMode": "EXPANDED", "order": 2}
]
```

`#2c3e50` is the only explicit color in any of these reports: a muted dark slate for the
track under discussion, with the reference left in its default below it. Reuse it for a
"this is the call being argued about" track rather than picking a new accent.

## Region table

Table columns in every report so far: `unique_id, chrom, start, end, name`, i.e. a
4-column BED plus the row id igv-reports adds. Build `regions.bed` as

```
chr6	63572172	63583887	ENSG00000285976
chr9	128720570	128724427	ENSG00000160446
```

and pass `--info-columns name`. Keep `name` a gene ID or symbol: it is the only info
column the reports display, so it is the only label a viewer gets for the row.

## Page-level session options

igv-reports sets these, and they are right for every report of this shape:

```json
{"showChromosomeWidget": false, "showCenterGuide": true, "search": false}
```
