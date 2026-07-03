# HTML Export Playbook

The package must double as a **presentation**. Every build (and every don't-build) ships the primary document as a self-contained HTML file next to the Markdown:

- `PRD.md` → `PRD.html`
- `VERDICT.md` → `VERDICT.html`

`PRD.md` stays the single source of truth — the HTML is a render of it, regenerated whenever it changes (revise mode step 6). Never hand-edit the HTML as the master.

Diagrams are authored as **D2** (`terrastruct/d2`), not mermaid — D2's output is markedly cleaner (curved connectors, real SQL tables, proper containers), it supports **native animated connections**, and it renders from pure WASM with **no headless browser**. It stays text-authored, so the regenerate-from-source workflow is unchanged.

## What "presentation-ready" means (the bar)

1. **One file, opens offline.** Double-click → renders in any browser with **no network**. No `<link>`/`<script src>` to a CDN, no external fonts or images. Everything inlined. (Same rule as any artifact Iqbal owns — own the folder.)
2. **Every diagram rendered.** No raw diagram source showing as code, no blank boxes. If a diagram won't compile, fix the D2 — don't ship it broken.
3. **Legible on a projector.** Real type scale, generous whitespace, body capped ~72ch, diagrams full-width. A stakeholder deliverable, not a dumped `<pre>`.
4. **Two modes:** a scrollable **doc** view with a sticky section nav, and a **Present** toggle where each `##` section is a slide (←/→/Space to move, Esc to exit).
5. **Prints clean.** Browser "Print → Save as PDF" gives one section per page, nav hidden, diagrams fit the page — a shareable PDF with zero extra work. D2's connection animation auto-stops in print.

## Rendering — D2 → inline SVG

D2 ships as an ESM WASM package: `npm install @terrastruct/d2` (no Chrome, no system binary). Write each diagram to a `.d2` file, then render with a small **ESM** script (`.mjs` — the package is ESM-only):

```js
// render-d2.mjs  — reads d2/*.d2, writes diagrams/*.svg
import { D2 } from '@terrastruct/d2';
import { readFileSync, writeFileSync } from 'fs';
const d2 = new D2();
for (const n of ['flow','er','seq','arch','build']) {
  const src = readFileSync(`d2/${n}.d2`, 'utf8');
  const c   = await d2.compile(src, { layout: 'dagre', themeID: 0, sketch: false, pad: 16 });
  const svg = await d2.render(c.diagram, c.renderOptions);   // self-contained SVG (fonts inlined)
  writeFileSync(`diagrams/${n}.svg`, svg);
}
process.exit(0);
```

Then inline each `diagrams/*.svg` into its section in the HTML (strip any leading `<?xml …?>`). The SVG carries its own styles, fonts, and connection animation — nothing external.

## Diagram styling — colour semantics + animated arrows

Default D2 already reads as designed. Two things make it *yours*:

**Colour semantics** — same *kind* of node, same colour. Put this `classes` block at the top of any diagram and tag nodes; this is the single biggest "looks intentional" lever:

```d2
classes: {
  entry: { style: { fill: "#eef2ff"; stroke: "#6366f1"; font-color: "#3730a3" } }  # actor / start / end
  proc:  { style: { fill: "#f1f5f9"; stroke: "#64748b"; font-color: "#0f172a" } }  # process / service
  store: { style: { fill: "#fef3c7"; stroke: "#f59e0b"; font-color: "#92400e" } }  # datastore
  ext:   { style: { fill: "#ccfbf1"; stroke: "#14b8a6"; font-color: "#0f766e" } }  # external / 3rd-party
}
visitor: Visitor lands { shape: oval; class: entry }
api: API { class: proc }
db: Save { shape: cylinder; class: store }
```

Convention: **entry/actor** = indigo, **process** = slate, **datastore** = amber, **external** = teal. Reinforce with shape (`oval` for actors, `cylinder` for stores, `diamond` for decisions, `sql_table` for schema). Keep to ~4 colours.

**Animated arrows** — native, per connection. No CSS trick, and it auto-stops in print:

```d2
visitor -> api: { style.animated: true }
api -> db: submit { style.animated: true }
```

## D2 gotchas (these will bite once each)

- **ESM only** — the render script must be `.mjs` (or `"type":"module"`), and use `import`, not `require`.
- **Reserved keywords can't be bare keys.** `label`, `class`, `style`, `shape`, `icon`, `constraint`, `direction`, `link`, `tooltip`, `width`, `height`, `near` are D2 keywords. To use one as a literal node/column name (e.g. a SQL column called `label`), **quote it**: `"label": text` — otherwise D2 silently renames the *table* to "text" instead of adding the column.
- **Braces in a label** are parsed as a map. Quote the whole label: `a -> b: "200 {url}"`, not `a -> b: 200 {url}`.
- **SQL tables**: `shape: sql_table`, columns as `name: type { constraint: primary_key | foreign_key }`. **Sequence**: top-level `shape: sequence_diagram`. **Containers**: nest nodes inside a parent block.

## The deck shell (engine-agnostic — nav + Present + print)

The HTML frame around the diagrams is the same regardless of diagram engine. Assemble each PRD `##` section as `<section id="…"><h2>…</h2>… <div class="diagram">‹inlined svg›</div></section>`.

```html
<style>
  :root { color-scheme: light dark;
    --bg:#fff; --fg:#0f172a; --muted:#64748b; --line:#e2e8f0; --accent:#6366f1; }
  @media (prefers-color-scheme: dark) { :root {
    --bg:#0b1120; --fg:#e2e8f0; --muted:#94a3b8; --line:#1e293b; --accent:#818cf8; } }
  body { margin:0; background:var(--bg); color:var(--fg); font:17px/1.65 Inter, system-ui, sans-serif; }
  .wrap { display:grid; grid-template-columns:260px 1fr; }
  nav.toc { position:sticky; top:0; align-self:start; height:100vh; overflow:auto;
    padding:2rem 1.5rem; border-right:1px solid var(--line); }
  nav.toc a { display:block; color:var(--muted); text-decoration:none; padding:.4rem .6rem;
    border-radius:8px; font-size:.9rem; }
  nav.toc a:hover, nav.toc a.on { color:var(--fg); background:color-mix(in srgb, var(--accent) 12%, transparent); }
  main { padding:2.5rem clamp(1.25rem,5vw,4.5rem); }
  main > section { max-width:74ch; padding-bottom:2.5rem; margin-bottom:2.5rem; border-bottom:1px solid var(--line); }
  h2 { font-size:1.5rem; letter-spacing:-.02em; }
  /* diagram card: always light, so text is always dark even in a dark deck */
  .diagram { margin:1.4rem 0; padding:1.5rem; background:#fff; border:1px solid var(--line);
    border-radius:16px; box-shadow:0 1px 3px rgba(15,23,42,.06), 0 10px 30px rgba(15,23,42,.05);
    overflow-x:auto; color:#1e293b; }
  .diagram svg { max-width:100%; height:auto; display:block; margin:0 auto; }
  .diagram foreignObject div, .diagram span { color:#1e293b; }   /* safety if an engine emits uncoloured labels */
  .present-btn { position:fixed; top:1rem; right:1rem; z-index:10; cursor:pointer; border:1px solid var(--line);
    background:var(--accent); color:#fff; font:600 .85rem Inter,sans-serif; padding:.5rem .9rem; border-radius:10px; }
  body.present nav.toc, body.present .hint { display:none; }
  body.present .wrap { grid-template-columns:1fr; }
  body.present main { display:flex; align-items:center; justify-content:center; min-height:100vh; padding:4vh 6vw; }
  body.present main > section { display:none; max-width:1000px; width:100%; border:0; margin:0; padding:0; }
  body.present main > section.active { display:block; animation:fade .35s ease; }
  body.present h2 { font-size:2.1rem; }
  @keyframes fade { from{opacity:0; transform:translateY(8px);} to{opacity:1;} }
  @media print { nav.toc, .present-btn, .hint { display:none; } .wrap { display:block; }
    main > section { break-before:page; border:0; max-width:none; } .diagram { box-shadow:none; } }
</style>

<button class="present-btn" onclick="togglePresent()">▶ Present</button>
<div class="wrap">
  <nav class="toc"><!-- one <a href="#id"> per section --></nav>
  <main><!-- sections with inlined diagrams --></main>
</div>
<script>
  const secs = () => [...document.querySelectorAll('main > section')];
  let i = 0;
  function show(n){ const s=secs(); i=Math.max(0,Math.min(n,s.length-1));
    s.forEach((el,x)=>el.classList.toggle('active',x===i)); s[i].scrollIntoView({block:'nearest'}); }
  function togglePresent(){ const on=document.body.classList.toggle('present');
    document.querySelector('.present-btn').textContent = on ? '✕ Exit' : '▶ Present'; if(on) show(i); }
  addEventListener('keydown', e => {
    if(!document.body.classList.contains('present')) return;
    if(e.key==='ArrowRight'||e.key===' '){ show(i+1); e.preventDefault(); }
    if(e.key==='ArrowLeft') show(i-1);
    if(e.key==='Escape') togglePresent();
  });
</script>
```

Wrap each `##` heading and its content in a `<section id>` so nav and Present work off the same structure. The `.diagram` card is intentionally always light — D2 text is dark, so it stays legible whether the viewer's deck is light or dark.

## Don't-build packages

`VERDICT.md` gets the same treatment → `VERDICT.html`. It's shorter, but a "deploy X instead / here's why not now" call is exactly the thing a stakeholder wants walked through — so it ships as a deck too.
