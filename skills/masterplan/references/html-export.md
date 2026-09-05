# HTML Export Playbook

The package doubles as a **presentation**. `masterplan.html` is a self-contained render of `masterplan.md`: one file, no build step, no external tooling, opens offline in any browser.

- `masterplan.md` → `masterplan.html`
- `VERDICT.md` → `VERDICT.html` (same treatment, on a false-premise stop)

The Markdown stays the single source of truth — the HTML is a render of it, regenerated whenever it changes (revise mode step 6). Never hand-edit the export as the master.

## How to produce it

Write the HTML directly — it is a document, not a build:

1. **Single file, fully inline.** All CSS in a `<style>` block; diagrams **inlined as SVG markup** (paste each `references/diagrams/*.svg` file's `<svg>…</svg>` into its section). No external requests of any kind — the file must open from `file://` with no network and render everything.
2. **Style from §15 Design direction.** The deck previews the product's own look: mood words, palette, typography from the masterplan's design section. Not a generic theme. Keep it readable: one section per screen block, sticky nav of section links, code blocks monospaced. Dark surface works well with the SVG diagrams' dark palette — check contrast either way.
3. **Structure mirrors the masterplan.** One top-level `<section id="s1">`…`<section id="sN">` per masterplan section, in order. Build a hierarchical table of contents: section → epic/module → linked detail document; do not flatten hundreds of documents into one list. Inline each detail document beneath its owning section or link it from that subsection, matching `references/INDEX.md`. A reader reaches every detail without searching the filesystem.
4. **Verify after writing:** open the file (browser or `python3 -m http.server` locally), confirm every section renders, every inlined SVG paints (a missing paste shows as empty space — fix and regenerate), tables are readable, zero network requests (check devtools Network tab or grep the file for `http` src/href outside anchor links). Record the check in `references/decisions.md` (Phase 6 block).

## Review use

During Gate C, hand the user the HTML file path — they open it, read, and give feedback in conversation. Revise the Markdown/SVG sources, regenerate the HTML, repeat until approved. The deck is regenerated from scratch each time; there is no incremental edit.

## Without a browser

The text package is complete on its own. If the HTML genuinely cannot be verified in the runtime, say so honestly and ship the Markdown + SVGs — never hand-roll a fake deck you could not open.
