# GCETTS site — images setup

Two image areas: **faculty headshots** and the **event gallery**.
Both degrade gracefully — missing images never break the page (faculty falls
back to initials; gallery shows a styled placeholder tile).

---

## 1. Faculty photos (permanent + fast)

The faculty page now points at local files in `assets/faculty/`.
Each `<img>` tries, in order:

1. `assets/faculty/<slug>.jpg`  (your local copy — fast, permanent)
2. the original Google-hosted URL  (fallback if the local file is missing)
3. a coloured monogram with the person's initials  (final fallback)

### Get the photos in one step

From your repo root, run **either**:

    python3 download_faculty_photos.py      # cross-platform

or

    bash download_faculty_photos.sh         # macOS / Linux (curl)

This creates `assets/faculty/` and saves all 30 photos with the exact
filenames the page expects. Re-run any time to refresh; existing files are
skipped (python version).

- `faculty_photos_manifest.csv` — filename, name, department, source URL
- `faculty-photo-filenames.txt` — the same list, human-readable

If you ever replace a photo, just overwrite the file of the same name.

---

## 2. Event gallery

Open `gallery.html` and edit the `GALLERY = [ ... ]` block near the top of the
script. Each event looks like:

    { id:"texavision", title:"TEXAVISION — Annual Fest", date:"January",
      featured:true, blurb:"...", photos:[ ... ] }

A photo in `photos:[ ]` can be any of:

- **Local file**  — `"assets/gallery/texavision/01.jpg"`
- **Google Drive** — `{ drive:"FILE_ID", cap:"Optional caption" }`
- **Any URL**     — `{ src:"https://…/photo.jpg", cap:"Optional caption" }`

You can mix all three in one event.

### Folder layout for local images

    assets/
      gallery/
        texavision/   01.jpg 02.jpg 03.jpg ...
        convocation/  01.jpg 02.jpg ...
        workshops/    ...
        sports/       ...
        campus/       ...

### Using Google Drive (no download needed)

1. Upload photos to a Drive folder.
2. For each file: Share → General access → **Anyone with the link** (Viewer).
3. Open the file; its link looks like
   `https://drive.google.com/file/d/THIS_IS_THE_ID/view`.
4. Put `THIS_IS_THE_ID` into `{ drive:"THIS_IS_THE_ID" }`.

The page builds the displayable image URL automatically as
`https://drive.google.com/thumbnail?id=<ID>&sz=w1600`.

> Tip: local files load fastest and never rate-limit. Drive is great when you
> want to update albums without committing large images to the repo.

### How the gallery is organised
- **Album landing grid** — every event shows as a cover-thumbnail card
  (auto-uses the first photo, or set `cover:` explicitly). A large **featured
  banner** sits on top (mark one event `featured:true`).
- **Click a card** → that album opens (its masonry of photos) with a
  "← All albums" back button and Prev/Next album navigation.
- **Lightbox** — arrow keys (← →), Esc, swipe on mobile, click-outside,
  photo counter and captions.
- Lazy loading, hover zoom + caption, scroll-reveal, reduced-motion aware.

---

## 3. Auto-import a Google Drive folder (no manual lists)

Instead of typing photo arrays, point each event at a **Drive folder** and let
the script build the data for you.

1. `pip` not needed — it uses only Python's standard library.
2. Get a free Google API key (Drive API enabled) — see the header comment in
   `build_gallery_from_drive.py`.
3. Edit `API_KEY` and the `EVENTS` list (id, title, date, folder URL/id).
4. Run:

        python3 build_gallery_from_drive.py

   It writes **`gallery-data.js`** next to `gallery.html`. The page picks it up
   automatically (`window.GALLERY_DATA`) and overrides the built-in sample data.
   Re-run any time you add photos to a folder.

Make sure each Drive folder is shared **Anyone with the link → Viewer**.

---

## 4. Faster images: responsive variants (optional)

`optimize_images.py` pre-resizes local images into `name-400.jpg`,
`name-800.jpg`, `name-1280.jpg` (+ `.webp`), which the gallery serves via
`srcset` so phones download small files and desktops get sharp ones.

    pip install pillow
    python3 optimize_images.py

Then enable local responsive images by adding one line to `gallery-data.js`
(or any small script that runs before the gallery):

    window.GALLERY_RESPONSIVE_LOCAL = true;

Notes:
- Google Drive photos are **already responsive** (the page requests multiple
  widths automatically) — the flag above only affects **local** files.
- All `<img>`s use `loading="lazy"` and `decoding="async"` regardless.

---

## 5. Automatic builds on every push (GitHub Action)

`.github/workflows/deploy.yml` rebuilds and deploys the site automatically
whenever you push to `main`:

1. Generates responsive image variants (`optimize_images.py`) and writes
   `gallery-responsive.js` — so local `srcset` switches on by itself.
2. **Optionally** rebuilds `gallery-data.js` from your Drive folders
   (`build_gallery_from_drive.py`) — only if a secret API key is set.
3. Publishes the result to GitHub Pages.

Generated files (image variants, `gallery-data.js`, `gallery-responsive.js`)
are produced during the build and deployed — they are **not** committed back,
so your repo stays clean and there are no commit loops.

### One-time setup
1. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Commit your source files (`index.html`, `faculty.html`, `gallery.html`,
   the `.py` scripts, and any images under `assets/`) plus this workflow.
3. Push to `main`. The Action runs and your site goes live.

### To enable the Drive import in CI (optional)
1. Edit the `EVENTS` list in `build_gallery_from_drive.py` with your real
   folder URLs/ids and commit it (folder ids are not secret).
2. Repo **Settings → Secrets and variables → Actions → New repository secret**
   named **`GALLERY_DRIVE_API_KEY`** with your Google API key.
3. The workflow auto-detects the secret and runs the import step; without it,
   that step is skipped and your committed `gallery-data.js` (or sample data)
   is used.

> Prefer classic branch-based Pages instead? Then drop the `deploy` job and the
> Pages steps, and replace them with a step that commits the generated files
> back to the branch your Pages serves from. The Actions-based deploy above is
> the cleaner default.
