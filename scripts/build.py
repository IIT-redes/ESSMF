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
def replace_visible_tmf(soup):
    # User-facing text spells out Theoretical Market Framework. Internal IDs, file paths,
    # and Giscus discussion terms are intentionally left unchanged for compatibility.
    for node in list(soup.find_all(string=True)):
        if node.parent and node.parent.name in ('script','style'):
            continue
        value=str(node)
        if re.search(r'\bTMF\b', value):
            node.replace_with(re.sub(r'\bTMF\b','Theoretical Market Framework',value))
    for tag in soup.find_all(True):
        for attr in ('alt','title','aria-label'):
            if tag.has_attr(attr) and isinstance(tag.get(attr), str):
                tag[attr]=re.sub(r'\bTMF\b','Theoretical Market Framework',tag[attr])

def save(soup,path):
    replace_visible_tmf(soup)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(str(soup),encoding='utf-8')
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


def add_or_update_download_button(soup, actions, href, label):
    # v5: the worksheet is shown once in the dedicated pillar worksheet card below.
    # Remove any legacy inline duplicate beside the feedback icons.
    if actions:
        for old in actions.select('.worksheet-inline-link'):
            old.decompose()

def make_pillar_table_preview(soup, pd, depth=1):
    if not pd: return None
    preview=pd.get('preview_image',''); word=pd.get('download_file',''); pdf=pd.get('pdf_file','')
    if not (preview or word or pdf): return None
    card=soup.new_tag('article', attrs={'class':'pillar-worksheet-preview reveal'})
    copy=soup.new_tag('div', attrs={'class':'pillar-worksheet-copy'})
    h=soup.new_tag('h3'); h.string=pd.get('worksheet_title','Ready-to-fill Theoretical Market Framework mapping table'); copy.append(h)
    p=soup.new_tag('p'); p.string=pd.get('worksheet_text','Use this blank table to map your own market using the same pillar structure.'); copy.append(p)
    links=soup.new_tag('div', attrs={'class':'worksheet-preview-links'})
    if word:
        a=soup.new_tag('a', attrs={'class':'button primary','href':asset_path(word,depth),'download':''}); a.string='Download editable Word table'; links.append(a)
    if pdf:
        a=soup.new_tag('a', attrs={'class':'button ghost','href':asset_path(pdf,depth),'target':'_blank','rel':'noopener'}); a.string=pd.get('pdf_label','Open blank PDF'); links.append(a)
    copy.append(links); card.append(copy)
    if preview:
        fig=soup.new_tag('figure', attrs={'class':'pillar-worksheet-figure'})
        a=soup.new_tag('a', attrs={'href':asset_path(pdf or preview,depth),'target':'_blank','rel':'noopener'})
        img=soup.new_tag('img', attrs={'src':asset_path(preview,depth),'alt':pd.get('preview_alt','Blank Theoretical Market Framework pillar table')})
        a.append(img); fig.append(a)
        cap=soup.new_tag('figcaption'); cap.string='Blank table supplied for expert mapping. Click to open the full-size template.'; fig.append(cap)
        card.append(fig)
    return card

def add_or_update_spain_mapping_table(soup, sec, sp):
    if not sec: return
    for old in sec.select('.spain-mapping-card'):
        old.decompose()
    rows=sp.get('mapping_rows',[]) if sp else []
    if not rows: return
    host=sec.select_one('.spain-example-side') or sec
    card=soup.new_tag('div', attrs={'class':'spain-mapping-card'})
    h=soup.new_tag('h3'); h.string=sp.get('mapping_title','From table entries to the figure'); card.append(h)
    wrap=soup.new_tag('div', attrs={'class':'spain-mapping-table-wrap'})
    table=soup.new_tag('table', attrs={'class':'spain-mapping-table'})
    thead=soup.new_tag('thead'); tr=soup.new_tag('tr')
    for label in ['Filled Theoretical Market Framework table input','What it determines','Visible result in the case figure']:
        th=soup.new_tag('th'); th.string=label; tr.append(th)
    thead.append(tr); table.append(thead)
    tbody=soup.new_tag('tbody')
    for row in rows:
        tr=soup.new_tag('tr')
        for key in ['table_input','determines','figure_output']:
            td=soup.new_tag('td'); td.string=row.get(key,''); tr.append(td)
        tbody.append(tr)
    table.append(tbody); wrap.append(table); card.append(wrap)
    note=soup.new_tag('p', attrs={'class':'spain-source-note'}); note.string=sp.get('source_note',''); card.append(note)
    downloads=host.select_one('.spain-example-downloads')
    if downloads: downloads.insert_before(card)
    else: host.append(card)


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
        sp=s.new_tag('span',attrs={'class':'pdf-icon'}); sp.string=('DOCX' if str(item.get('file','')).lower().endswith('.docx') else 'PDF'); a.append(sp)
        st=s.new_tag('strong'); st.string=item['title']; a.append(st)
        em=s.new_tag('em'); em.string=item['description']; a.append(em)
        sm=s.new_tag('small'); sm.string=item.get('link_label','Open document →'); a.append(sm); grid.append(a)
    save(s,DIST/'index.html')

def patch_team():
    d=load('team.yml'); p=SRC/'pages/who-we-are.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    set_text(s.select_one('.team-hero .eyebrow'),d['eyebrow']); set_text(s.select_one('.team-hero h1'),d['title']); set_text(s.select_one('.team-hero p:not(.eyebrow)'),d['intro'])
    grid=s.select_one('.team-grid')
    if grid:
        grid.clear()
        for item in d.get('members',[]):
            el=s.new_tag('article',attrs={'class':'team-card reveal'})
            photo=s.new_tag('div',attrs={'class':'team-photo'})
            fallback=s.new_tag('span',attrs={'class':'team-photo-fallback'}); fallback.string=item.get('initials',''); photo.append(fallback)
            if item.get('photo_url'):
                img=s.new_tag('img',attrs={'src':item['photo_url'],'alt':item.get('name',''),'loading':'lazy','referrerpolicy':'no-referrer'})
                img['onerror']="this.style.display='none'"
                photo.append(img)
            el.append(photo)
            h2=s.new_tag('h2'); name=s.new_tag('a',attrs={'class':'team-name-link','href':item.get('profile_url','#'),'target':'_blank','rel':'noopener'}); name.string=item.get('name',''); h2.append(name); el.append(h2)
            role=s.new_tag('div',attrs={'class':'team-role'}); role.string=item.get('role',''); el.append(role)
            prog=s.new_tag('div',attrs={'class':'team-program'}); prog.string=item.get('program',''); el.append(prog)
            bio=s.new_tag('p'); bio.string=item.get('bio',''); el.append(bio)
            if item.get('email'):
                mail=s.new_tag('a',attrs={'class':'team-email','href':'mailto:'+item['email']}); mail.string=item['email']; el.append(mail)
            grid.append(el)
    strip=s.select_one('.team-strip-reference')
    if strip:
        if d.get('team_image'):
            img=strip.find('img');
            if img: img['src']=asset_path(d.get('team_image',''),1)
        else:
            strip.decompose()
    save(s,DIST/'pages/who-we-are.html')

def patch_work():
    d=load('work.yml'); p=SRC/'pages/our-work.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    set_text(s.select_one('.team-hero .eyebrow'),d['eyebrow']); set_text(s.select_one('.team-hero h1'),d['title'])
    host=s.select_one('.work-placeholder, .work-experience')
    if host:
        host.clear(); host['class']=['work-experience']
        q=s.new_tag('p',attrs={'class':'work-intro'}); q.string=d.get('intro',''); host.append(q)
        note=s.new_tag('p',attrs={'class':'work-source-note'}); note.string='Selected experience verified against public IIT researcher profiles and European Commission CORDIS project records.'; host.append(note)
        grid=s.new_tag('div',attrs={'class':'eu-project-grid'})
        for item in d.get('projects',[]):
            card=s.new_tag('article',attrs={'class':'eu-project-card reveal'})
            top=s.new_tag('div',attrs={'class':'eu-project-top'})
            ac=s.new_tag('span',attrs={'class':'project-acronym'}); ac.string=item.get('acronym',''); top.append(ac)
            pg=s.new_tag('span',attrs={'class':'project-programme'}); pg.string=item.get('programme',''); top.append(pg); card.append(top)
            h2=s.new_tag('h2'); a=s.new_tag('a',attrs={'href':item.get('url','#'),'target':'_blank','rel':'noopener'}); a.string=item.get('title',''); h2.append(a); card.append(h2)
            details=s.new_tag('div',attrs={'class':'project-details'}); details.string=f"Grant {item.get('grant','')} · {item.get('period','')}"; card.append(details)
            ppl=s.new_tag('p',attrs={'class':'project-people'}); ppl.string='Team experience: '+item.get('people',''); card.append(ppl)
            desc=s.new_tag('p'); desc.string=item.get('relevance',''); card.append(desc)
            link=s.new_tag('a',attrs={'class':'project-source-link','href':item.get('url','#'),'target':'_blank','rel':'noopener'}); link.string='European Commission project record →'; card.append(link)
            grid.append(card)
        host.append(grid)
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
    d=load('mechanisms/tmf.yml'); feedback=load('feedback.yml'); feedback_map={x['key']:x for x in feedback.get('tmf_sections',[])}
    p=SRC/'pages/theoretical-market-framework.html'; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    h=s.select_one('.hero-copy'); hd=d['hero']; set_text(h.find('h1'),hd['title']); set_text(h.select_one('.statement'),hd['statement']); set_text(h.select_one('.lead'),hd['lead']); set_text(h.select_one('.button.primary'),hd['primary_button']); set_text(h.select_one('.button.ghost'),hd['secondary_button'])
    for sid,data in d['sections'].items(): section_patch(s.select_one('#'+sid),data)
    for item in d['pillars']:
        sec=s.select_one('#'+item['id'])
        if not sec: continue
        set_text(sec.select_one('.eyebrow'),item['eyebrow']); h2=sec.find('h2'); set_text(h2.find('a') if h2 and h2.find('a') else h2,item['title'])
        ps=[p for p in sec.find_all('p') if 'eyebrow' not in (p.get('class') or [])]
        if ps: set_text(ps[0],item['summary'])
        try:
            pd=yaml.safe_load((CONTENT/'pillars'/f"{item['id']}.yml").read_text(encoding='utf-8'))
        except Exception:
            pd={}
        # v15: main page is a concise gateway. The full questionnaire and Giscus live on the pillar sub-page.
        qbox=sec.select_one('.pillar-review-question')
        if qbox:
            qbox.clear()
            strong=s.new_tag('strong'); strong.string='Review this pillar in context'; qbox.append(strong)
            ptxt=s.new_tag('p'); ptxt.string='Read the definitions and data-entry table first, then leave your feedback on the pillar page.'; qbox.append(ptxt)
            a=s.new_tag('a',attrs={'class':'button primary pillar-feedback-gateway','href':f"{pd.get('file',item['id']+'.html')}#pillar-feedback"})
            a.string='Leave feedback'; qbox.append(a)
        # Main page no longer hosts discussion widgets or the three feedback controls.
        for box in sec.select('.comments-box'): box.decompose()
        for old in sec.select('.pillar-worksheet-preview'):
            old.decompose()
    ex=d.get('sections',{}).get('case-example',{})
    sec=s.select_one('#case-example')
    if sec and ex:
        set_text(sec.select_one('.section-heading .eyebrow'),ex.get('eyebrow'))
        set_text(sec.select_one('.section-heading h2'),ex.get('title'))
        p0=sec.select_one('.section-heading p:not(.eyebrow)'); set_text(p0,ex.get('text'))
        sp=d.get('case_example',{})
        img=sec.select_one('.spain-example-figure img') or sec.select_one('.case-example-figure img')
        if img and sp.get('image'):
            img['src']=asset_path(sp.get('image'),1); img['alt']=sp.get('image_alt','Illustrative case market structure')
        set_text(sec.select_one('figcaption'),sp.get('image_caption'))
        set_text(sec.select_one('.spain-example-explanation h3') or sec.select_one('.case-example-explanation h3'),sp.get('explanation_title'))
        exhost=sec.select_one('.spain-example-explanation') or sec.select_one('.case-example-explanation')
        intro = exhost.select_one('.example-intro') if exhost else None
        if not intro and exhost:
            host = exhost.find('h3')
            if host:
                intro = s.new_tag('p', attrs={'class':'example-intro'}); host.insert_after(intro)
        set_text(intro, sp.get('explanation_intro'))
        ol=exhost.find('ol') if exhost else None
        if ol:
            ol.clear()
            for x in sp.get('explanation_points',[]):
                li=s.new_tag('li'); li.string=x; ol.append(li)
        downloads=sec.select_one('.spain-example-downloads') or sec.select_one('.case-example-downloads')
        if downloads:
            set_text(downloads.find('h3'),sp.get('downloads_title'))
            grid=downloads.select_one('.download-card-grid')
            if grid:
                grid.clear()
                for dl in sp.get('downloads',[]):
                    a=s.new_tag('a',attrs={'class':'download-card hover-lift','href':asset_path(dl.get('file',''),1)})
                    if str(dl.get('file','')).lower().endswith(('.docx','.png','.pdf')): a['download']=''
                    st=s.new_tag('strong'); st.string=dl.get('title',''); a.append(st)
                    em=s.new_tag('em'); em.string=dl.get('description',''); a.append(em)
                    sm=s.new_tag('small'); sm.string=dl.get('label','Download'); a.append(sm)
                    grid.append(a)
        add_or_update_spain_mapping_table(s, sec, sp)

    # Remove explicit source-document cards requested for the public framework page.
    for card in list(s.select('#resources a.pdf-card')):
        href=str(card.get('href','')).lower()
        if ('onenet-' in href) or ('tmf-tso-dso-coordination-energies-2023.pdf' in href):
            card.decompose()

    # General comments use the same Giscus repository/category, but a dedicated discussion term.
    general_term=feedback.get('general',{}).get('general_giscus_term','Theoretical Market Framework — General comments')
    final_sec=s.select_one('#final-feedback')
    if final_sec:
        old=final_sec.select_one('.general-feedback-link')
        if old:
            btn=s.new_tag('button',attrs={'class':'button primary load-comments general-comments-discussion','type':'button','aria-expanded':'false','data-giscus-term':general_term})
            btn.string='Leave general comments'
            old.replace_with(btn)
        if not final_sec.select_one('.comments-box.general-comments-box'):
            box=s.new_tag('div',attrs={'class':'comments-box general-comments-box','aria-live':'polite','id':'comments-general-framework'})
            final_sec.append(box)
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
    feedback=load('feedback.yml'); fmap={x['key']:x for x in feedback.get('tmf_sections',[])}
    key_map={
        'market-architecture':'marketArchitecture',
        'sub-market-coordination':'subMarketCoordination',
        'market-optimization':'marketOptimization',
        'market-operation':'marketOperation',
        'network-representation':'networkRepresentation',
    }
    for y in sorted((CONTENT/'pillars').glob('*.yml')):
        d=yaml.safe_load(y.read_text(encoding='utf-8'))
        p=SRC/'pages'/d['file']; s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        h=s.select_one('.detail-hero'); set_text(h.select_one('.eyebrow'),d.get('eyebrow')); set_text(h.find('h1'),d.get('title'))
        ps=[p for p in h.find_all('p') if 'eyebrow' not in (p.get('class') or [])]
        if ps: set_text(ps[0],d.get('subtitle'))
        hero_btn=h.select_one('.button.primary')
        if hero_btn: hero_btn['href']='#pillar-feedback'; set_text(hero_btn,'Jump to feedback')

        # Clearer floating return control: icon + text.
        floating=s.select_one('.floating-home')
        if floating:
            floating.clear(); floating['aria-label']='Back to pillar on the framework page'; floating['title']='Back to pillar'
            icon=s.new_tag('span',attrs={'aria-hidden':'true','class':'floating-home-icon'}); icon.string='↩'; floating.append(icon)
            lab=s.new_tag('span',attrs={'class':'floating-home-text'}); lab.string='Back to pillar'; floating.append(lab)

        set_text(s.select_one('.pillar-philosophy-text'), d.get('philosophy'))
        set_text(s.select_one('.pillar-flow-caption'), d.get('flowchart_caption'))
        set_text(s.select_one('.tutorial-intro'), d.get('tutorial_intro'))

        badges=s.select_one('.pillar-source-badges')
        if badges: badges.decompose()

        grid=s.select_one('.tutorial-grid')
        if grid:
            grid.clear()
            for item in d.get('tutorial_sections',[]):
                card=s.new_tag('article',attrs={'class':'tutorial-step-card reveal'})
                h3=s.new_tag('h3'); h3.string=item.get('title',''); card.append(h3)
                ptxt=s.new_tag('p'); ptxt.string=item.get('text',''); card.append(ptxt)
                if item.get('items'):
                    ul=s.new_tag('ul')
                    for x in item.get('items',[]): li=s.new_tag('li'); li.string=x; ul.append(li)
                    card.append(ul)
                grid.append(card)

        # v15: merge terminology definitions into the feature matrix.
        matrix_sec=s.select_one('.pillar-feature-map-section')
        if matrix_sec:
            set_text(matrix_sec.select_one('.section-heading h2'),'Feature definitions and data types')
        set_text(s.select_one('.feature-matrix-intro'), d.get('feature_matrix_intro'))
        table=s.select_one('.feature-matrix-table')
        if table:
            thead=table.find('thead')
            if thead:
                thead.clear(); tr=s.new_tag('tr')
                for label in ['Feature','Sub-feature / decision','Data type','Definition','How to read the choice','Definition source']:
                    th=s.new_tag('th'); th.string=label; tr.append(th)
                thead.append(tr)
        body=s.select_one('.feature-matrix-body')
        if body:
            body.clear()
            for row in d.get('feature_matrix',[]):
                tr=s.new_tag('tr')
                for key in ['feature','subfeature','datatype','definition','meaning']:
                    td=s.new_tag('td'); td.string=row.get(key,''); tr.append(td)
                src_td=s.new_tag('td',attrs={'class':'definition-source-cell'})
                refs=row.get('references',[]) or []
                for i,ref in enumerate(refs):
                    block=s.new_tag('div',attrs={'class':'definition-reference'})
                    label=s.new_tag('span',attrs={'class':'definition-reference-label'}); label.string=ref.get('label','Source'); block.append(label)
                    actions=s.new_tag('span',attrs={'class':'definition-reference-actions'})
                    f=ref.get('file','')
                    if f:
                        href='../'+f.lstrip('/')
                        p=ref.get('page')
                        open_a=s.new_tag('a',attrs={'href': href + (f'#page={p}' if p else ''),'target':'_blank','rel':'noopener'}); open_a.string='Open'; actions.append(open_a)
                        dl=s.new_tag('a',attrs={'href':href,'download':''}); dl.string='Download'; actions.append(dl)
                    block.append(actions); src_td.append(block)
                tr.append(src_td)
                body.append(tr)

        # v16: source/evidence and apply-the-pillar sections are intentionally removed.
        for old in s.select('.pillar-design-intelligence-section,.pillar-mapping-checklist-section,.pillar-source-panel'):
            old.decompose()

        # Remove the old standalone terminology repository; definitions now live row-by-row in the matrix.
        for old in s.select('.terminology-repository,.term-repo-grid'): old.decompose()

        # The ready-to-fill mapping table belongs on the detailed pillar page, next to the definitions it applies to.
        for old in s.select('.pillar-worksheet-preview'): old.decompose()
        worksheet_card=make_pillar_table_preview(s,d,depth=1)
        matrix_sec=s.select_one('.pillar-feature-map-section')
        if worksheet_card:
            if matrix_sec: matrix_sec.insert_after(worksheet_card)
            else: s.select_one('main').append(worksheet_card)

        # Build pillar-specific feedback where the reviewer has just read the tutorial and definitions.
        for old in s.select('.pillar-feedback-section'): old.decompose()
        key=key_map.get(d.get('slug','')); fi=fmap.get(key,{})
        fsec=s.new_tag('section',attrs={'class':'pillar-feedback-section pillar-section reveal','id':'pillar-feedback','data-section-key':key or d.get('slug',''),'data-giscus-term':fi.get('qna_term','')})
        head=s.new_tag('div',attrs={'class':'section-heading'})
        eye=s.new_tag('p',attrs={'class':'eyebrow'}); eye.string='Expert feedback'; head.append(eye)
        hh=s.new_tag('h2'); hh.string='Evaluate this pillar'; head.append(hh)
        pp=s.new_tag('p'); pp.string=fi.get('qna_prompt',''); head.append(pp); fsec.append(head)
        ul=s.new_tag('ul',attrs={'class':'pillar-review-prompts'})
        for prompt in fi.get('qna_prompts',[]): li=s.new_tag('li'); li.string=prompt; ul.append(li)
        fsec.append(ul)
        actions=s.new_tag('div',attrs={'class':'feedback-actions'})
        poll=s.new_tag('a',attrs={'class':'button primary structured-poll-link','data-feedback-action':'poll','href':'#','target':'_blank','rel':'noopener'}); poll.string='Submit structured feedback'; actions.append(poll)
        qna=s.new_tag('button',attrs={'class':'button ghost load-comments','data-feedback-action':'qna','type':'button','aria-expanded':'false'}); qna.string='Open discussion'; actions.append(qna)
        nf=s.new_tag('button',attrs={'class':'button feedback-action-button looks-fine-button','data-pillar':'tmf-'+d.get('slug',''),'data-progress-key':key or d.get('slug',''),'type':'button'}); nf.string='No further feedback'; actions.append(nf)
        fsec.append(actions)
        helper=s.new_tag('p',attrs={'class':'giscus-helper'}); helper.string='Open the discussion to comment here through the project GitHub Q&A thread. Any one of the three feedback actions completes this pillar in the review progress.'; fsec.append(helper)
        comments=s.new_tag('div',attrs={'class':'comments-box','aria-live':'polite','id':'comments-tmf-'+d.get('slug','')}); fsec.append(comments)
        s.select_one('main').append(fsec)

        for old in s.select('.pillar-extra-area,.detail-discussion-panel,.worksheet-card,.detail-worksheet-preview,.detail-worksheet-pdf-link'):
            old.decompose()
        # All pillar pages need the five-pillar configuration so one click counts as 20%, not 100%.
        if not s.find('script',src='../assets/feedback-config.js'):
            interactive=s.find('script',src='../assets/interactive-tmf.js')
            cfg_script=s.new_tag('script',src='../assets/feedback-config.js')
            if interactive: interactive.insert_before(cfg_script)
            else: s.body.append(cfg_script)
        save(s,DIST/'pages'/d['file'])

def build_feedback_config():
    d=load('feedback.yml'); obj={'githubHubUrl':d['general']['github_hub_url'],'pollUrl':d['general']['poll_url'],'uploadUrl':d['general']['upload_url'],'generalFeedbackUrl':d['general']['general_feedback_url'],'generalGiscusTerm':d['general'].get('general_giscus_term','Theoretical Market Framework — General comments')}
    obj['feedbackPages']={x['key']:{'label':x['label'],'googleFormUrl':x['form_url'],'giscusTerm':x['giscus_term'],'giscusCategory':x.get('giscus_category',''),'giscusCategoryId':x.get('giscus_category_id','')} for x in d['dimension_pages']}
    obj['mechanisms']={x['key']:{'label':x['label'],'googleFormUrl':x['form_url'],'giscusTerm':x['giscus_term'],'giscusCategory':x.get('giscus_category',''),'giscusCategoryId':x.get('giscus_category_id','')} for x in d['mechanisms']}
    obj['sections']={x['key']:{'label':x['label'],'googleFormUrl':x.get('form_url','#'),'pollUrl':x.get('poll_url','#'),'pollTitle':x.get('poll_title',''),'giscusTerm':x.get('qna_term') or x.get('giscus_term') or x['key'],'qnaTitle':x.get('qna_title',''),'qnaPrompt':x.get('qna_prompt','')} for x in d['tmf_sections']}
    g=d['giscus']; obj['giscus']={'enabled':bool(g['enabled']),'repo':g['repo'],'repoId':g['repo_id'],'category':g['category'],'categoryId':g['category_id'],'theme':g['theme'],'lang':g['lang'],'mapping':g.get('mapping','specific'),'strict':str(g.get('strict','1')),'reactionsEnabled':str(g.get('reactions_enabled','1')),'emitMetadata':str(g.get('emit_metadata','0')),'inputPosition':g.get('input_position','top'),'loading':g.get('loading','lazy')}
    (DIST/'assets/feedback-config.js').write_text('window.TMF_FEEDBACK_CONFIG = '+json.dumps(obj,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    shutil.copytree(SRC,DIST)
    patch_home(); patch_team(); patch_work(); patch_mechanism('tariff'); patch_mechanism('connection'); patch_tmf(); patch_dimensions(); patch_pillars(); build_feedback_config()
    print(f'Built site at {DIST}')
if __name__=='__main__': main()
