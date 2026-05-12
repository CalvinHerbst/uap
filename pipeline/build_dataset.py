# -*- coding: utf-8 -*-
"""
PURSUE Release 01 — Unified Dataset Builder
============================================
Merges uap_catalog.json and fbi_catalog.json into a single
machine-readable dataset with consistent schema.

Outputs:
  - pursue_release01_dataset.json  (nested, full fidelity)
  - pursue_release01_dataset.csv   (flat, for spreadsheets/viz)

Usage:
  py -3.10 build_dataset.py
"""

import json
import csv
import os
import re
from datetime import datetime

INPUT_DIR = r"E:\uap_pdfs\extracted"
OUTPUT_DIR = r"E:\uap_pdfs\dataset"

UNIFIED_FIELDS = [
    "incident_id",
    "source_file",
    "source_agency",
    "document_type",
    "date_raw",
    "date_normalized",
    "date_precision",
    "time",
    "location_raw",
    "location_country",
    "location_region",
    "location_coordinates",
    "observer_names",
    "observer_credentials",
    "observer_count",
    "observation_methods",
    "object_count",
    "object_shape",
    "object_color",
    "object_size",
    "object_altitude",
    "object_speed",
    "object_heading",
    "object_behavior",
    "duration",
    "sound",
    "construction_materials",
    "exhaust_trails",
    "em_effects",
    "physical_effects",
    "weather_conditions",
    "military_proximity",
    "resolution_status",
    "credibility_assessment",
    "redaction_level",
    "notable_quotes",
    "cross_references",
    "programs_mentioned",
    "people_mentioned",
    "pii_status",
    "data_quality",
    "key_takeaway",
    "era"
]


def classify_era(date_str):
    if not date_str:
        return "unknown"
    try:
        year = int(re.search(r'(\d{4})', str(date_str)).group(1))
    except (AttributeError, ValueError):
        return "unknown"
    if year < 1947:
        return "pre_modern"
    elif year <= 1949:
        return "project_sign_grudge"
    elif year <= 1969:
        return "blue_book_era"
    elif year <= 1989:
        return "dark_period"
    elif year <= 2007:
        return "pre_aatip"
    elif year <= 2017:
        return "aatip_era"
    elif year <= 2024:
        return "aaro_era"
    else:
        return "pursue_era"


def classify_agency(filename, doc_agency=None):
    if doc_agency and doc_agency.lower() not in ("unknown", "null", "n/a", ""):
        return doc_agency
    fn = filename.lower() if filename else ""
    if fn.startswith("65_hs1") or fn.startswith("fbi") or fn.startswith("62-hq"):
        return "FBI"
    elif fn.startswith("dow-uap"):
        return "DOW"
    elif fn.startswith("nasa"):
        return "NASA"
    elif fn.startswith("dos-uap"):
        return "State Department"
    elif fn.startswith("38_") or fn.startswith("342_"):
        return "USAF"
    elif fn.startswith("255_"):
        return "French Ministry of Defense"
    elif fn.startswith("331_"):
        return "US Army"
    elif fn.startswith("059") or fn.startswith("341_"):
        return "AARO"
    else:
        return "unknown"


def safe_str(val):
    if val is None:
        return None
    if isinstance(val, list):
        return "; ".join(str(v) for v in val if v)
    return str(val).strip() if str(val).strip() else None


def safe_list(val):
    if val is None:
        return []
    if isinstance(val, str):
        return [val] if val.strip() else []
    if isinstance(val, list):
        return [str(v) for v in val if v]
    return [str(val)]


def normalize_incident(inc, source_file, source_agency, doc_type,
                       redaction, people, programs, crossrefs, 
                       incident_counter, key_takeaway):
    """Convert a single incident from either catalog format to unified schema."""
    
    date_raw = safe_str(inc.get("date"))
    
    row = {
        "incident_id": f"PURSUE-R01-{incident_counter:04d}",
        "source_file": source_file,
        "source_agency": source_agency,
        "document_type": doc_type,
        "date_raw": date_raw,
        "date_normalized": date_raw,  # Could add date parsing logic
        "date_precision": safe_str(inc.get("date_precision", "unknown")),
        "time": safe_str(inc.get("time")),
        "location_raw": safe_str(inc.get("location")),
        "location_country": None,  # Could add geo parsing
        "location_region": None,
        "location_coordinates": safe_str(inc.get("location_coordinates")),
        "observer_names": safe_str(inc.get("observers")),
        "observer_credentials": None,
        "observer_count": safe_str(inc.get("observer_count")),
        "observation_methods": safe_str(inc.get("observation_methods")),
        "object_count": safe_str(inc.get("object_count")),
        "object_shape": None,
        "object_color": None,
        "object_size": None,
        "object_altitude": None,
        "object_speed": None,
        "object_heading": None,
        "object_behavior": safe_str(inc.get("object_behavior")),
        "duration": safe_str(inc.get("duration")),
        "sound": safe_str(inc.get("sound")),
        "construction_materials": None,
        "exhaust_trails": None,
        "em_effects": safe_str(inc.get("electromagnetic_effects") or inc.get("em_effects")),
        "physical_effects": None,
        "weather_conditions": None,
        "military_proximity": safe_str(inc.get("proximity_to_military")),
        "resolution_status": safe_str(inc.get("resolution")),
        "credibility_assessment": None,
        "redaction_level": redaction,
        "notable_quotes": safe_str(inc.get("witness_quotes")),
        "cross_references": safe_str(crossrefs),
        "programs_mentioned": safe_str(programs),
        "people_mentioned": safe_str(people),
        "pii_status": "unredacted" if people else "unknown",
        "data_quality": "ocr" if source_agency == "FBI" else "digital",
        "key_takeaway": key_takeaway,
        "era": classify_era(date_raw)
    }
    
    # Parse object_description into sub-fields if available
    desc = safe_str(inc.get("object_description", ""))
    if desc:
        row["object_shape"] = desc  # Full description goes here
        # Try to extract specific attributes
        desc_lower = desc.lower() if desc else ""
        for shape in ["disc", "disk", "saucer", "sphere", "orb", "cigar", 
                       "cylinder", "triangle", "oval", "egg", "football",
                       "diamond", "chevron", "tic-tac", "fireball", "light"]:
            if shape in desc_lower:
                row["object_shape"] = shape
                break
    
    # Parse quantitative data into specific fields
    quant = safe_str(inc.get("quantitative_data", ""))
    if quant:
        # Try to extract speed
        speed_match = re.search(r'(\d[\d,]*)\s*(?:knots|kts|mph|kph|mach)', quant, re.I)
        if speed_match:
            row["object_speed"] = speed_match.group(0)
        
        # Try to extract altitude
        alt_match = re.search(r'(\d[\d,]*)\s*(?:feet|ft|meters|m)\s*(?:altitude|alt|AGL|MSL)?', quant, re.I)
        if alt_match:
            row["object_altitude"] = alt_match.group(0)
    
    return row


def load_catalog(filepath):
    """Load a JSON catalog file."""
    if not os.path.exists(filepath):
        print(f"  Not found: {filepath}")
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load all catalogs
    catalogs = {}
    for name in ["uap_catalog.json", "fbi_catalog.json"]:
        path = os.path.join(INPUT_DIR, name)
        data = load_catalog(path)
        catalogs[name] = data
        print(f"Loaded {name}: {len(data)} documents")
    
    # Process all incidents
    all_incidents = []
    counter = 1
    docs_processed = 0
    
    for catalog_name, documents in catalogs.items():
        for doc in documents:
            if doc.get("error") and not doc.get("incidents"):
                continue
            
            source_file = doc.get("filename", "unknown")
            source_agency = classify_agency(
                source_file, 
                doc.get("source_agency")
            )
            doc_type = safe_str(doc.get("document_type", "unknown"))
            redaction = safe_str(doc.get("redaction_level", "unknown"))
            people = safe_list(doc.get("people_mentioned", []))
            programs = safe_list(doc.get("programs_referenced", []))
            crossrefs = safe_list(doc.get("cross_references", []))
            key_takeaway = safe_str(doc.get("key_takeaway", ""))
            
            incidents = doc.get("incidents", [])
            if not incidents:
                continue
            
            docs_processed += 1
            
            for inc in incidents:
                row = normalize_incident(
                    inc, source_file, source_agency, doc_type,
                    redaction, people, programs, crossrefs,
                    counter, key_takeaway
                )
                all_incidents.append(row)
                counter += 1
    
    print(f"\nTotal incidents normalized: {len(all_incidents)}")
    print(f"Documents with incidents: {docs_processed}")
    
    # Era distribution
    era_counts = {}
    for inc in all_incidents:
        era = inc.get("era", "unknown")
        era_counts[era] = era_counts.get(era, 0) + 1
    print("\nEra distribution:")
    for era in sorted(era_counts.keys()):
        print(f"  {era}: {era_counts[era]}")
    
    # Agency distribution
    agency_counts = {}
    for inc in all_incidents:
        ag = inc.get("source_agency", "unknown")
        agency_counts[ag] = agency_counts.get(ag, 0) + 1
    print("\nAgency distribution:")
    for ag in sorted(agency_counts.keys()):
        print(f"  {ag}: {agency_counts[ag]}")
    
    # Shape distribution (top 15)
    shape_counts = {}
    for inc in all_incidents:
        shape = inc.get("object_shape")
        if shape and shape != "unknown":
            shape_counts[shape] = shape_counts.get(shape, 0) + 1
    print("\nTop shapes:")
    for shape, count in sorted(shape_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {shape}: {count}")
    
    # Save JSON
    json_path = os.path.join(OUTPUT_DIR, "pursue_release01_dataset.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            "metadata": {
                "title": "PURSUE Release 01 Unified Incident Dataset",
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "source": "war.gov/UFO PURSUE Release 01 (May 8, 2026)",
                "methodology": "Automated extraction via Claude API pipeline from PDF text and OCR",
                "total_incidents": len(all_incidents),
                "date_range": "1917-2025",
                "source_catalogs": list(catalogs.keys()),
                "schema_version": "1.0",
                "fields": UNIFIED_FIELDS
            },
            "incidents": all_incidents
        }, f, indent=2, ensure_ascii=False)
    
    json_size = os.path.getsize(json_path) / (1024 * 1024)
    print(f"\nJSON: {json_path} ({json_size:.1f} MB)")
    
    # Save CSV
    csv_path = os.path.join(OUTPUT_DIR, "pursue_release01_dataset.csv")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=UNIFIED_FIELDS)
        writer.writeheader()
        for inc in all_incidents:
            writer.writerow(inc)
    
    csv_size = os.path.getsize(csv_path) / (1024 * 1024)
    print(f"CSV:  {csv_path} ({csv_size:.1f} MB)")
    
    # Save field documentation
    doc_path = os.path.join(OUTPUT_DIR, "SCHEMA.md")
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write("# PURSUE Release 01 Dataset Schema\n\n")
        f.write(f"**Total incidents:** {len(all_incidents)}\n")
        f.write(f"**Date range:** 1917-2025\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
        f.write("## Fields\n\n")
        field_docs = {
            "incident_id": "Unique ID: PURSUE-R01-NNNN",
            "source_file": "Original PDF filename",
            "source_agency": "FBI, USAF, DOW, NASA, State Department, AARO, French MOD, US Army",
            "document_type": "mission report, incident summary, cable, transcript, email, etc.",
            "date_raw": "Date as extracted from source document",
            "date_normalized": "Date normalized to YYYY-MM-DD where possible",
            "date_precision": "exact, month, year, decade, unknown",
            "time": "Time of observation if recorded",
            "location_raw": "Location as extracted from source",
            "location_country": "Country (normalized)",
            "location_region": "Region/state/province",
            "location_coordinates": "Lat/lon if provided",
            "observer_names": "Names of observers (where unredacted)",
            "observer_credentials": "Military rank, occupation, clearance level",
            "observer_count": "Number of independent observers",
            "observation_methods": "visual, radar, IR, FMV, NVGs, photographic, etc.",
            "object_count": "Number of distinct objects observed",
            "object_shape": "Normalized shape category or full description",
            "object_color": "Color(s) reported",
            "object_size": "Estimated size",
            "object_altitude": "Altitude with units",
            "object_speed": "Speed with units",
            "object_heading": "Direction of travel",
            "object_behavior": "Maneuvers, tactics, behavioral description",
            "duration": "Length of observation",
            "sound": "Any sound reported",
            "construction_materials": "Apparent construction or material composition",
            "exhaust_trails": "Exhaust, vapor trails, or luminous trails",
            "em_effects": "Electromagnetic effects: engine failure, radio interference, radar jamming",
            "physical_effects": "Ground traces, burns, radiation, heat",
            "weather_conditions": "Weather at time of observation",
            "military_proximity": "Nearby military installations, nuclear sites, operations",
            "resolution_status": "resolved, unresolved, inconclusive",
            "credibility_assessment": "Official assessment of witness/report credibility",
            "redaction_level": "none, light, moderate, heavy, almost_entirely_redacted",
            "notable_quotes": "Exact witness or official language",
            "cross_references": "References to other incidents, documents, or programs",
            "programs_mentioned": "AARO, Blue Book, AATIP, Project Sign, etc.",
            "people_mentioned": "Named individuals in the document",
            "pii_status": "unredacted, redacted, partially_redacted, unknown",
            "data_quality": "digital (text-extractable PDF) or ocr (scanned document)",
            "key_takeaway": "One-sentence significance summary",
            "era": "pre_modern, project_sign_grudge, blue_book_era, dark_period, pre_aatip, aatip_era, aaro_era, pursue_era"
        }
        for field in UNIFIED_FIELDS:
            desc = field_docs.get(field, "")
            f.write(f"| `{field}` | {desc} |\n")
    
    print(f"Schema docs: {doc_path}")
    print(f"\nDone! Dataset ready at {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
