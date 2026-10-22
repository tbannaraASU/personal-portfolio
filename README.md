# Than Bannarat — Portfolio V8: Hashtag Pages + Albums + SQLite Manager

A real photography portfolio for **@foto_4th**, with **92 photographs**, **71 photo sets**, **30 imported hashtags**, and **4 starter albums** based on real hashtags in the supplied Instagram archive. The public gallery is static and can be published on GitHub Pages; editing happens privately on your Mac with Python and SQLite.

## What changed in V8

- `photography.html`: no longer displays all photo sets from all tags together. Shows **hashtag collection cards** and a separate **Albums** tab.
- `tag.html?tag=%23filmphotography`: a dedicated URL per hashtag. Only matching photo sets appear. Toggle to **Related albums** to see curated albums containing those photos.
- `album.html?id=film-stories`: a dedicated page for each manually curated album. Photos from different hashtags can be in the same album.
- Each photo set is a clickable multi-image viewer, with previous/next navigation and original captions and tags.
- Local Admin `/admin`: upload photos and assign them to albums; edit an existing photo set's caption, tags, and album memberships; **create, rename, describe, set cover for, and delete albums**; **create, rename/merge, and delete hashtags**.
- Changes are stored in `local/gallery.sqlite` and automatically exported to `data/gallery.json` + `data/gallery-data.js` for GitHub Pages. No cloud server required.

## What a hashtag is vs. an album

- A **hashtag** is a label assigned to a photo set. One set may have multiple hashtags and therefore appear on multiple separate tag pages. Tag pages are generated dynamically from metadata, so you don't have to create 30 individual HTML files.
- An **album** is a curated set of whole photo sets, independently chosen in Admin. It can contain photos with different tags. One photo set can belong to multiple albums.
- Albums with no assigned photo sets remain editable in Admin but won't appear in public pages until populated.
- The supplied V8 database has 4 *starter* albums assembled from **existing real tags**: Film Stories (`#filmphotography`), Fujifilm Frames (`#fujifilm`), Panoramic Stories (`#panoramicphotography`), and Black & White (`#blackwhitephotography`). These groupings are automatically seeded suggestions, not claims that the Instagram creator curated those albums.

## Run on Mac

```bash
cd ~/ASU/Capstone/GitHub_Competency_Starter
source .venv/bin/activate
python tools/admin_server.py
```

Open:

| What | URL |
|---|---|
| Portfolio home | http://127.0.0.1:8765/index.html |
| Collections & albums overview | http://127.0.0.1:8765/photography.html |
| Film hashtag page | http://127.0.0.1:8765/tag.html?tag=%23filmphotography |
| Film album page | http://127.0.0.1:8765/album.html?id=film-stories |
| Private Admin | http://127.0.0.1:8765/admin |

Your Mac must have Python and Pillow (`python -m pip install Pillow`). Stop with **Control+C**. Restart the server after replacing Python code.

## SAFE upgrade from V6/V7 (keep your existing photos and edits)

**Back up your repository and local database before changing files.** If you already added photos via the V6 Admin, do NOT replace your existing `local/gallery.sqlite` with the copy from the ZIP. That would discard edits made after the previous version.

1. In Terminal in your existing repository, run `git status`. Commit or back up changes before switching branches. Then `git switch main` and `git pull origin main` (only after you have a clean working directory). Run `git switch -c feature/album-tag-pages`.
2. Extract the ZIP. Copy the updated `photography.html`, **new** `tag.html` and `album.html`, `photography.css`, `photography.js`, `tools/` and `README.md` into your existing repository. Copy `index.html` only if you want the supplied V8 version to replace your local version.
3. If your existing `photos/` already includes additions made since V6, keep that folder and add only missing photos. Similarly, preserve any newer `data/` until you rebuild from your own database.
4. **Preserve `local/gallery.sqlite` already on your Mac.** The upgraded Python code will create the new `albums` and `album_posts` tables automatically, without deleting existing posts/photos. If you wish to create the optional starter albums from your existing actual tags, run:

   ```bash
   python tools/gallery.py seed-albums
   ```

   Otherwise create only your own albums using Admin.
5. Export static data (especially if you skipped starter albums):

   ```bash
   python tools/gallery.py build
   python tools/gallery.py status
   ```

6. Stop any running old Admin server with Control+C, then start the upgraded one: `python tools/admin_server.py`. Visit `/admin`, `/photography.html`, a tag page and an album page to verify.

**If starting fresh:** Extract the full V8 ZIP as its own directory. It already contains the 92 original photos and the imported local SQLite database with 4 starter albums. Do not overwrite a database containing your newer work.

## Using Admin

**New photo set:** Choose 1–12 photographs, set Title, Caption, Hashtags and optional Date/Instagram URL, tick the album(s) it belongs to, then click **Add photo set**. Images are re-encoded using Pillow to strip EXIF/GPS metadata. Photos, SQLite and gallery exports update together.

**Edit photo set:** Choose a photo set, change title/caption/hashtags, tick or untick assigned albums, click **Save photo set**.

**Album manager:** Choose an existing album to edit or enter a name to **Create new album**. Search the photo sets, tick the desired ones, choose an optional cover, then Save. Deleting an album does **not** delete photographs or tags.

**Tag manager:** Add a hashtag, rename it (renaming to an existing tag merges them), or delete it. Renaming/deleting tags updates all photo set relationships but does not rewrite the original Instagram captions, and never deletes images. A newly created tag without assigned photos is hidden from the public collection overview until you tag a photo set with it.

## Publish to GitHub Pages

From a current feature branch, after reviewing your photos for consent and privacy:

```bash
git add index.html photography.html tag.html album.html photography.css photography.js README.md tools/ data/ photos/ .gitignore
git status
git commit -m "Add dedicated hashtag pages and editable photography albums"
git push -u origin feature/album-tag-pages
```

Open a Pull Request and merge to `main`, then enable GitHub Pages from `main` / root if not already enabled. In subsequent releases, Push updated HTML/CSS/JS if changed, `data/` JSON/JS and `photos/` only. Do **not** commit `local/`, `.venv/`, private ZIP archives, or original Instagram account exports.

### Technical details

Local relational structure: `posts` 1:N `photos`, `posts` N:M `hashtags` via `post_hashtags`, `albums` N:M `posts` via `album_posts`. The tags overview and the album pages are rendered from static JSON in the browser. **SQLite cannot run on GitHub Pages.** The local manager regenerates published JSON on every successful edit.

This project does not scrape Instagram or sync continuously. To import newer Instagram posts, use your own JSON export with `python tools/gallery.py import-instagram ARCHIVE.zip --include-unlinked` followed by `python tools/gallery.py build`, or upload manually through the local Admin.
