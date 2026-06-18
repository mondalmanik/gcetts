#!/usr/bin/env node
/*
 * precompile.js — ahead-of-time JSX compilation for production.
 *
 * Each page keeps an editable inline <script type="text/babel"> for easy local
 * editing/preview (the browser compiles it via @babel/standalone). For the
 * deployed copy we don't want visitors to download or run Babel at all, so this
 * script compiles that inline JSX to plain JavaScript and writes a production
 * copy of every page into the output directory:
 *
 *   - the <script type="text/babel" ...>…</script> becomes a plain <script>…</script>
 *     containing React.createElement(...) output
 *   - the @babel/standalone CDN <script> tag is removed (no longer needed)
 *   - React / ReactDOM CDN tags are kept (still required at runtime)
 *
 * Source files are NOT modified — only the copies written to OUT.
 *
 * Usage:  node precompile.js [srcDir] [outDir]
 *         defaults: srcDir="."  outDir="_site"
 *
 * Requires @babel/standalone to be installed (npm install @babel/standalone).
 */
const fs = require("fs");
const path = require("path");
const Babel = require("@babel/standalone");

const SRC = process.argv[2] || ".";
const OUT = process.argv[3] || "_site";

const PAGES = [
  "index.html", "faculty.html", "gallery.html", "notices.html",
  "departments.html", "contact.html", "research.html", "emagazine.html",
  "aicte.html",
];

const BABEL_RE = /<script type="text\/babel"[^>]*>([\s\S]*?)<\/script>/;
const STANDALONE_RE = /[ \t]*<script[^>]*@babel\/standalone[^>]*><\/script>\r?\n?/g;

fs.mkdirSync(OUT, { recursive: true });

let compiledCount = 0, copiedCount = 0;
for (const name of PAGES) {
  const src = path.join(SRC, name);
  if (!fs.existsSync(src)) { console.warn("skip (missing): " + name); continue; }
  let html = fs.readFileSync(src, "utf8");
  const m = html.match(BABEL_RE);
  if (!m) {
    fs.writeFileSync(path.join(OUT, name), html);
    copiedCount++;
    console.warn("no inline JSX, copied as-is: " + name);
    continue;
  }
  let code;
  try {
    code = Babel.transform(m[1], { presets: ["react"], filename: name }).code;
  } catch (e) {
    console.error("FAILED to compile " + name + ": " + e.message);
    process.exit(1);
  }
  html = html.replace(BABEL_RE, "<script>\n" + code + "\n</script>");
  html = html.replace(STANDALONE_RE, "");
  fs.writeFileSync(path.join(OUT, name), html);
  compiledCount++;
  console.log("compiled: " + name);
}
console.log("Precompiled " + compiledCount + " page(s), copied " + copiedCount + ", into " + OUT + "/");
