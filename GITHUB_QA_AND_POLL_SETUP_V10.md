# GitHub Q&A + future Poll setup — TMF website v10

This website intentionally uses **two separate feedback channels for each TMF pillar**:

- **Open discussion** → embedded **Giscus Q&A**. This is the qualitative/explanatory expert discussion.
- **Submit structured feedback** → a **GitHub Poll URL**. This is reserved for a future quantitative/structured vote. No poll question is imposed in v10.

## A. Create the five Q&A Discussions first

Repository: `IIT-redes/ESSMF`
Category: **Q&A**

Create one GitHub Discussion for each pillar. The title must match the website `qna_term` exactly. With `data-mapping="specific"` and strict matching enabled, Giscus looks for that exact title in the configured Q&A category.

### Pillar 1 — Entire Market Architecture

**Exact title**

`TMF Pillar 1 — Entire Market Architecture`

**Recommended discussion body**

> Does the Entire Market Architecture pillar provide a sufficiently complete and unambiguous common language to reconstruct an existing flexibility market and to specify a new distribution-level market before coordination and clearing are designed?
>
> Please consider the following points in your response:
> 1. Can every sub-market be described consistently through number, GOT, GCT, MTU and sub-market type?
> 2. Are service and product sufficiently separated, including product type and technical requirements?
> 3. Are locational granularity, responsible SO, voltage level, buyer, seller, market operator, eligible technologies, aggregation and participation rules sufficient for cross-country comparison?
> 4. Which feature is missing, ambiguous, overlapping or too context-specific to support harmonised European market descriptions?
> 5. Would this pillar alone let another expert reproduce the high-level architecture of your market without relying on undocumented local knowledge?
>
> Where possible, please refer to a concrete market, demonstrator, country, or implementation experience.

### Pillar 2 — Sub-market Coordination

**Exact title**

`TMF Pillar 2 — Sub-market Coordination`

**Recommended discussion body**

> Does the Sub-market Coordination pillar capture the decisions needed to allocate the same flexibility resource pool across interacting local, TSO/DSO, wholesale or balancing sub-markets without double use, conflicting activation or avoidable barriers to value stacking?
>
> Please consider:
> 1. For each pair of interacting sub-markets, are priority/exclusivity rules between system operators explicit enough?
> 2. Are TSO access to DERs and formal versus conditional commitment to bid selection sufficient to reconstruct how a real design works?
> 3. Is bid forwarding described at the right level, including whether filtering, aggregation or another intermediate processing step is required?
> 4. Are the coordination phases—prequalification, procurement, activation, measurement and settlement—sufficiently explicit?
> 5. Which additional rule would be needed to expose gaming risk, conflicting activations or inefficient overlapping procurement?
>
> Please distinguish between features needed to **describe an existing market** and features needed to **guide a new market integration**.

### Pillar 3 — Market Optimisation

**Exact title**

`TMF Pillar 3 — Market Optimisation`

**Recommended discussion body**

> Do the TMF choices for optimisation methodology, the relationship among sub-market clearings and the clearing objective provide enough information to distinguish existing designs and to guide a new coordinated distribution-level market?
>
> Please consider:
> 1. Is the distinction between centralised, decentralised and distributed organisation sufficiently clear for real implementations?
> 2. Does simultaneous, sequential or independent optimisation fully describe the relationship between coupled sub-markets in your case?
> 3. Is the objective—cost minimisation, social-welfare maximisation, reducing counter-activations or other—explicit enough to explain the resulting dispatch/procurement?
> 4. What additional information is needed to understand grid-data requirements, information exchange and computational responsibility?
> 5. Can the pillar reveal risks of double procurement, counter-activations or system-wide inefficiency created by local-first or sequential clearing?

### Pillar 4 — Market Operation

**Exact title**

`TMF Pillar 4 — Market Operation`

**Recommended discussion body**

> Does the Market Operation pillar contain the minimum operational information needed to compare how flexibility sub-markets actually run and to implement a new one without confusing operational rules with other TMF dimensions?
>
> Please consider:
> 1. Are the remuneration options sufficient to describe how successful providers are paid in your market?
> 2. Is it clear whether availability, activation or both are remunerated and for active, reactive or apparent power?
> 3. Do continuous/discrete clearing and procurement frequency capture the temporal operating logic without duplicating GOT/GCT?
> 4. Are minimum bid size and bid structure sufficient to understand participation barriers and interoperability with other markets?
> 5. Which operational element, if any, is indispensable for implementation but genuinely missing from this pillar rather than belonging to another pillar/process?

### Pillar 5 — Network Representation

**Exact title**

`TMF Pillar 5 — Network Representation`

**Recommended discussion body**

> Does the Network Representation pillar adequately capture how and when distribution/transmission constraints are introduced so that a market result can be physically feasible while remaining implementable in terms of data, computation and information sharing?
>
> Please consider:
> 1. Is the distinction between comprehensive grid data, partial grid data and empirical rules sufficient for the network models used in practice?
> 2. At which phases should network constraints be introduced: procurement-area definition, prequalification, procurement, activation, measurement and/or settlement?
> 3. What validation or corrective step is required when simplified network representation is used?
> 4. Does the pillar expose the trade-off between physical fidelity and data/computational/cyber-security burden?
> 5. Which additional representation or timing option is necessary for real DSO-level implementation, if any?

## B. How the Q&A is bridged into the website

The shared Giscus configuration is already in `content/feedback.yml`:

```yaml
giscus:
  enabled: true
  repo: IIT-redes/ESSMF
  repo_id: R_kgDOTaxKGA
  category: Q&A
  category_id: DIC_kwDOTaxKGM4DBV_N
  mapping: specific
  strict: '1'
```

Each pillar has its own `qna_term`. Example:

```yaml
- key: marketArchitecture
  qna_term: TMF Pillar 1 — Entire Market Architecture
```

**If you create the GitHub Q&A with exactly that title, no additional URL needs to be pasted into the website.** Clicking **Open discussion** loads Giscus, and Giscus finds the matching Q&A Discussion in the Q&A category.

If you later change a GitHub Discussion title, update `qna_term` in `content/feedback.yml` to the same title and rebuild the site.

## C. Future Poll capability

v10 deliberately leaves every `poll_url` as `'#'`. The site capability is present, but no poll question or poll is imposed yet.

When you are ready:

1. GitHub → `IIT-redes/ESSMF` → **Discussions**.
2. Open the **Polls** category.
3. Create the poll for the relevant pillar.
4. GitHub assigns a discussion number automatically, for example `/discussions/17`.
5. Copy the complete Discussion URL.
6. Paste it in `content/feedback.yml` under the related pillar:

```yaml
- key: marketArchitecture
  poll_url: https://github.com/IIT-redes/ESSMF/discussions/17
```

7. Run `python scripts/build.py` and deploy/push as usual.

The **Submit structured feedback** button then opens that poll. Until a URL is configured, the website displays a clear configuration message instead of sending reviewers to an incorrect page.

## D. Where to edit these values in Pages CMS

Open **Forms and giscus settings → TMF pillar Poll + Q&A channels**.

For each pillar you can edit:
- `poll_title`
- `poll_url`
- `qna_title`
- `qna_term`
- `qna_prompt`
- `qna_prompts`

The shared repository/category values remain under the global `giscus` object.

## E. Important philosophy

Giscus is **not a questionnaire generator**. It is the bridge that embeds a GitHub Discussion inside the website. The qualitative question is designed first (the recommended texts above), then created as a GitHub Q&A Discussion, and Giscus connects the website to that Discussion by the exact `qna_term` title. GitHub Polls are separate Discussion objects and are connected to **Submit structured feedback** by their URL.
