import json, os

json_path = r"E:\downloads\uap_pdfs\extracted\uap_catalog.json"
output_path = r"E:\downloads\uap_pdfs\extracted\UAP_CATALOG_SUMMARY.md"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

md = "# PURSUE Release 01 - Structured Incident Catalog\n\n"
md += f"Auto-extracted from {len(data)} documents.\n\n---\n\n"

total_incidents = sum(len(r.get("incidents", [])) for r in data)
md += f"**Documents:** {len(data)} | **Incidents:** {total_incidents}\n\n---\n\n"

for r in data:
    fn = r.get("filename", "unknown")
    md += f"### {fn}\n\n"
    
    if r.get("error"):
        md += f"*Extraction error: {r['error']}*\n\n---\n\n"
        continue
    
    md += f"**Agency:** {r.get('source_agency','?')} | "
    md += f"**Type:** {r.get('document_type','?')} | "
    md += f"**Redaction:** {r.get('redaction_level','?')}\n\n"
    
    if r.get("key_takeaway"):
        md += f"> {r['key_takeaway']}\n\n"
    
    for j, inc in enumerate(r.get("incidents", []), 1):
        parts = []
        if inc.get("date"): parts.append(inc["date"])
        if inc.get("location"): parts.append(inc["location"])
        if inc.get("object_description"): parts.append(inc["object_description"])
        md += f"**Incident {j}:** " + " | ".join(parts) + "\n"
        if inc.get("object_behavior"):
            md += f"- Behavior: {inc['object_behavior']}\n"
        if inc.get("quantitative_data"):
            md += f"- Data: {inc['quantitative_data']}\n"
        if inc.get("observation_methods"):
            methods = inc["observation_methods"]
            if isinstance(methods, list):
                md += f"- Observed via: {', '.join(methods)}\n"
            else:
                md += f"- Observed via: {methods}\n"
        if inc.get("witness_quotes"):
            for q in inc["witness_quotes"]:
                md += f'- Quote: "{q}"\n'
        if inc.get("electromagnetic_effects"):
            md += f"- EM effects: {inc['electromagnetic_effects']}\n"
        if inc.get("proximity_to_military"):
            md += f"- Military proximity: {inc['proximity_to_military']}\n"
        md += "\n"
    
    if r.get("people_mentioned"):
        p = r["people_mentioned"]
        if isinstance(p, list):
            md += f"**People:** {', '.join(str(x) for x in p)}\n"
    if r.get("programs_referenced"):
        p = r["programs_referenced"]
        if isinstance(p, list):
            md += f"**Programs:** {', '.join(str(x) for x in p)}\n"
    if r.get("cross_references"):
        p = r["cross_references"]
        if isinstance(p, list):
            md += f"**Cross-refs:** {', '.join(str(x) for x in p)}\n"
    if r.get("notable_language"):
        md += f"**Notable language:** {r['notable_language']}\n"
    
    md += "\n---\n\n"

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(md)

size_kb = os.path.getsize(output_path) / 1024
words = len(md.split())
tokens = int(words * 1.3)
print(f"Created: {output_path}")
print(f"Size: {size_kb:.0f} KB | {words:,} words | ~{tokens:,} tokens")
if tokens < 120000:
    print("FITS in one Claude chat!")
else:
    print(f"Too large - need to split")
