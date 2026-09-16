# ESSMF website deployment package v12

This ZIP is repo-root ready. Copy/commit the **contents of this ZIP** directly into the root of `IIT-redes/ESSMF`.

It supports both GitHub Pages modes:

1. **Recommended: GitHub Actions**
   - Repository Settings -> Pages -> Build and deployment -> Source: **GitHub Actions**.
   - The workflow `.github/workflows/deploy-pages.yml` builds `site_src + content` into `dist` and deploys `dist`.

2. **Fallback: Deploy from branch/root**
   - This package also copies the generated website files (`index.html`, `assets/`, `pages/`, `docs/`) to the repository root.
   - Therefore, if Pages is set to deploy from `main / root`, it will show the real website rather than the README page.

If the live site shows a README-style page saying "CMS-ready repository", GitHub Pages is serving the repository root without a real root `index.html`, or the ZIP was uploaded as a nested folder instead of its contents being committed at repo root.
