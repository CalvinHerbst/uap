# PURSUE Release 01 — Extraction Methodology

## Overview

This dataset was produced by extracting, OCR-processing, and structuring every identifiable UAP/UFO incident from the 113 PDF files in the PURSUE Release 01 (May 8, 2026, war.gov/UFO). The goal was to convert unstructured government documents into a machine-readable research dataset.

## Pipeline

### Step 1: Document Acquisition

All 162 files from war.gov/UFO were downloaded. Of these, 113 were PDFs (the remainder were video and image files not processed in this pipeline).

### Step 2: Document Classification

Each PDF was classified as either:
- **Digital** (50 files): Born-digital PDFs with extractable text layers. These include AARO reports, NASA debriefings, State Department cables, and some modern FBI documents.
- **Scanned** (63 files): Image-only PDFs requiring OCR. These are primarily historical FBI documents (1940s–1970s typewritten pages), the COMETA report, and USAF Project Sign/Grudge checklists.

### Step 3: Text Extraction

- Digital PDFs: text extracted directly using standard PDF text extraction.
- Scanned PDFs: processed through Tesseract OCR. 63 documents totaling approximately 3,500 pages.

### Step 4: OCR Quality Assessment

Tesseract output quality varied significantly by source:
- **High quality:** 1960s–1970s FBI documents (clean typewritten text, good scan quality)
- **Medium quality:** 1950s FBI documents (some fading, inconsistent scan quality)
- **Low quality:** 1940s FBI documents (poor carbon copies, heavy redaction, degraded paper)
- **Variable:** COMETA report (French text, mixed typography), USAF checklists (form fields with handwritten entries)

No manual correction was applied to OCR output. The `data_quality` field flags each row as `digital` or `ocr` to enable quality-aware analysis.

### Step 5: Structured Extraction

All extracted text was processed through Claude's API (claude-sonnet-4-20250514) with a structured extraction prompt designed to:

1. Identify each discrete incident described in the document
2. Extract all available information into the 36-field schema
3. Normalize dates, locations, and shape descriptions where possible
4. Preserve original language in quotation and description fields
5. Flag cases where multiple incidents are described in a single document passage

The extraction prompt instructed the model to:
- Treat each distinct sighting as a separate incident (even when multiple appear on a single page)
- Preserve uncertainty (use null rather than guess when information is ambiguous)
- Retain original witness language in quote fields
- Flag OCR artifacts rather than silently correcting them

### Step 6: Deduplication

Incidents appearing in multiple source documents (e.g., an FBI field office report and a headquarters summary of the same event) were deduplicated by matching on date + location + description. Where duplicates existed, the version with the most complete information was retained.

### Step 7: Validation

- Row count was validated against document-level incident counts
- Date ranges were checked for plausibility
- Location fields were spot-checked against source documents
- Shape normalization was reviewed for consistency
- Nuclear and military proximity flags were validated against known facility locations

## Known Issues

1. **OCR errors in names and numbers.** Particularly in 1940s FBI documents, proper names, dates, and numeric values may be garbled. These are flagged by `data_quality: ocr` but not individually corrected.

2. **Incident boundary ambiguity.** Some source documents describe ongoing multi-day events (e.g., three days of radar tracking at Oak Ridge). These were treated as single incidents with duration noted, but could reasonably be decomposed into multiple daily incidents.

3. **USAF checklist decomposition.** The USAF Project Sign/Grudge checklists (incidents 1–233) were processed at the document level. Not all 233 incidents were fully decomposed into individual dataset rows. This is noted in the README as a known gap.

4. **Redaction handling.** Many FBI documents contain redacted passages (names, locations, sources). Redacted content is not represented in the dataset. The extent of redaction is not systematically tracked but is substantial in some sections.

5. **Translation.** The COMETA report is in French. Extraction was performed on the French text with translation handled by the LLM during structured extraction. Some nuance may be lost in translation.

## Reproducibility

The extraction pipeline is deterministic given the same input documents, OCR engine, and LLM prompt. However:
- Tesseract OCR output may vary slightly across versions
- LLM extraction may produce minor variations across runs (temperature-dependent)
- The source PDFs from war.gov/UFO are the authoritative input; if they are modified or removed, the pipeline cannot be reproduced

## Tools Used

- **PDF text extraction:** Python (PyPDF2/pdfplumber)
- **OCR:** Tesseract 5.x
- **Structured extraction:** Claude API (Anthropic)
- **Data processing:** Python (pandas)
