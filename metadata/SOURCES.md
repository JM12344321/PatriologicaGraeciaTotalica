# Sources and Provenance

## Policy

Translations are generated from openly reusable Greek, never from a copyrighted modern English translation. Source selection follows the Open Greek Corpus preference order: clean open TEI or manual transcription first, then established Patrologia Graeca OCR, then another usable public-domain edition, with legacy Migne OCR as a fallback.

The full Greek source corpus is not duplicated here. Every translated work has a machine-readable record in `source_manifest.jsonl`, including a stable work identifier, source loci, license, URL, retrieval date, and SHA-256 digest. A status of “complete” means that every passage present in the selected source has been translated; for a fragment collection it does not imply recovery of material absent from that source.

## Open Greek Corpus snapshot

- Repository: [open-greek/open-greek-corpus](https://github.com/open-greek/open-greek-corpus)
- Commit inspected: `39938c0b48caff0856a6ad00991b7f88e2c85445`
- Retrieval date: 2026-09-03
- Aggregate license: CC BY-SA 4.0, with component licenses recorded per work

## Current translated source family

The initial PG 17 batch uses normalized passage files derived from [OpenGreekAndLatin/First1KGreek](https://github.com/OpenGreekAndLatin/First1KGreek). The work registry identifies edition `1st1K-grc1`, provider `first1k`, and license CC BY-SA 4.0. These are clean open editions of the same works represented in PG; this release does not claim exact identity with Migne’s printed wording or invent column alignment.

| Author | Work | PG | CTS identifier | Passages | Corpus tokens |
|---|---|---:|---|---:|---:|
| Origen | Selections on Judges (Fragments from Catenae) | 12 | `tlg2042.tlg055` | 7 | 265 |
| Origen | Fragments from the Commentary on Ezekiel | 13 | `tlg2042.tlg061` | 4 | 328 |
| Origen | Notes on Genesis | 17 | `tlg2042.tlg066` | 7 | 635 |
| Origen | Notes on Exodus | 17 | `tlg2042.tlg067` | 4 | 246 |
| Origen | Notes on Joshua (Fragments from Catenae) | 17 | `tlg2042.tlg071` | 4 | 171 |
| Origen | Notes on Judges | 17 | `tlg2042.tlg072` | 2 | 136 |
| Origen | Notes on Leviticus (Fragments from Catenae) | 17 | `tlg2042.tlg068` | 8 | 475 |
| Origen | Notes on Numbers | 17 | `tlg2042.tlg069` | 8 | 209 |

Required attribution is preserved to OpenGreekAndLatin/First1KGreek and the Open Greek Corpus aggregation/normalization work under CC BY-SA 4.0.
