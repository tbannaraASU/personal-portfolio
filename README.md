# Than Bannarat — Personal Portfolio

A responsive personal portfolio showcasing **software engineering, accessibility work, academic projects, and photography**.

**Live site:** https://tbannaraasu.github.io/personal-portfolio/  
**Repository:** https://github.com/tbannaraASU/personal-portfolio

> This README documents the **V15 codebase and optional enhancements**. The live website reflects V15 only after the V15 changes have been merged into `main` and GitHub Pages deployment has succeeded.

## Features

- **Homepage:** introduction, technical skills, selected featured projects, featured photography, experience, and contact links.
- **Project archive:** `projects.html` with topic filters and direct links to individual case studies.
- **Case studies:** `project.html?id=...`, populated from real project records. The Local Portfolio Admin supports timeline, role, skills, overview, challenge, approach, results, highlights, screenshots, and project links. V15 adds a *Copy case study link* control and a completeness checker; it does not generate fictional project results.
- **Photography:** `photography.html`, `tag.html?tag=...`, and `album.html?id=...`; hashtag browsing, curated albums, image viewer with previous/next navigation, and an Instagram link to [@foto_4th](https://www.instagram.com/foto_4th/).
- **Featured content:** choose up to three featured projects and three featured photographs through the appropriate local admin pages.
- **Responsive design:** light/dark themes, mobile navigation, photo thumbnails in WebP, native image lazy loading, keyboard support, and reduced-motion refinements.
- **V15 SEO:** refreshed sitemap generation, canonical URL enhancement, and a local static-site audit script.
- **V15 optional analytics:** Cloudflare Web Analytics integration is **disabled by default**. No analytics beacon runs until a valid site token is explicitly configured and published.
- **Safe publishing:** V14 local content publisher previews public content, pushes a new branch, and opens or links to a pull request. **It does not merge automatically** or publish code changes.

This is a **static GitHub Pages site**. Python and SQLite run only on the author's local machine for editing; site visitors do not have access to a remote admin server.

## Technology

- HTML, CSS, vanilla JavaScript
- Python 3, SQLite, Pillow (for local content/image management)
- Git and GitHub Pages
- Optional Cloudflare Web Analytics (manual opt-in)

## Pages

| Page | Purpose |
| --- | --- |
| `index.html` | Featured projects, selected photos, profile and contact |
| `projects.html` | All published projects |
| `project.html?id=...` | Individual project case study |
| `photography.html` | Photography collection browser |
| `tag.html?tag=...` | Photo sets within one hashtag |
| `album.html?id=...` | Curated photography album |
| `404.html` | Custom not-found page |

## Local editing

From the repository directory on your Mac:

```bash
source .venv/bin/activate
python tools/admin_server.py
```

- Portfolio Admin: http://127.0.0.1:8765/admin/portfolio
- Photography Admin: http://127.0.0.1:8765/admin
- Local website: http://127.0.0.1:8765/index.html

After saving content (or before a manual publication):

```bash
python tools/gallery.py build
python tools/portfolio.py build
```

`data/gallery.json`, `data/gallery-data.js`, `data/portfolio.json`, and `data/portfolio-data.js` are the **public exports** consumed by GitHub Pages. The local SQLite database (`local/gallery.sqlite`) must never be committed.

### V15 quality tools

```bash
python tools/check_projects_v15.py       # Suggested missing case-study fields; read-only
python tools/build_sitemap_v15.py        # Regenerates public sitemap.xml
python tools/check_site_v15.py           # Static HTML references and metadata
python tools/cleanup_readmes_v15.py     # Preview optional root README cleanup
```

Run Chrome DevTools Lighthouse and test the live website on a real phone as well. Static checks cannot certify accessibility or performance.

### Optional visitor analytics

1. Create a **Cloudflare Web Analytics** site for the published hostname and obtain the *Web Analytics site token* (not a Cloudflare API token).
2. Enable the public beacon configuration:

```bash
python tools/configure_analytics_v15.py --token YOUR_32_HEX_SITE_TOKEN
```

To switch tracking off:

```bash
python tools/configure_analytics_v15.py --disable
```

This modifies only `assets/v15-analytics-config.js`. Review the diff and publish it through the usual **code** pull-request workflow. It is not included in the V14 content-only publisher. With the token empty, V15 makes **no Cloudflare Analytics request**. Dashboard statistics remain on Cloudflare, not in the repository.

## Publishing

- **Content edits:** Save in Local Admin → **Preview changes** in V14 Publish → review changed public JSON/media → **Push & open PR** → review/merge PR into `main`.
- **Code, README, sitemap and V15 updates:** stage the specific changed paths yourself in a feature branch, review `git diff --cached`, commit, push, open PR, and merge manually.
- GitHub Pages is served from `main` / root after its deployment finishes. The local admin does not push straight to `main`.

## Search and metadata

`tools/build_sitemap_v15.py` creates `sitemap.xml` for published pages, visible case studies, and populated albums using **already public** exports. Submit the resulting sitemap in Google Search Console after deployment. A sitemap does not guarantee indexing.

**GitHub Pages project-site caveat:** `robots.txt` under `/personal-portfolio/robots.txt` is not the hostname-root `/robots.txt`, so it cannot be relied upon as the site's robots policy. If moving to a custom domain, update site URLs, canonical URLs, and the sitemap base accordingly.

## Privacy and security

- **Do not commit:** `local/`, `.venv/`, `.env`, secret keys, private databases, resume PDFs, raw account exports, or unpublished personal files.
- All public `data/` exports, images, captions, project descriptions, and links are accessible to everyone. Review them before merging.
- A public GitHub repository also exposes commit history. Removing a file from the latest commit does not delete old copies from history.
- The local admin is intended for `127.0.0.1` on the author's own Mac, not internet hosting.
- Do not add private phone numbers, home addresses, personal API keys, or passwords to repository files.

## Status

V15 is an additive upgrade. Personal AI remains a future/in-progress project; **no working AI demo is claimed or bundled**. A publicly downloadable resume is deliberately not included.

## License and media

Code and photography are not declared open-source or Creative Commons unless a separate license explicitly says so. Contact the repository owner before reusing original photographs.
