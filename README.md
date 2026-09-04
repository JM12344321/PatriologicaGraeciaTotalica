# Patrologia Graecia Totalica

*Patrologia Graecia Totalica* is an open corpus of English translations made directly from Greek works represented in Migne’s *Patrologia Graeca*.

These are **AI-assisted first-pass translations for orientation and study**. They are not critical editions, do not claim scholarly authority, and are not substitutes for checking the Greek text and specialist scholarship.

Every completed work is published in two forms:

- [`Word for Word/`](Word%20for%20Word/) gives grammatical English that stays conspicuously close to the Greek argument, repetitions, connective logic, and technical vocabulary.
- [`Thought for Thought/`](Thought%20for%20Thought/) gives more natural modern English without summarizing or omitting what the Greek asserts.

## Sources and licensing

The campaign begins with the [Open Greek Corpus](https://github.com/open-greek/open-greek-corpus) source registry and prefers clean, openly licensed editions over OCR. Each work records its exact source, identifier, license, relationship to PG, completeness, and source hash in [`metadata/source_manifest.jsonl`](metadata/source_manifest.jsonl) and in its reader-facing header. See [`metadata/SOURCES.md`](metadata/SOURCES.md) for the policy and current attributions.

Translations and project-authored metadata are released under [CC BY-SA 4.0](LICENSE.md). Upstream Greek sources retain their own recorded licenses.

## Status and uncertainty

Current coverage is summarized in [`PROGRESS.md`](PROGRESS.md). Compact translation notes mark genuinely uncertain readings; machine-readable review items are stored in [`metadata/qa_flags.jsonl`](metadata/qa_flags.jsonl). Exact PG column markers are included only when the selected source supplies reliable alignment.

The Greek campaign does not translate Latin-only material. Anything encountered is logged in [`metadata/latin_only.csv`](metadata/latin_only.csv) for the future Latin project rather than silently omitted.

Corrections, textual observations, and scholarly review are welcome. Please identify the work and source locus and explain the proposed change against the Greek.
