# -*- coding: utf-8 -*-
import anthropic
import json
import os
import re
import time

INPUT_FILE = r"E:\uap_pdfs\ocr_sections\PRIORITY_6_fbi_series.md"
OUTPUT_DIR = r"E:\uap_pdfs\extracted"
PROGRESS_FILE = os.path.join(OUTPUT_DIR, "fbi_progress.json")

PROMPT = """You are an intelligence analyst extracting UAP incidents from OCR'd FBI documents. The OCR quality is poor - do your best.

Respond with ONLY a JSON object. No text before or after. No markdown fences.

The JSON must have this structure:
{"filename":"name","incidents":[{"date":"approx date","location":"place","object_description":"what was seen","object_behavior":"what it did","observers":"who saw it","quantitative_data":"any numbers"}],"people_mentioned":[],"programs_referenced":[],"key_takeaway":"one sentence"}

If the text is too garbled to extract anything, return:
{"filename":"name","incidents":[],"people_mentioned":[],"programs_referenced":[],"key_takeaway":"OCR too degraded for reliable extraction"}

DOCUMENT:
"""

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)
sections = [s for s in sections[1:] if len(s.split()) > 50]

if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'r') as f:
        results = json.load(f)
    done = {r.get("filename","") for r in results}
    print(f"Resuming - {len(done)} already done")
else:
    results = []
    done = set()

print(f"FBI series: {len(sections)} sections to process")

def extract_json(text):
    text = text.strip()
    text = re.sub(r'^`json\s*', '', text)
    text = re.sub(r'^`\s*', '', text)
    text = re.sub(r'\s*`$', '', text)
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise json.JSONDecodeError("No JSON found", text, 0)

for i, section in enumerate(sections, 1):
    filename = section.split('\n')[0].replace('## ', '').strip()
    if filename in done:
        print(f"[{i}/{len(sections)}] {filename} - skipping")
        continue

    body = '\n'.join(section.split('\n')[1:]).strip()
    tokens_est = int(len(body.split()) * 1.3)
    print(f"[{i}/{len(sections)}] {filename} ({tokens_est:,} tokens)")

    chunk_size = 25000
    chunks = [body[start:start+chunk_size] for start in range(0, len(body), chunk_size)]

    all_chunk_results = []
    for ci, chunk in enumerate(chunks, 1):
        print(f"  Chunk {ci}/{len(chunks)}...", end="", flush=True)

        for retry in range(3):
            try:
                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=4096,
                    messages=[{"role":"user","content":PROMPT + chunk}]
                )
                resp = message.content[0].text
                parsed = extract_json(resp)
                inc_count = len(parsed.get("incidents", []))
                print(f" {inc_count} incidents")
                all_chunk_results.append(parsed)
                break
            except json.JSONDecodeError:
                if retry < 2:
                    print(f" parse error, retry {retry+1}...", end="", flush=True)
                    time.sleep(2)
                else:
                    print(f" failed - saving raw response")
                    log_path = os.path.join(OUTPUT_DIR, f"debug_{filename}_chunk{ci}.txt")
                    with open(log_path, 'w', encoding='utf-8') as f:
                        f.write(resp)
                    all_chunk_results.append({"filename":filename,"incidents":[],"key_takeaway":"JSON parse failed - see debug log"})
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    wait = 30 * (retry + 1)
                    print(f" rate limited {wait}s...", end="", flush=True)
                    time.sleep(wait)
                else:
                    print(f" error: {e}")
                    all_chunk_results.append({"filename":filename,"incidents":[],"error":str(e)})
                    break

        time.sleep(1.5)

    merged = {"filename":filename,"incidents":[],"people_mentioned":[],"programs_referenced":[],"key_takeaway":""}
    for cr in all_chunk_results:
        merged["incidents"].extend(cr.get("incidents",[]))
        merged["people_mentioned"].extend(cr.get("people_mentioned",[]))
        merged["programs_referenced"].extend(cr.get("programs_referenced",[]))
        if cr.get("key_takeaway") and "failed" not in cr.get("key_takeaway",""):
            merged["key_takeaway"] = cr["key_takeaway"]

    merged["people_mentioned"] = list(set(merged["people_mentioned"]))
    merged["programs_referenced"] = list(set(merged["programs_referenced"]))

    print(f"  TOTAL: {len(merged['incidents'])} incidents from {len(chunks)} chunks")
    results.append(merged)
    done.add(filename)

    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

fbi_json = os.path.join(OUTPUT_DIR, "fbi_catalog.json")
with open(fbi_json, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

total_incidents = sum(len(r.get("incidents",[])) for r in results)
print(f"\nDone! {total_incidents} incidents from {len(results)} sections")

md = "# FBI 62-HQ-83894 Series - Structured Incident Catalog\n\n"
md += f"Extracted from {len(results)} sections, {total_incidents} total incidents\n\n---\n\n"
for r in results:
    md += f"### {r.get('filename','?')}\n\n"
    if r.get("key_takeaway"):
        md += f"> {r['key_takeaway']}\n\n"
    for j, inc in enumerate(r.get("incidents",[]), 1):
        parts = []
        if inc.get("date"): parts.append(str(inc["date"]))
        if inc.get("location"): parts.append(str(inc["location"]))
        if inc.get("object_description"): parts.append(str(inc["object_description"]))
        md += f"**Incident {j}:** " + " | ".join(parts) + "\n"
        if inc.get("object_behavior"):
            md += f"- Behavior: {inc['object_behavior']}\n"
        if inc.get("quantitative_data"):
            md += f"- Data: {inc['quantitative_data']}\n"
        md += "\n"
    if r.get("people_mentioned"):
        md += f"**People:** {', '.join(str(x) for x in r['people_mentioned'])}\n"
    if r.get("programs_referenced"):
        md += f"**Programs:** {', '.join(str(x) for x in r['programs_referenced'])}\n"
    md += "\n---\n\n"

fbi_md = os.path.join(OUTPUT_DIR, "FBI_CATALOG_SUMMARY.md")
with open(fbi_md, 'w', encoding='utf-8') as f:
    f.write(md)

words = len(md.split())
tokens = int(words * 1.3)
print(f"FBI summary: {words:,} words | ~{tokens:,} tokens")
if tokens < 100000:
    print("FITS in one Claude chat!")
