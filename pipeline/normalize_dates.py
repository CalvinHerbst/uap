import json, re
with open(r'E:\uap_pdfs\dataset\pursue_release01_dataset.json','r',encoding='utf-8') as f:
    data = json.load(f)

normalized = 0
for inc in data['incidents']:
    raw = inc.get('date_raw','') or ''
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', raw)
    if match:
        inc['date_normalized'] = match.group(0)
        normalized += 1
        continue
    match = re.search(r'(\w+ \d{1,2},?\s*\d{4})', raw)
    if match:
        inc['date_normalized'] = match.group(0)
        normalized += 1

with open(r'E:\uap_pdfs\dataset\pursue_release01_dataset.json','w',encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

total = len(data['incidents'])
print(f'Normalized {normalized} of {total} dates')
