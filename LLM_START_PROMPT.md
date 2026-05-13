# LLM Start Prompt

Paste everything below this line into Claude, ChatGPT, or any LLM.

**How to load the data:**
- **Minimum:** Upload `pursue-release01-dataset/pursue_release01_dataset.csv` (or `.json`) to your chat alongside this prompt.
- **Targeted analysis:** Upload specific files based on your goal. The LLM will recommend which files to add as you go.
- **Full repo access:** Use [Claude Code](https://docs.anthropic.com/en/docs/claude-code) to give the LLM direct access to the entire cloned repository — dataset, raw extracted text, pipeline, external references, and analysis.

---

## Context

You have the PURSUE Release 01 structured dataset — 721 UAP/UFO incidents extracted from 162 declassified U.S. government files released at war.gov/UFO on May 8, 2026.

**How it was built:** 113 PDFs downloaded. 63 scanned historical documents (3,500 pages) OCR'd via Tesseract. All text processed through Claude's API with a structured extraction prompt. Every identifiable incident normalized into 36 fields.

**Sources:** FBI (656 incidents, 1944–1977), DOW/AARO (51, 2016–2025), NASA (8, 1969–1974), State Department (5, 1985–1994), USAF (via incident summaries, 1947–1949).

**What this is:** Raw structured data from declassified government files. No editorializing in the dataset itself. Every row traces to a specific document. The `data_quality` field flags OCR vs. digital extraction.

**What this is NOT:** Complete. Notable absences: zero Navy reports, zero Nimitz/Tic-Tac/Gimbal cases, near-total gap 1970–2015, no AARO analytical products. What was selected and what was withheld is itself a data point.

**This repository contains:**

| Folder | Contents | Upload when... |
|--------|----------|----------------|
| `pursue-release01-dataset/` | CSV/JSON dataset (721 incidents, 36 fields), schema, methodology | Always — this is the core data |
| `raw-extracted-text/` | OCR output from 63 scanned PDFs, structured catalogs | You want to read original source text or verify extraction |
| `pipeline/` | Python extraction scripts | You want to reproduce or modify the pipeline |
| `external-reference-data/` | Compiled sources: scientific publications, government reports, physical evidence, astrophysics | You want to cross-reference against published literature |
| `data-analysis/` | Incident catalogs, quantified patterns, hypothesis rankings — all grounded in data | You want pre-computed analysis to build on |
| `speculative-analysis/` | Inference and speculation beyond what data directly shows | You want the full hypothetical framework (treat as exploratory, not established) |

## Key Patterns in the Data

These are observable without inference:

1. **Nuclear facility concentration.** 28 incidents near nuclear sites. 17 at Oak Ridge. Geographic center migrates with nuclear infrastructure: Hanford (1947) → Oak Ridge (1950) → White Sands (1957) → CENTCOM (2020s).

2. **EM interaction scaling.** 9 confirmed cases across 80 years. Interference targets scale with technology: engine ignition (1944) → radio (1957) → automotive electrical (1966) → phased-array radar with active jamming (2020s).

3. **Morphological evolution.** Disc 53% in 1940s → 2% in 2020s. Sphere 11% → 25%. Cylinder persists across all eras.

4. **Performance envelope consistency.** Objects exceed human capability by a constant margin across 78 years.

5. **Institutional behavior.** 78 years of systematic collection while publicly denying significance. Three current AARO products delayed (all involve nuclear weapons or sensor data). One published on schedule (no strategic weapons content).

## 19 Irreducible Anomalous Core Cases

Multi-sensor, multi-witness, trained observers, extended duration, beyond known technology. Includes Oak Ridge radar surveillance (1950), White Sands missile-following (1949), Andrews AFB pursuit (1948), Ohio 86-mile chase (1966), October 2020 vanishing pair with radar jamming, Western US multi-day event. Ask for the full list with incident IDs.

## Your Task

Read the dataset. Then:

1. **Ask me what I want to explore.** The dataset supports temporal, geographic, morphological, sensor, behavioral, and institutional analysis.

2. **Recommend files to upload** based on my goals. If I want pattern analysis, suggest `data-analysis/04-quantified-patterns.md`. If I want to cross-reference external sources, suggest `external-reference-data/`. If I want the full picture, suggest Claude Code.

3. **Ground every claim in incident IDs.**

4. **Distinguish layers.** Label findings as DATA (in the dataset), INFERENCE (derived but not stated), or SPECULATION (beyond data). Tell me which layer I'm on.

5. **Use web search when needed.** Cross-reference against Blue Book records, AARO reports, Kosloski testimony, SCU analyses, Hastings nuclear-UAP data, GEIPAN, Condon Report.

6. **Present competing explanations.** For any pattern: conventional explanation, anomalous explanation, distinguishing evidence.

7. **Challenge assumptions.** If I'm overreading a pattern, say so.

Start by confirming data loaded, reporting incident count, date range, agency breakdown, and field population rates. Then ask what I want to dig into.
