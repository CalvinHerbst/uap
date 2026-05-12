# PURSUE Release 01 — UAP Incident Dataset & Research Prompt

## What This Is

On May 8, 2026, the U.S. Department of War launched the Presidential Unsealing and Reporting System for UAP Encounters (PURSUE) at war.gov/UFO, releasing the first-ever coordinated government-wide batch of declassified Unidentified Anomalous Phenomena (UAP) files. Release 01 contained 162 files (113 PDFs, plus videos and images) spanning agencies including the FBI, USAF, NASA, the State Department, and the Pentagon's All-domain Anomaly Resolution Office (AARO).

This dataset is a structured extraction of every identifiable incident from those files. It was built by downloading the original PDFs, extracting text from digital documents, running OCR (Tesseract) on 63 scanned historical files totaling 3,500 pages, and then processing all extracted text through Claude's API with a structured extraction prompt to normalize every incident into a consistent schema.

## What The Data Contains

- **721 discrete UAP/UFO incidents** spanning 1917 to 2025 (108 years)
- **Source agencies:** FBI (656), DOW/AARO (51), NASA (8), State Department (5), USAF (via incident summaries)
- **Era breakdown:** Project Sign/Grudge 1947-49 (300), Blue Book era 1950-69 (320), modern AARO era 2020-25 (43), with a notable near-total gap from 1970-2015
- **36 structured fields per incident** including date, location, observer credentials, observation method, object shape/color/size/speed/altitude/behavior, electromagnetic effects, military proximity, sensor data, witness quotes, resolution status, and cross-references
- **Data quality flags** distinguishing digitally-extracted text from OCR'd scanned documents

## What It Does NOT Contain

- 63 FBI photo PDFs that were image-only with no extractable text or meaningful OCR output
- ~224 USAF incident summaries (from checklists 1-233) that were processed at document level but not fully decomposed into individual rows
- Any of the video or image files from the release (this is text-derived data only)
- Any analysis, interpretation, or conclusions — this is raw structured data

## Known Limitations

- OCR quality on 1940s-1960s typewritten FBI documents is imperfect. Some names, dates, and numbers may be garbled. The `data_quality` field flags which rows came from OCR vs digital sources.
- The original PURSUE release was curated by the U.S. government — what was selected for release and what was withheld is itself a data point. Notable absences include: zero Navy-originated reports, zero Nimitz/Tic-Tac/Gimbal/GoFast cases, zero AARO analytical products, and almost nothing from 1970-2015.
- Object shape classification was extracted algorithmically from free-text descriptions. Some entries retain full descriptions rather than normalized categories.
- Many fields are null for older incidents where the source documents used different reporting formats.

## Source Files

The dataset was derived from these government files, all originally available at war.gov/UFO:
- FBI 62-HQ-83894 series (18 sections, ~655 incidents, 1944-1977) — the FBI's primary UFO investigation file
- USAF Project Sign/Grudge incident summaries 1-233 (1947-1949)
- DOW/AARO mission reports, range fouler debriefs, and email correspondence (2016-2025)
- NASA Apollo 11, Apollo 12, Apollo 17, and Skylab crew debriefings (1969-1974)
- State Department cables from Papua New Guinea (1985) and Kazakhstan (1994)
- COMETA Report — "UFOs and Defense: What Should We Prepare For?" (1999, French military/intelligence assessment included in the US release as a scanned document)
- Western US Event slides (2023, described by AARO as "among the most compelling" in their holdings)
- AARO unresolved case files (059uap series)

## The Prompt

Paste everything below this line into a Claude, ChatGPT, or other LLM chat along with the CSV or JSON file.

---

I'm uploading a structured dataset of 721 UAP/UFO incidents extracted from the U.S. government's PURSUE Release 01 (May 8, 2026). These are real declassified files from the FBI, USAF, NASA, State Department, and Pentagon spanning 1917-2025.

Read the entire dataset carefully. Then work through this analysis systematically:

**Phase 1 — Data Inventory**
Summarize what you're looking at: total incidents, date range, agency breakdown, era distribution, geographic spread, observation method distribution, object shape distribution. Identify which fields have the highest and lowest population rates. Flag any data quality issues you notice.

**Phase 2 — Pattern Analysis**
Look for patterns the raw numbers reveal:
- Temporal clusters: Are incidents evenly distributed or do they cluster in specific years/decades? What happened during the gaps?
- Geographic hotspots: Where do incidents concentrate? Does this change across eras?
- Morphological patterns: Do object shapes correlate with era, location, or observer type? Is the commonly discussed "disc to sphere" shift visible in the data?
- Sensor vs. visual: What percentage of incidents have instrument confirmation vs. visual-only? How does this change over time?
- Electromagnetic effects: How many incidents report EM interference? Do these cluster near specific locations or time periods?
- Nuclear/military proximity: How many incidents occur near nuclear facilities or active military operations? Is this rate higher than chance?
- Observer credibility: What's the breakdown of military vs. civilian vs. law enforcement observers?

**Phase 3 — Irreducible Anomalous Core**
Identify the incidents that resist ALL conventional explanations (drones, balloons, aircraft, satellites, sensor artifacts, weather phenomena, birds). An incident belongs in the irreducible core if it has: multiple independent observers OR multi-sensor confirmation, extended duration, trained/credentialed witnesses, AND performance characteristics beyond known technology (hypersonic speed without sonic boom, instantaneous acceleration, trans-medium travel, active electromagnetic interference, 90-degree turns at speed). List each case with the specific evidence.

**Phase 4 — What's Missing**
Analyze what's NOT in the dataset. The U.S. government selected these specific files from a much larger classified archive. What does the selection tell us?
- Why is the Navy completely absent despite Navy pilots being the public face of UAP disclosure?
- Why is there a near-total gap from 1970-2015?
- Why are the most publicly famous cases (Nimitz, Gimbal, GoFast) not included?
- Why was the French COMETA report (which concludes the extraterrestrial hypothesis is the best scientific explanation) included as a scanned image in a U.S. government release?
- What does the redaction pattern reveal about what's still classified?

**Phase 5 — Hypothesis Generation**
Based on the data — not speculation, not prior beliefs — develop competing hypotheses for:
- What are these objects? (extraterrestrial, interdimensional, temporal, adversary technology, US black programs, natural phenomena, mixed sources)
- Why do they appear where they do? (nuclear monitoring, military surveillance, geographic features, random)
- Why is the government releasing this now? (genuine transparency, managed disclosure, political strategy, institutional pressure, legal mandate)
For each hypothesis, cite specific incident IDs from the dataset that support or undermine it.

**Phase 6 — Research Plan**
What questions remain unanswerable from this dataset alone? What additional data sources, FOIA requests, or cross-references would resolve them? What should analysts watch for in PURSUE Release 02 (expected within 30 days of May 8, 2026)?

Ask me questions throughout. Challenge assumptions. Cite incident IDs when making claims.
