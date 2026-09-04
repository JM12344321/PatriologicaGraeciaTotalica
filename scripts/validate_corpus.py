#!/usr/bin/env python3
"""Deterministic structural checks for the translation corpus.

MIT License. This deliberately checks only facts a script can establish; it is
not a substitute for comparing the English with the Greek.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODES = ("Word for Word", "Thought for Thought")
LOCUS_RE = re.compile(r"<!--\s*source-locus:\s*([^\s]+)\s*-->")
GREEK_RE = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]")
WORD_RE = re.compile(r"\b[^\W\d_]+(?:[\u2019'][^\W\d_]+)?\b", re.UNICODE)
CHATTER = (
    "as an ai language model",
    "here is the translation",
    "i cannot translate",
    "certainly!",
    "translation requested:",
)


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: invalid JSON: {exc}") from exc
    return rows


def translation_files(mode: str) -> list[Path]:
    return sorted(
        path
        for path in (ROOT / mode).glob("PG [0-9][0-9][0-9]/*.md")
        if path.name != "_INDEX.md"
    )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        sources = load_jsonl(ROOT / "metadata" / "source_manifest.jsonl")
        statuses = load_jsonl(ROOT / "metadata" / "translation_status.jsonl")
        load_jsonl(ROOT / "metadata" / "work_manifest.jsonl")
        load_jsonl(ROOT / "metadata" / "qa_flags.jsonl")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    ids = [row.get("work_id") for row in sources]
    duplicates = [key for key, count in Counter(ids).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate source work IDs: {duplicates}")

    files_by_mode = {mode: translation_files(mode) for mode in MODES}
    relative_sets = {
        mode: {path.relative_to(ROOT / mode) for path in paths}
        for mode, paths in files_by_mode.items()
    }
    if relative_sets[MODES[0]] != relative_sets[MODES[1]]:
        only_wfw = sorted(relative_sets[MODES[0]] - relative_sets[MODES[1]])
        only_tft = sorted(relative_sets[MODES[1]] - relative_sets[MODES[0]])
        errors.append(f"translation trees differ; only WFW={only_wfw}, only TFT={only_tft}")

    texts: dict[Path, str] = {}
    for mode, paths in files_by_mode.items():
        for path in paths:
            try:
                text = path.read_text(encoding="utf-8", errors="strict")
            except UnicodeError as exc:
                errors.append(f"{path}: invalid UTF-8: {exc}")
                continue
            texts[path] = text
            lower = text.lower()
            if not text.startswith("# "):
                errors.append(f"{path}: missing H1 title")
            if "**Status:** Complete" not in text:
                errors.append(f"{path}: not explicitly marked Complete")
            if "AI-assisted first-pass translation" not in text:
                errors.append(f"{path}: missing public first-pass disclosure")
            if "TODO" in text or "TBD" in text:
                errors.append(f"{path}: contains TODO/TBD")
            for phrase in CHATTER:
                if phrase in lower:
                    errors.append(f"{path}: contains model chatter {phrase!r}")
            letters = [ch for ch in text if ch.isalpha()]
            greek_ratio = (sum(bool(GREEK_RE.match(ch)) for ch in letters) / len(letters)) if letters else 0
            if greek_ratio > 0.08:
                warnings.append(f"{path}: Greek-letter ratio {greek_ratio:.1%} may indicate untranslated text")

    status_by_id = {row.get("work_id"): row for row in statuses}
    for source in sources:
        work_id = source["work_id"]
        cts_id = source["cts_id"]
        expected_loci = source["source_loci"]
        if source.get("segment_count") != len(expected_loci):
            errors.append(f"{work_id}: segment_count disagrees with source_loci")
        status = status_by_id.get(work_id)
        if not status or status.get("status") != "complete":
            errors.append(f"{work_id}: source manifest lacks complete translation status")

        found: dict[str, Path] = {}
        for mode in MODES:
            matches = [path for path in files_by_mode[mode] if cts_id in texts.get(path, "")]
            if len(matches) != 1:
                errors.append(f"{work_id}: expected one {mode} file containing {cts_id}, found {len(matches)}")
                continue
            path = matches[0]
            found[mode] = path
            actual_loci = LOCUS_RE.findall(texts[path])
            if Counter(actual_loci) != Counter(expected_loci):
                errors.append(
                    f"{path}: source loci differ; expected={expected_loci}, actual={actual_loci}"
                )
            if len(actual_loci) != len(set(actual_loci)):
                errors.append(f"{path}: duplicate source-locus marker")

            body = re.sub(r"<!--.*?-->", " ", texts[path], flags=re.DOTALL)
            word_count = len(WORD_RE.findall(body))
            source_tokens = int(source.get("corpus_tokens", 0))
            if source_tokens and word_count < source_tokens * 0.55:
                warnings.append(
                    f"{path}: only {word_count} English words for {source_tokens} source tokens"
                )
            if source_tokens and word_count > source_tokens * 5:
                warnings.append(
                    f"{path}: {word_count} English words for {source_tokens} source tokens"
                )

        if len(found) == 2:
            left = LOCUS_RE.findall(texts[found[MODES[0]]])
            right = LOCUS_RE.findall(texts[found[MODES[1]]])
            if left != right:
                errors.append(f"{work_id}: WFW and TFT locus order differs")

    manifest_ids = set(ids)
    extra_statuses = sorted(set(status_by_id) - manifest_ids)
    if extra_statuses:
        warnings.append(f"translation statuses without source records: {extra_statuses}")

    print(
        f"Validated {len(sources)} works, "
        f"{len(files_by_mode[MODES[0]])} mirrored translation pairs, "
        f"and {sum(len(row['source_loci']) for row in sources)} source loci."
    )
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED with {len(errors)} error(s) and {len(warnings)} warning(s).")
        return 1
    print(f"PASS with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
