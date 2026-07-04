# Status: ai-tools-affiliate

**PRD version:** v1.0
**Started:** —
**Last updated:** 2026-07-03 by masterplan (package creation)

**Marker convention:**
- `[ ]` pending
- `[x]` done — only with evidence in the note (evidence rule in EXECUTE.md)
- `[!]` needs rework — set by revise mode when a change invalidated a built milestone; treat as unchecked and rebuild per its note. Never silently uncheck history; `[!]` preserves the fact that it was built once.

## Milestones

- [ ] **M1 — Scaffold** — adapt minted-directory-astro; site runs locally with template demo content.
  - Note: —
  - Evidence: —
- [ ] **M2 — Schemas & data** — tools.json format + zod content-collection schemas; build fails on a deliberate bad entry.
  - Note: —
  - Evidence: —
- [ ] **M3 — Redirect layer** — /go/<slug> from tools.json + click-logging Pages Function; unknown slug → 404.
  - Note: —
  - Evidence: —
- [ ] **M4 — Layouts** — tool profile + comparison article (verdict table, rank badges, per-row CTA, our-pick box, disclosure, lastReviewed).
  - Note: —
  - Evidence: —
- [ ] **M5 — Legal & SEO surface** — /about /privacy /terms, 404, empty states, sitemap, robots.txt, canonicals, OG images, schema.org.
  - Note: —
  - Evidence: —
- [ ] **M6 — Content pipeline + seed batch** — generator script; 5 articles + 15 profiles generated from owner-verified seed data, all validating.
  - Note: —
  - Evidence: —
- [ ] **M7 — Deploy** — live on Cloudflare Pages + domain; analytics wired; /go/ logging verified in production. *(needs owner credentials — see EXECUTE rule 4)*
  - Note: —
  - Evidence: —
- [ ] **M8 — Full QA pass** — run every acceptance criterion from the PRD end-to-end and record evidence; Lighthouse ≥90 perf / ≥95 SEO; 375px verified.
  - Note: —
  - Evidence: —

## Blockers

*(none)* — when blocked, record: what, since when, what is needed to unblock, and which milestone it stops.
