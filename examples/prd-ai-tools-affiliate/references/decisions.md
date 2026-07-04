# Decisions Log — ai-tools-affiliate

*Generator state for masterplan. Appended per phase; a fresh session resumes from the first incomplete phase.*

> **Test-drive note:** this package was produced as a worked example with the owner delegating fully — every question resolved via the "you decide" escape hatch, recorded below as agent decisions. GATE A and GATE C are marked *pending user*.

## Phase 1 — Pitch (agent-locked 2026-07-03; GATE A pending user)

A curated AI-tools review site that earns affiliate commissions. It's for people trying to pick the right AI tool for a job; the core action is reading a hands-on comparison ("best AI tool for X") and clicking a tracked affiliate link to the winning tool.

- Agent decision — niche "AI tools": owner's domain expertise, real SaaS recurring commissions, easy to research.

## Phase 2 — Prior-art verdict

**Verdict: Build with differentiation** — where "build" means *adapt, not write*: the software is commodity, covered ~80% by minted-directory-astro (MIT). Custom development from scratch was rejected.

**The one difference:** editorial depth over breadth — ~50 hands-on-tested tools with per-job verdicts, versus scraped directories of thousands with no opinion. The project's main effort is content, not code.

Scan: Futurepedia (~4,000 tools; affiliate + premium listings + sponsorship), There's An AI For That, Toolify — all breadth-first directories. Open-source reference: minted-directory-astro (MIT, 154★, Astro + Tailwind; search, tags, listings, sponsored slots, markdown/CSV/Sheets content sources).

## Phase 3 — Product decisions (all via "you decide")

| Question | Decision | Rationale |
|---|---|---|
| First user | Solo maker / small-business owner picking an AI tool for one concrete job | Highest-intent affiliate clicker |
| Today's workaround | Googling "best AI for X" → SEO spam or Reddit | The gap the editorial depth fills |
| Core feature | Comparison articles with ranked verdict + affiliate CTA | Tool pages & tag browse are secondary |
| Non-goals v1 | No user accounts, no tool-submission portal, no newsletter, no auto-scraping | Keep it a static content site |
| Budget | ~$0–10/month | Domain only; free-tier hosting |
| Revenue | Affiliate commissions only | Sponsored slots exist in template for later |
| Fate | Commercial personal project, closed repo | MIT template is license-compatible |
| Look references | Futurepedia's clean grid + Wirecutter's editorial style | Credible, clean, fast |
| Day-one content | 20 comparison articles + 50 tool profiles; AI-drafted, human-reviewed | Never ship empty |

## Phase 4 — Technical decisions

- Stack: Astro + Tailwind (inherited from the adapted template); content as markdown collections.
- No database, no backend: fully static; affiliate links are tagged outbound URLs.
- Deploy: Cloudflare Pages free tier. Analytics: Cloudflare Web Analytics (free).
- Owner-provided credentials: affiliate program accounts (Impact / PartnerStack / per-vendor), Cloudflare account, domain.
- Reference map: minted-directory-astro (MIT → code, adapt directly); Wirecutter (pattern only — review format); Futurepedia (pattern only — tool cards/grid).

## Phase 5 — Validation

Red-team run 2026-07-03 (fresh agent, decision summary only). Full report: `validation-report.md`. 4 blockers, 5 improvements, 2 nice-to-haves.

**Blockers → decision revisions (all accepted):**
1. *Fabricated verdicts* — the one-shot deliverable is now the **machine** (site + schema + redirect layer + content pipeline), never tool facts. Verified tool data (pricing, tested verdicts) enters via a structured `tools.json` seed file the owner curates; the agent generates pages from data and never invents tool facts.
2. *Affiliate links unavailable at build time* — every outbound CTA routes through `/go/<tool-slug>` (Cloudflare Pages `_redirects`), launching with plain vendor URLs; affiliate URLs swap in per approval. Per-tool `affiliateStatus` field. Acceptance criteria test the redirect layer, not real tags.
3. *No legal surface* — FTC affiliate-disclosure component above the fold on every monetized page + `/privacy`, `/terms`, `/about` in launch scope.
4. *Bulk content kills the one-shot* — content-collection zod schema is an explicit first deliverable; a generator script produces pages from seed data; the one-shot caps at 5 articles + 15 profiles proving the pipeline; scaling to 20/50 is post-launch content work.

**Improvements (all accepted):** Cloudflare Web Analytics only (Plausible has no free tier — verified); `/go/` layer doubles as click measurement via a Pages Function; the comparison-article component (verdict table, rank badges, per-row CTA, "our pick" box — Wirecutter pattern) specced explicitly with its own criteria; concrete acceptance numbers (404/empty states, 375px, Lighthouse ≥90 perf / ≥95 SEO, sitemap + schema.org validate); `lastReviewed` frontmatter surfaced on every page + documented verdict-update procedure.

**Rejected (→ PRD §20):** email capture at launch — contradicts the v1 non-goal "no newsletter"; revisit post-launch. Sponsored slots explicitly excluded from launch acceptance criteria.

**GATE B: passed after revisions.** GATE C (user package review): *pending user*.
