from pathlib import Path
import yaml, re

root=Path('/mnt/data/site_v19_work')
P=root/'content/pillars'

TR_FILE='docs/materials/tmf-tso-dso-coordination-energies-2023.pdf'
ON_FILE='docs/materials/onenet-d11-2-techno-economic-assessment.pdf'

def ref(label,file,page):
    return {'label':label,'file':file,'page':page}

maps={
 'market-architecture.yml':{
   'default':[ref('Troncia et al. (2023), §2.1',TR_FILE,4)],
   'Gate Opening Time (GOT)':[ref('OneNet D11.2, §5.1.1',ON_FILE,58)],
   'Gate Closure Time (GCT)':[ref('OneNet D11.2, §5.1.1',ON_FILE,58)],
   'Market Time Unit (MTU)':[ref('OneNet D11.2, §5.1.1',ON_FILE,58)],
   'Type of product':[ref('Troncia et al. (2023), §2.1',TR_FILE,4),ref('OneNet D11.2, §5.1.1',ON_FILE,58)],
   'Technical requirements':[ref('OneNet D11.2, §5.1.1',ON_FILE,58)],
   'Allowed technologies':[ref('OneNet D11.2, §5.1.1',ON_FILE,58)],
   'Aggregation method':[ref('OneNet D11.2, §5.1.1',ON_FILE,58)],
   'Aggregation mix allowed':[ref('OneNet D11.2, §5.1.1',ON_FILE,58)],
 },
 'sub-market-coordination.yml':{
   'default':[ref('Troncia et al. (2023), §2.2',TR_FILE,5),ref('OneNet D11.2, §5.1.2',ON_FILE,61)]
 },
 'market-optimization.yml':{
   'default':[ref('Troncia et al. (2023), §2.3',TR_FILE,5),ref('OneNet D11.2, §5.1.3',ON_FILE,61)]
 },
 'market-operation.yml':{
   'default':[ref('Troncia et al. (2023), §2.4',TR_FILE,6)],
   'Minimum bid size':[ref('OneNet D11.2, §5.1.4',ON_FILE,62)],
   'Bid structure':[ref('OneNet D11.2, §5.1.4',ON_FILE,62)],
 },
 'network-representation.yml':{
   'default':[ref('Troncia et al. (2023), §2.5',TR_FILE,7),ref('OneNet D11.2, §5.1.5',ON_FILE,64)]
 },
}

for fname, smap in maps.items():
    path=P/fname
    d=yaml.safe_load(path.read_text())
    d['feature_matrix_intro']='Use the table as a compact terminology and data-entry guide. The final column links each definition to its source section; open the cited page or download the full source PDF.'
    for row in d.get('feature_matrix',[]):
        row['references']=smap.get(row.get('subfeature')) or smap.get('default',[])
    path.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=110), encoding='utf-8')

# Patch build.py feature matrix output.
bp=root/'scripts/build.py'
s=bp.read_text(encoding='utf-8')
old="""                for label in ['Feature','Sub-feature / decision','Data type','Definition','How to read the choice']:\n                    th=s.new_tag('th'); th.string=label; tr.append(th)\n                thead.append(tr)\n        body=s.select_one('.feature-matrix-body')\n        if body:\n            body.clear()\n            for row in d.get('feature_matrix',[]):\n                tr=s.new_tag('tr')\n                for key in ['feature','subfeature','datatype','definition','meaning']:\n                    td=s.new_tag('td'); td.string=row.get(key,''); tr.append(td)\n                body.append(tr)\n"""
new="""                for label in ['Feature','Sub-feature / decision','Data type','Definition','How to read the choice','Definition source']:\n                    th=s.new_tag('th'); th.string=label; tr.append(th)\n                thead.append(tr)\n        body=s.select_one('.feature-matrix-body')\n        if body:\n            body.clear()\n            for row in d.get('feature_matrix',[]):\n                tr=s.new_tag('tr')\n                for key in ['feature','subfeature','datatype','definition','meaning']:\n                    td=s.new_tag('td'); td.string=row.get(key,''); tr.append(td)\n                src_td=s.new_tag('td',attrs={'class':'definition-source-cell'})\n                refs=row.get('references',[]) or []\n                for i,ref in enumerate(refs):\n                    block=s.new_tag('div',attrs={'class':'definition-reference'})\n                    label=s.new_tag('span',attrs={'class':'definition-reference-label'}); label.string=ref.get('label','Source'); block.append(label)\n                    actions=s.new_tag('span',attrs={'class':'definition-reference-actions'})\n                    f=ref.get('file','')\n                    if f:\n                        href='../'+f.lstrip('/')\n                        p=ref.get('page')\n                        open_a=s.new_tag('a',attrs={'href': href + (f'#page={p}' if p else ''),'target':'_blank','rel':'noopener'}); open_a.string='Open'; actions.append(open_a)\n                        dl=s.new_tag('a',attrs={'href':href,'download':''}); dl.string='Download'; actions.append(dl)\n                    block.append(actions); src_td.append(block)\n                tr.append(src_td)\n                body.append(tr)\n"""
if old not in s:
    raise SystemExit('build.py target block not found')
s=s.replace(old,new,1)
bp.write_text(s,encoding='utf-8')

# Patch Pages CMS schema for row references.
pp=root/'.pages.yml'
s=pp.read_text(encoding='utf-8')
old="""                      - { name: definition, type: text }\n                      - { name: meaning, type: text }\n"""
new="""                      - { name: definition, type: text }\n                      - { name: meaning, type: text }\n                      - name: references\n                        label: Definition references\n                        type: object\n                        list: true\n                        fields:\n                          - { name: label, type: string }\n                          - { name: file, type: string }\n                          - { name: page, type: number }\n"""
if old not in s:
    raise SystemExit('.pages.yml target block not found')
s=s.replace(old,new,1)
pp.write_text(s,encoding='utf-8')

# CSS in source and root asset copies.
css_add='''\n/* v19 — row-level definition references */\n.feature-matrix-table{min-width:1320px}\n.feature-matrix-table td:first-child{width:12%}\n.feature-matrix-table td:nth-child(2){width:15%}\n.feature-matrix-table td:nth-child(3){width:13%}\n.feature-matrix-table td:nth-child(4){width:22%}\n.feature-matrix-table td:nth-child(5){width:20%}\n.feature-matrix-table td:nth-child(6){width:18%}\n.definition-source-cell{min-width:205px}\n.definition-reference{display:flex;flex-direction:column;gap:6px;padding:2px 0 8px}\n.definition-reference+.definition-reference{border-top:1px solid #dbe8f1;padding-top:9px}\n.definition-reference-label{font-weight:750;color:#264f6f;line-height:1.35}\n.definition-reference-actions{display:flex;gap:8px;flex-wrap:wrap}\n.definition-reference-actions a{display:inline-flex;align-items:center;padding:4px 9px;border-radius:999px;border:1px solid #c9ddea;background:#f7fbfe;color:#0b5f8f;font-weight:750;font-size:.78rem;text-decoration:none}\n.definition-reference-actions a:hover{background:#eaf5fb;border-color:#9dc8dd}\n@media(max-width:680px){.feature-matrix-table{min-width:1240px}}\n'''
for cp in [root/'site_src/assets/interactive-tmf.css', root/'assets/interactive-tmf.css']:
    cs=cp.read_text(encoding='utf-8')
    if '/* v19 — row-level definition references */' not in cs:
        cp.write_text(cs+'\n'+css_add,encoding='utf-8')

# Version note
(root/'WEBSITE_REVISION_NOTES_V19.md').write_text('''# Website revision v19\n\n- Added a **Definition source** column to the terminology/data-type table on all five pillar pages.\n- Each definition now links to the source section used for that terminology.\n- **Open** jumps to the cited page in the local PDF; **Download** downloads the full source PDF.\n- Architecture timing and other OneNet-added sub-features point to OneNet D11.2; foundational pillar definitions point to Troncia et al. (2023), with both sources shown where appropriate.\n- Added editable reference metadata to Pages CMS.\n- Website structure, feedback logic, and navigation remain unchanged.\n''',encoding='utf-8')
(root/'VERSION.txt').write_text('v19\n',encoding='utf-8')
