# PURSUE Release 01 Dataset Schema

**Total incidents:** 721
**Date range:** 1917-2025
**Generated:** 2026-05-10T01:54:24.546162

## Fields

| `incident_id` | Unique ID: PURSUE-R01-NNNN |
| `source_file` | Original PDF filename |
| `source_agency` | FBI, USAF, DOW, NASA, State Department, AARO, French MOD, US Army |
| `document_type` | mission report, incident summary, cable, transcript, email, etc. |
| `date_raw` | Date as extracted from source document |
| `date_normalized` | Date normalized to YYYY-MM-DD where possible |
| `date_precision` | exact, month, year, decade, unknown |
| `time` | Time of observation if recorded |
| `location_raw` | Location as extracted from source |
| `location_country` | Country (normalized) |
| `location_region` | Region/state/province |
| `location_coordinates` | Lat/lon if provided |
| `observer_names` | Names of observers (where unredacted) |
| `observer_credentials` | Military rank, occupation, clearance level |
| `observer_count` | Number of independent observers |
| `observation_methods` | visual, radar, IR, FMV, NVGs, photographic, etc. |
| `object_count` | Number of distinct objects observed |
| `object_shape` | Normalized shape category or full description |
| `object_color` | Color(s) reported |
| `object_size` | Estimated size |
| `object_altitude` | Altitude with units |
| `object_speed` | Speed with units |
| `object_heading` | Direction of travel |
| `object_behavior` | Maneuvers, tactics, behavioral description |
| `duration` | Length of observation |
| `sound` | Any sound reported |
| `construction_materials` | Apparent construction or material composition |
| `exhaust_trails` | Exhaust, vapor trails, or luminous trails |
| `em_effects` | Electromagnetic effects: engine failure, radio interference, radar jamming |
| `physical_effects` | Ground traces, burns, radiation, heat |
| `weather_conditions` | Weather at time of observation |
| `military_proximity` | Nearby military installations, nuclear sites, operations |
| `resolution_status` | resolved, unresolved, inconclusive |
| `credibility_assessment` | Official assessment of witness/report credibility |
| `redaction_level` | none, light, moderate, heavy, almost_entirely_redacted |
| `notable_quotes` | Exact witness or official language |
| `cross_references` | References to other incidents, documents, or programs |
| `programs_mentioned` | AARO, Blue Book, AATIP, Project Sign, etc. |
| `people_mentioned` | Named individuals in the document |
| `pii_status` | unredacted, redacted, partially_redacted, unknown |
| `data_quality` | digital (text-extractable PDF) or ocr (scanned document) |
| `key_takeaway` | One-sentence significance summary |
| `era` | pre_modern, project_sign_grudge, blue_book_era, dark_period, pre_aatip, aatip_era, aaro_era, pursue_era |
