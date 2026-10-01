from pathlib import Path
import yaml
ROOT=Path('/mnt/data/site_v18_work/content')

def load(rel):
    p=ROOT/rel
    return p,yaml.safe_load(p.read_text(encoding='utf-8'))

def save(p,d):
    p.write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True,width=110),encoding='utf-8')

# HOME
p,d=load('home.yml')
d['hero'].update({
'philosophy':'Flexibility is not one market. It is a portfolio of choices on infrastructure, access, pricing, obligations, and procurement.',
'lead':'DSOs can combine rules, flexible connections, network tariffs, and market-based procurement, alongside reinforcement and DSO-owned resources.',
'invitation':'Review the framework, challenge the boundaries between mechanisms, and help turn it into a practical European reference.'})
d['road_intro']['text']='Start from the network need, compare the available routes, then combine mechanisms only where their roles and interactions are clear.'
road={
'01':'Describe the need by location, timing, duration, severity, and certainty.',
'02':'Compare reinforcement, operational measures, DSO-owned resources, and third-party flexibility on cost, reliability, timing, and long-term value.',
'03':'Use mandatory requirements only where justified; define the legal basis, proportionality, and user protection.',
'04':'Use tariffs to influence routine grid use. Their value depends on a clear network cost driver, customer response, and coordination with other price signals.',
'05':'Use flexible access when firm capacity is constrained. Define access rights, curtailment, compensation, control, and the path to reinforcement.',
'06':'Use explicit procurement when a measurable service can be competitively bought. Success depends on liquidity, transparent rules, and compatibility with other markets.',
'07':'Build a portfolio with clear boundaries, signal priority, protection against double charging or reward, and a defined role for reinforcement.'}
for item in d['road_turns']:
    if item['number'] in road: item['text']=road[item['number']]
d['focus_intro']['text']='We focus on three interfaces: price signals, access conditions, and explicit service procurement.'
d['focus_cards'][0]['text']='Implicit and preventive. Useful for recurring network needs, but sensitive to granularity, fairness, response, and interaction with explicit markets.'
d['focus_cards'][1]['text']='Contractual and locational. It can unlock capacity quickly, but requires clear curtailment rights, compensation, control, and a reinforcement pathway.'
d['focus_cards'][2]['text']='Explicit and measurable. It can reveal flexibility value, but depends on products, liquidity, clearing, coordination, settlement, and network constraints.'
d['interaction_callout']['text']='A customer may face a tariff, a connection condition, and a local-market opportunity at the same time. The key questions are signal priority, baselines, double commitment, compensation, liquidity, and reinforcement.'
d['mechanisms_intro']['text']='Open a mechanism page, review its key dimensions, and leave focused feedback.'
d['expert_invitation']['title']='Turn European experience into practical design guidance'
d['expert_invitation']['text']='Choose a mechanism, test its design choices, and share the evidence or experience that should change the framework.'
save(p,d)

# TARIFF
p,d=load('mechanisms/tariff.yml')
d['hero']['philosophy']='A network tariff is a price signal about when, where, and how grid capacity is used.'
d['hero']['lead']='Tariffs recover network costs and can also influence withdrawals and injections. Good design links a real network cost driver to a signal customers can understand and act on.'
d['sections']['overview']['text']='Tariffs acquire flexibility indirectly: they change routine consumption, charging, storage, and injection decisions rather than buying a specific activation.'
d['sections']['why']['text']='A tariff can reduce one peak but shift another, distort baselines, or burden users who cannot respond. Test both network value and distributional impact.'
d['sections']['who']['where_text']='Best suited to recurring, measurable network patterns where customers have enough information and controllability to respond.'
d['sections']['framework']['text']='Open a dimension to review its design choices and leave focused feedback.'
for card in d.get('visual_cards',[]):
    card['text']={
      'The customer interface':'Bills and charging structures turn network design into a customer signal.',
      'A changing resource base':'Renewables, EVs, storage, and electrification reshape network costs.',
      'Network context':'The same tariff can have different value across locations and grid conditions.',
      'Distributional outcomes':'Tariff choices can shift costs and benefits across customer groups.',
      'Behavioural response':'Response depends on incentives, automation, and practical constraints.'}.get(card['title'],card['text'])
d['challenge_intro']['text']='Open a stakeholder card to test the design from that perspective.'
d['final_feedback']['text']='Share relevant regulatory examples, studies, data, or implementation lessons.'
save(p,d)

# CONNECTION
p,d=load('mechanisms/connection.yml')
d['hero']['philosophy']='A flexible connection defines how scarce capacity, operational limits, risk, and responsibility are shared.'
d['hero']['lead']='Flexible connections can accelerate access when firm capacity is unavailable. The agreement must make access rights, curtailment, compensation, control, review, and the path to firm access clear.'
d['sections']['overview']['text']='A flexible connection uses controllable access conditions to connect demand, generation, or storage within a constrained network envelope.'
d['sections']['why']['text']='Poor design can create unbankable curtailment, unequal treatment, market conflicts, or indefinite delay of reinforcement.'
d['sections']['who']['where_text']='Most relevant where useful access can be offered before reinforcement and the constraint can be monitored and managed transparently.'
d['sections']['framework']['text']='Open a dimension to review its design choices and leave focused feedback.'
for card in d.get('visual_cards',[]):
    card['text']={
      'A negotiated access boundary':'Match user investment with a clear, secure access envelope.',
      'The constrained network':'Feeders and substations define the physical capacity available.',
      'Connection-point implementation':'Metering, protection, control, and communication make limits operational.',
      'The wider network envelope':'Access must remain consistent with upstream network constraints.',
      'Dynamic operating conditions':'Capacity can change over time, so control logic must be predictable.',
      'Monitoring and accountability':'Operational data and oversight support fair implementation.'}.get(card['title'],card['text'])
d['challenge_intro']['text']='Open a stakeholder card to test the agreement from that perspective.'
d['final_feedback']['text']='Share contract examples, regulatory decisions, operational data, or case evidence.'
save(p,d)

# THEORETICAL MARKET FRAMEWORK MAIN PAGE
p,d=load('mechanisms/tmf.yml')
d['hero']['lead']='A common language for describing, comparing, and improving flexibility-market designs. Review the five pillars and contribute expert feedback.'
d['sections']['journey']['text']='Four short questions introduce the proposal before the five pillars.'
d['sections']['case-example']['text']='A worked case shows the process: complete the five pillar tables with consistent market labels, then translate them into one architecture view.'
d['sections']['framework-view']['text']='Each pillar captures one design layer; together they provide a comparable market description.'
d['sections']['review']['text']='Open a pillar page, scan the definitions and mapping table, then leave focused feedback.'
d['sections']['final-feedback']['text']='Share cross-pillar comments, concerns, examples, references, or supporting material.'
sp=d['case_example']
sp['image_caption']='Worked architecture produced from the five filled framework tables.'
sp['explanation_intro']='Keep the same Market 1–4 labels across all five tables. Record only known information; use Additional Information for assumptions, exceptions, and pairwise conditions.'
sp['explanation_points']=[
'1. Pillar 1 defines each market: timing, product, location, and actors. Each market becomes a block.',
'2. Keep the same labels in Pillars 2–5 to describe coordination, clearing, operation, and network constraints.',
'3. Use “Not applicable” where needed and record uncertainty in Additional Information.',
'4. Position blocks in time using GOT/GCT/MTU and by layer using buyer, operator, and location.',
'5. Draw links only when coordination rules support them; use the remaining pillars to explain how the sessions work.'
]
sp['downloads'][0]['description']='Five filled framework tables plus the resulting market-architecture figure.'
sp['downloads'][1]['description']='Standalone architecture figure derived from the structured mapping.'
sp['source_note']='Illustrative worked case only; it is not a definitive national-market representation.'
save(p,d)

# PILLAR PAGES
pillars={
'market-architecture.yml':{
'philosophy':'Describes the market as interacting sub-markets: what exists, when it operates, what it trades, where it applies, and who participates.',
'tutorial_intro':'Start here: these choices define the market objects that the other pillars coordinate, clear, operate, and constrain.',
'worksheet_text':'Use one column per market, keep the same Market 1–4 labels across all five pillar tables, and note assumptions or exceptions in Additional Information.',
'feature_matrix_intro':'Use the table as a compact terminology reference and data-entry guide.'},
'sub-market-coordination.yml':{
'philosophy':'Describes how markets compete for or share the same flexibility resources, including priority, access, commitment, forwarding, and timing.',
'tutorial_intro':'Use the same Market 1–4 labels and describe only the interactions that actually apply.',
'worksheet_text':'Keep the Market 1–4 labels from Pillar 1 and record the coordination rule for each relevant interaction.',
'feature_matrix_intro':'Use the table to define each coordination choice and the data expected.'},
'market-optimization.yml':{
'philosophy':'Describes where optimisation responsibility sits, how related clearings are linked, and what objective selects the outcome.',
'tutorial_intro':'Record the clearing logic for each market and its relationship with the others.',
'worksheet_text':'For each market, record the optimisation method, clearing relationship, and objective.',
'feature_matrix_intro':'Use the table to define the optimisation choices and expected data.'},
'market-operation.yml':{
'philosophy':'Describes the practical operating rules: payment, what is remunerated, clearing mode, procurement frequency, and bid properties.',
'tutorial_intro':'Record the rules participants face in each market.',
'worksheet_text':'For each market, record remuneration, clearing type, procurement frequency, minimum bid size, and bid structure.',
'feature_matrix_intro':'Use the table to define each operating rule and expected data.'},
'network-representation.yml':{
'philosophy':'Connects market decisions to grid physics by stating how network constraints are represented and when they affect the process.',
'tutorial_intro':'State how physical feasibility is checked and what network information is used.',
'worksheet_text':'For each market, record the network representation and the phase(s) where constraints enter.',
'feature_matrix_intro':'Use the table to define the network-modelling choices and expected data.'}
}
for fn,upd in pillars.items():
    p,d=load('pillars/'+fn)
    for k,v in upd.items(): d[k]=v
    # Tighten tutorial card text while preserving steps and bullet structure.
    for sec in d.get('tutorial_sections',[]):
        sec['text']=sec['text'].replace('Record the ','Record ').replace('State whether ','State ').replace('Use this pillar to ','')
    # tighten repeated how-to wording
    for row in d.get('feature_matrix',[]):
        m=row.get('meaning','')
        m=m.replace('Record the ','Record ').replace('Select the ','Select ').replace('State the ','State ').replace('Identify the ','Identify ').replace('Enter the ','Enter ').replace('Choose the ','Choose ')
        row['meaning']=m
    save(p,d)

# DIMENSION PAGES: reduce prose, keep choices/questions/evidence intact.
for p in sorted((ROOT/'dimensions').glob('*.yml')):
    d=yaml.safe_load(p.read_text(encoding='utf-8'))
    paras=d.get('definition_paragraphs',[])
    if len(paras)>=2:
        # keep the full core definition, compress the consequence sentence
        second=paras[1]
        # generic concise risk phrasing based on page content
        d['definition_paragraphs']=[paras[0], second.split('. ')[0].rstrip('.')+'.']
    d['review_principle']='A credible design links the choice to a measurable network, regulatory, commercial, or customer outcome.'
    d['feedback_text']='Please comment on the definition, choices, feasibility, evidence, and interaction with other flexibility mechanisms.'
    # keep examples but cap to two sentences where longer
    ex=d.get('example_text','')
    parts=[x.strip() for x in ex.split('. ') if x.strip()]
    if len(parts)>2:
        d['example_text']='. '.join(parts[:2]).rstrip('.')+'.'
    save(p,d)

# TEAM/WORK: only minor tightening, no structural changes.
for rel in ['team.yml','work.yml']:
    p,d=load(rel)
    if rel=='work.yml' and d.get('intro'):
        d['intro']='Selected European projects showing the team’s experience in flexibility, market design, coordination, and power-system innovation.'
    save(p,d)
