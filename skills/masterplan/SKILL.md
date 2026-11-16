---
name: masterplan
description: >
  Use when turning a product idea, or a given repo/SaaS/workflow, into a
  build-ready masterplan package, or changing an existing package. Trigger:
  /masterplan, plan this product, rebuild this repo, bongkar repo ini, our
  version of X.
license: MIT
metadata:
  version: 0.3.0
  status: draft
  author: Hermes
  tags: [prd, requirements, planning, one-shot, product]
---

# masterplan

> **Every decision made before the first line of code.**

Turn a raw idea, or a given source (repo, product, workflow), into a **masterplan package**: a folder any capable coding agent builds end-to-end from one prompt, resumable if interrupted. You are running an investigation that ends in a document where every question is already answered, so execution can be one-shot. Given a readable repo, map it folder by folder and reconstruct its logic **before** deciding what our version keeps, drops, or changes.

A change to a project that already has a package goes to **Revise mode** at the bottom.

## Core principles

1. **Decisions, not discussion.** Every section resolves to one chosen answer with a short rationale. No option lists, no "TBD".
2. **Adopt-heavy builder, not a gatekeeper.** The standing assumption is *we are building*. Prior art exists to be absorbed (flows, patterns, architectures, and code when the license allows), never to veto the build. The only honest stop is a **false premise** (Phase 2).
3. **Chimera principle.** Products are assembled from proven parts. Anchor every major component to a reference implementation (observe, imitate, modify), license checked.
4. **Cheap before expensive.** Tools are allowed in any phase once the spend has a purpose. Read-only inspection of an existing target is cheap and encouraged early. Deep or online research waits until the pitch is locked; quick-scan before deep-dive; validate before writing.
5. **Authority answers product; you decide technical; the stack is ratified.** Resolve the decision authority from `references/workflow-binding.md` (usually the user). Ask them about audience, features, budget, and the product's fate. Decide architecture, data model, and security yourself and write down why. **Weigh quality, simplicity, robustness, scalability, and long-term maintainability above development cost** in every technical decision: the cheaper-to-build option never wins by being cheaper.
6. **Grill: critical adversarial collaborator in every phase and gate.** Challenge rather than transcribe: the premise and "why now" (Phase 1), unknowing reinvention (2), feature bloat and vague flows (3), the easy default (4), the whole decision set (5). Every challenge is anchored to evidence and resolves into a recorded decision; adversarial is not contrarian. Gates A/B/C are real checks.
7. **Proportional depth, uniform shape.** Every package has the same required files and template sections; size follows scope. A small tool gets short sections, about five questions, a handful of tickets, no optional detail docs, and only the diagrams its applicable **[diagram]** sections require (a section marked Not applicable carries none). A large scope may get hundreds of tickets and detail documents; that is success, not bloat. Completeness is never traded for brevity. `masterplan.md` stays the index and decision record; overflow detail goes to self-contained topic docs under `references/`, each linked from the section it elaborates.
8. **Ticket-local execution.** Every build unit gets an immutable contract `references/tickets/<ID>.md`, cataloged in `references/tickets/INDEX.md`, so an executor completes one ready ticket without reading the whole masterplan. The canonical project queue owns mutable status (fallback: `STATUS.md`), mapped 1:1 by stable ID. Schema and protocol: `references/ticket-contract.md`.
9. **Portable text core, rendered deck.** Markdown is the source of truth and runs on any runtime. Diagrams are Mermaid blocks inline in the Markdown (`references/diagrams.md`); every section a reader follows visually gets one. `masterplan.html` is a self-contained, offline deck rendered from the Markdown with the diagrams as inline SVG, styled by §15 Design direction (`references/html-export.md`).
10. **UI baseline is a floor, not a feature.** Button states, focus, loading/empty/error, keyboard operability and the rest are a standing standard (`references/ui-baseline.md`) that every package with a UI carries and every executor satisfies. Never interrogate them; the user decides only what goes above the floor.

## When to use

- A product/app/website idea, clear or vague, that should be specified for building.
- A given repo, SaaS, workflow, or video whose **our** version should be specified (artifact-first).
- A messy brainstorm chat that should become an executable plan.
- A change to an existing masterplan package (Revise mode).

Not for: a small bugfix or feature in a codebase without a package; implementation planning when a final PRD already exists; copywriting or marketing content.

Phases 1 and 3 *are* the interrogation: while masterplan is active, run no separate brainstorming skill.

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
6. Write the package (+ self-review) ── GATE C: resolved reviewer approves package
```

**Before Phase 1**, resolve roles, authority, workspace isolation, capabilities, artifact root, and canonical task state via `references/workflow-binding.md`; save the result as package `references/workflow-binding.md`. Project and runtime policy win; generic safe fallbacks apply when absent. After each phase, append its confirmed outcomes to package `references/decisions.md` (`references/decisions-template.md`). If a partial package exists, resume from the first incomplete phase without re-interviewing. Gates, interrogation, and reviews run in plain conversation on every runtime.

### Question style (Phases 1 and 3)

- One question per turn; let each answer steer or eliminate later questions.
- Multiple choice where the answer space allows, through the platform's question UI when available, else numbered options.
- Mark a recommended option with a one-line reason.
- Every question ends with a **"you decide"** hatch. Choosing it is a real answer: decide, and record it as an agent decision with rationale in `references/decisions.md` and in the owning masterplan section. After "you decide" three times in a row, decide the rest yourself and list every agent decision at Gate C.
- Look facts up yourself, from the target or your own knowledge; the user's job is decisions, not research.

## Phase 1 — Intake + clarification loop

Accept the idea in any form: a sentence, a voice-note transcript, a contradictory chat dump, **or a given source** (repo URL, local checkout, SaaS URL, video, workflow). A given source is the pitch target. Classify it:

- **white-box** (readable repo): Gate A states what the source is, who our version is for, and the core action. Map the source before inventing a different product.
- **black-box** (no source): Gate A locks who / what / core action; Phase 2 reconstructs observed behavior only (pattern-only, no `code-absorption.md`).
- **idea-first** (no source): the clarification loop below.

Cheap read-only inspection of a given source before Gate A keeps the pitch true; folder-by-folder mapping belongs to Phase 2.

Before expensive research you must be able to write a **researchable pitch**, one paragraph stating **what** the thing is, **who** it is for, and the user's **core action**. Until you can, run a clarification loop: conversation, model knowledge, and read-only inspection of any codebase, product, or files the idea attaches to. That inspection is often the fastest way to lock the pitch, and it catches false premises ("my app has no memory" when it already does). Offer directions ("like this, or like that?") until the shape is firm.

Grill branch by branch until shared understanding is explicit. Challenge the premise with evidence: is this the real problem or a symptom, and why build it now? A premise that survives locks stronger.

**GATE A — Lock the pitch before prior-art or online research.** Present the paragraph and get an explicit "yes, that's what I mean." If the pitch is writable at intake, run Gate A and record it in `references/decisions.md` **before the first search call**; this checkpoint is the rule's only enforcement.

**Delegation.** Under full delegation (below), skip asking: decide each question yourself and record it as an agent decision with rationale. When the user is merely away, you may self-confirm a gate only toward *less* spend (a false-premise stop, a narrower scope), marked `provisional / agent-decided` so a returning user can correct it. Self-confirming into the expensive phases needs explicit delegation of the whole pipeline ("run it, bring me the package"): then every gate may self-confirm, each marked `provisional / agent-decided`, and all of them batch into one review at Gate C. Full delegation never stalls the pipeline.

## Phase 2 — Research + absorption map

Follow `references/research-playbook.md`. Map first, adapt later: keep/drop/invert decisions wait until the source or confirmed prior art is mapped.

**Artifact-first.** Skip the 3-5 scan as the primary path; deep-dive the given source first. For a readable repo, run `references/code-absorption.md` Stages 1-3: pin, walk folders one by one into a tree-map, reconstruct logic from that map, then license. One or two comparables may follow the map when divergence needs market context; they never replace it.

**Idea-first**, staged so waste stays cheap:

1. **Quick scan**: the 3-5 existing products or projects closest to the pitch.
2. **Direction check**: "your idea resembles X and Y; their flow works like this; is that what you mean?" Classify each divergence as deliberate differentiation or an unknown proven pattern, name unknowing reinvention plainly, and resolve each into a decision.
3. **Deep-dive** after the authority confirms direction: flows, page structures, stacks, open-source availability, licenses. Confirmed OSS that may contribute code takes the tree-map → logic path in `code-absorption.md`.

**Absorption map** (both entries): what proven prior art do we absorb, and how heavily? Every level is a build outcome.

| Absorption level | Meaning |
|---|---|
| **Fork & adapt** | A compatibly-licensed base is already close *in scope and size*: start from it, modify heavily, make it yours. A much larger superset (multi-user platform for a single-user tool) is Differentiate |
| **Assemble (chimera)** | Compose from several proven components/patterns, each anchored to a reference |
| **Differentiate** | Similar things exist with a clear gap: build with the stated difference, borrow the patterns |
| **Fresh** | Genuinely novel (rare): still anchor components to references where possible |

Patterns and ideas (flows, UX, architecture) are free to absorb from anything, proprietary products included. Actual code is license-gated by the table in `references/research-playbook.md`.

**The one brake: false premise.** When grounding shows the request rests on a factually wrong premise (the thing already exists in the user's own target, or the ask rests on a mistaken belief), stop honestly. The package becomes `VERDICT.md` (`references/verdict-template.md`), rendered as `VERDICT.html` per `references/html-export.md`, plus `references/` (decisions, audits, scan); no masterplan, EXECUTE, or STATUS, and Phases 3-6 are skipped. "The facts differ" is a successful finding. "A similar product exists" is never a reason to stop; the ladder absorbs it.

## Phase 3 — Product/business interrogation

Ask the authority **only product and business questions**: audience, features and their behavior, monthly infrastructure/API budget, design taste, day-one content, and the product's fate (open source / commercial / internal). After an artifact-first map, the load-bearing questions are keep / drop / invert against that map and logic, never against a marketing summary. Draw from `references/question-bank.md`; about a dozen questions for a typical product, fewer for a small tool, as many as completeness needs for a large one.

The user may describe the flows they want in their own words. Grill with evidence. Challenge bloat ("what breaks if v1 ships without this?"), vague flows, and unjustified scope. When the user's flow conflicts with research: "X, Y, Z all do it this way because ⟨reason⟩. Deliberate difference, or adopt the proven pattern?"

## Phase 4 — Technical research + reference map

Make the technical decisions by the values in principle 5, verify them against reality, and challenge the easy default: will it scale, will it stay maintainable?

- **Design the stack twice; the authority decides.** Generate 2-3 genuinely different viable stacks, via parallel subagents where available so they are not one idea reskinned. Without subagents, generate them in deliberately separate passes (a different architecture family per pass) and record the single-designer caveat in `references/decisions.md`. Compare on product-framed axes (quality, scalability, maintainability, ecosystem/lock-in), give one opinionated recommendation, and put the call to the authority with the "you decide" hatch (which returns it to your recommendation). §10 records the one chosen stack; runner-ups and why they lost go to §20. Design-it-twice covers the stack and architecture only.
- **Verify external APIs are alive** and their current pricing fits the stated budget.
- **Build the per-component reference map**: "video timeline → adapt pattern from repo X (MIT)". Check licenses with the evidence order in `references/research-playbook.md`; never guess a license from a name, and never absorb incompatible code (e.g. GPL into a closed-source product). When Phase 2 chose Fork & adapt or Assemble, or any row says `Code — adapt`, complete `references/code-absorption.md` Stages 4-7 on top of Stages 1-3 (they fail closed without the tree-map INDEX and logic analysis): absorption units, source→target maps, chimera seam contracts, exhaustive implementation steps.
- **Decide the testing strategy**: tests target external behavior at acceptance level, never implementation, so they survive refactors. Map the §4 acceptance criteria and primary flows into §18 and each owning ticket's acceptance criteria and validation commands.

Present the architecture and data model as Mermaid diagrams where they help review; the component + license map is a table.

## Phase 5 — Validate (red team)

Before writing, submit the decision set to a **fresh agent with no conversation context**, per `references/validation-rubric.md`. Send the decision summary (pitch, absorption map, features, flows, technical decisions with rationale, reference map, proposed ticket graph). **Never send the conversation transcript**: a validator that reads it inherits its bias. The mandate is to find what is wrong across completeness, consistency, feasibility, optimization, and risk, reported as 🔴 Blocker / 🟡 Improvement / 🟢 Nice-to-have.

Blockers return to their owning phase. Improvements are decided with the authority. Rejected suggestions go to §20 so the executor won't "fix" deliberate choices. Save the report as package `references/validation-report.md`, present it in the same format, and collect one disposition per finding (fix / decide-with-user / reject→§20).

**GATE B — No masterplan while blockers remain.** Validation runs by default; the authority may skip it for a tiny project. Without subagents, run the rubric yourself in a clean context: weaker, but the gate still exists.

## Phase 6 — Write the package

Build outcomes only. Complete the package shell created at intake in the artifact root resolved by workflow binding (project-local fallback, never a universal fixed path):

```
masterplan-<slug>/
├── masterplan.md    ← references/masterplan-template.md
├── masterplan.html  ← references/html-export.md
├── EXECUTE.md       ← references/execute-template.md
├── STATUS.md        ← references/status-template.md
└── references/      ← decisions.md, validation-report.md, workflow-binding.md,
                       research notes, ui-baseline.md (UI products),
                       tickets/INDEX.md + tickets/<ID>.md, evidence/<ID>/*,
                       absorption/* (code absorbed), diagrams/*.svg (deck renders), deck-theme.css,
                       INDEX.md + detail docs (as many as completeness needs)
```

1. **`masterplan.md`**: every template section; a section that does not apply keeps its heading with "Not applicable — ⟨reason⟩". Sections marked **[diagram]** carry a Mermaid block per `references/diagrams.md`. Overflow goes to detail docs listed in package `references/INDEX.md` (`references/detail-index-template.md`); the section keeps the decision, the doc keeps the depth, and no doc is orphaned.
2. **Tickets**: decompose §18 per `references/ticket-contract.md` into `references/tickets/INDEX.md` plus one `<ID>.md` per execution unit. §18 lists every catalog ticket once with matching milestone and no unknown IDs; every stable ID maps into canonical task state. Each ticket links enough context to execute without the whole masterplan.
3. **`STATUS.md`**: canonical mutable status when no project queue exists, otherwise a durable read-only export of it; ticket prose lives only in the contracts.
4. **UI baseline**: a product with any user-facing UI gets `references/ui-baseline.md` copied verbatim. Headless API / library / CLI: note "No UI — interaction baseline N/A" in §6.
5. **`masterplan.html`**: per `references/html-export.md`, write `references/deck-theme.css` from §15, render the diagrams with this skill's `scripts/render-diagrams.py <package>` (exit 2 = no renderer: hand-author the deck SVGs per `references/diagrams.md`), build with `scripts/build-deck.py <package>`, and screenshot the result at desktop and phone width.
6. **Validate**: run this skill's `python3 scripts/validate-package.py <package>`. It checks required artifacts, placeholders, internal links, Mermaid block structure (closed, non-empty, known type; full syntax is proven by rendering), SVG XML, detail-doc indexing, the ticket schema, catalog, dependency graph and status mapping, and absorption state.
7. **Self-review**:
   - **Placeholders**: no "TBD", "TODO", or vague requirement anywhere.
   - **Consistency**: no section contradicts another; the build order covers every feature; every feature has acceptance criteria.
   - **Ambiguity**: a requirement readable two ways gets one explicit reading.
   - **Diagrams**: every visually followed flow has one and passes the checks in `references/diagrams.md`: syntax, coverage, and a screenshot read at both widths; record method and outcome in `references/decisions.md`.

**GATE C — The resolved final reviewer approves the package.** Present `masterplan.html` as the review surface, walk the load-bearing decisions briefly, and revise until approved. Under full delegation, every `provisional / agent-decided` decision gets its one batch review here.

## Reference files

- `masterplan-template.md`: authoritative package sections, including the §18 ticket map.
- `ticket-contract.md`: ticket schema, catalog, queue mapping, executor protocol.
- `execute-template.md`, `status-template.md`: execution prompt and status/export surface.
- `workflow-binding.md`: roles, authority, capabilities, artifact root, canonical queue.
- `decisions-template.md`: generator state and resume.
- `diagrams.md` + `scripts/render-diagrams.py`, `html-export.md` + `scripts/build-deck.py`: diagrams and the deck, used by every build package.
- `validation-rubric.md` and `scripts/validate-package.py`: semantic red team and deterministic checks.
- Load the rest when their branch fires: `research-playbook.md`, `code-absorption.md`, `question-bank.md`, `ui-baseline.md`, `detail-index-template.md`, `verdict-template.md`, `revise-playbook.md`.

## Revise mode

A masterplan that cannot change becomes a lie the first time the product changes. Follow `references/revise-playbook.md`:

1. **Load state**: masterplan.md, package `references/workflow-binding.md` and `references/decisions.md`, and the canonical task state named by the binding (`STATUS.md` only when it is the fallback); understand what is built.
2. **Classify the change** and run only the affected phases: a new feature may need a prior-art check and a few questions, a stack swap needs Phase 4, a copy tweak needs neither.
3. **Impact analysis**: show the authority which sections change and which built milestones are invalidated, before writing.
4. **Validate** significant changes through a scaled-down red team that sees the change and its impact.
5. **Write the delta**: update sections and ticket contracts/catalog, bump the version, append the changelog, update canonical status, mark invalidated done tickets `needs-rework`, preserve stable IDs and history, and regenerate the `STATUS.md` export and `masterplan.html`.

EXECUTE.md's change-guard refuses ad-hoc scope changes and points here; together they keep the document truthful.
