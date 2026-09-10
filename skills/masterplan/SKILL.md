---
name: masterplan
description: >
  Use when turning a product idea, or a given repo/SaaS/workflow, into a
  build-ready masterplan package. Trigger: /masterplan, plan this product,
  rebuild this repo, bongkar repo ini, our version of X.
version: 0.2.0
author: Hermes
license: MIT
metadata:
  tags: [prd, requirements, planning, one-shot, product]
---

# masterplan

> **Every decision made before the first line of code.**

Turn a raw product idea, or a given source (repo, product, workflow), into a **masterplan package**: a folder any capable coding agent can pick up and build end-to-end from a single prompt, with resumable progress if the run is interrupted. The interrogation is thorough so the execution can be one-shot. You are not filling in a template - you are running an investigation that ends in a document where every question is already answered. Given a readable repo, map it folder by folder and reconstruct its logic **before** deciding what our version keeps, drops, or changes.

If the user's request is a change to a project that already has a masterplan package, skip to **Revise mode** at the bottom.

## Core principles

1. **Decisions, not discussion.** Every masterplan section resolves to one chosen answer with a short rationale. No option lists. No "TBD".
2. **Adopt-heavy builder, not a gatekeeper.** The standing assumption is *we are building*; prior art exists to be absorbed, not to veto the build. Research finds what to take — flows, patterns, architectures, and (license permitting) code — and how heavily: fork & adapt, assemble, differentiate, or fresh (Phase 2's adoption ladder). The only honest stop is a **factually false premise** — the thing already exists in the user's own target, or the ask rests on a mistaken belief. Never stop because a similar product exists somewhere.
3. **Nothing from scratch without a reason (the chimera principle).** Products are assembled from proven parts. Anchor every major component to a reference implementation — observe, imitate, modify — with licenses checked.
4. **Cheap before expensive — gate the spend, not the tool.** Tools and research are allowed in *any* phase once there is a clear purpose for the spend. Reading an existing target (codebase, product, files) read-only to ground a fuzzy idea is cheap and encouraged early. What's held back is *expensive or online* research spent on a still-shallow target that may change tomorrow: clarify the target before prior-art/web research, quick-scan before a deep-dive, validate before writing the document. The rule is never "don't research" — it's "don't research *deep/online* while the goal is still shallow."
5. **The decision authority answers product questions; you make technical decisions — except the stack, which they ratify.** Resolve the decision authority from `references/workflow-binding.md` (usually the user, but project policy may name another role). Ask about audience, features, budget, and the product's fate. Decide architecture, data model, and security yourself, and write down why. For the **stack**, design it twice: 2–3 genuinely different viable options, a product-framed comparison, one opinionated recommendation, the resolved authority decides (Phase 4). The options live in the decision process, never in the document — masterplan.md §10 records exactly one chosen stack; runner-up rationale goes to §20. **When making technical decisions, do not give much weight to development cost; instead prefer quality, simplicity, robustness, scalability, and long-term maintainability.**
6. **Critical adversarial collaborator — in every phase, at every gate.** Adversarial toward ideas and decisions, collaborative toward the goal of a great build. Actively challenge rather than transcribe: the premise and the "why now" in phase 1, unknowing reinvention in phase 2, feature bloat and vague flows in phase 3, the easy default in phase 4, the whole decision set in phase 5. Gates A/B/C are real checks, not rubber stamps. Calibration: adversarial is not contrarian — every challenge is anchored to evidence and resolves into a recorded decision, never an objection left hanging. The reflexive naysayer is just a yes-man inverted.
7. **As detailed as the build needs — no ceiling.** A small tool still gets a short masterplan, but a large scope gets a correspondingly large one: hundreds of milestones and tickets are fine when the project warrants them, and **the initial document set may span hundreds of detail documents** — that is a success, not bloat. Length is an output, not a target — but completeness is never traded for brevity. Multi-doc structure: `masterplan.md` stays the index and decision record; detail overflows into topic documents under `references/` (one per module, integration, flow, or domain area), each self-contained, each linked from the section it elaborates.
8. **Ticket-local execution.** Every build unit gets an immutable local contract in `references/tickets/<ID>.md`, cataloged by `references/tickets/INDEX.md`, so an executor can claim and complete one ready ticket without reading the whole masterplan. `references/ticket-contract.md` defines the schema, dependency graph, queue mapping, and executor protocol. Canonical project queue owns mutable status; fallback `STATUS.md` owns it when no queue exists. External queues map 1:1 by stable ID while local ticket files remain execution truth.
9. **Portable text core, self-contained HTML artifact.** The text package (`masterplan.md`, `EXECUTE.md`, `STATUS.md`, local ticket contracts, `decisions.md`) is the source of truth and runs on any agent runtime — plain Markdown, diagrams as hand-authored SVG files (`references/diagrams.md` system — dark tech aesthetic, semantic colors, no runtime library). Diagrams are first-class, not decoration: **every step or section a reader would follow visually gets a diagram**, not just prose. The finished package also carries `masterplan.html` — a self-contained walkthrough render with the SVGs inlined, offline-openable, styled by the product's own §15 Design direction. See `references/html-export.md`.
10. **Baseline interaction quality is a default, not a feature.** Every app with a UI already needs button states, focus, disabled/loading, empty/error states, keyboard operability, and the rest — the things a one-shot build skips because nothing forces them. These are never interrogated as product questions; they are a standing standard (`references/ui-baseline.md`) that every build package with a UI carries and every executing agent must satisfy. Raise the floor by default; the user only decides what goes *above* it.

## When to use

- The user has a product/app/website idea - clear or vague - and wants it specified for building.
- The user hands a repo, SaaS, workflow, or video and wants **our** version specified for building (artifact-first).
- A messy brainstorm chat needs to become an executable plan.
- An existing masterplan package needs a change (→ Revise mode).

**Do not use when:** the task is a small bugfix or feature in an existing codebase without a package; a final PRD already exists and only implementation planning is needed; the user wants copywriting or marketing content only.

**Skill precedence:** masterplan subsumes generic brainstorming/ideation skills — phases 1 and 3 *are* the interrogation. While masterplan is active, do not also invoke a separate brainstorming skill (e.g. superpowers' `brainstorming`); one interrogation, not two.

## Pipeline

```
1. Intake + clarification loop ── GATE A: researchable pitch confirmed
   (idea-first or artifact-first)
2. Research: map the source (or prior art) before any adapt
   idea-first: quick scan → direction → deep-dive → absorption map
   artifact-first: deep-dive given source (tree-map → logic) → optional comparables → absorption map
3. Product/business interrogation with evidence-based correction
4. Technical research + per-component reference map
5. Validate: fresh red-team agent ── GATE B: zero blockers
6. Write the package (+ final self-review) ── GATE C: resolved reviewer approves package
```

**Before Phase 1**, resolve roles, authority, workspace isolation, capabilities, artifact root, and canonical task state via `references/workflow-binding.md`; save the result as package `references/workflow-binding.md`. Project/runtime policy wins; generic safe fallbacks apply when absent. After each phase completes, append its confirmed outcomes to the package's `references/decisions.md` (see **Generator state** below). If a partial package already exists when you start, resume from the first incomplete phase — do not re-interview.

Gates, interrogation, and reviews run in plain conversation on every runtime. The one generated artifact is the final `masterplan.html` walkthrough (`references/html-export.md`), produced in phase 6 and regenerated on every revision.

## Phase 1 — Intake + clarification loop

Accept the idea in any form: one sentence, a voice-note transcript, a long contradictory chat dump, **or a given source** (repo URL, local checkout, SaaS URL, video, workflow).

**Artifact-first.** If the owner hands a source as the thing to rebuild, that source is the pitch target. Classify it:

- **white-box** (readable repo): Gate A states what the source is, who our version is for, and the core action. Do not invent a different product before mapping the source.
- **black-box** (no source): Gate A still locks who / what / core action. Phase 2 reconstructs observed behavior only (pattern-only). Do not run `code-absorption.md`.
- **idea-only**: existing clarification loop below.

A given source is not a shallow target. Cheap read-only inspection *before* Gate A is allowed so the pitch is true. Folder-by-folder mapping is Phase 2, not Phase 1.

Before any expensive research, you must be able to write a **researchable pitch** - one paragraph stating:

1. **What** the thing is,
2. **who** it is for,
3. the user's **core action** (the one thing a user does with it).

If you cannot write that paragraph yet, run a **clarification loop** until the shape locks: conversation, model knowledge, and - when the idea attaches to an existing codebase, product, or files - **read-only inspection of that target**. That grounding is cheap and often the fastest way to lock the pitch; it also catches false premises (e.g. "my app has no memory" when it already does) - the one finding that stops a build (Phase 2). Offer directions ("do you mean something like this, or like that?") until the shape is firm. What you hold back here is *online / prior-art* research on a still-unconfirmed pitch - the expensive phase (Phase 2's job) - not tools in general; don't spend it on a pitch that may still change tomorrow.

**Grill, don't transcribe.** Look up facts yourself — never ask the user something the target or your own knowledge can answer; the user's job is decisions, not research. Walk the idea branch by branch instead of firing one blast of questions; every question carries a recommended answer with a one-line reason; and do not move on until shared understanding is explicit. Challenge the premise itself, with evidence: is this the real problem or a symptom of one, and why build it now? A premise that survives the challenge locks stronger; one that doesn't just saved the whole pipeline.

**GATE A — Lock the pitch before spending prior-art / online research.** Present the paragraph and get an explicit "yes, that's what I mean." **Ordering checkpoint: if the pitch is already writable at intake, run Gate A and record it in `references/decisions.md` BEFORE the first search call** — the rule has no other enforcement, so this checkpoint is it. Read-only grounding of an existing target (above) is fine *before* this gate — it's often what makes the pitch confirmable.

**Delegation mode.** If the user has fully delegated or is away, you may self-confirm and proceed **only toward *less* spend** (e.g. a false-premise stop or a narrower-scope call); mark it provisional/agent-decided so a returning user can correct it. Never self-confirm your way *into* the expensive phases. Exception — the user *explicitly delegates the whole pipeline* ("run it, bring me the package"): every gate may then be self-confirmed, each marked `provisional / agent-decided`, and all provisional decisions batch into one review at Gate C. The adaptive rule from `references/question-bank.md` governs the questions: after "you decide" ≥3× in a row, decide the rest yourself and list every agent decision at Gate C. Full delegation never stalls the pipeline.

## Phase 2 — Research + absorption map

Follow `references/research-playbook.md`. Map first, adapt later. Do not write keep/drop/invert decisions until the source (or confirmed prior art) is mapped.

**Artifact-first (given source).** Skip the 3-5 scan as the primary path. Deep-dive the given source first. For a readable repo, run `references/code-absorption.md` Stages 1-3: pin, walk folders one by one into a tree-map, reconstruct logic from that map, then license. Optional 1-2 comparables may follow the map if divergence needs market context; they must not replace it.

**Idea-first.** Staged, so waste stays cheap:

1. **Quick scan** - identify the 3-5 existing products/projects closest to the pitch.
2. **Direction check** - present them: "your idea resembles X and Y; their flow works like this - is that what you have in mind?" Classify each divergence: deliberate differentiation, or the user simply didn't know the proven pattern? This is the adversarial read of the scan - name what the user is reinventing unknowingly, plainly, and resolve each case into a decision.
3. **Deep-dive** - only after the resolved decision authority confirms direction: flows, page structures, tech stacks, open-source availability, licenses. Confirmed OSS that may contribute code takes the same tree-map → logic path in `code-absorption.md`.

**Absorption map** (both entries) - the standing assumption is *we are building*; the question is **what proven prior art do we absorb, and how heavily?** Pick the level on the adoption ladder (all are BUILD outcomes):

| Absorption level | Meaning |
|---|---|
| **Fork & adapt** | A compatibly-licensed base is already close — start from it, modify heavily, make it yours |
| **Assemble (chimera)** | Compose from several proven components/patterns, each anchored to a reference |
| **Differentiate** | Similar things exist but there is a clear gap — build with the stated difference, borrow the patterns |
| **Fresh** | Genuinely novel (rare) — still anchor components to references where possible |

Two absorption currencies, one rule: **patterns and ideas** (flows, UX, architecture) are free to absorb from anything, including proprietary products. **Actual code** (the fork/copy path) is license-gated — the license table in `references/research-playbook.md` governs it.

**The one brake — false premise.** If grounding shows the request rests on a **factually wrong premise** — the thing already exists *in the user's own target/codebase*, or the ask is built on a mistaken belief (e.g. "my app has no memory" when it already has one) — stop honestly. This is the *only* outcome that yields `VERDICT.md` (use `references/verdict-template.md`) instead of a build, and it is rare. The pipeline **stops here**: the package is that investigation record + `references/` (decisions.md, audits/scan) — no masterplan/EXECUTE/STATUS, skip Phases 3–6. "The facts differ" is a successful finding, not a failed run. "A similar product exists" is never a reason to stop — that is what the ladder above absorbs.

## Phase 3 — Product/business interrogation

Ask the resolved decision authority **only product and business questions** - audience, features and their behavior, monthly budget for infrastructure/APIs, design taste, day-one content, and the product's fate (open source / commercial / internal). After an artifact-first map, the load-bearing questions are keep / drop / invert against that map and logic, not against a marketing summary. Aim for about a dozen questions, not sixty - unless the project is large: then ask as many as completeness needs, still one at a time, still with recommendations. Draw from `references/question-bank.md` and let answers eliminate later questions. Run the interrogation in conversation: multiple choice where the answer space allows, one question per turn, recommended option marked, "you decide" hatch on every one.

Hold the adversarial stance here, not just at validation — the grilling rules from Phase 1 still apply (facts looked up yourself, decisions belong to the resolved decision authority, branch by branch, recommended answers). Challenge feature bloat ("what breaks if v1 ships without this?"), vague flows, and unjustified scope — with evidence, not opinion. The user may describe the flows they want in their own words. Correct with evidence: "the flow you describe conflicts with how users behave in X, Y, Z — all of them do it this way because ⟨reason⟩. Deliberate difference, or adopt the proven pattern?" Every disagreement resolves into a recorded decision — never an objection left hanging.

**Question style (applies to phases 1 and 3):**

- **One question per turn.** Each answer steers what gets asked next; answers can eliminate later questions entirely.
- **Multiple choice preferred** wherever the answer space allows. Use the platform's interactive question UI if available; otherwise numbered options in text.
- **Mark a recommended option** with a one-line reason.
- **Always include a "you decide" escape hatch.** Choosing it is not a non-answer: make the decision yourself and record it in the masterplan as an agent decision with rationale. Full delegation never stalls the pipeline.

## Phase 4 — Technical research + reference map

You make the technical decisions, verify them against reality, and **question the easy default** — a choice that is merely easiest to build gets challenged before it gets written: will it actually scale, will it stay maintainable?

- **When making technical decisions, do not give much weight to development cost; instead prefer quality, simplicity, robustness, scalability, and long-term maintainability.** This governs the stack comparison, architecture, data model, and reference map — the cheaper-to-build option does not win by being cheaper.
- **Design the stack twice; the resolved decision authority decides.** Generate 2–3 genuinely different viable stacks — via parallel sub-agents where available, so they are really different, not one idea reskinned. **Fallback — no subagent support:** generate the options yourself in deliberately separate passes (a different architecture family per pass, no peeking back), and record the single-designer-bias caveat in `references/decisions.md`: options from one head are weaker evidence than from two. Compare them on product-framed axes weighted by the values above (quality, scalability, maintainability, ecosystem/lock-in — not raw dev cost), give one opinionated recommendation, and put the call to the resolved decision authority with the standard "you decide" hatch (which returns it to your recommendation). §10 records the one chosen stack; runner-up rationale lands in §20 so the executor doesn't second-guess it. Design-it-twice applies to the **stack and the architecture** — not to every decision; per-decision option generation bloats the process.
- **Verify external APIs are alive** and check current pricing against the stated budget. A masterplan naming a dead API or an unaffordable tier fails at execution time.
- **Build the per-component reference map:** anchor each major component to a proven implementation - "video timeline → adapt pattern from repo X (MIT)"; "chat streaming → proven in repo Y." Check licenses so no incompatible code (e.g. GPL into a closed-source product) gets absorbed; see the license table and its evidence order in `references/research-playbook.md` - never guess a license from the project's name or vibe. If Phase 2 selected **Fork & adapt**, **Assemble (chimera)**, or any row says `Code — adapt`, complete `references/code-absorption.md` Stages 4-7 in Phase 4, building on the pinned clones, tree-map, logic reconstruction, and license decisions from Stages 1-3. Stages 4-7 fail closed if the tree-map INDEX or logic analysis is missing. Choose absorption units, build source→target maps and chimera seam contracts, then derive exhaustive implementation steps.
- **Decide the testing strategy:** tests target **external behaviour at acceptance level** — what the product does, never how it is implemented — so they survive refactors. State what must be covered (the §4 acceptance criteria and primary flows) and map it into §18 plus each owning ticket's acceptance criteria and validation commands.

Where a visual helps review, present the architecture and data model SVG diagrams inline (rendered from `references/diagrams/`); the component + license map presents as a table.

## Phase 5 — Validate (red team)

Before writing anything, submit the decision set to a **fresh agent with no conversation context**. Follow `references/validation-rubric.md`. This gate is the culmination of the adversarial stance held since Phase 1 — a fresh set of eyes attacking decisions that have already survived your own challenges — not the first time criticism appears.

- Send the **decision summary** — pitch, absorption map, feature list, flows, technical decisions with rationale, reference map, and proposed ticket graph/contracts. **Never send the conversation transcript**; a validator that reads the conversation inherits its bias.
- The mandate is adversarial: **find what is wrong, not what is good.** Axes: completeness, consistency, feasibility, optimization, risk.
- The report comes back at three levels: 🔴 **Blocker**, 🟡 **Improvement**, 🟢 **Nice-to-have**. Blockers return to their owning phase and get fixed. Improvements are decided with the resolved decision authority. Rejected suggestions are recorded in the masterplan's considered-and-rejected section so the executing agent doesn't "fix" deliberate choices.
- Save the report to the package's `references/validation-report.md`. Present the 🔴🟡🟢 report to the resolved reviewer in that same format and collect one disposition per finding (fix / decide-with-user / reject→§20).

**GATE B — Do not write the masterplan while blockers remain.**

Validation runs **by default**. The resolved decision authority may skip it for tiny projects. On platforms without subagent support, run the same rubric yourself in a clean context (a fresh conversation or a deliberate fresh-eyes pass) — weaker, but the gate still exists.

## Phase 6 — Write the package

*(Build outcomes only. A false-premise stop ends at Phase 2 — see `references/verdict-template.md`.)*

Produce one folder:

```
masterplan-<slug>/
├── masterplan.md    ← the complete document — use references/masterplan-template.md
├── masterplan.html  ← self-contained walkthrough artifact — use references/html-export.md
├── EXECUTE.md       ← the single execution prompt — use references/execute-template.md
├── STATUS.md        ← canonical fallback status table, or durable read-only export of configured queue
└── references/      ← research notes: prior-art comparison, absorbed patterns,
                       decisions.md, validation-report.md,
                       ui-baseline.md (copy of the skill's standing standard, if the product has a UI),
                       workflow-binding.md, diagrams/*.svg,
                       tickets/INDEX.md + tickets/<ID>.md immutable execution contracts,
                       evidence/<ID>/* execution evidence,
                       absorption/* (when code is absorbed),
                       INDEX.md + ⟨topic⟩.md overflow detail docs, one per module/flow/domain (as many as completeness needs)
```

Create the folder at the artifact root resolved by `references/workflow-binding.md` — project-local fallback, never a universal fixed path. Generate `STATUS.md` from `references/status-template.md`: it is canonical mutable status when no project queue exists, otherwise a durable read-only export of that queue. In both modes every ticket stable ID maps 1:1 to one status row; ticket prose lives only in local contracts.

If the product has any user-facing UI, copy `references/ui-baseline.md` into the package's `references/` verbatim — it is the standing interaction standard the masterplan and EXECUTE both point to. For headless API / library / pure-CLI projects, skip it and note "no UI — interaction baseline N/A" in masterplan §6.

Write the masterplan section by section (all sections in the template are required; mark a section "Not applicable — ⟨reason⟩" rather than deleting it). Where detail overflows the section, copy `references/detail-index-template.md` to package `references/INDEX.md`, write topic documents under `references/`, and link them — the section keeps the decision, the docs keep the depth. Every detail doc appears in `references/INDEX.md`; no orphan documents. Decompose §18 into immutable local contracts using `references/ticket-contract.md`; write `references/tickets/INDEX.md` plus one `references/tickets/<ID>.md` per execution unit, list every catalog ticket once in §18 with matching milestone and no unknown IDs, and map every stable ID into canonical task state. Each ticket must carry enough linked context to execute without reading all of `masterplan.md`. Each section that a reader follows visually carries an **SVG diagram** per `references/diagrams.md` — the template marks which (§5 flows, §7 data model, §8 multi-actor endpoints, §11 architecture, §18 build order). Then generate `masterplan.html` per `references/html-export.md` — a self-contained walkthrough deck with the SVGs inlined, driven by §15 Design direction so the deck previews the product's own look. (On a **false-premise stop**, the same export applies to `VERDICT.md` → `VERDICT.html`.) Run this skill's `scripts/validate-package.py <package-folder>` with Python 3 through the runtime's shell tool; the deterministic validator checks required artifacts, placeholders, internal links, SVG XML, detail-doc indexing, ticket schema/catalog/dependency graph/status mapping, and absorption-state structure. Then **self-review** before handing over:

1. **Placeholder scan** — no "TBD", "TODO", or vague requirements anywhere.
2. **Consistency** — no section contradicts another; the build order covers every feature; every feature has acceptance criteria.
3. **Ambiguity** — if a requirement can be read two ways, pick one and make it explicit.
4. **Diagram coverage** — every flow/step a reader would follow visually has a diagram, and every diagram passes the deterministic checks in `references/diagrams.md`: well-formed XML (`xml.dom.minidom.parse` per file), named-node coverage against the section text, render check. Where SVG genuinely cannot be produced, the Mermaid fallback is marked `MERMAID-FALLBACK`. Record method + outcome in `references/decisions.md` (Phase 6 block) — never mark a diagram valid by eye alone.

**GATE C — The resolved final reviewer reviews the package.** Present it (the HTML deck is the review surface — open `masterplan.html`), walk through the load-bearing decisions briefly, and revise until approved. In delegation mode, this gate is where every `provisional / agent-decided` decision gets its one batch review.

## Generator state — `references/decisions.md`

The pipeline itself must survive interruption, mirroring what it preaches. Create the package shell at intake in the artifact root resolved by workflow binding; write `references/workflow-binding.md` first. As each phase completes, append its confirmed outcomes to `references/decisions.md` inside that package. If Gate A rejects the pitch, remove the empty shell or retain it as an explicitly rejected investigation record according to local policy:

```markdown
## Phase 1 — Pitch (confirmed YYYY-MM-DD)
⟨the confirmed pitch paragraph⟩

## Phase 2 — Absorption map
⟨entry: idea-first | artifact-first + source⟩
⟨tree-map path + logic analysis path, or N/A for idea-only / black-box⟩
⟨absorption level + the one difference + scan summary⟩

## Phase 3 — Product decisions
⟨each Q → decision, including "agent decided: ⟨rationale⟩" entries⟩

## Phase 4 — Technical decisions
⟨stack (decision-authority-ratified; runner-ups → §20), APIs verified, reference map, testing strategy⟩

## Phase 5 — Validation
⟨blockers found → resolutions; rejected suggestions⟩

## Phase 6 — Package written + self-review
⟨files written (incl. overflow detail docs under references/); self-review results: placeholder scan, consistency, diagram verification method + outcome; Gate C approval⟩
```

On session start with a partial package: read this file, state which phase you are resuming, and continue.

## Reference files

- `references/masterplan-template.md` — authoritative package sections, including §18 ticket map.
- `references/ticket-contract.md` — local ticket schema, catalog, generic queue mapping, executor protocol.
- `references/execute-template.md` and `references/status-template.md` — execution prompt and status/export surface.
- `references/workflow-binding.md` — roles, authority, capabilities, artifact root, canonical queue.
- `references/validation-rubric.md` and `scripts/validate-package.py` — semantic red team and deterministic package checks.
- Load other playbooks/templates when their branch fires: prior art, code absorption, UI, diagrams, HTML, overflow details, false-premise verdict, revision.

## Revise mode — the masterplan stays alive

A masterplan that cannot change becomes a lie the first time the product changes. When the user requests a change to a project with an existing package, follow `references/revise-playbook.md`:

1. **Load state** — read masterplan.md, `references/workflow-binding.md`, `references/decisions.md`, and the canonical task state named by the binding (`STATUS.md` only when it is the fallback); understand what is already built.
2. **Classify the change** and run **only the affected phases** — a new user-facing feature may need a prior-art check and a few interrogation questions; a stack swap needs phase 4; a copy tweak needs neither.
3. **Impact analysis** — show the resolved decision authority which masterplan sections change and which built milestones are invalidated, before writing anything.
4. **Validate** — significant changes go through the red-team gate again, scaled down: the validator sees the change and its impact, not the whole package.
5. **Write the delta** — update affected sections and local ticket contracts/catalog, bump version, append changelog, update canonical status, and mark invalidated completed tickets `needs-rework`. Preserve stable IDs and history. Regenerate external-mode `STATUS.md` export and `masterplan.html` (`references/html-export.md`).

Revise mode pairs with EXECUTE.md's change-guard rule: the executor refuses ad-hoc scope changes and points here; revise mode makes the front door cheap. Together they keep the document permanently truthful.
