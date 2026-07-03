# Validation Report — ai-tools-affiliate

Red-team pass, 2026-07-03. Fresh agent, decision summary only (no conversation transcript). Verified externally before judging: minted-directory-astro is real, MIT, ships search/tags/sponsored slots; Plausible has **no free tier** (30-day trial, then paid).

## Findings

🔴 BLOCKER — CONSISTENCY: The differentiation ("~50 hands-on-tested tools with per-job verdicts") contradicts AI-drafted day-one content executed by a coding agent that has never used the tools; it will fabricate verdicts, pricing, and feature claims — launching exactly the scraped-breadth-with-fake-opinion product the prior-art verdict said loses. Fix: split the machine (site + content pipeline, one-shot buildable) from the content (owner-verified seed data per tool); the agent generates pages from data and never invents tool facts.

🔴 BLOCKER — COMPLETENESS: Affiliate enrollment assumed, not planned. Programs require publisher approval — typically against an already-live site — and some top AI tools have no affiliate program at all. The criterion "affiliate links carry tracking params" is unsatisfiable at build time. Fix: `/go/<tool-slug>` redirect indirection (Pages `_redirects`), launch with plain vendor URLs, swap per approval; `affiliateStatus` field per tool; acceptance criteria test the redirect layer.

🔴 BLOCKER — COMPLETENESS: No legal/compliance surface — no FTC affiliate disclosure, privacy policy, terms, or owner identity (checked during publisher approval). Fix: disclosure component above the fold on every monetized page; `/privacy`, `/terms`, `/about` in launch scope and acceptance criteria.

🔴 BLOCKER — RISK: Bulk content generation (70 pieces inline) is where the one-shot dies: context exhaustion, quality decay from piece ~15, inconsistent frontmatter breaking content-collection schema validation late in the build. Fix: zod schema as an explicit first deliverable; generator script produces pages from seed data; cap the one-shot at 5 articles + 15 profiles; scale in follow-up runs.

🟡 IMPROVEMENT — CONSISTENCY: "Plausible trial or Cloudflare Web Analytics" contradicts itself and the budget (Plausible: no free tier). Fix: Cloudflare Web Analytics only.

🟡 IMPROVEMENT — COMPLETENESS: No outbound-click tracking on the only revenue action. Fix: the `/go/` layer doubles as the measurement point (Pages Function click log) — still $0.

🟡 IMPROVEMENT — FEASIBILITY: "Software is commodity" understates the custom work: the core product is editorial comparison articles with ranked verdict tables — a content type the directory template does not have. Fix: spec the comparison-article component explicitly (verdict table, rank badges, per-row CTA, "our pick" box; Wirecutter's verdict-box as the concrete reference) with its own acceptance criteria.

🟡 IMPROVEMENT — COMPLETENESS: Acceptance criteria omit error/empty states, mobile, and measurable SEO. Fix: 404 + zero-results + empty-tag states; verified at 375px; Lighthouse ≥90 perf / ≥95 SEO as numbers; sitemap.xml, robots.txt, canonical URLs, OG images, schema.org ItemList/Review validate.

🟡 IMPROVEMENT — RISK: No post-launch content-update workflow for a product whose value is verdict freshness. Fix: `lastReviewed` frontmatter surfaced on every page + a documented "update a verdict" procedure.

🟢 NICE-TO-HAVE — OPTIMIZATION: Sponsored slots are template-native but "later use" — exclude from launch acceptance criteria so the agent doesn't wire and test them.

🟢 NICE-TO-HAVE — COMPLETENESS: No email capture; 100% Google-dependent. Fix suggested: static newsletter signup.

## Disposition

- All 4 blockers: **accepted**; decisions revised (see `decisions.md`, Phase 5). GATE B passed after revision.
- All 5 improvements: **accepted**; folded into PRD sections 4, 9, 12, 15, 18.
- 🟢 sponsored-slot exclusion: **accepted** (PRD §19).
- 🟢 email capture: **rejected** — contradicts the v1 non-goal "no newsletter"; revisit post-launch (PRD §20).
