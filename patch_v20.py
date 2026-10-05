from pathlib import Path
from bs4 import BeautifulSoup
import re

root = Path('/mnt/data/site_v20_work')
src_pages = root/'site_src'/'pages'
pillar_slugs = [
    'market-architecture',
    'sub-market-coordination',
    'market-optimization',
    'market-operation',
    'network-representation',
]

# 1) Remove Comillas logo/link from all source pages where it appears.
for path in src_pages.glob('*.html'):
    html = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    changed = False

    # Remove any visible Comillas brand/logo anchors.
    for a in list(soup.select('a.brand-link')):
        img = a.find('img')
        href = a.get('href','')
        alt = img.get('alt','') if img else ''
        src = img.get('src','') if img else ''
        if ('comillas' in href.lower() or 'comillas' in alt.lower() or 'comillas' in src.lower()):
            # Preserve navigation usability on detail pages with a neutral Home link.
            home = soup.new_tag('a', attrs={'class':'site-home-link hover-lift', 'href':'../index.html#top'})
            home.string = 'Home'
            a.replace_with(home)
            changed = True

    # Remove any remaining direct Comillas institutional anchor(s) and keep neutral text only when needed.
    for a in list(soup.find_all('a', href=re.compile(r'^https?://(?:www\.)?comillas\.edu/?', re.I))):
        if a.find('img'):
            a.decompose()
        else:
            # On the framework footer, remove the institution reference entirely.
            a.decompose()
        changed = True

    # Clean framework footer sentence left by removing institutional anchor.
    for p in soup.select('footer.footer p'):
        txt = ' '.join(p.stripped_strings)
        if 'Electricity System Services Market expert-review platform' in txt:
            # Rebuild footer compactly, preserving Back to top.
            p.clear()
            p.append('Electricity System Services Market expert-review platform. ')
            back = soup.new_tag('a', href='#top')
            back.string = 'Back to top'
            p.append(back)
            changed = True

    if changed:
        path.write_text(str(soup), encoding='utf-8')

# 2) Remove unconfigured structured-feedback/poll link from the five pillar pages.
for slug in pillar_slugs:
    path = src_pages/f'{slug}.html'
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    for link in list(soup.select('.pillar-feedback-section .structured-poll-link, .pillar-feedback-section [data-feedback-action="poll"]')):
        link.decompose()
    helper = soup.select_one('.pillar-feedback-section .giscus-helper')
    if helper:
        helper.string = ('Open the discussion to comment through the project GitHub Q&A thread. '
                         'Opening the discussion or selecting “No further feedback” records this pillar once in the review progress.')
    path.write_text(str(soup), encoding='utf-8')

# 3) Persist the same logic in build.py so future rebuilds do not restore the poll button.
bp = root/'scripts'/'build.py'
s = bp.read_text(encoding='utf-8')
old = """        actions=s.new_tag('div',attrs={'class':'feedback-actions'})\n        poll=s.new_tag('a',attrs={'class':'button primary structured-poll-link','data-feedback-action':'poll','href':'#','target':'_blank','rel':'noopener'}); poll.string='Submit structured feedback'; actions.append(poll)\n        qna=s.new_tag('button',attrs={'class':'button ghost load-comments','data-feedback-action':'qna','type':'button','aria-expanded':'false'}); qna.string='Open discussion'; actions.append(qna)\n        nf=s.new_tag('button',attrs={'class':'button feedback-action-button looks-fine-button','data-pillar':'tmf-'+d.get('slug',''),'data-progress-key':key or d.get('slug',''),'type':'button'}); nf.string='No further feedback'; actions.append(nf)\n        fsec.append(actions)\n        helper=s.new_tag('p',attrs={'class':'giscus-helper'}); helper.string='Open the discussion to comment here through the project GitHub Q&A thread. Any one of the three feedback actions completes this pillar in the review progress.'; fsec.append(helper)\n"""
new = """        actions=s.new_tag('div',attrs={'class':'feedback-actions'})\n        qna=s.new_tag('button',attrs={'class':'button ghost load-comments','data-feedback-action':'qna','type':'button','aria-expanded':'false'}); qna.string='Open discussion'; actions.append(qna)\n        nf=s.new_tag('button',attrs={'class':'button feedback-action-button looks-fine-button','data-pillar':'tmf-'+d.get('slug',''),'data-progress-key':key or d.get('slug',''),'type':'button'}); nf.string='No further feedback'; actions.append(nf)\n        fsec.append(actions)\n        helper=s.new_tag('p',attrs={'class':'giscus-helper'}); helper.string='Open the discussion to comment through the project GitHub Q&A thread. Opening the discussion or selecting “No further feedback” records this pillar once in the review progress.'; fsec.append(helper)\n"""
if old not in s:
    raise SystemExit('Could not find pillar feedback builder block in build.py')
s = s.replace(old, new, 1)
bp.write_text(s, encoding='utf-8')

# 4) Update progress JS so only the two remaining pillar feedback actions are tracked.
for jp in [root/'site_src'/'assets'/'interactive-tmf.js', root/'assets'/'interactive-tmf.js']:
    if not jp.exists():
        continue
    js = jp.read_text(encoding='utf-8')
    js = js.replace('// Any of the three feedback actions completes that pillar once; repeat clicks never add more than 20%.',
                    '// Either remaining feedback action completes that pillar once; repeat clicks never add more than 20%.')
    js = js.replace("const progressActions = [...document.querySelectorAll('.structured-poll-link, .load-comments, .looks-fine-button')]",
                    "const progressActions = [...document.querySelectorAll('.load-comments, .looks-fine-button')]")
    jp.write_text(js, encoding='utf-8')

# 5) Remove logo image assets from source/root. They are no longer part of the website UI.
for rel in [
    'site_src/assets/COMILLAS.png', 'site_src/assets/comillas-transparent.png',
    'assets/COMILLAS.png', 'assets/comillas-transparent.png',
    'dist/assets/COMILLAS.png', 'dist/assets/comillas-transparent.png',
]:
    p = root/rel
    if p.exists():
        p.unlink()

# 6) Update docs that explicitly tell editors the logo asset exists.
setup = root/'site_src'/'docs'/'GITHUB_PAGES_AND_FEEDBACK_SETUP.md'
if setup.exists():
    txt = setup.read_text(encoding='utf-8')
    txt = re.sub(r'^.*comillas-transparent\.png.*\n?', '', txt, flags=re.M|re.I)
    setup.write_text(txt, encoding='utf-8')

(root/'WEBSITE_REVISION_NOTES_V20.md').write_text('''# Website revision v20\n\n- Removed the Comillas institutional logo and direct Comillas website link from the framework page and all five pillar subpages.\n- Replaced the former logo/home control on pillar subpages with a neutral **Home** text link.\n- Removed the unconfigured **Submit structured feedback** action from all five pillar feedback sections.\n- Pillar feedback now offers **Open discussion** and **No further feedback** only. Either action records the pillar once in progress; repeated actions still count only once.\n- Removed obsolete Comillas logo image assets from the deployable website.\n''', encoding='utf-8')
(root/'VERSION.txt').write_text('v20\n', encoding='utf-8')
