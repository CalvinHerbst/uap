import re

with open(r'E:\uap_pdfs\ocr_sections\PRIORITY_6_fbi_series.md', 'r', encoding='utf-8') as f:
    content = f.read()

sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)

for i, s in enumerate(sections[1:], 1):
    filename = s.split('\n')[0].replace('## ', '').strip()
    words = len(s.split())
    tokens = int(words * 1.3)
    print(f'  Section {i}: {tokens:>8,} tokens | {filename}')

print(f'\nTotal sections: {len(sections)-1}')
print(f'Average: {sum(len(s.split()) for s in sections[1:]) * 1.3 / max(len(sections)-1,1):,.0f} tokens each')
