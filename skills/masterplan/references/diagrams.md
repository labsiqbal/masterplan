# Diagram System (hand-authored SVG)

Every diagram in the package is a **standalone inline-SVG file** in the package's `references/diagrams/` folder — one file per diagram, no build step, no runtime library, no external requests. Markdown embeds them (`![](references/diagrams/<name>.svg)`), GitHub and most viewers render SVG natively, and the HTML deck inlines the same markup.

Use the runtime's `architecture-diagram` skill/capability when available. Otherwise follow this reference directly; the output contract stays the same on every runtime. Design system adapted from that skill (MIT, Cocoon AI): dark tech aesthetic, semantic colors, grid background.

## File shape

Single `.svg` file, `viewBox` sized to content, everything inline:

- **Background:** slate-950 `#020617` with a 40px grid pattern (`stroke="#1e293b"`, `stroke-width="0.5"`)
- **Font:** `font-family="'JetBrains Mono', monospace"` on the root `<svg>`; sizes 12px names, 9px sublabels, 8px annotations, 7px tiny
- **Components:** rounded rects `rx="6"`, 1.5px stroke. Double-rect masking: opaque `#0f172a` rect first, then the semi-transparent styled rect on top — arrows never show through
- **Arrows:** drawn early (right after the grid) so they render behind boxes; arrowheads via SVG `<marker>`; dashed `4,4` for security/async flows, `8,4` for boundaries
- **Spacing:** 60px standard component height, ≥40px vertical gaps, legend outside all boundaries
- **Title block:** top-left `<text>` — diagram name 14px `#e2e8f0`, one-line purpose 9px `#64748b`

## Semantic color map

| Component type | Fill | Stroke |
|---|---|---|
| Frontend / entry | `rgba(8, 51, 68, 0.4)` | `#22d3ee` cyan-400 |
| Backend / process | `rgba(6, 78, 59, 0.4)` | `#34d399` emerald-400 |
| Database / datastore | `rgba(76, 29, 149, 0.4)` | `#a78bfa` violet-400 |
| Cloud / hosting | `rgba(120, 53, 15, 0.3)` | `#fbbf24` amber-400 |
| Security / error | `rgba(136, 19, 55, 0.4)` | `#fb7185` rose-400 |
| Message bus / external | `rgba(30, 41, 59, 0.5)` | `#94a3b8` slate-400 |

The same kind of node always gets the same color, in every diagram of the package.

## Diagram types (per masterplan section)

- **§5 user flows** — boxes = screens/actions, arrows = transitions with edge labels; entry node cyan, success end-state emerald; one file per primary flow
- **§7 data model** — one rect per table (name + fields as sublabel lines, PK/FK marked), arrows = relations with cardinality labels (`1..n`)
- **§8 multi-actor endpoints** — lifelines as vertical dashed lines, actors as header boxes, calls as horizontal arrows top-to-bottom (a sequence diagram in SVG)
- **§11 architecture** — dashed boundary rects (`rx="12"`, `8,4`) for "what runs where" (host/region/browser), components inside, arrows between
- **§18 build order** — one box per milestone, arrows = blocking edges; independent slices visibly parallel; milestone count is NOT capped, so lay out in rows/columns as needed

## Verification (deterministic, phase-6 self-review)

1. **Well-formed XML:** `python3 -c "import xml.dom.minidom,glob;[xml.dom.minidom.parse(f) for f in glob.glob('references/diagrams/*.svg')]"` — any parse error is a broken diagram, loud not blank
2. **Coverage:** every node/actor/table named in the corresponding masterplan section appears as a `<text>` in the SVG — check by grepping the file for each name
3. **Render:** open each `.svg` in a browser (or inline into the HTML deck and open that) — colors, labels, arrows visible

Record method + outcome in `references/decisions.md` (Phase 6 block). Never mark a diagram valid by eye alone.

## When the runtime cannot produce SVG

Fall back to a Mermaid fenced block in the Markdown (renders on GitHub/most viewers), mark the diagram `MERMAID-FALLBACK` in the self-review record, and note it for later upgrade to SVG. The package is never blocked on diagram tooling.
