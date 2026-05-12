"""
UAP Document Pre-Extraction Pipeline
=====================================
Reads each document from the extracted markdown files,
sends it to Claude API for structured data extraction,
and outputs a compressed incident catalog as JSON + summary markdown.

This compresses ~500K tokens of raw text into ~30-50K tokens of structured data
that fits in a single Claude analysis chat.

Requirements:
    pip install anthropic

Usage:
    set ANTHROPIC_API_KEY=sk-ant-...
    python uap_pipeline.py
"""

import anthropic
import json
import os
import re
import time
import sys

# --- Configuration ---
INPUT_DIR = r"E:\downloads\uap_pdfs"
OUTPUT_DIR = r"E:\downloads\uap_pdfs\extracted"
MD_FILES = ["UAP_PART_1_of_2.md", "UAP_PART_2_of_2.md", "UAP_OCR_SCANNED.md"]
# Add OCR file when ready:
# MD_FILES = ["UAP_PART_1_of_2.md", "UAP_PART_2_of_2.md", "UAP_OCR_SCANNED.md"]

EXTRACTION_PROMPT = """You are a meticulous intelligence analyst cataloging UAP/UFO documents.

Analyze this document section and extract ALL factual data points into structured JSON.

Return ONLY a JSON object (no markdown fences, no preamble) with this structure:
{
  "filename": "the filename from the ## heading",
  "document_type": "mission report | range fouler debrief | email correspondence | cable | transcript | incident summary | photo description | launch summary | other",
  "source_agency": "FBI | DOW | NASA | State Department | AARO | unknown",
  "classification_markings": "any classification stamps visible",
  "redaction_level": "none | light | moderate | heavy | almost_entirely_redacted",
  "incidents": [
    {
      "date": "YYYY-MM-DD or approximate",
      "date_precision": "exact | month | year | decade | unknown",
      "location": "as specific as possible",
      "location_coordinates": "if given, otherwise null",
      "observers": "who saw it - branch, rank, number of witnesses",
      "observation_methods": ["visual", "IR_sensor", "radar", "NVGs", "photographic", "other"],
      "object_description": "shape, size, color, physical characteristics",
      "object_count": "number of objects observed",
      "object_behavior": "speed, maneuvers, altitude, notable actions",
      "quantitative_data": "any numbers - speed in knots, altitude in feet, duration, bearing, range",
      "duration": "how long the observation lasted",
      "electromagnetic_effects": "any equipment interference noted",
      "proximity_to_military": "nuclear sites, carriers, combat zones, test ranges",
      "witness_quotes": ["exact notable quotes from witnesses"],
      "resolution": "resolved | unresolved | inconclusive",
      "proposed_explanations": "any explanations offered or rejected"
    }
  ],
  "people_mentioned": ["names, titles, roles"],
  "programs_referenced": ["AARO", "Blue Book", "AATIP", "any named programs"],
  "cross_references": ["other documents, cases, or files referenced"],
  "procedural_notes": "how was this report filed? chain of command visible?",
  "notable_language": "any unusual phrasing, hedging, or emphasis in official language",
  "key_takeaway": "one sentence summary of what makes this document significant"
}

If the document contains multiple incidents, include all of them in the incidents array.
If a field has no data, use null.
If the document is a scanned photo with no text, note that in key_takeaway.

DOCUMENT CONTENT:
"""

def split_into_documents(md_content):
    """Split a markdown file into individual document sections."""
    sections = re.split(r'^## ', md_content, flags=re.MULTILINE)
    docs = []
    for section in sections[1:]:  # skip header before first ##
        lines = section.strip().split('\n', 1)
        filename = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""
        
        # Skip empty/scanned docs
        if "[Scanned document" in content or "[OCR returned no" in content:
            docs.append((filename, content, True))  # True = empty
        elif "[Error reading" in content:
            docs.append((filename, content, True))
        else:
            docs.append((filename, content, False))
    
    return docs

def extract_with_claude(client, filename, content, retry_count=0):
    """Send a document to Claude for structured extraction."""
    # Truncate very long documents to avoid token limits per call
    max_chars = 80000  # ~20K tokens, leaves room for response
    if len(content) > max_chars:
        content = content[:max_chars] + "\n\n[TRUNCATED - document continues beyond extraction limit]"
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": EXTRACTION_PROMPT + f"\n\n## {filename}\n\n{content}"
            }]
        )
        
        response_text = message.content[0].text.strip()
        # Clean up any markdown fences
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        
        return json.loads(response_text)
    
    except json.JSONDecodeError as e:
        if retry_count < 2:
            print(f"  JSON parse error, retrying... ({e})")
            time.sleep(2)
            return extract_with_claude(client, filename, content, retry_count + 1)
        print(f"  JSON parse failed after retries: {e}")
        return {"filename": filename, "error": str(e), "raw_response": response_text[:500]}
    
    except Exception as e:
        if "rate_limit" in str(e).lower() and retry_count < 3:
            wait = 30 * (retry_count + 1)
            print(f"  Rate limited, waiting {wait}s...")
            time.sleep(wait)
            return extract_with_claude(client, filename, content, retry_count + 1)
        print(f"  API error: {e}")
        return {"filename": filename, "error": str(e)}

def build_summary_markdown(all_results):
    """Convert extracted JSON into a compressed markdown summary for analysis."""
    md = "# PURSUE Release 01 — Structured Incident Catalog\n\n"
    md += f"Auto-extracted from {len(all_results)} documents via Claude API pipeline.\n\n"
    md += "---\n\n"
    
    # Stats
    total_incidents = sum(len(r.get("incidents", [])) for r in all_results if "error" not in r)
    agencies = {}
    doc_types = {}
    locations = []
    dates = []
    
    for r in all_results:
        if "error" in r:
            continue
        ag = r.get("source_agency", "unknown")
        agencies[ag] = agencies.get(ag, 0) + 1
        dt = r.get("document_type", "unknown")
        doc_types[dt] = doc_types.get(dt, 0) + 1
        for inc in r.get("incidents", []):
            if inc.get("location"):
                locations.append(inc["location"])
            if inc.get("date"):
                dates.append(inc["date"])
    
    md += "## Quick Stats\n\n"
    md += f"- **Documents processed:** {len(all_results)}\n"
    md += f"- **Total incidents cataloged:** {total_incidents}\n"
    md += f"- **Date range:** {min(dates) if dates else 'N/A'} to {max(dates) if dates else 'N/A'}\n"
    md += f"- **Agencies:** {json.dumps(agencies)}\n"
    md += f"- **Document types:** {json.dumps(doc_types)}\n\n"
    
    md += "---\n\n"
    
    # Per-document summaries
    for r in all_results:
        fn = r.get("filename", "unknown")
        md += f"### {fn}\n\n"
        
        if "error" in r:
            md += f"*Extraction error: {r['error']}*\n\n"
            continue
        
        md += f"**Agency:** {r.get('source_agency', '?')} | "
        md += f"**Type:** {r.get('document_type', '?')} | "
        md += f"**Redaction:** {r.get('redaction_level', '?')}\n\n"
        
        if r.get("key_takeaway"):
            md += f"> {r['key_takeaway']}\n\n"
        
        for j, inc in enumerate(r.get("incidents", []), 1):
            md += f"**Incident {j}:** "
            parts = []
            if inc.get("date"): parts.append(inc["date"])
            if inc.get("location"): parts.append(inc["location"])
            if inc.get("object_description"): parts.append(inc["object_description"])
            md += " | ".join(parts) + "\n"
            
            if inc.get("object_behavior"):
                md += f"- Behavior: {inc['object_behavior']}\n"
            if inc.get("quantitative_data"):
                md += f"- Data: {inc['quantitative_data']}\n"
            if inc.get("observation_methods"):
                md += f"- Observed via: {', '.join(inc['observation_methods'])}\n"
            if inc.get("witness_quotes"):
                for q in inc["witness_quotes"]:
                    md += f"- Quote: \"{q}\"\n"
            if inc.get("electromagnetic_effects"):
                md += f"- EM effects: {inc['electromagnetic_effects']}\n"
            if inc.get("proximity_to_military"):
                md += f"- Military proximity: {inc['proximity_to_military']}\n"
            md += "\n"
        
        if r.get("people_mentioned"):
            md += f"**People:** {', '.join(r['people_mentioned'])}\n"
        if r.get("programs_referenced"):
            md += f"**Programs:** {', '.join(r['programs_referenced'])}\n"
        if r.get("cross_references"):
            md += f"**Cross-refs:** {', '.join(r['cross_references'])}\n"
        if r.get("notable_language"):
            md += f"**Notable language:** {r['notable_language']}\n"
        
        md += "\n---\n\n"
    
    return md

def main():
    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: Set your API key first:")
        print("  $env:ANTHROPIC_API_KEY = 'sk-ant-...'")
        print("")
        print("Get one at: https://console.anthropic.com/settings/keys")
        sys.exit(1)
    
    client = anthropic.Anthropic(api_key=api_key)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load all documents
    all_docs = []
    for md_file in MD_FILES:
        filepath = os.path.join(INPUT_DIR, md_file)
        if not os.path.exists(filepath):
            print(f"Skipping {md_file} — not found")
            continue
        print(f"Loading {md_file}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        docs = split_into_documents(content)
        all_docs.extend(docs)
    
    # Deduplicate by filename
    seen = set()
    unique_docs = []
    for filename, content, is_empty in all_docs:
        if filename not in seen:
            seen.add(filename)
            unique_docs.append((filename, content, is_empty))
    
    print(f"\nTotal unique documents: {len(unique_docs)}")
    text_docs = [(f, c, e) for f, c, e in unique_docs if not e]
    empty_docs = [(f, c, e) for f, c, e in unique_docs if e]
    print(f"  With text: {len(text_docs)}")
    print(f"  Empty/scanned: {len(empty_docs)}")
    
    # Check for existing progress (resume support)
    progress_file = os.path.join(OUTPUT_DIR, "progress.json")
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            all_results = json.load(f)
        done = {r["filename"] for r in all_results}
        print(f"  Resuming — {len(done)} already processed")
    else:
        all_results = []
        done = set()
    
    # Process each document with text
    for i, (filename, content, _) in enumerate(text_docs, 1):
        if filename in done:
            continue
        
        print(f"[{i}/{len(text_docs)}] {filename} ({len(content)} chars)...", end="", flush=True)
        
        result = extract_with_claude(client, filename, content)
        all_results.append(result)
        done.add(filename)
        
        print(f" -> {len(result.get('incidents', []))} incidents")
        
        # Save progress after each document
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        # Rate limit courtesy
        time.sleep(1)
    
    # Add empty docs as stubs
    for filename, content, _ in empty_docs:
        if filename not in done:
            all_results.append({
                "filename": filename,
                "document_type": "scanned_image",
                "source_agency": "unknown",
                "redaction_level": "unknown",
                "incidents": [],
                "key_takeaway": "Scanned document with no extractable text — requires visual analysis"
            })
    
    # Save full JSON
    json_output = os.path.join(OUTPUT_DIR, "uap_catalog.json")
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\nFull JSON catalog: {json_output}")
    
    # Build compressed markdown summary
    summary = build_summary_markdown(all_results)
    md_output = os.path.join(OUTPUT_DIR, "UAP_CATALOG_SUMMARY.md")
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    size_kb = os.path.getsize(md_output) / 1024
    word_count = len(summary.split())
    token_est = int(word_count * 1.3)
    
    print(f"Compressed summary: {md_output}")
    print(f"  Size: {size_kb:.0f} KB | {word_count:,} words | ~{token_est:,} tokens")
    print(f"  Compression ratio: ~{int(285972 / max(word_count, 1))}x")
    
    if token_est < 100000:
        print(f"\n  >> FITS IN ONE CLAUDE CHAT with room for analysis! <<")
    else:
        print(f"\n  Still large — may need to split for analysis chat")
    
    print("\nDone! Next steps:")
    print("1. Open a new Claude chat")
    print("2. Upload UAP_CATALOG_SUMMARY.md + UAP_RESEARCH_PROMPT.md")
    print("3. Send Phase 1 from the research prompt")

if __name__ == "__main__":
    main()
