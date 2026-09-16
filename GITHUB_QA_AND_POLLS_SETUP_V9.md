# TMF expert review: GitHub Q&A + Poll setup

This website uses two different GitHub Discussion channels for each TMF pillar.

- **Open discussion** -> Giscus -> a GitHub **Q&A** Discussion. This is for qualitative expert reasoning and replies.
- **Submit structured feedback** -> the native GitHub **Poll** Discussion. This is for a quick structured vote. The website opens the poll's GitHub URL directly.

Giscus is therefore the bridge for the Q&A comment thread. The Poll button is intentionally a normal GitHub Discussion link: GitHub owns the poll/voting interface, while Giscus is used here as the embedded discussion/comment layer.

## 1. Shared Giscus configuration

The site is already configured for:

- Repository: `IIT-redes/ESSMF`
- Repository ID: `R_kgDOTaxKGA`
- Discussion category: `Q&A`
- Category ID: `DIC_kwDOTaxKGM4DBV_N`
- Mapping: `specific`
- Strict title matching: `1`
- Reactions: enabled
- Comment box: above comments
- Lazy loading: enabled

The Giscus GitHub App must have access to `IIT-redes/ESSMF`, and GitHub Discussions must remain enabled.

## 2. Create the five Q&A Discussions

In GitHub: **ESSMF -> Discussions -> Q&A -> New discussion**.

Create one discussion with each exact title below. Exact titles matter because the website uses them as the Giscus `data-term` values.

### Pillar 1
**Title:** `TMF Pillar 1 — Entire Market Architecture`

**Suggested question:**
Does the Entire Market Architecture pillar provide a sufficiently complete and unambiguous description of the sub-markets, timing, services/products, location, actors, eligibility and aggregation rules to (a) reconstruct an existing flexibility-market design and (b) guide the design or integration of a new distribution-level market? Which feature or sub-feature is missing, unclear, overlapping or unnecessarily detailed?

### Pillar 2
**Title:** `TMF Pillar 2 — Sub-market Coordination`

**Suggested question:**
Does the Sub-market Coordination pillar make resource allocation across system operators and sub-markets sufficiently explicit, including priority/exclusivity, commitment to bid selection, bid forwarding and the market phase in which coordination occurs? What would an expert still need in order to diagnose an existing coordination arrangement or design a new one without double use, conflicting activation or gaming opportunities?

### Pillar 3
**Title:** `TMF Pillar 3 — Market Optimisation`

**Suggested question:**
Does the Market Optimisation pillar sufficiently distinguish centralised, decentralised and distributed arrangements; simultaneous, sequential and independent strategies; and the optimisation objective? Can these dimensions explain the clearing intelligence of an existing design and guide a new TSO–DSO/DSO-level design while making efficiency, coordination and information-sharing trade-offs visible?

### Pillar 4
**Title:** `TMF Pillar 4 — Market Operation`

**Suggested question:**
Does the Market Operation pillar capture the operational rules needed to compare and design markets: remuneration, the remunerated product attribute, continuous/discrete clearing, procurement frequency, minimum bid size and bid structure? Which additional operational rule, if any, is necessary to make the framework implementation-ready without losing its cross-country comparability?

### Pillar 5
**Title:** `TMF Pillar 5 — Network Representation`

**Suggested question:**
Does the Network Representation pillar adequately describe how physical network constraints enter a market design and at which acquisition phase? Are the levels of grid representation and timing choices sufficient to compare existing approaches and guide a feasible distribution-level market while making data, computation, privacy and physical-feasibility trade-offs visible?

You do **not** need to paste Q&A URLs into the website if the exact titles above are used. Giscus finds them by the configured specific term. If a discussion does not exist, Giscus can create a matching thread when a user first interacts, but pre-creating it is recommended because you can control the opening question/body.

## 3. Create the five Poll Discussions

In GitHub: **ESSMF -> Discussions -> Polls -> New discussion**.

Create one poll per pillar. GitHub assigns each poll a Discussion URL such as:
`https://github.com/IIT-redes/ESSMF/discussions/17`

You do not choose the number. Copy the final URL after creating the poll.

Suggested poll question for every pillar:
**How well does this pillar support both mapping an existing market design and guiding the design/integration of a new distribution-level market?**

Suggested options:
1. Sufficient as currently structured
2. Mostly sufficient — minor clarification/additions needed
3. Important design elements are missing
4. Substantial restructuring is needed

Use a pillar-specific title, for example:
- `TMF Pillar 1 — Structured assessment`
- `TMF Pillar 2 — Structured assessment`
- `TMF Pillar 3 — Structured assessment`
- `TMF Pillar 4 — Structured assessment`
- `TMF Pillar 5 — Structured assessment`

## 4. Connect each Poll to the website

After each poll exists, paste its full GitHub Discussion URL into:

`content/feedback.yml -> tmf_sections -> [pillar] -> poll_url`

or in Pages CMS:

**Forms and giscus settings -> TMF pillar Poll + Q&A channels -> [pillar] -> poll_url**

Example:

```yaml
- key: marketArchitecture
  label: Market architecture
  poll_title: TMF Pillar 1 — Structured assessment
  poll_url: https://github.com/IIT-redes/ESSMF/discussions/17
  qna_term: TMF Pillar 1 — Entire Market Architecture
```

Rebuild/deploy the site after saving. The **Submit structured feedback** button then opens that exact poll.

## 5. If you later change the Q&A category

Use giscus.app again and replace the shared `category` and `category_id` values in `content/feedback.yml`. The five `qna_term` values can remain unchanged unless you rename the GitHub Discussions.

If you rename a Q&A Discussion, update the matching `qna_term` in `content/feedback.yml` so the website and GitHub still refer to exactly the same title.
