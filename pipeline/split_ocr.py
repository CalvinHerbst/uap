import re, os

with open(r'E:\downloads\uap_pdfs\UAP_OCR_SCANNED.md', 'r', encoding='utf-8') as f:
    content = f.read()

out_dir = r'E:\downloads\uap_pdfs\ocr_sections'
os.makedirs(out_dir, exist_ok=True)

sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)

# Priority groups
groups = {
    'PRIORITY_1_incident_summaries': ['38_143685'],
    'PRIORITY_2_flying_discs_1949': ['342_hs1-416511228'],
    'PRIORITY_3_apollo_skylab': ['nasa-uap'],
    'PRIORITY_4_cometa_report': ['255_413270'],
    'PRIORITY_5_german_armament': ['331_120752'],
    'PRIORITY_6_fbi_series': ['65_hs1-834228961'],
    'PRIORITY_7_other': []
}

for s in sections[1:]:
    filename = s.split('\n')[0].replace('## ', '').strip()
    words = len(s.split())
    if words < 20:
        continue
    
    matched = False
    for group_name, patterns in groups.items():
        if group_name == 'PRIORITY_7_other':
            continue
        for pat in patterns:
            if pat in filename:
                group_file = os.path.join(out_dir, f'{group_name}.md')
                with open(group_file, 'a', encoding='utf-8') as f:
                    f.write(f'## {filename}\n\n')
                    body = '\n'.join(s.split('\n')[1:]).strip()
                    f.write(body + '\n\n---\n\n')
                matched = True
                break
    
    if not matched:
        group_file = os.path.join(out_dir, 'PRIORITY_7_other.md')
        with open(group_file, 'a', encoding='utf-8') as f:
            f.write(f'## {filename}\n\n')
            body = '\n'.join(s.split('\n')[1:]).strip()
            f.write(body + '\n\n---\n\n')

print('Created files:')
print('-' * 70)
for f in sorted(os.listdir(out_dir)):
    path = os.path.join(out_dir, f)
    size = os.path.getsize(path)
    with open(path, 'r', encoding='utf-8') as fh:
        words = len(fh.read().split())
    tokens = int(words * 1.3)
    fits = 'FITS in chat' if tokens < 100000 else 'TOO BIG - feed in chunks'
    print(f'  {tokens:>8,} tokens | {f} | {fits}')
