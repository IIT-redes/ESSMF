# Website Revision Notes — v11

## Review-control ordering
For all five TMF pillars on the main Theoretical Market Framework page, the feedback controls have been moved from the introductory pillar box to the expert-review panel.

The visual sequence is now:
1. Pillar explanation (left) + pillar flowchart (right)
2. Expert review question and prompts
3. Submit structured feedback / Open discussion / No further feedback
4. Giscus helper and, when opened, the discussion thread

This ordering is enforced both in `site_src/pages/theoretical-market-framework.html` and in `scripts/build.py`, so rebuilding the website will not restore the former placement.

## Validation
- Source template checked for all five pillars.
- Built `dist` checked for all five pillars.
- `scripts/build.py` and `scripts/validate.py` completed successfully.
- No feedback-action group remains inside `.pillar-text`.
