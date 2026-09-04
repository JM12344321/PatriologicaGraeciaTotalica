# Next Run Handoff

Continue the Patrologia Graeca translation campaign from this repository.

1. Read `README.md`, `metadata/SOURCES.md`, and `metadata/progress.json`.
2. Inspect `metadata/work_manifest.jsonl` and continue a `ready` high-priority work; do not retranslate a work already marked `complete`.
3. Acquire Greek through the Open Greek Corpus registry and its recorded open sources. Do not use copyrighted modern English translations or proprietary TLG text.
4. Translate each complete source work into both `Word for Word/PG NNN/` and `Thought for Thought/PG NNN/`, directly from the Greek. Preserve every source locus and record sparse uncertainty notes.
5. Add provenance and hashes to the manifests, update both volume indexes and progress counts, run `python scripts/validate_corpus.py`, and review any flagged passage against the Greek.
6. Commit and push each completed work or small bundle before starting another large item.

Prioritize useful complete short works over large unfinished fragments, and preserve the distinction between source-complete fragment collections and fully preserved ancient works.
