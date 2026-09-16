# Giscus setup and testing (v8)

The website uses one active Giscus widget at a time and a unique `specific` mapping term for each TMF pillar.

## Required GitHub-side setup
1. Repository Discussions must be enabled for `IIT-redes/ESSMF`.
2. Install/authorise the **Giscus** GitHub App for `IIT-redes/ESSMF`: https://github.com/apps/giscus
3. The configured category is **Q&A** with category ID `DIC_kwDOTaxKGM4DBV_N`.

## Important test method
Do **not** test Giscus by double-clicking an HTML file (`file://...`). Use either the deployed GitHub Pages site or run `preview_local.bat` / `preview_local.sh` and open `http://localhost:8000`.

## Pillar mapping terms
- TMF Pillar 1 — Entire Market Architecture
- TMF Pillar 2 — Sub-market Coordination
- TMF Pillar 3 — Market Optimisation
- TMF Pillar 4 — Market Operation
- TMF Pillar 5 — Network Representation

The same term is used on the framework page and the corresponding detailed pillar page, so each pillar resolves to one GitHub Discussion.
