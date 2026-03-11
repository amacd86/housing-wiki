from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

SECTIONS = [
    {"id": "zoning", "label": "Zoning Fundamentals", "icon": "⚖️"},
    {"id": "legislation", "label": "NH Legislation", "icon": "📜"},
    {"id": "portsmouth", "label": "Portsmouth Specifics", "icon": "🏛️"},
    {"id": "people", "label": "People & Relationships", "icon": "👥"},
    {"id": "meetings", "label": "Meeting Notes", "icon": "📝"},
    {"id": "glossary", "label": "Glossary", "icon": "📖"},
]

def get_section_file(section_id):
    return os.path.join(DATA_DIR, f"{section_id}.json")

def load_section(section_id):
    f = get_section_file(section_id)
    if os.path.exists(f):
        with open(f) as fp:
            return json.load(fp)
    return {"entries": []}

def save_section(section_id, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(get_section_file(section_id), 'w') as fp:
        json.dump(data, fp, indent=2)

def seed_data():
    """Seed initial content from our research"""
    seeds = {
        "zoning": {"entries": [
            {"id": str(uuid.uuid4()), "title": "Zoning Basics", "body": "**Zoning code has 2 parts: Map + Regulations**\n\n**Map** assigns every parcel to a district:\n- Residential (single family → high rise)\n- Commercial (retail, restaurants, hotels)\n- Industrial\n- Institutional (schools, public buildings)\n- Open Space\n\nDistricts separate uses AND intensity (e.g. C1, C2, C3 for increasing commercial density).\n\n**Overlay Zones** layer on top of other zones adding additional restrictions/regulations — this is what the GNOD is.\n\n**Regulations (zoning ordinance)** contain:\n- Use tables — what's allowed, conditional, or prohibited per zone\n- Development standards — setbacks, side yards, min lot sizes, building heights\n- Impact regulations — signage, parking standards, historic preservation (not zone-specific)", "tags": ["basics", "map", "regulations"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Missing Middle Housing", "body": "**The problem:** America built a two-option system — sprawl OR towers — by making everything in between illegal.\n\n**Missing middle** = duplexes, triplexes, fourplexes, courtyard cottages, townhouses, small apartment buildings. Legal before ~1940s. Zoned out of existence after WWII via Euclidean zoning + car-centric policy.\n\n**Why developers build towers instead:** Zoning approval is costly and uncertain. Only worth fighting if profit margin justifies it. Middle housing doesn't pencil out under current rules.\n\n**Parking minimums** compound the problem — requiring X spaces per unit makes dense small buildings financially impossible.\n\n**Examples of reform:**\n- Minneapolis (2019): abolished single-family zoning, allows duplexes/triplexes citywide\n- Portland: allows fourplexes and cottage courts\n- Montgomery County MD: 50/50 market rate / affordable model\n\n**Form-based codes** regulate size/shape of buildings instead of use — an alternative to traditional Euclidean zoning.", "tags": ["missing middle", "density", "parking", "reform"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Exclusionary Zoning", "body": "Zoning has historically been used for exclusion — originally explicitly by race/ethnicity, now through economic mechanisms.\n\n**Modern exclusionary tools:**\n- Large minimum lot sizes (1+ acre requirements → only expensive homes built)\n- High parking minimums\n- Setback/height restrictions that increase construction cost\n- Single-family-only zoning over vast areas (San Jose: 94% of residential land)\n\n**Effect:** Cities become enclaves for the wealthy. Working families, essential workers, and seniors get priced out.\n\n**Segregation of uses** also creates sterile environments and forces car dependency — mixed-use zoning is the antidote but not widespread.", "tags": ["exclusion", "equity", "history"], "created": datetime.now().isoformat()},
        ]},
        "legislation": {"entries": [
            {"id": str(uuid.uuid4()), "title": "SB 284 — Parking Minimums (2025)", "body": "**Status:** Became law July 15, 2025. Effective September 13, 2025.\n\n**What it does:** Restricts NH municipalities from imposing mandatory on-site parking minimums. Cities/towns can no longer require a set number of parking spaces per housing unit.\n\n**Why it matters:** Parking minimums are one of the biggest hidden barriers to missing middle housing. Requiring 1.5 spaces/unit in dense urban areas like Portsmouth makes small apartment buildings financially impossible.\n\n**Portsmouth implication:** Planning Board flagged this in November 2025 — city must amend zoning ordinance to comply. One of the 'quick wins' on the barriers register Tabor mentioned.\n\n**Vote:** 197-144 in the House — not a blowout. 144 no votes = municipalities wanting to keep local control. Classic state mandate vs. local control tension.\n\n**Sponsor:** Sen. Keith R. Murphy (R)", "tags": ["parking", "state law", "2025", "active"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "HB 577 — ADUs By Right (2025)", "body": "**Status:** Law, 2025.\n\n**What it does:** Requires ALL NH municipalities to allow both attached AND detached ADUs by right in single-family residential zones.\n\n**Key specs:**\n- Min ADU size: 750 sq ft\n- Max ADU size: 950 sq ft (can be larger if locally authorized)\n- ADUs can qualify as workforce housing if they meet rental affordability criteria\n- Allows property owners to satisfy portion of regional fair-share housing obligation\n\n**Portsmouth implication:** Portsmouth Planning Board working on ordinance amendments as of late 2025. ADU streamlining (simplified permitting, reduced fees) is one of Tabor's priority quick wins.\n\n**Significance:** Biggest state-driven change to zoning in years. Effectively legalizes missing middle at smallest scale statewide.", "tags": ["ADU", "state law", "2025", "active"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "RSA 674:58-61 — Workforce Housing Statute", "body": "**What it is:** NH state statute requiring municipalities to provide 'reasonable and realistic opportunities' for workforce housing.\n\n**Portsmouth status:** One of 18 qualifying communities in 2024. Others include Dover, Nashua, Manchester, Rochester, Salem.\n\n**Legal exposure:** Municipalities that fail to comply face legal action. This is the stick behind a lot of Portsmouth's housing urgency.\n\n**InvestNH HOP Grants:** Program funded voluntary zoning reform. Portsmouth qualified 2024. Funding contested in current budget — House version strips it, Senate version extends existing $5M.", "tags": ["workforce housing", "state law", "compliance"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "79-E — Community Revitalization Tax Relief", "body": "**What it is:** Property tax relief incentive to encourage rehabilitation of underutilized buildings in downtowns and town/village centers.\n\n**Adoption:** 68 NH communities have adopted it.\n\n**Conway innovation (2024):** First community to adopt a Housing Opportunity Zone variant — offers up to 14 years of relief (10 standard, 14 for historic preservation) for affordable housing projects.\n\n**Portsmouth relevance:** A tool worth exploring for underutilized downtown parcels. Tabor has referenced financial tools like tax abatements — 79-E is the state-level version of that thinking.", "tags": ["tax relief", "state law", "financial tools"], "created": datetime.now().isoformat()},
        ]},
        "portsmouth": {"entries": [
            {"id": str(uuid.uuid4()), "title": "Portsmouth Housing Authority (PHA) — Overview", "body": "**Founded:** 1953. HUD-recognized high-performing agency.\n\n**Scale:**\n- 650+ apartments across 12 properties\n- 1,700+ residents housed\n- 460+ Housing Choice Vouchers (Section 8)\n\n**Structure:** Two entities:\n1. Portsmouth Housing Authority (PHA) — owns/operates\n2. PHA Housing Development Ltd. — affiliated nonprofit, develops using LIHTC + CDFA credits\n\n**Key contact:** Craig Welch, Executive Director — craigwelch@nh-pha.com / 603-436-4310\n\n**Mission:** Quality, affordable housing for low- and moderate-income residents through fiscally responsible, creative organization.", "tags": ["PHA", "overview"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Key Projects", "body": "**Ruth Griffin Place**\n- 82 units, ~$1,000/month rents\n- Built on city-owned land with private capital + federal tax credits\n- Tabor calls it 'the template for success' — proof that below-market housing can be built well in Portsmouth's core\n\n**Sherburne School**\n- 127 affordable units\n- Former city-owned elementary school\n- Originally proposed at 80-160 units, cut to 80-100 after Pannaway neighborhood pushback, then scrapped entirely before being revived\n- Finally crossed finish line — Tabor's signature win\n\n**Lafayette Road / Christ Church**\n- 44 workforce housing units\n- Also includes HAVEN domestic violence HQ + Little Blessings Childcare\n- Funded partly by CDFA tax credits ($193k FY2026)\n- Model for church/nonprofit surplus land partnerships", "tags": ["projects", "PHA", "Sherburne", "Ruth Griffin"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Gateway Neighborhood Overlay District (GNOD)", "body": "**What it is:** Overlay district passed 2024 covering Commerce Way and Portsmouth Boulevard — formerly office-research zoned land.\n\n**What it allows:**\n- Higher density housing and workforce housing\n- Up to 6 stories\n- Up to 120 dwelling units per building\n- Bonus incentives for affordability\n\n**Scale:** ~23 acres, walkable to downtown and grocery stores\n\n**Land transfer option:** Could create 80+ units for PHA or similar nonprofit developers\n\n**Quote from Tabor:** 'Regardless of how it got here, the discussions led to a lot of innovative ideas and innovative zoning that's going to allow us to boost the city housing stock in a location that's not going to have a lot of neighborhood impact.'\n\n**Significance:** Proof of concept for the overlay model — Tabor wants to replicate this approach for other underutilized zones.", "tags": ["GNOD", "overlay", "density", "Commerce Way"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Housing Action Plan — Four Pillars", "body": "Framework Tabor described — council tasking committee to turn advocate recommendations into executable plan.\n\n**1. Remove Zoning Barriers**\n- Audit ordinance for parking minimums, setbacks, use restrictions, density caps\n- Identify quick wins\n- Feed into 2027 zoning rewrite\n- Study Nashua and other NH cities on enabling legislation\n- Build 'barriers register' — living doc tracking obstacles + status\n\n**2. Put More Land Into Use**\n- Inventory city-owned parcels (Sherburne = proof of concept)\n- Identify surplus land from nonprofits/churches (Lafayette Rd = model)\n- Map underutilized commercial/office zones (GNOD = template)\n- Prioritize walkable sites\n\n**3. Increase Density Strategically**\n- Differentiate by neighborhood — higher near downtown/commercial, gentler (ADUs, duplexes) in residential like Pannaway\n- ADU streamlining\n- 50/50 market rate / affordable model (Montgomery County MD template)\n- GNOD as replicable overlay tool\n\n**4. Deploy Financial Tools**\n- Tax abatements (sunset when affordability covenants expire)\n- Tax deferrals for low-income homeowners\n- LIHTC / CDFA credits via PHA Housing Development Ltd.\n- Housing Trust Fund — ensure active deployment, push for dedicated staff\n- HUD/Section 8 optimization — voucher utilization + landlord participation\n- Benchmark against comparable Seacoast/NH markets\n\n**Cross-cutting: Data & Accountability**\n- Baseline metrics: units/year, waitlist trend, voucher utilization, cost/unit\n- Demand signals: emergency assistance requests rose 28 → 81 between July–Sept 2024\n- Regular public reporting", "tags": ["action plan", "pillars", "strategy"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Council Strategic Goals (Housing)", "body": "**Goal summary:** Increase supply, decrease cost, simplify process, expand below-market options.\n\n**Strategic objectives:**\n- Create a Homeowners Bill of Rights (by end of 2027)\n- Rewrite the zoning ordinance (by end of 2027)\n- Create a Housing Action Plan including review of former Housing Navigator plans (by July 2026)\n- Implement the Housing Action Plan (by end of 2027)\n\n**Target:** Tabor has stated Portsmouth needs ~1,500 units in 2 years to balance the market.", "tags": ["council", "goals", "2027"], "created": datetime.now().isoformat()},
        ]},
        "people": {"entries": [
            {"id": str(uuid.uuid4()), "title": "John Tabor", "body": "**Role:** City Councilor, co-chair Housing Committee and Blue Ribbon Housing Committee\n\n**Background:** Retired publisher, Seacoast Media Group (grew from $4.5M to $29M). Yale grad. Elected to council after retiring in 2018.\n\n**Committees:** Legislative Affairs, Audit, Housing, Governance, Energy Advisory, Fee\n\n**Housing record:**\n- Led Sherburne School project to 127 affordable units\n- Championed the GNOD\n- Co-chaired Portsmouth Listens for 20 years\n- Pushed 50/50 market rate / affordable model\n- Initiated Flashvote electronic polling for community engagement\n\n**Philosophy:** Community process is non-negotiable. Data matters. Incremental wins compound. Government can be a force for good.\n\n**Key quote:** 'We need 1,500 units in the next two years to balance our market.'\n\n**Contact:** Via city website form (public record)", "tags": ["Tabor", "council", "housing committee"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Craig Welch", "body": "**Role:** Executive Director, Portsmouth Housing Authority\n\n**Contact:** craigwelch@nh-pha.com / 603-436-4310 x118\n\n**Notes:** Operational lead for the PHA. Has been the implementation partner for Ruth Griffin Place and Lafayette Road projects.", "tags": ["PHA", "Welch"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Joanna Kelley", "body": "**Role:** Assistant Mayor, co-chair Housing Blue Ribbon Committee with Tabor\n\n**Focus:** Project sizing and community buy-in. Learned from Pannaway/Sherburne backlash — 'everything in terms of development is balance, balance in terms of aesthetics and balance of size.'\n\n**Notes:** More cautious than Tabor on density numbers. Important to understand her position when proposals come to committee.", "tags": ["council", "housing committee", "Kelley"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Peter Stith", "body": "**Role:** City Planning Manager\n\n**Function:** Manages zoning ordinance changes, supports Planning Board process. Key staff contact for the 2027 zoning rewrite.\n\n**Notes:** Will be the person shepherding SB 284 and HB 577 compliance amendments through the Planning Board.", "tags": ["planning", "zoning", "staff"], "created": datetime.now().isoformat()},
        ]},
        "glossary": {"entries": [
            {"id": str(uuid.uuid4()), "title": "ADU — Accessory Dwelling Unit", "body": "Secondary housing unit on a single-family lot. Can be attached (above garage, basement) or detached (backyard cottage). HB 577 (2025) now requires NH municipalities to allow both types by right in single-family zones.", "tags": ["ADU", "density"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "CDFA — Community Development Finance Authority", "body": "NH state tax credit program for affordable housing development. PHA Housing Development Ltd. uses these — $193k awarded for Lafayette Road project FY2026.", "tags": ["financing", "state"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Euclidean Zoning", "body": "Traditional US zoning model that strictly separates land uses into distinct zones (residential, commercial, industrial, etc.). Named after a 1926 Supreme Court case (Euclid v. Ambler). The system that made missing middle housing illegal in most of America.", "tags": ["zoning", "history"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "GNOD — Gateway Neighborhood Overlay District", "body": "Portsmouth's overlay district covering Commerce Way and Portsmouth Blvd. Passed 2024. Allows up to 6-story, 120-unit residential buildings on formerly office-research zoned land. ~23 acres walkable to downtown.", "tags": ["Portsmouth", "overlay", "density"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "HCV — Housing Choice Voucher (Section 8)", "body": "Federal subsidy allowing low-income renters to rent in the private market. PHA administers 460+ vouchers. Voucher utilization rate and landlord participation are key metrics to monitor.", "tags": ["HUD", "vouchers", "Section 8"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "LIHTC — Low-Income Housing Tax Credits", "body": "Federal program. Primary financing mechanism for affordable housing nationally. PHA Housing Development Ltd. uses these for development projects.", "tags": ["financing", "federal"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Missing Middle Housing", "body": "Housing types between single-family homes and large apartment towers: duplexes, triplexes, fourplexes, townhouses, courtyard buildings, small apartment buildings. Legal pre-WWII. Zoned out of existence in most US/Canadian cities by Euclidean zoning + parking minimums.", "tags": ["density", "housing types"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "Overlay Zone", "body": "A zoning district layered on top of existing base zoning that adds permissions, restrictions, or regulations without replacing the base zone. The GNOD is Portsmouth's primary recent example — it added high-density residential permissions on top of existing office-research zoning.", "tags": ["zoning", "overlay"], "created": datetime.now().isoformat()},
            {"id": str(uuid.uuid4()), "title": "79-E", "body": "Community Revitalization Tax Relief Incentive Program. Encourages rehab of underutilized buildings in downtowns via property tax relief. 68 NH communities have adopted it. Conway created a Housing Opportunity Zone variant offering up to 14 years of relief for affordable projects.", "tags": ["tax relief", "state law", "financing"], "created": datetime.now().isoformat()},
        ]},
        "meetings": {"entries": [
            {"id": str(uuid.uuid4()), "title": "Call with John Tabor — March 2026", "body": "**Context:** Tabor called after reading Housing Authority board application.\n\n**Key takeaways:**\n- Committee tasked with turning advocate framework into executable action plan\n- Housing is complex — combination of removing zoning barriers, putting more land into use, increasing density, financial tools\n- Getting a crash course in land use regulation is a major area of progress\n- Always looking at tax abatements, tax deferrals as financial levers\n- Mentioned Nashua as a city to study for enabling legislation\n- Zoning rewrite is a major 2027 goal\n\n**My questions to follow up on:**\n- Which zoning provisions are the biggest bottlenecks right now?\n- Has the GNOD generated developer interest since it passed?\n- Is the Housing Trust Fund being actively deployed?\n- Where would a data/analytics lens be most useful?", "tags": ["Tabor", "call", "March 2026"], "created": datetime.now().isoformat()},
        ]},
    }

    for section_id, data in seeds.items():
        f = get_section_file(section_id)
        if not os.path.exists(f):
            save_section(section_id, data)

@app.route('/')
def index():
    return render_template('index.html', sections=SECTIONS)

@app.route('/section/<section_id>')
def section(section_id):
    data = load_section(section_id)
    section_meta = next((s for s in SECTIONS if s['id'] == section_id), None)
    if not section_meta:
        return redirect(url_for('index'))
    entries = sorted(data.get('entries', []), key=lambda x: x.get('created', ''), reverse=True)
    return render_template('section.html', section=section_meta, entries=entries, sections=SECTIONS)

@app.route('/entry/<section_id>/<entry_id>')
def entry(section_id, entry_id):
    data = load_section(section_id)
    e = next((x for x in data['entries'] if x['id'] == entry_id), None)
    section_meta = next((s for s in SECTIONS if s['id'] == section_id), None)
    return render_template('entry.html', entry=e, section=section_meta, sections=SECTIONS)

@app.route('/new/<section_id>', methods=['GET', 'POST'])
def new_entry(section_id):
    section_meta = next((s for s in SECTIONS if s['id'] == section_id), None)
    if request.method == 'POST':
        data = load_section(section_id)
        tags = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
        entry = {
            "id": str(uuid.uuid4()),
            "title": request.form['title'],
            "body": request.form['body'],
            "tags": tags,
            "created": datetime.now().isoformat()
        }
        data['entries'].append(entry)
        save_section(section_id, data)
        return redirect(url_for('section', section_id=section_id))
    return render_template('edit.html', section=section_meta, entry=None, sections=SECTIONS)

@app.route('/edit/<section_id>/<entry_id>', methods=['GET', 'POST'])
def edit_entry(section_id, entry_id):
    section_meta = next((s for s in SECTIONS if s['id'] == section_id), None)
    data = load_section(section_id)
    e = next((x for x in data['entries'] if x['id'] == entry_id), None)
    if request.method == 'POST':
        e['title'] = request.form['title']
        e['body'] = request.form['body']
        e['tags'] = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
        e['updated'] = datetime.now().isoformat()
        save_section(section_id, data)
        return redirect(url_for('entry', section_id=section_id, entry_id=entry_id))
    return render_template('edit.html', section=section_meta, entry=e, sections=SECTIONS)

@app.route('/delete/<section_id>/<entry_id>', methods=['POST'])
def delete_entry(section_id, entry_id):
    data = load_section(section_id)
    data['entries'] = [x for x in data['entries'] if x['id'] != entry_id]
    save_section(section_id, data)
    return redirect(url_for('section', section_id=section_id))

@app.route('/search')
def search():
    q = request.args.get('q', '').lower()
    results = []
    if q:
        for s in SECTIONS:
            data = load_section(s['id'])
            for e in data.get('entries', []):
                if q in e['title'].lower() or q in e['body'].lower() or any(q in t.lower() for t in e.get('tags', [])):
                    results.append({**e, 'section_id': s['id'], 'section_label': s['label'], 'section_icon': s['icon']})
    return render_template('search.html', results=results, query=request.args.get('q', ''), sections=SECTIONS)

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "Portsmouth Housing Wiki",
        "short_name": "HousingWiki",
        "description": "Portsmouth housing policy reference",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0f1117",
        "theme_color": "#1a73e8",
        "icons": [
            {"src": "/static/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/static/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}
        ]
    })

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    seed_data()
    app.run(host='0.0.0.0', port=5050, debug=False)
