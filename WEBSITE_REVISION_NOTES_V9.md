# Website revision v9 — TMF tutorial + terminology repository + GitHub Poll/Q&A readiness

## Detailed pillar pages
- Rebuilt the five pillar detail pages as source-grounded tutorials.
- The TMF flowchart now sits beside the pillar philosophy/explanation card on desktop and stacks cleanly on smaller screens.
- Added a step-by-step “Market-design intelligence” tutorial to every pillar page.
- Added a pillar-specific “Standard terminology repository” with definitions and a source label for every term.
- Added direct source-basis links to the OneNet D11.2 report and Troncia et al. (2023) TMF paper.
- Removed worksheet download controls and discussion controls from the detailed pillar pages. These remain on the main framework/review page only.

## Main TMF page
- Preserved the existing main-page structure and pillar worksheet areas.
- Preserved clickable pillar titles that open the richer tutorial pages.
- “Submit structured feedback” is now reserved for a native GitHub Poll URL per pillar.
- “Open discussion” remains the Giscus-powered Q&A channel per pillar.

## GitHub Discussion configuration
- Shared Giscus category: Q&A.
- Specific-term mapping with one unique term per pillar.
- Strict title matching enabled.
- Five separate `poll_url` fields added to `content/feedback.yml` and Pages CMS.
- Added `GITHUB_QA_AND_POLLS_SETUP_V9.md` with exact titles, suggested questions, poll options and setup instructions.

## CMS
- Added editable fields for tutorial philosophy, flowchart caption, tutorial sections, terminology repository and source basis.
- Added editable Giscus behavior fields.
- Added pillar-specific Poll URL/title and Q&A term fields.

## Validation
- Site build completed successfully.
- Internal link validation passed.
- JavaScript syntax check passed.
- `.pages.yml` and feedback YAML parsed successfully.
