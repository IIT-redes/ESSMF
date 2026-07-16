from pathlib import Path
from bs4 import BeautifulSoup
import sys, yaml, re
ROOT=Path(__file__).resolve().parents[1]
TARGET=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'dist'
errors=[]
for p in TARGET.rglob('*.html'):
    s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    ids={x.get('id') for x in s.select('[id]')}
    for a in s.select('a[href]'):
        href=a.get('href','')
        if href.startswith('#') and len(href)>1 and href[1:] not in ids: errors.append(f'{p.relative_to(TARGET)}: missing anchor {href}')
        if href.startswith(('http://','https://','mailto:','javascript:','#')) or not href: continue
        base=href.split('#',1)[0].split('?',1)[0]
        if not base: continue
        dest=(p.parent/base).resolve()
        try: dest.relative_to(TARGET.resolve())
        except ValueError: continue
        if not dest.exists(): errors.append(f'{p.relative_to(TARGET)}: missing local link {href}')
for y in (ROOT/'content').rglob('*.yml'):
    try: yaml.safe_load(y.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'{y.relative_to(ROOT)}: invalid YAML: {e}')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'Validation passed: {TARGET}')
