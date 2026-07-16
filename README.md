# Flexibility Acquisition Mechanisms — CMS-ready repository

This repository separates **content** from **design**. Colleagues edit YAML files through Pages CMS; GitHub Actions rebuilds and publishes the website.

## Important folders

- `content/` — editable website text, review dimensions, library, team, forms, and giscus settings.
- `site_src/` — HTML/CSS/JavaScript design source. Editors should normally not change it.
- `scripts/build.py` — combines content with the existing design.
- `dist/` — generated website uploaded to GitHub Pages.
- `.pages.yml` — Pages CMS editing interface.
- `.github/workflows/` — validation and publication automation.

Read `CMS_SETUP_AND_EDITING_GUIDE.md` first. A one-page colleague guide is in `QUICK_GUIDE_FOR_EDITORS.md`.
