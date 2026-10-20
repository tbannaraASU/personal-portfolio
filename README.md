# Than Bannarat — Photography Portfolio V5 / @foto_4th

A static, mobile-friendly personal portfolio with an Instagram photography gallery **grouped automatically by actual hashtags**. Includes SQLite for managing post, photo, and hashtag relationships locally.

## What is in this download?

- `index.html` — your existing main portfolio, linked to the gallery
- `photography.html`, `photography.css`, `photography.js` — photo gallery page, filter/search, responsive design, modal photo viewer, persisted dark/light theme
- `tools/gallery.py`, `tools/schema.sql` — imports Instagram export or curated CSV into SQLite, builds static web data
- `data/gallery-data.js`, `data/gallery.json` — metadata output published with the website (empty until you import photos)
- `data/photos_template.csv` — CSV format for manually adding photo sets
- `photos/` — images imported intentionally from your own photos
- `local/gallery.sqlite` — PRIVATE local database created when importing; excluded from Git

**Important:** I could not retrieve the image/caption/hashtag data directly from Instagram. This download contains **no guessed images, posts, or hashtags**. The gallery will show an import-ready empty state until you import your own data.

## Option A: Import YOUR Instagram posts (recommended)

1. On Instagram, open **Settings → Accounts Center → Your information and permissions → Export your information** (labels may vary).
2. Choose **@foto_4th**, choose posts/media if the export allows, select **JSON** rather than HTML, and include photo media. Choose only content you intend to publish on a public website.
3. Download the resulting ZIP to your Mac. Keep it private; do NOT commit the original ZIP or share a full account export publicly.
4. From Terminal in this folder:

```bash
python3 -m pip install Pillow  # optional but recommended to strip photo EXIF metadata
python3 tools/gallery.py import-instagram ~/Downloads/instagram-export.zip
python3 tools/gallery.py status
python3 tools/gallery.py build
open photography.html
```

Replace `instagram-export.zip` with the exact filename; type the path or drag the ZIP from Finder into Terminal.

The import reads `posts_1.json`, `posts_2.json`, or `posts.json` plus local image files from typical Instagram JSON archives. It imports JPG, PNG and WebP images, and skips videos/HEIC and unsupported archive structures. Instagram may change its export format: if no photo sets import, use Option B or share only the posts JSON structure so the importer can be adjusted.

## Option B: Add selected photo sets manually from CSV

Create `data/my_photos.csv` with the header:

```
id,title,caption,date,permalink,hashtags,images
```

Example only (replace with your **real** records and files before importing):

```
001,Sunset,"A view from the mountains #landscape #sunset",2026-07-10,https://www.instagram.com/p/EXAMPLE/,"#landscape #sunset","/Users/YOU/Pictures/sunset1.jpg;/Users/YOU/Pictures/sunset2.jpg"
```

Each row = one photo set / one Instagram post. `images` accepts multiple file paths separated by `;`. All images in a row appear inside one lightbox carousel. Hashtags are extracted automatically from the caption plus the optional `hashtags` column. Files are copied to `photos/` with stable names.

Then run:

```bash
python3 tools/gallery.py import-csv data/my_photos.csv
python3 tools/gallery.py build
open photography.html
```

## Database structure

- `posts`: original caption, title, publication date and link
- `photos`: one or more photos ordered per post
- `hashtags`: unique normalized hashtags (`#landscape`, `#street`, etc.)
- `post_hashtags`: many-to-many relationship: one photo set can appear in several hashtag collections

`local/gallery.sqlite` stays on your Mac and is NOT included in website files. The generator writes only the website-needed public info into `data/gallery.json` and `data/gallery-data.js`. **GitHub Pages cannot query SQLite directly**, so the `build` command generates a small static dataset the browser can read without a server. `gallery-data.js` lets you use `open photography.html` directly on macOS without a local web server.

To inspect SQL locally:

```bash
sqlite3 local/gallery.sqlite 'SELECT tag FROM hashtags ORDER BY tag;'
sqlite3 local/gallery.sqlite 'SELECT COUNT(*) FROM posts;'
```

## Publish through GitHub

1. Copy this package into the existing personal-portfolio repository after you pull your latest `main` branch. Make sure you preserve any newer edits you've already made.
2. Import only the photos you WANT to show to everyone. Review all images, captions and data; omit private locations, faces or information you do not want public.
3. Run `python3 tools/gallery.py build`, check `open photography.html`, and review `data/gallery.json`.
4. In your existing Git repository:

```bash
git switch main
git pull origin main
git switch -c feature/instagram-hashtag-gallery
git add index.html photography.html photography.css photography.js README.md .gitignore tools/ data/ photos/
git commit -m "Add Instagram hashtag photo collections with SQLite"
git push -u origin feature/instagram-hashtag-gallery
```

Create and merge a pull request on GitHub. Do **not** add `local/` or the Instagram export ZIP. The script is offline, not a live Instagram sync: rerun import + build for new posts.

## Privacy and implementation notes

- EXIF: Pillow (optional) strips image metadata on successful imports; without it, image files are copied with existing metadata. Inspect images and exported fields before publishing.
- Captions and hashtags are treated as text in JavaScript; no user content is inserted as HTML.
- Photo URLs are local assets; no unreliable direct Instagram CDN hotlinking.
- The importer uses JSON exports and local images; it does not scrape Instagram or request login credentials.
- Imported posts without public permalinks link to the @foto_4th profile from the viewer.
- Re-importing a record with the same id updates its tags, images, and caption. Old unused photo assets might require manual cleanup.
