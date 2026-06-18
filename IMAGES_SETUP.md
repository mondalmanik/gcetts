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

---

## 6. Notices & Tenders (Drive-backed, newest first)

The **Notices & Tenders** page (`notices.html`) and the homepage ticker read a
date-sorted feed of files from two Drive folders — the same pattern as the
gallery.

Files involved:
- `drive-feed.js` — shared loader (used by `index.html` and `notices.html`)
- `notices-data.js` — the generated data (ships with clearly-labelled SAMPLE
  rows so you can see the UI; replaced by the build step below)
- `build_notices_from_drive.py` — generates `notices-data.js` from Drive

### Generate from Drive
1. Put your two folders in `build_notices_from_drive.py`
   (`NOTICES_FOLDER`, `TENDERS_FOLDER`) — each shared *Anyone with link: Viewer*.
2. Provide the key: `export DRIVE_API_KEY=xxxx` (or reuse the same
   `GALLERY_DRIVE_API_KEY` secret in CI).
3. Run:

        python3 build_notices_from_drive.py

   -> writes `notices-data.js`, files newest-first, with type icons (PDF/DOC/…),
   dates, a "New" badge for the last 14 days, search and tabs on the page.

### Homepage ticker
The scrolling strip under the hero shows the **latest 3 notices + 1 tender**.
If both feeds are empty it renders **nothing** (the strip disappears).

### Optional: live mode (no rebuilds)
Create `drive-config.js` (don't commit a secret key — restrict it by HTTP
referrer in Google Cloud) :

    window.DRIVE_CONFIG = {
      apiKey: "YOUR_REFERRER_RESTRICTED_KEY",
      noticesFolder: "https://drive.google.com/drive/folders/...",
      tendersFolder: "https://drive.google.com/drive/folders/..."
    };

If present (and no generated `notices-data.js`), the page/ticker fetch Drive
live in the browser.

### CI behaviour
`.github/workflows/deploy.yml` now also:
- runs `build_notices_from_drive.py` when the Drive key secret is set,
- **empties** `notices-data.js` on deploy when no key is set (so the sample
  never shows on a real site), and
- runs on a **6-hourly schedule** so new notices/tenders go live automatically
  without a code push.

---

## 7. Latest News carousel (homepage)

The homepage shows an auto-scrolling **"Latest News"** band of images pulled from
a single Drive folder. Each image's caption is its **file name without the
extension** — so naming a file `Convocation 2025.jpg` shows "Convocation 2025"
on the image.

Files involved:
- `drive-feed.js` — shared loader (already used for notices); now also resolves
  the Latest News images
- `latestnews-data.js` — the generated data (ships with clearly-labelled SAMPLE
  tiles; replaced by the build step below)
- `build_latestnews_from_drive.py` — generates `latestnews-data.js` from Drive

### Generate from Drive
1. Put your image folder in `build_latestnews_from_drive.py`
   (`LATEST_NEWS_FOLDER`) — shared *Anyone with link: Viewer*.
2. Provide the key: `export DRIVE_API_KEY=xxxx` (or reuse the same
   `GALLERY_DRIVE_API_KEY` secret in CI).
3. Run:

        python3 build_latestnews_from_drive.py

   -> writes `latestnews-data.js`, images newest-first, captions from filenames.

### Behaviour
- The band auto-scrolls, pauses on hover, fades at both edges, and respects
  "reduce motion" (becomes a normal horizontal scroll).
- If the folder is empty (or no data file), the **entire section is hidden**.
- Optional live mode: add `latestNewsFolder` to `window.DRIVE_CONFIG` in
  `drive-config.js` to fetch in the browser without rebuilds.

### CI behaviour
`.github/workflows/deploy.yml` now also runs `build_latestnews_from_drive.py`
when the Drive key secret is set, and **empties** `latestnews-data.js` on deploy
when no key is set (so the sample never shows on a real site). The existing
6-hourly schedule keeps it fresh.


---

## 8. Research Highlights box (homepage, right of Latest News)

The homepage now shows **two side-by-side single-image boxes** that auto-advance
from inside the box:

- **Latest News** (left) — folder set in `build_latestnews_from_drive.py`
- **Research Highlights** (right) — a *different* folder, set in
  `build_research_highlights_from_drive.py`

Both behave the same: one image at a time slides within a fixed box, captions are
the file names without extension, dots let you jump, hover pauses, and clicking
opens the enlarged lightbox. Each box hides itself if its folder is empty.

### Generate Research Highlights from Drive
1. Put your image folder in `build_research_highlights_from_drive.py`
   (`RESEARCH_HIGHLIGHTS_FOLDER`) — shared *Anyone with link: Viewer*.
2. `export DRIVE_API_KEY=xxxx` (or reuse the `GALLERY_DRIVE_API_KEY` secret).
3. Run:

        python3 build_research_highlights_from_drive.py

   -> writes `research-highlights-data.js`, images newest-first.

### Optional live mode
Add `researchHighlightsFolder` (and `latestNewsFolder`) to `window.DRIVE_CONFIG`
in `drive-config.js` to fetch live in the browser without rebuilds.

### CI behaviour
`.github/workflows/deploy.yml` runs both image builders when the Drive key secret
is set, and empties both `latestnews-data.js` and `research-highlights-data.js` on
deploy when no key is set (so samples never show on a real site). The 6-hourly
schedule keeps them fresh.

---

## 9. Ahead-of-time JSX compile (no Babel in the browser)

Pages are written with an editable inline `<script type="text/babel">` so you can
open and preview any `.html` file directly. For the **deployed** site, CI now
compiles that JSX to plain JavaScript so visitors never download or run Babel
(faster, and immune to CDN/Babel version changes blanking the page).

- `precompile.js` — Node script: for each page it compiles the inline JSX to
  `React.createElement(...)`, removes the `@babel/standalone` `<script>`, keeps
  React/ReactDOM, and writes the production copy into `_site/`. **Source files
  are not modified.**
- The deploy workflow runs `npm install @babel/standalone` then
  `node precompile.js . _site`, and the asset copy step now excludes `*.html`
  (the compiled copies already live in `_site`).

Run it locally to preview the production output:

    npm install @babel/standalone@7.26.7
    node precompile.js . dist
    # open dist/index.html — it has no Babel and runs the compiled JS

Editing stays the same: change the JSX in the source `.html` files; CI compiles
on deploy.

---

## 10. AICTE EOA Reports page (auto-listing a Drive folder)

`aicte.html` lists the institute's **AICTE EOA Reports** Drive folder. Any file
(or sub-folder) added to that folder appears on the page automatically — no code
change needed.

Files involved:
- `drive-feed.js` — shared loader (now also resolves the AICTE folder)
- `aicte-data.js` — generated data (ships with a clearly-labelled sample)
- `build_aicte_from_drive.py` — lists the folder into `aicte-data.js`

### How auto-update works
- The folder id is already set in `build_aicte_from_drive.py` (the institute's
  public AICTE EOA folder). With the `GALLERY_DRIVE_API_KEY` secret set, CI runs
  the builder on every push **and on the 6-hourly schedule**, so newly uploaded
  EOA letters show up within a few hours with no edits.
- For instant updates, enable live mode: in `drive-config.js` set
  `window.DRIVE_CONFIG = { apiKey:"…", aicteFolder:"…folder url/id…" }`.
- Items are newest-first; sub-folders (e.g., year folders) are shown too and open
  in Drive. The empty state links straight to the folder.

### CI behaviour
The deploy workflow builds `aicte-data.js` from Drive when the key is set, and
empties it when no key is set (so the sample never shows on a live site).
