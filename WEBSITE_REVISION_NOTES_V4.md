# BRIDGE / TMF website revision v4

This revision addresses the four requested issues precisely:

1. **Spain implementation example**
   - Added a full explanation of how the five filled TMF tables are transformed into the Spanish market-architecture figure.
   - Added a table-to-figure translation table.
   - Explicitly distinguishes the four OneNet DSO sub-markets from the existing TSO/energy/balancing markets shown for context.
   - Keeps downloads for the filled Spanish DOCX, Spain case PDF, standalone figure, and OneNet D11.2.

2. **Blank pillar tables in the correct pillar sections**
   - Each of the five user-supplied blank pillar PDFs is displayed inside its corresponding pillar section.
   - Each pillar has an editable Word download button placed exactly between **Open discussion** and **No further feedback**.
   - Each pillar also offers the exact supplied blank PDF.
   - The same preview/downloads are included on each pillar detail page.

3. **Feedback progress and 100% celebration**
   - Progress now counts unique pillar completions robustly and works even if browser localStorage is unavailable.
   - At 100%, the progress card enters a completed state and a full-screen light/spark celebration is launched together with the congratulations banner.

4. **Back to pillar navigation**
   - All five full-size pillar figure pages now link back to the exact corresponding pillar anchor on `theoretical-market-framework.html`.
   - Added scroll margin so the returned pillar title/actions are not hidden under navigation.

5. **CMS editability**
   - Spain explanation, mapping rows, source note, and downloads are exposed in Pages CMS.
   - Pillar Word/PDF files, preview image, worksheet title and worksheet explanatory text are exposed in Pages CMS.

Validation performed:
- `python scripts/build.py`
- `python scripts/validate.py dist`
- all local links and cross-page anchors checked: 0 missing links, 0 invalid anchors
- JavaScript syntax checked with `node --check`
- `.pages.yml` parsed successfully
- all five blank DOCX worksheets and the filled Spain DOCX rendered for visual QA
