---
name: masterplan
description: Use when turning a product idea — from a one-sentence thought to a long messy chat — into a complete, execution-ready PRD package that a coding agent can build end-to-end from a single prompt. Covers idea clarification, prior-art research with an honest build/don't-build verdict, product interrogation, technical decisions with per-component reference maps, adversarial validation, and revision of existing packages. Also use when the user asks to add features or change scope on a project that already has a masterplan package (revise mode).
version: 1.0.0
license: MIT
metadata:
  tags: [prd, requirements, planning, one-shot, product]
---

# masterplan

> **Measure twice, cut once.**

Turn a raw product idea into a **PRD package**: a folder any capable coding agent can pick up and build end-to-end from a single prompt, with resumable progress if the run is interrupted. The interrogation is thorough so the execution can be one-shot. You are not filling in a template — you are running an investigation that ends in a document where every question is already answered.

If the user's request is a change to a project that already has a masterplan package, skip to **Revise mode** at the bottom.

## Core principles

1. **Decisions, not discussion.** Every PRD section resolves to one chosen answer with a short rationale. No option lists. No "TBD".
2. **Honest consultant, not a PRD machine.** If research shows the idea already exists as a deployable product, say "don't build this — deploy X" and produce a setup/adaptation document instead.
3. **Nothing from scratch without a reason (the chimera principle).** Products are assembled from proven parts. Anchor every major component to a reference implementation — observe, imitate, modify — with licenses checked.
4. **Cheap before expensive — gate the spend, not the tool.** Tools and research are allowed in *any* phase once there is a clear purpose for the spend. Reading an existing target (codebase, product, files) read-only to ground a fuzzy idea is cheap and encouraged early. What's held back is *expensive or online* research spent on a still-shallow target that may change tomorrow: clarify the target before prior-art/web research, quick-scan before a deep-dive, validate before writing the document. The rule is never "don't research" — it's "don't research *deep/online* while the goal is still shallow."
5. **The user answers product questions; you make technical decisions.** Ask about audience, features, budget, and the product's fate. Decide stack, database, architecture, and security yourself, and write down why.
6. **You are not a yes-man.** The user can describe any flow they want; challenge vague or contradicted choices with evidence from research, not opinion.
7. **Scale the document to the project.** A small tool gets a short PRD; a large app may need 50 pages. Length is an output, not a target.
8. **The package is presentation-ready.** The primary document (PRD or VERDICT) always ships as **both** Markdown **and** a self-contained `*.html` that opens in a browser — offline, every diagram rendered — usable to walk a stakeholder through the plan. Diagrams are first-class, not decoration: **every step or section a reader would follow visually gets a flow diagram**, not just prose. See `references/html-export.md`.

## When to use

- The user has a product/app/website idea — clear or vague — and wants it specified for building.
- A messy brainstorm chat needs to become an executable plan.
- An existing masterplan package needs a change (→ Revise mode).

**Do not use when:** the task is a small bugfix or feature in an existing codebase without a package; a final PRD already exists and only implementation planning is needed; the user wants copywriting or marketing content only.

## Pipeline

```
1. Intake + clarification loop ── GATE A: researchable pitch confirmed
2. Prior-art: quick scan → direction confirmed → deep-dive → honest verdict
3. Product/business interrogation with evidence-based correction
4. Technical research + per-component reference map
5. Validate: fresh red-team agent ── GATE B: zero blockers
6. Write the package (+ final self-review) ── GATE C: user reviews package
```

After each phase completes, append its confirmed outcomes to the package's `references/decisions.md` (see **Generator state** below). If a partial package already exists when you start, resume from the first incomplete phase — do not re-interview.

## Phase 1 — Intake + clarification loop

Accept the idea in any form: one sentence, a voice-note transcript, a long contradictory chat dump.

Before any research, you must be able to write a **researchable pitch** — one paragraph stating:

1. **What** the thing is,
2. **who** it is for,
3. the user's **core action** (the one thing a user does with it).

If you cannot write that paragraph yet, run a **clarification loop** until the shape locks: conversation, model knowledge, and — when the idea attaches to an existing codebase, product, or files — **read-only inspection of that target**. That grounding is cheap and often the fastest way to lock the pitch; it also catches false premises (e.g. "my app has no memory" when it already does). Offer directions ("do you mean something like this, or like that?") until the shape is firm. What you hold back here is *online / prior-art* research — the expensive phase (Phase 2's job) — not tools in general; don't spend it on a pitch that may still change tomorrow.

**GATE A — Lock the pitch before spending prior-art / online research.** Present the paragraph and get an explicit "yes, that's what I mean." Read-only grounding of an existing target (above) is fine *before* this gate — it's often what makes the pitch confirmable. If the user has fully delegated or is away, you may self-confirm and proceed **only toward *less* spend** (e.g. a don't-build or narrower-scope call); mark it provisional/agent-decided so a returning user can correct it. Never self-confirm your way *into* the expensive phases.

## Phase 2 — Prior-art research + honest verdict

Follow `references/research-playbook.md`. Staged, so waste stays cheap:

1. **Quick scan** — identify the 3–5 existing products/projects closest to the pitch.
2. **Direction check** — present them: "your idea resembles X and Y; their flow works like this — is that what you have in mind?" Classify each divergence: deliberate differentiation, or the user simply didn't know the proven pattern?
3. **Deep-dive** — only after the user confirms direction: flows, page structures, tech stacks, open-source availability, licenses.
4. **Honest verdict** — exactly one of:

| Verdict | Meaning | The package becomes |
|---|---|---|
| **Don't build — deploy X** | A deployable product already covers the idea | A setup/adaptation document for that product |
| **Don't build (yet)** | The premise is false, or the need isn't real/urgent enough to justify building now (YAGNI) | An **investigation record** — `VERDICT.md` (use `references/verdict-template.md`): what reality/the code actually shows, why not now, a zero-build fallback, and concrete revisit-triggers that flip it to build |
| **Build with differentiation** | Similar things exist, but there is a gap | A full PRD that states **the one clear difference** justifying the build |
| **Build fresh** | No meaningful prior art | A full PRD; components still anchored to references where possible |

Deliver the verdict honestly even when the user hoped to build. "Deploy X, save three months" is a success, not a failure. On either **don't-build** verdict the pipeline **stops here**: the package is that one document + `references/` (decisions.md, audits/scan) — no PRD/EXECUTE/STATUS, skip Phases 3–6. A don't-build reached honestly is a finished, successful run.

## Phase 3 — Product/business interrogation

Ask the user **only product and business questions** — audience, features and their behavior, monthly budget for infrastructure/APIs, design taste, day-one content, and the product's fate (open source / commercial / internal). Aim for about a dozen questions, not sixty. Draw from `references/question-bank.md` and let answers eliminate later questions.

The user may describe the flows they want in their own words. Correct with evidence: "the flow you describe conflicts with how users behave in X, Y, Z — all of them do it this way because ⟨reason⟩. Deliberate difference, or adopt the proven pattern?" Every disagreement resolves into a recorded decision.

**Question style (applies to phases 1 and 3):**

- **One question per turn.** Each answer steers what gets asked next; answers can eliminate later questions entirely.
- **Multiple choice preferred** wherever the answer space allows. Use the platform's interactive question UI if available; otherwise numbered options in text.
- **Mark a recommended option** with a one-line reason.
- **Always include a "you decide" escape hatch.** Choosing it is not a non-answer: make the decision yourself and record it in the PRD as an agent decision with rationale. Full delegation never stalls the pipeline.

## Phase 4 — Technical research + reference map

You make every technical decision and verify it against reality:

- **Choose the stack** (never list options), justified against the product's needs, budget, and fate.
- **Verify external APIs are alive** and check current pricing against the stated budget. A PRD naming a dead API or an unaffordable tier fails at execution time.
- **Build the per-component reference map:** anchor each major component to a proven implementation — "video timeline → adapt pattern from repo X (MIT)"; "chat streaming → proven in repo Y." Check licenses so no incompatible code (e.g. GPL into a closed-source product) gets absorbed; see the license table in `references/research-playbook.md`.

## Phase 5 — Validate (red team)

Before writing anything, submit the decision set to a **fresh agent with no conversation context**. Follow `references/validation-rubric.md`.

- Send the **decision summary** — pitch, verdict, feature list, flows, technical decisions with rationale, reference map. **Never send the conversation transcript**; a validator that reads the conversation inherits its bias.
- The mandate is adversarial: **find what is wrong, not what is good.** Axes: completeness, consistency, feasibility, optimization, risk.
- The report comes back at three levels: 🔴 **Blocker**, 🟡 **Improvement**, 🟢 **Nice-to-have**. Blockers return to their owning phase and get fixed. Improvements are decided with the user. Rejected suggestions are recorded in the PRD's considered-and-rejected section so the executing agent doesn't "fix" deliberate choices.
- Save the report to the package's `references/validation-report.md`.

**GATE B — Do not write the PRD while blockers remain.**

Validation runs **by default**. The user may skip it for tiny projects. On platforms without subagent support, run the same rubric yourself in a clean context (a fresh conversation or a deliberate fresh-eyes pass) — weaker, but the gate still exists.

## Phase 6 — Write the package

*(Build verdicts only. A don't-build verdict stops at Phase 2 — see its verdict row and `references/verdict-template.md`.)*

Produce one folder:

```
prd-<slug>/
├── PRD.md        ← the complete document — use references/prd-template.md
├── PRD.html      ← self-contained, presentation-ready render of PRD.md, all diagrams rendered — use references/html-export.md
├── EXECUTE.md    ← the single execution prompt — use references/execute-template.md
├── STATUS.md     ← milestone checklist — use references/status-template.md
└── references/   ← research notes: prior-art comparison, absorbed patterns,
                    decisions.md, validation-report.md
```

Create the folder where the workspace's conventions say project artifacts go — project-local by default. Never a fixed path.

Write the PRD section by section (all sections in the template are required; mark a section "Not applicable — ⟨reason⟩" rather than deleting it). Each section that a reader follows visually carries a diagram — the template marks which (§5 flows, §7 data model, §8 multi-actor endpoints, §11 architecture, §18 build order). Then generate `PRD.html` per `references/html-export.md` — a single file that opens offline with every diagram rendered, so the package doubles as the walkthrough deck. (For a **don't-build** run, the same export applies to `VERDICT.md` → `VERDICT.html`.) Then **self-review** before handing over:

1. **Placeholder scan** — no "TBD", "TODO", or vague requirements anywhere.
2. **Consistency** — no section contradicts another; the build order covers every feature; every feature has acceptance criteria.
3. **Ambiguity** — if a requirement can be read two ways, pick one and make it explicit.
4. **Diagram coverage** — every flow/step a reader would follow visually has a diagram, and `PRD.html` opens offline with all of them rendered (no broken/blank diagram, no CDN dependency).

**GATE C — The user reviews the package.** Present it, walk through the load-bearing decisions briefly, and revise until approved.

## Generator state — `references/decisions.md`

The pipeline itself must survive interruption, mirroring what it preaches. As each phase completes, append its confirmed outcomes to `references/decisions.md` inside the package folder. Create the folder at the end of phase 1, when the pitch locks — placed where the workspace's conventions say project artifacts go, project-local by default, never a fixed path:

```markdown
## Phase 1 — Pitch (confirmed YYYY-MM-DD)
⟨the confirmed pitch paragraph⟩

## Phase 2 — Prior-art verdict
⟨verdict + the one difference + scan summary⟩

## Phase 3 — Product decisions
⟨each Q → decision, including "agent decided: ⟨rationale⟩" entries⟩

## Phase 4 — Technical decisions
⟨stack, APIs verified, reference map⟩

## Phase 5 — Validation
⟨blockers found → resolutions; rejected suggestions⟩
```

On session start with a partial package: read this file, state which phase you are resuming, and continue.

## Revise mode — the PRD stays alive

A PRD that cannot change becomes a lie the first time the product changes. When the user requests a change to a project with an existing package, follow `references/revise-playbook.md`:

1. **Load state** — read PRD.md, STATUS.md, and `references/decisions.md`; understand what is already built.
2. **Classify the change** and run **only the affected phases** — a new user-facing feature may need a prior-art check and a few interrogation questions; a stack swap needs phase 4; a copy tweak needs neither.
3. **Impact analysis** — show the user which PRD sections change and which built milestones are invalidated, before writing anything.
4. **Validate** — significant changes go through the red-team gate again, scaled down: the validator sees the change and its impact, not the whole package.
5. **Write the delta** — update affected sections, bump the version, append to the changelog, add new milestones to STATUS.md, and mark invalidated ones `[!] needs rework`. Never silently uncheck history.

Revise mode pairs with EXECUTE.md's change-guard rule: the executor refuses ad-hoc scope changes and points here; revise mode makes the front door cheap. Together they keep the document permanently truthful.
