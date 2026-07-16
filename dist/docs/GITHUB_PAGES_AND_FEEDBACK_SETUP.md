# Final Polished TMF Website Setup

Upload all files and folders to GitHub Pages:

```text
index.html
assets/
docs/
pages/
README.md
```

The pillar figures are stored in:

```text
docs/source/images/
```

The full-size figure pages are stored in:

```text
pages/*-figure.html
```

Configure feedback links in:

```text
assets/feedback-config.js
```

Set:
- `githubHubUrl`
- `pollUrl`
- `uploadUrl`
- `generalFeedbackUrl`
- each pillar `googleFormUrl`
- each pillar `giscusTerm`
- giscus repository settings


The detailed pillar figures were restored from the previous design package. Make sure `docs/source/images/` is uploaded to GitHub.


## Reference library

PDF files should be located in:

```text
docs/materials/
```

The reference library links directly to these PDFs. When pushing to GitHub, make sure the PDF files are committed with the rest of the project.

## Dynamic table of contents

The left-side table of contents is generated in `index.html` and highlighted by `assets/interactive-tmf.js`.


## Professional TOC version

The site now uses a slim left-side table-of-contents rail. Submenus appear on hover.
The four-question section includes an image sequence handled by `assets/interactive-tmf.js`.


## Final background/navigation revision

The site uses:
- `assets/comillas-transparent.png` for the transparent Comillas logo.
- `assets/global-background-1.jpeg`, `assets/global-background-2.webp`, and `assets/global-background-3.webp` as faded background imagery.
- A stable clickable left-side TOC with robust active-section highlighting.
