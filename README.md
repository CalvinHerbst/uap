# UAP Research Data

Structured datasets, extraction pipeline, and analysis of declassified U.S. government UAP files from [PURSUE Release 01](https://war.gov/UFO) (May 8, 2026).

## Repository Structure

```
uap/
├── pursue-release01-dataset/    # The structured dataset
│   ├── pursue_release01_dataset.csv   (721 incidents, 36 fields)
│   ├── pursue_release01_dataset.json
│   ├── SCHEMA.md
│   ├── METHODOLOGY.md
│   └── README.md
│
├── raw-extracted-text/          # OCR and text extraction output
│   ├── PRIORITY_1–7 .md files   (sectioned OCR text from 63 scanned PDFs)
│   ├── uap_catalog.json         (structured extraction from digital PDFs)
│   ├── fbi_catalog.json         (structured extraction from FBI files)
│   └── *_SUMMARY.md files       (human-readable catalog summaries)
│
├── pipeline/                    # Python extraction scripts
│   ├── extract.py               (digital PDF text extraction)
│   ├── ocr_extract.py           (Tesseract OCR pipeline)
│   ├── uap_pipeline.py          (Claude API structured extraction)
│   ├── fbi_pipeline.py          (FBI-specific extraction)
│   ├── build_dataset.py         (CSV/JSON dataset builder)
│   └── *.py                     (supporting scripts)
│
├── external-reference-data/     # Compiled external sources
│   ├── CATEGORY_A (scientific publications)
│   ├── CATEGORY_B (government reports)
│   └── CATEGORY_C+D (physical evidence, astrophysics)
│
├── data-analysis/               # Data-supported findings
│   ├── 01–02 incident catalogs  (modern + historical, full tables)
│   ├── 03 revised statistics    (after FBI integration)
│   ├── 04 quantified patterns   (time-series, shape, geography)
│   ├── 05 hypothesis ranking    (11 hypotheses scored against data)
│   └── 06 ETH sub-theories      (7 sub-theories ranked)
│
├── speculative-analysis/        # Inference and speculation beyond data
│   ├── 01–04 interpretive analysis
│   ├── 05 deep speculative threads
│   └── 06 speculative framework (the full hypothetical picture)
│
├── LLM_START_PROMPT.md           # Start here — paste into any LLM
└── README.md                    # This file
```

## What This Is

On May 8, 2026, the U.S. government released 162 declassified UAP files. This repo contains:

- **A structured dataset** of every identifiable incident (721 total, 1917–2025, 36 fields each) built by OCR-processing 63 scanned historical documents and running all text through Claude's API
- **The raw extracted text** from all 113 PDFs
- **The extraction pipeline** (Python scripts, reproducible)
- **External reference data** compiled from peer-reviewed and government sources
- **Analysis** separated into data-supported findings and speculative inference

Everything outside `speculative-analysis/` is grounded in declassified government documents, peer-reviewed publications, or verifiable public records.

## Quick Start

See [`LLM_START_PROMPT.md`](LLM_START_PROMPT.md) — paste into any LLM with the CSV attached. For full repo access, use [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Source

All data derived from files originally released at [war.gov/UFO](https://war.gov/UFO). The source PDFs are U.S. government works in the public domain. They are not included in this repo due to size (~2.5GB) but remain available at the source URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Author

Calvin Herbst / [Distant Fringe Pictures LLC](https://distantfringe.com)
