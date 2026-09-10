# masterplan.md Template

Copy this structure into the package's `masterplan.md` and fill every section. **Every section resolves to a DECISION with a short rationale. No option lists. No TBD.** If a section genuinely does not apply, keep the heading and write "Not applicable — ⟨reason⟩" so the executing agent knows it was considered, not forgotten. Scale depth to the project: a small tool gets short sections, a large app gets long ones.

**Decisions in prose, not artifacts that go stale.** Record decisions as prose and contracts, not brittle file paths or implementation snippets that rot the moment the executor names things differently. One deliberate exception: a snippet that *encodes a decision* — a state machine, reducer, schema, or type shape — may be inlined, trimmed to its decision-rich part (§7's schema is exactly this).

**Diagrams are first-class (so the package doubles as a presentation).** Any step or structure a reader would follow visually gets a diagram, not just prose. Diagrams are **hand-authored SVG files** in the package's `references/diagrams/` folder, embedded as `![⟨caption⟩](references/diagrams/⟨name⟩.svg)` — full design system, color semantics, per-type layouts, and verification procedure in `references/diagrams.md`. The sections below marked **[diagram]** must carry one; add more wherever a flow, state machine, or relationship is easier seen than read: §5 user flows, §7 data model, §8 multi-actor/async endpoints, §11 architecture, §18 build order. One SVG file per diagram, named after its section (`s5-flow-checkout.svg`, `s7-data-model.svg`, `s11-architecture.svg`). The same node kind gets the same color in every diagram of the package.

---

## 1. Summary & problem

What this product is, the problem it solves, and for whom — a half page maximum. The confirmed pitch paragraph from phase 1 belongs here, refined.

## 2. Prior-art & differentiation

The evidence that this should exist. Table plus the single most important sentence in the document:

| Product | What it does | What we absorb | License |
|---|---|---|---|
| ExampleApp | Link-in-bio pages with analytics | Page-builder flow, pricing model | Proprietary (pattern only) |
| example-oss | Self-hosted link pages | Data model, deploy setup | MIT |

**Absorption level (phase 2):** ⟨fork & adapt ⟨base repo⟩ / assemble (chimera) / differentiate / fresh⟩ — one line on why this rung.

**The one difference:** ⟨what makes this build distinct from the closest existing product — mandatory for "differentiate"; for the other rungs, what makes it yours⟩

## 3. Target users & business model

Who uses it (concrete persona, not "everyone"), how many at launch scale, and how it sustains itself: free / one-time / subscription / internal cost center. Include the resolved decision authority's stated monthly budget for infrastructure and APIs — later sections must fit inside it.

## 4. Features

One block per feature. A feature without acceptance criteria does not exist.

### 4.1 ⟨Feature name⟩
**What it does:** one paragraph, concrete behavior.
**Priority:** core / secondary (core = the product is broken without it).
**Acceptance criteria:**
- [ ] ⟨observable, testable statement — "a visitor can submit the form and sees a confirmation within 2s"⟩
- [ ] ⟨…⟩

## 5. User flows **[diagram]**

One SVG flow diagram per primary flow, plus a sentence naming its start and success end-state:

```
![Visitor signup → first item published](references/diagrams/s5-flow-first-item.svg)
```

## 6. Pages & screens

Inventory of every page/screen with its components — the executing agent builds exactly this list.

| Page | Route | Components | Notes |
|---|---|---|---|
| Home | `/` | Hero, feature grid, CTA, footer | Public |
| Dashboard | `/app` | Nav, item list, create button, empty state | Auth required |

**Interaction baseline applies to every screen here.** The default states each page and control must handle — loading / empty / error / populated, and every interactive element's hover / focus / disabled / loading — are the standing standard in `references/ui-baseline.md`, copied into this package. Do **not** restate it per page; this section only records **additions or deliberate exceptions** for a specific screen (e.g. "this table also has a bulk-select toolbar state"). For a headless API/library/CLI project with no UI, write "No UI — interaction baseline N/A" and skip it.

## 7. Data model **[diagram]**

The actual schema, not "needs a database". Lead with an SVG data-model diagram (one rect per table, fields as sublabels, relation arrows with cardinality) so relations read at a glance, then the exact schema below it:

```
![users ⋯ items data model](references/diagrams/s7-data-model.svg)
```

Every table/collection, every field, every relation — the SVG diagram shows them; the schema below is the executable truth:

```sql
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT UNIQUE NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE items (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','published')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

If the product has no persistent data, state that and why.

## 8. API contracts

Internal endpoints the frontend consumes — route, payload, response, error shape. For any endpoint that is **multi-actor or async** (webhook, background job, third-party callback, streaming), add an SVG sequence diagram (lifelines + horizontal call arrows top-to-bottom) showing who calls whom in what order:

```
![POST /api/items sequence](references/diagrams/s8-seq-create-item.svg)
```

The endpoint list — route, payload, response, error shape:

```
POST /api/items
Request:  { "title": "My first item" }
Response: 201 { "id": "…", "title": "My first item", "status": "draft" }
Errors:   401 unauthenticated · 422 { "error": "title required" }
```

## 9. External integrations & AI roles

Every third-party service and what it does here. Each entry verified alive during phase 4, with pricing at the expected volume:

| Service | Role | Plan/tier | Est. monthly cost | Verified on |
|---|---|---|---|---|
| ⟨payment provider⟩ | Checkout | Standard, 2.9% + fee | ~⟨amount⟩ | ⟨date⟩ |
| ⟨LLM API⟩ | Generates descriptions | Pay-as-you-go | ~⟨amount⟩ | ⟨date⟩ |

If AI is part of the product, specify exactly where it acts, which model tier, and the fallback when it fails.

## 10. Tech stack

The chosen stack — one choice per layer, with rationale tied to sections 3 and 9:

| Layer | Choice | Why |
|---|---|---|
| Frontend | ⟨framework⟩ | ⟨reason⟩ |
| Backend | ⟨framework/runtime⟩ | ⟨reason⟩ |
| Database | ⟨engine⟩ | ⟨reason⟩ |
| Hosting | ⟨platform⟩ | ⟨reason — must fit §3 budget⟩ |

One stack, already decided: the phase-4 comparison (2–3 options, ratified by the resolved decision authority) happened in the decision process, not here. Runner-up stacks and why they lost go to §20 so the executor doesn't second-guess this table.

## 11. Architecture **[diagram]**

How the pieces connect — a short prose description plus an SVG diagram with dashed boundary rects for what runs where (browser / host / region):

```
![System architecture](references/diagrams/s11-architecture.svg)
```

Name the boundaries: what runs where, what talks to what, what is stateless.

## 12. Security

Concrete requirements, scaled to the product's fate (§21): auth mechanism, session/token handling, input validation strategy, secrets handling (env vars, never committed), rate limiting if public, data privacy obligations if user data is stored.

## 13. Deployment & infrastructure

Where it runs, how it ships, and what it costs: hosting target, deploy method (the executing agent must be able to perform it), domain/TLS, backups if there is a database, and the monthly total — which must fit the §3 budget.

## 14. Component reference map

The chimera map: each major component anchored to a proven implementation. Pattern = re-derive the approach; code = adapt with attribution (license permitting).

| Component | Reference (repo/product) | License | Absorb |
|---|---|---|---|
| ⟨e.g. drag-drop editor⟩ | ⟨repo URL⟩ | MIT | Code — adapt directly |
| ⟨e.g. onboarding flow⟩ | ⟨product⟩ | Proprietary | Pattern only |

Quality bar for what's worth anchoring to: prefer simple, deep interfaces — small surface, complexity hidden — for long-term maintainability.

When any row absorbs code, link package artifacts produced by `references/code-absorption.md`: pinned repos, tree-map INDEX (the recheck surface), logic analysis, path-level license report, source→target records, and (for Assemble) chimera seam contracts. Every such record maps to §18 and one or more stable local ticket contracts.

## 15. Design direction

Prevents functionally-correct-but-generic output:

- **Register:** brand (expressive, marketing) or product (calm, workhorse UI) — pick per surface.
- **Mood:** 3–5 words ("warm, editorial, unhurried").
- **Look references:** 2–3 existing products whose visual quality is the bar.
- **Must NOT look like:** ⟨the failure mode — e.g. "a default component-library dashboard with stock gradients"⟩.
- **Industry UX conventions (from phase-2 research):** the table-stakes patterns this product's *category* expects, cited from the deep-dive — "products X and Y in this space all do ⟨pattern⟩, so we adopt it" (e.g. fintech → transaction confirmations + audit trail; SaaS dashboard → filters/saved views/bulk actions; consumer → onboarding coach + rich empty states). List which the build adopts and any it deliberately drops (→ §20). This is the layer *above* the universal `references/ui-baseline.md` floor — it makes the product feel native to its industry, not just generically correct.

This section covers **taste** (what it should feel like). The **mechanics** — interaction states, empty/error handling, keyboard, responsive, motion — are the non-negotiable floor in `references/ui-baseline.md` and are not re-decided here. Design direction sets the bar *above* that floor. EXECUTE.md's design-stack rule tells the executing agent which design skills to engage to hit this bar — this section is enforced at build time, not advisory. It also drives the look of the HTML walkthrough artifact (`references/html-export.md`), so the deck previews the product faithfully.

## 16. Content & seed data

What the product contains on day one so it ships alive, not as an empty shell: what content, from where (AI-generated / authority-provided / imported), and minimum quantities ("20 seeded articles", "5 example projects"). If the executing agent generates it, say so and set the quality bar.

## 17. Required credentials

Everything the resolved authority must provide or authorize, and when the build needs it:

| Credential | Used by | Needed at milestone |
|---|---|---|
| ⟨API key⟩ | §9 integration | M4 — integrations |
| ⟨hosting token⟩ | §13 deploy | M7 — deploy |

## 18. Build order **[diagram]**

This section is the milestone map, not executor prose. Decompose every milestone into immutable local ticket contracts per `references/ticket-contract.md`: package `references/tickets/INDEX.md` catalogs them and each `references/tickets/<ID>.md` is one execution-ready vertical slice that fits one agent context window. The executor must be able to complete that ticket by reading its contract and linked docs, without reading this whole masterplan. Canonical project queue owns mutable status; fallback `STATUS.md` owns it when no queue exists. Both map 1:1 by stable ticket ID.

Milestones are **tracer bullets**: after the walking skeleton, each is a complete vertical slice through every layer (UI → API → data), demoable alone. A milestone may contain many dependency-ordered tickets; each ticket names exact target paths/contracts, changes, retained and changed behavior, acceptance criteria, commands, evidence destination, and rollback boundary. When prior art contributes code, ticket source repository + pinned SHA + source paths + license/attribution are mandatory. No horizontal tickets, cyclic dependencies, or catch-all integration tickets.

```
![Build order — blocking edges](references/diagrams/s18-build-order.svg)
```

| Milestone | Outcome | Ticket IDs | Depends on |
|---|---|---|---|
| `M1` — Walking skeleton | ⟨thinnest runnable end-to-end slice⟩ | `PRJ-001` | none |
| `M2` — ⟨core feature⟩ | ⟨demoable feature through every layer⟩ | `PRJ-002`, `PRJ-003` | `M1` |
| `M9` — Full QA | Every §4 criterion and required UI baseline check evidenced | `PRJ-999` | all feature tickets |

**Ticket graph:** [ticket catalog](references/tickets/INDEX.md) is deterministic graph truth. Every catalog ticket appears once in §18 table with matching milestone; §18 contains no unknown IDs. Generate SVG build-order diagram from this validated catalog graph rather than treating SVG as independently parsed graph data.

**Testing strategy (decided in phase 4):** tests target **external behaviour at acceptance level** — what the product does, never how it is implemented — so they survive refactors. Each ticket lands with tests for its mapped §4 acceptance criteria. Full QA ticket verifies every criterion, required primary flow, and — for UI projects — `references/ui-baseline.md` with evidence.

**Queue/export binding:** name canonical task state and link its durable `STATUS.md` snapshot. Queue records contain stable ID, mutable status, dependencies, contract link, and evidence pointer; ticket prose remains local.

## 19. Non-goals

What is deliberately NOT built, so the executing agent doesn't helpfully add it: ⟨e.g. "no mobile app; no multi-language; no admin panel in v1"⟩.

## 20. Considered and rejected

Deliberate choices that might look like mistakes — from validation and interrogation — so nobody "fixes" them:

| Suggestion | Source | Why rejected |
|---|---|---|
| ⟨e.g. use a CMS⟩ | Validation 🟡 | ⟨reason⟩ |

## 21. Product fate

Open source / commercial / internal — and what that implies here: license choice, README/docs expectations, hardening level, telemetry stance.

## 22. Version & changelog

Maintained by revise mode. Bump minor for additive changes, major for changes to already-built behavior.

- **v1.0 — ⟨YYYY-MM-DD⟩ — initial**
