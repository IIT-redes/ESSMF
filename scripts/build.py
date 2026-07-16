from __future__ import annotations
from pathlib import Path
from bs4 import BeautifulSoup
import shutil, yaml, json, re

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'site_src'; CONTENT=ROOT/'content'; DIST=ROOT/'dist'

def load(path): return yaml.safe_load((CONTENT/path).read_text(encoding='utf-8'))
def text(el): return el.get_text(' ',strip=True) if el else ''
def set_text(el,value):
    if el is not None and value is not None: el.clear(); el.append(str(value))
def save(soup,path): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(str(soup),encoding='utf-8')
def asset_path(value, depth=0):
    if not value: return value
    v=str(value).replace('\\','/').lstrip('/')
    if v.startswith('site_src/'): v=v[len('site_src/'):]
    if v.startswith('../'): return v
    if v.startswith('assets/') or v.startswith('docs/'):
        return ('../'*depth)+v
    return v

def section_patch(sec,data):
    if not sec or not data: return
    head=sec.select_one('.section-heading') or sec
    set_text(head.select_one('.eyebrow'),data.get('eyebrow'))
    set_text(head.find(['h1','h2']),data.get('title'))
    ps=[p for p in head.find_all('p',recursive=False) if 'eyebrow' not in (p.get('class') or [])]
    if ps and data.get('text') is not None: set_text(ps[0],data.get('text'))

def patch_home():
    d=load('home.yml'); lib=load('library.yml')
    p=SRC/'index.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    h=s.select_one('.hero-copy'); hd=d['hero']
    set_text(h.select_one('.eyebrow'),hd['eyebrow']); set_text(h.find('h1'),hd['title']); set_text(h.select_one('.landing-philosophy-line'),hd['philosophy']); set_text(h.select_one('.lead'),hd['lead']); set_text(h.select_one('.landing-invitation'),hd['invitation']); set_text(h.select_one('.button.primary'),hd['primary_button']); set_text(h.select_one('.button.ghost'),hd['secondary_button'])
    section_patch(s.select_one('#mechanism-road'),d['road_intro'])
    for el,item in zip(s.select('#mechanism-road .road-turn'),d['road_turns']):
        set_text(el.select_one('.road-marker'),item['number']); set_text(el.select_one('.road-kicker'),item['kicker']); set_text(el.find('h3'),item['title'])
        ps=[x for x in el.find_all('p') if 'road-kicker' not in (x.get('class') or [])]
        if ps: set_text(ps[0],item['text'])
        if el.name=='a' and item.get('href'): el['href']=item['href']
    section_patch(s.select_one('#philosophy'),d['focus_intro'])
    for el,item in zip(s.select('#philosophy .focus-card'),d['focus_cards']): set_text(el.find('span'),item['badge']); set_text(el.find('h3'),item['title']); set_text(el.find('p'),item['text'])
    call=s.select_one('#philosophy .interaction-callout'); set_text(call.find('h3'),d['interaction_callout']['title']); set_text(call.find('p'),d['interaction_callout']['text'])
    section_patch(s.select_one('#mechanisms'),d['mechanisms_intro'])
    for el,item in zip(s.select('#mechanisms .mechanism-card'),d['mechanism_cards']):
        el['href']=item['href']; img=el.find('img');
        if img: img['src']=asset_path(item['image'],0)
        set_text(el.select_one('.mechanism-badge'),item['badge']); set_text(el.find('h3'),item['title']); set_text(el.find('p'),item['summary']); set_text(el.find('small'),item['link_label'])
        ul=el.select_one('.dimension-preview');
        if ul:
            ul.clear()
            for x in item['dimensions']:
                li=s.new_tag('li'); li.string=x; ul.append(li)
    inv=s.select_one('.expert-invitation-card'); iv=d['expert_invitation']; set_text(inv.select_one('.eyebrow'),iv['eyebrow']); set_text(inv.find('h2'),iv['title']); set_text(inv.find('p'),iv['text']); set_text(inv.select_one('.button'),iv['button'])
    box=inv.select_one('.invitation-steps'); box.clear()
    for x in iv['steps']:
        span=s.new_tag('span'); span.string=x; box.append(span)
    res=s.select_one('#resources'); section_patch(res,lib['intro']); grid=res.select_one('.resource-grid'); grid.clear()
    for item in lib['items']:
        a=s.new_tag('a',attrs={'class':'pdf-card hover-lift','href':item['file'],'target':'_blank','rel':'noopener'})
        sp=s.new_tag('span',attrs={'class':'pdf-icon'}); sp.string='PDF'; a.append(sp)
        st=s.new_tag('strong'); st.string=item['title']; a.append(st)
        em=s.new_tag('em'); em.string=item['description']; a.append(em)
        sm=s.new_tag('small'); sm.string=item.get('link_label','Open document →'); a.append(sm); grid.append(a)
    save(s,DIST/'index.html')

def patch_team():
    d=load('team.yml'); p=SRC/'pages/who-we-are.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    set_text(s.select_one('.team-hero .eyebrow'),d['eyebrow']); set_text(s.select_one('.team-hero h1'),d['title']); set_text(s.select_one('.team-hero p:not(.eyebrow)'),d['intro'])
    cards=s.select('.team-card')
    for el,item in zip(cards,d['members']):
        set_text(el.select_one('.team-photo'),item['initials']); set_text(el.find('h2'),item['name']); set_text(el.select_one('.team-role'),item['role']); set_text(el.select_one('.team-program'),item['program']); set_text(el.find('p'),item['bio']); a=el.select_one('.team-email'); a['href']='mailto:'+item['email']; set_text(a,item['email'])
    img=s.select_one('.team-strip-reference img');
    if img: img['src']=asset_path(d.get('team_image',''),1)
    save(s,DIST/'pages/who-we-are.html')

def patch_work():
    d=load('work.yml'); p=SRC/'pages/our-work.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser'); set_text(s.select_one('.team-hero .eyebrow'),d['eyebrow']); set_text(s.select_one('.team-hero h1'),d['title'])
    host=s.select_one('.work-placeholder')
    if host: host.clear(); q=s.new_tag('p'); q.string=d.get('intro',''); host.append(q)
    save(s,DIST/'pages/our-work.html')

def patch_mechanism(key):
    d=load(f'mechanisms/{key}.yml'); p=SRC/'pages'/d['file']; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser'); h=s.select_one('.mechanism-page-hero'); hd=d['hero']
    set_text(h.select_one('.eyebrow'),hd['eyebrow']); set_text(h.find('h1'),hd['title']); set_text(h.select_one('.mechanism-philosophy-line'),hd['philosophy']); set_text(h.select_one('.lead'),hd['lead']); set_text(h.select_one('.button.primary'),hd['primary_button']); set_text(h.select_one('.button.ghost'),hd['secondary_button'])
    for sid in ['overview','idea','why','who','framework']:
        if sid in d['sections']: section_patch(s.select_one('#'+sid),d['sections'][sid])
    who=d['sections'].get('who',{}); sec=s.select_one('#who'); cols=sec.select('.split-layout > div') if sec else []
    if len(cols)>=2:
        set_text(cols[1].find('h2'),who.get('where_title')); ps=[p for p in cols[1].find_all('p') if 'eyebrow' not in (p.get('class') or [])];
        if ps: set_text(ps[0],who.get('where_text'))
    for el,item in zip(s.select('#framework .dimension-card'),d['dimensions']):
        el['href']=item['href']; el['id']=item['id']; set_text(el.find('span'),item['number']); set_text(el.find('h3'),item['title']); set_text(el.find('p'),item['summary']); set_text(el.find('small'),item['link_label'])
    for el,item in zip(s.select('.visual-card'),d.get('visual_cards',[])):
        set_text(el.find('h3'),item['title']); set_text(el.find('p'),item['text']); img=el.find('img');
        if img and item.get('image'): img['src']=asset_path(item['image'],1)
    section_patch(s.select_one('#feedback'),d['feedback']); section_patch(s.select_one('.interaction-zone'),d['challenge_intro'])
    for el,item in zip(s.select('.interaction-zone .challenge-card'),d['challenges']):
        el['id']=item['id']; set_text(el.find('h3'),item['title']); set_text(el.select_one('.challenge-question'),item['question']); ul=el.find('ul');
        if ul:
            ul.clear()
            for x in item['prompts']:
                li=s.new_tag('li'); li.string=x; ul.append(li)
    section_patch(s.select_one('#final-feedback'),d['final_feedback'])
    save(s,DIST/'pages'/d['file'])

def patch_tmf():
    d=load('mechanisms/tmf.yml'); p=SRC/'pages/theoretical-market-framework.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser'); h=s.select_one('.hero-copy'); hd=d['hero']; set_text(h.find('h1'),hd['title']); set_text(h.select_one('.statement'),hd['statement']); set_text(h.select_one('.lead'),hd['lead']); set_text(h.select_one('.button.primary'),hd['primary_button']); set_text(h.select_one('.button.ghost'),hd['secondary_button'])
    for sid,data in d['sections'].items(): section_patch(s.select_one('#'+sid),data)
    for item in d['pillars']:
        sec=s.select_one('#'+item['id']); set_text(sec.select_one('.eyebrow'),item['eyebrow']); set_text(sec.find('h2'),item['title']); ps=[p for p in sec.find_all('p') if 'eyebrow' not in (p.get('class') or [])];
        if ps: set_text(ps[0],item['summary'])
    save(s,DIST/'pages/theoretical-market-framework.html')

def patch_dimensions():
    for y in sorted((CONTENT/'dimensions').glob('*.yml')):
        d=yaml.safe_load(y.read_text(encoding='utf-8')); p=SRC/'pages'/d['file']; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser'); h=s.select_one('.dimension-detail-hero'); h['style']=f"--dimension-hero:url('{asset_path(d['hero_image'],1)}')"; set_text(h.select_one('.eyebrow'),d['eyebrow']); set_text(h.find('h1'),d['title']); set_text(h.select_one('.lead'),d['subtitle'])
        intro=s.select_one('#meaning'); set_text(intro.find('h2'),d['definition_title']); ps=intro.select('.dimension-explainer')
        for el,val in zip(ps,d['definition_paragraphs']): set_text(el,val)
        for el,item in zip(s.select('.dimension-choice-card'),d['choices']): set_text(el.find('h3'),item['title']); set_text(el.find('p'),item['text'])
        pr=s.select_one('.framework-zone'); set_text(pr.find('h2'),d['example_title']); set_text(pr.select_one('.dimension-explainer'),d['example_text']); set_text(pr.select_one('.dimension-review-principle p'),d['review_principle'])
        for el,item in zip(s.select('.stakeholder-implication'),d['stakeholders']): set_text(el.find('h3'),item['name']); set_text(el.find('p'),item['text'])
        cols=s.select('.interaction-zone .split-layout > div')
        for idx,vals in enumerate([d['questions'],d['evidence']]):
            if idx<len(cols):
                ul=cols[idx].find('ul'); ul.clear()
                for x in vals:
                    li=s.new_tag('li'); li.string=x; ul.append(li)
        fb=s.select_one('#dimension-feedback'); set_text(fb.select_one('.eyebrow'),d['feedback_eyebrow']); set_text(fb.find('h2'),d['feedback_title']); ps=[p for p in fb.find_all('p') if 'eyebrow' not in (p.get('class') or [])];
        if ps: set_text(ps[0],d['feedback_text'])
        save(s,DIST/'pages'/d['file'])

def patch_pillars():
    for y in sorted((CONTENT/'pillars').glob('*.yml')):
        d=yaml.safe_load(y.read_text(encoding='utf-8')); p=SRC/'pages'/d['file']; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser'); h=s.select_one('.detail-hero'); set_text(h.select_one('.eyebrow'),d['eyebrow']); set_text(h.find('h1'),d['title']); ps=[p for p in h.find_all('p') if 'eyebrow' not in (p.get('class') or [])];
        if ps: set_text(ps[0],d['subtitle'])
        for el,item in zip(s.select('.detail-card'),d['cards']):
            set_text(el.find('h2') or el.find('h3'),item['title']); set_text(el.find('p'),item['text']); ul=el.find('ul')
            if ul and item.get('items'):
                ul.clear()
                for x in item['items']:
                    li=s.new_tag('li'); li.string=x; ul.append(li)
        save(s,DIST/'pages'/d['file'])

def build_feedback_config():
    d=load('feedback.yml'); obj={'githubHubUrl':d['general']['github_hub_url'],'pollUrl':d['general']['poll_url'],'uploadUrl':d['general']['upload_url'],'generalFeedbackUrl':d['general']['general_feedback_url']}
    obj['feedbackPages']={x['key']:{'label':x['label'],'googleFormUrl':x['form_url'],'giscusTerm':x['giscus_term'],'giscusCategory':x.get('giscus_category',''),'giscusCategoryId':x.get('giscus_category_id','')} for x in d['dimension_pages']}
    obj['mechanisms']={x['key']:{'label':x['label'],'googleFormUrl':x['form_url'],'giscusTerm':x['giscus_term'],'giscusCategory':x.get('giscus_category',''),'giscusCategoryId':x.get('giscus_category_id','')} for x in d['mechanisms']}
    obj['sections']={x['key']:{'label':x['label'],'googleFormUrl':x['form_url'],'giscusTerm':x['giscus_term']} for x in d['tmf_sections']}
    g=d['giscus']; obj['giscus']={'enabled':bool(g['enabled']),'repo':g['repo'],'repoId':g['repo_id'],'category':g['category'],'categoryId':g['category_id'],'theme':g['theme'],'lang':g['lang']}
    (DIST/'assets/feedback-config.js').write_text('window.TMF_FEEDBACK_CONFIG = '+json.dumps(obj,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    shutil.copytree(SRC,DIST)
    patch_home(); patch_team(); patch_work(); patch_mechanism('tariff'); patch_mechanism('connection'); patch_tmf(); patch_dimensions(); patch_pillars(); build_feedback_config()
    print(f'Built site at {DIST}')
if __name__=='__main__': main()
