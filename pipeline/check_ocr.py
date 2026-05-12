import re

with open(r'E:\downloads\uap_pdfs\UAP_OCR_SCANNED.md', 'r', encoding='utf-8') as f:
    content = f.read()

sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)

results = []
for s in sections[1:]:
    filename = s.split('\n')[0].replace('## ', '').strip()
    words = len(s.split())
    tokens = int(words * 1.3)
    results.append((tokens, filename, len(s)))

results.sort(key=lambda x: -x[0])

total = sum(r[0] for r in results)
print(f'Total: {total:,} tokens across {len(results)} docs')
print('')
print('   Tokens | Document')
print('-' * 70)
for tokens, filename, chars in results:
    marker = ' <<<' if tokens > 10000 else ''
    print(f'{tokens:>10,} | {filename}{marker}')
