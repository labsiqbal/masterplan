# HTML Export Playbook

The package doubles as a **presentation**. `masterplan.html` is a self-contained render of the package: one file, opens offline from `file://` in any browser.

- `masterplan.md` → `masterplan.html`
- `VERDICT.md` → `VERDICT.html` (same treatment, on a false-premise stop)

The Markdown stays the single source of truth. The HTML is a build output, regenerated from scratch whenever the Markdown changes (revise mode included); never hand-edit it.

## How to produce it

1. **Theme from §15 Design direction.** Write `references/deck-theme.css`: a `:root{…}` block overriding the deck's custom properties (`--bg`, `--surface`, `--text`, `--muted`, `--accent`, `--border`, `--code`, `--font`, `--mono`) with the palette and typography §15 decided, so the deck previews the product's own look. Inline CSS only: no `@import`, no remote `url()`. Check text contrast against `--bg` and `--surface`.
2. **Render the diagrams.** `python3 <skill>/scripts/render-diagrams.py <package>` (`references/diagrams.md`).
3. **Build.** `python3 <skill>/scripts/build-deck.py <package>`. It renders the source document plus every package document under `references/` (evidence excluded) into one file with a hierarchical table of contents (masterplan sections, then documents by folder), turns local `.md` links into in-deck anchors, inlines each rendered SVG where its Mermaid block sits, and embeds local images. Exit 1 names what is wrong: a missing render, duplicate SVG ids, or an external request. Fix the source and rebuild until it prints `PASS: deck built`.
4. **Look at it.** Screenshot the deck at desktop and phone width and read the screenshots: every diagram legible without zoom, no clipped nodes, tables readable, nothing overflowing the page.

   ```bash
   for size in 1280,900 390,844; do
     google-chrome --headless --no-sandbox --hide-scrollbars --window-size=$size \
       --screenshot=deck-${size%%,*}.png "file://$PWD/masterplan.html"
   done
   ```

   To see every diagram at once, screenshot a copy with `section.block>:not(figure.diagram){display:none}nav{display:none}.layout{display:block}` appended to its `<style>`. A visual defect goes back to the Mermaid source (split the chart, switch direction), then re-render and rebuild. Record the check in `references/decisions.md` (Phase 6 block).

## Review use

During Gate C, hand the reviewer the HTML file path; they read it and give feedback in conversation. Revise the Markdown, re-render, rebuild, repeat until approved.

## Without a browser or Python

The text package is complete on its own. If the deck genuinely cannot be built or viewed in this runtime, say so honestly and ship the Markdown with its Mermaid blocks; never hand-roll a deck you could not open.
