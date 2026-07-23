# CMS setup, GitHub publication, and team editing guide

## A. Publish the repository for the first time

1. Create a new empty GitHub repository. A public repository is the simplest option for GitHub Pages.
2. Upload **all files and folders from this package to the repository root**. Do not upload only the `dist` folder.
3. Commit the files to the `main` branch.
4. Open the repository on GitHub and go to **Settings → Pages**.
5. Under **Build and deployment**, choose **GitHub Actions** as the source.
6. Open the **Actions** tab. The workflow named **Build and deploy website** should run automatically.
7. After it succeeds, open **Settings → Pages** again to see the published URL.

## B. Connect Pages CMS

1. Open `https://app.pagescms.org`.
2. Sign in with GitHub.
3. Install the Pages CMS GitHub App for the account or organization that owns the repository.
4. Give the app access to this repository.
5. Open the repository in Pages CMS. It will automatically read `.pages.yml`.
6. You should see editors for Homepage, Who we are, Library, Mechanisms, Review dimensions, ESSM pillars, and Feedback settings.

## C. Safest review workflow for colleagues

1. In GitHub, create a branch named `content-review` from `main`.
2. In Pages CMS, select the `content-review` branch before editing.
3. Ask colleagues to edit only through Pages CMS.
4. Each save creates a Git commit in `content-review`.
5. The **Validate content changes** workflow runs automatically on that branch.
6. When the edits are ready, open a Pull Request from `content-review` to `main`.
7. Review the changed YAML files and the validation result.
8. Merge the Pull Request. The main deployment workflow rebuilds and publishes the website.

## D. Invite a colleague

### Colleague has a GitHub account

1. Add the colleague to the GitHub repository with Write access, or add them through your organization/team.
2. Ask them to sign in to Pages CMS using GitHub.
3. Ask them to open the repository and choose `content-review`.

### Colleague does not have a GitHub account

Pages CMS supports email-invited collaborators. Invite them from the Pages CMS collaborator area. They can edit configured content and media, but they cannot change `.pages.yml` or administrative settings.

## E. Everyday editing

1. Open Pages CMS.
2. Confirm the branch is `content-review`.
3. Select the page or review dimension.
4. Change the text, list items, image, or link.
5. Set the editorial status to Draft, Ready for review, or Approved.
6. Save.
7. Wait for the validation check.
8. Create or update the Pull Request.
9. Merge only after approval.

## F. Edit forms and giscus

Open **Forms and giscus settings** in Pages CMS.

- `form_url` can be a Google Forms or Microsoft Forms URL.
- Each dimension can have its own form and giscus term/category.
- Set `giscus.enabled` to true only after entering the repository ID, category, and category ID.
- General links include GitHub, poll, upload, and overall feedback.

## G. Add or replace images

Use **Website images** in Pages CMS. Uploaded images are stored in `site_src/assets` and are copied to the published site during the build. After upload, select the image in an image field.

## H. Add a library document

1. Upload the PDF under **Library documents** in Pages CMS.
2. Open **Library**.
3. Add a new item with title, description, file, and link label.
4. Save and follow the Pull Request workflow.

## I. Local preview for maintainers

### Windows

Run `preview_local.bat`.

### macOS/Linux

Run `bash preview_local.sh`.

Then open `http://localhost:8000`.

## J. What colleagues should not edit

Colleagues should normally avoid direct changes to:

- `site_src/*.html`
- `site_src/assets/interactive-tmf.css`
- `site_src/assets/interactive-tmf.js`
- `scripts/`
- `.github/workflows/`
- `.pages.yml`

These files control design, functionality, validation, and deployment.

## K. Recommended GitHub protection

Protect the `main` branch and require:

- a Pull Request before merging;
- at least one approval;
- the validation workflow to pass;
- no direct pushes to `main` for ordinary editors.
