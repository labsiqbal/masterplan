# cut-once — Design Document

> *"Measure twice, cut once."*

**Date:** 2026-07-03
**Status:** Approved design, pre-implementation
**Replaces:** the former `complete-prd-builder-skill` draft (fully discarded by owner decision; git history retained)

## 1. What this is

`cut-once` is an agent skill that turns a raw product idea — anything from a one-sentence thought to a long messy chat dump — into a **complete, execution-ready PRD package**: a folder that any capable coding agent can pick up and build end-to-end from a **single prompt**, with resumable progress if the run is interrupted.

It is written in plain English with zero hardcoded paths, engine names, or workspace assumptions, packaged for publication (in the style of the superpowers plugin), and installable into any skill-capable agent system (Claude Code, Codex, Hermes, Gemini CLI) or usable as a manual playbook.

## 2. Why existing approaches fall short

- **Interactive brainstorming/design skills** (e.g. superpowers `brainstorming`) deliberately scope down to an MVP and hand off to iterative implementation. That philosophy is correct for interactive development but wrong for one-shot execution: the goal here is a *complete* document, with the full product vision intact, where build order sequences execution instead of shrinking scope.
- **Classic PRDs are written for humans.** Prose-heavy documents full of options and "TBD"s force the executing agent to guess. A one-shot-executable PRD must contain **decisions, not discussion**: a chosen stack, a real schema, concrete contracts, explicit acceptance criteria.
- **Nothing gets built from scratch without a reason.** Most product ideas are recombinations of things that already exist. A PRD that ignores prior art wastes the executing agent's effort re-inventing solved components — and wastes the owner's opportunity to simply deploy an existing tool when one fits.

## 3. Core principles

1. **Decisions, not discussion.** Every section of the PRD resolves to a single chosen answer with a short rationale. No option lists, no "TBD".
2. **Honest consultant, not a PRD machine.** If research shows the idea already exists as a deployable product, the skill says "don't build this — deploy X" and produces a setup/adaptation document instead of a from-scratch PRD.
3. **Nothing from scratch without a reason (chimera principle).** Products are assembled from proven parts. Every major component is anchored to a reference implementation (ideally open source, license-checked) to adapt or learn from — observe, imitate, modify.
4. **Cheap before expensive.** No research spend until the idea passes a clarity gate; no deep research until a quick scan confirms direction; no 50-page document until an independent validator passes the decision set.
5. **The user answers product questions; the agent makes technical decisions.** The user is asked about audience, features, budget, and the product's fate (open source / commercial / internal). Stack, database, architecture, security are decided by the agent and written down with rationale.
6. **The agent is not a yes-man.** The user can describe any flow they want, but the agent challenges vague or contradicted choices using evidence from prior-art research.
7. **Scale the document to the project.** A small tool gets a short PRD; a large app may legitimately need 50 pages. Length is an output, not a target.

## 4. Pipeline — six phases, three gates

```
1. Intake + clarification loop ── GATE A: researchable pitch confirmed
2. Prior-art: quick scan → direction confirmed → deep-dive → honest verdict
3. Product/business interrogation with evidence-based correction
4. Technical research + per-component reference map
5. Validate: fresh red-team agent ── GATE B: zero blockers
6. Write the package (+ final self-review) ── GATE C: user reviews package
```

### Phase 1 — Intake + clarification loop

Accept the idea in any form. Before any research, the agent must be able to state a **researchable pitch**: one paragraph covering (a) what the thing is, (b) who it is for, (c) the user's core action — and the user must confirm "yes, that's what I mean."

If the idea is too raw, the agent runs a **cheap clarification loop**: conversation and model knowledge only — no web research, no tools. It may offer directions ("do you mean like this, or like that?") until the pitch locks. **Gate A:** research may not start until the pitch is confirmed. Rationale: research is the most expensive phase; never spend it on an idea that may change shape tomorrow.

### Phase 2 — Prior-art research + honest verdict

Staged to keep waste cheap:

1. **Quick scan** — identify 3–5 existing products/projects closest to the pitch.
2. **Direction check** — present them to the user: "your idea resembles X and Y; their flow works like this — is that what you have in mind?" Differences surface here: is a divergence deliberate differentiation, or does the user simply not know the proven pattern?
3. **Deep-dive** — only after the user confirms direction: flows, page structures, tech stacks, open-source availability, licenses.
4. **Honest verdict** — one of:
   - **Don't build.** A deployable product already covers the idea. The output becomes a setup/adaptation document, not a from-scratch PRD.
   - **Build with differentiation.** Similar things exist but there is a gap. The PRD must state **the one clear difference** that justifies building.
   - **Build fresh.** No meaningful prior art; components still get anchored to references where possible.

### Phase 3 — Product/business interrogation with correction

The user is asked **only product and business questions** — target users, features and their behavior, monthly budget for infrastructure/APIs, the product's fate (open source / commercial product / internal tool). Target load: roughly a dozen questions, not sixty.

The user may describe the flows they want in their own words. The agent corrects with evidence, not opinion: "the flow you describe conflicts with how users behave in X, Y, Z — all of them do it this way because ⟨reason⟩. Deliberate difference, or adopt the proven pattern?" Every disagreement resolves into a recorded decision.

**Question style (applies to phases 1 and 3):**

- **One question per turn.** Never a wall of questions; each answer steers what gets asked next (adaptive — answers can eliminate later questions entirely).
- **Multiple choice preferred** over open-ended whenever the answer space allows it. On platforms with interactive question UI, use it; otherwise present numbered options in text.
- **Mark a recommended option** with a one-line reason, so a non-technical user can simply agree or steer away.
- **Always include a "you decide" escape hatch.** Choosing it is not a non-answer: the agent makes the decision itself and records it in the PRD as an agent decision with rationale. Full delegation never stalls the pipeline.

### Phase 4 — Technical research + reference map

The agent makes all technical decisions and verifies them against reality:

- **Stack chosen** (not listed as options), justified against the product's needs, budget, and fate.
- **External APIs verified alive**, with current pricing checked against the stated budget.
- **Per-component reference map:** each major component is anchored to a proven implementation — "video timeline → adapt pattern from repo X (MIT)"; "chat streaming → proven in repo Y." Licenses are checked so no incompatible code (e.g. GPL into a closed-source product) is pulled in.

### Phase 5 — Validate (red team)

A **fresh agent with no conversation context** reviews the full decision set before the PRD is written. It receives a **decision summary package** — pitch, prior-art verdict, feature list, flows, technical decisions with rationale, reference map — *not* the conversation transcript, so it cannot inherit the conversation's bias.

Its mandate is explicitly adversarial: *find what is wrong, not what is good.* Checklist:

- **Completeness** — forgotten aspects? (auth, payments, email, backups, legal/privacy, error handling, mobile)
- **Consistency** — do any decisions contradict each other?
- **Feasibility** — is the stack realistic? do the named APIs exist at the assumed price?
- **Optimization** — is there a simpler or cheaper path to the same outcome?
- **Risk** — what is most likely to break a one-shot execution midway?

Output is a structured report at three levels: 🔴 **Blocker** (must be resolved — return to the relevant phase), 🟡 **Improvement** (decide with the user), 🟢 **Nice-to-have**. Rejected suggestions are recorded in the PRD as "considered and rejected because ⟨reason⟩" so the executing agent doesn't "fix" deliberate choices. **Gate B:** the PRD may not be written while blockers remain.

Validation runs **by default**; the user may skip it for tiny projects. The report is saved to `references/validation-report.md`.

**Cross-engine note:** on platforms with subagent support this is a spawned agent; the skill describes the fallback for platforms without it — run the same rubric as a self-review in a separate, clean context (weaker, but the gate still exists).

### Phase 6 — Write the package

Written section by section, then self-reviewed (placeholder scan, internal consistency, ambiguity check) before being handed to the user. **Gate C:** the user reviews the finished package.

## 5. Output package

```
prd-<slug>/
├── PRD.md        ← the complete document (length scales with the project)
├── EXECUTE.md    ← the single execution prompt
├── STATUS.md     ← milestone checklist, pre-filled, maintained by the executor
└── references/   ← research notes: prior-art comparison, repos, absorbed patterns,
                    validation-report.md
```

The package is engine-agnostic markdown. Where the package folder is created follows the conventions of the workspace the skill runs in (project-local by default; never a hardcoded path).

### PRD.md — required sections

1. Summary & problem statement
2. Prior-art & differentiation table — what exists, what we absorb from each, **the one difference** that justifies building
3. Target users & business model
4. Feature list with **acceptance criteria per feature**
5. User flows (mermaid diagrams)
6. Pages/screens inventory with per-page components
7. Data model — a real schema, not "needs a database"
8. API contracts (internal endpoints: routes, payloads, responses)
9. External integrations & AI roles (verified alive, priced)
10. Chosen tech stack + rationale
11. Architecture overview
12. Security requirements
13. Deployment & infrastructure + monthly cost estimate
14. Per-component reference map (repo, license, what to adapt)
15. Design direction — visual register (brand vs product), mood, 2–3 look-reference products, and an explicit "what this must NOT look like". Prevents functionally-correct-but-generic output; executors with design skills run with it, executors without one at least have a direction.
16. Content & seed data — what the app contains on day one and where it comes from (AI-generated, user-provided, imported), with a minimum quantity so the product looks alive, not an empty shell.
17. Required credentials — every API key/account the owner must provide, and at which build milestone each is needed.
18. Build order (the sequence STATUS.md mirrors)
19. Explicit non-goals — what is deliberately NOT built
20. Considered-and-rejected decisions (from validation and interrogation)
21. Product fate: open source / commercial / internal, and what that implies (license, docs, hardening level)
22. Version & changelog — PRD version number plus a dated log of revisions (maintained by revise mode)

### EXECUTE.md — the single prompt

- "Read PRD.md fully; it contains every decision. Do not re-litigate decisions; the considered-and-rejected section explains deliberate choices."
- **Resume rule:** "Before starting, read STATUS.md. If items are checked, quickly verify they actually work — do not trust blindly — then continue from the first unchecked item."
- **Evidence rule:** a milestone may only be checked with evidence (test passing, page rendering, command succeeding) — never "the code is written."
- **Credentials rule:** never invent or fake keys. Generate `.env.example` early; when a milestone needs a real credential (per PRD's required-credentials section), stop and ask the owner — do not continue by pretending.
- **Change-guard rule:** if the owner (or anyone) requests a scope change mid-build, do not improvise. Redirect the change through cut-once's revise mode so the PRD is updated first; the PRD is the single source of truth for the build's entire life. This rule is the package's defense against document staleness.
- Build order and definition of done (derived from acceptance criteria).

### STATUS.md

Pre-filled by cut-once with the build order as unchecked milestones. The executing agent checks items off with a short note and evidence, and records blockers. Doubles as a human-readable progress view — the owner can check progress at any time without asking the agent.

The **final milestone is always a full QA pass**: run every acceptance criterion from the PRD end-to-end and record the evidence. "Done" means verified against the PRD, not "last feature milestone checked."

### Generator state — `references/decisions.md`

The pipeline itself is resumable, mirroring the philosophy it preaches. As each phase completes, cut-once appends its confirmed outcomes (locked pitch, prior-art verdict, interrogation decisions, technical decisions, validation results) to `references/decisions.md`. If the session dies mid-pipeline, a fresh session reads this file and resumes from the first incomplete phase instead of restarting the interview.

## 6. Revise mode — the PRD stays alive

A PRD that cannot change becomes a lie the first time the product changes. Revise mode is a first-class entry point: the user opens an existing package and requests a change (new feature, changed decision, dropped scope). Flow:

1. **Load state** — read PRD.md, STATUS.md, and `references/decisions.md`; understand what has already been built.
2. **Classify the change** and run **only the affected phases**: a new user-facing feature may need a prior-art check and interrogation questions; a stack swap needs technical research; a copy change needs neither.
3. **Impact analysis** — list which PRD sections change and which already-built milestones are invalidated.
4. **Validate** — significant changes go through the red-team gate again (scaled down: the validator sees the change + impact, not the whole package).
5. **Write the delta** — update affected PRD sections, bump the version, append to the changelog, add new milestones to STATUS.md, and mark invalidated ones as *needs rework* (never silently uncheck history).

Revise mode is the counterpart of EXECUTE.md's change-guard rule: the executor refuses ad-hoc scope changes and points to revise mode; revise mode makes going through the front door cheap. Together they keep the document permanently truthful — the defense against the stale-docs decay that kills most project documentation.

## 7. Packaging & repository layout

```
cut-once/                        (this repo — publishable skill package)
├── README.md                    (what it is, install instructions per engine)
├── LICENSE                      (MIT)
├── docs/
│   └── 2026-07-03-cut-once-design.md   (this document)
└── skills/
    └── cut-once/
        ├── SKILL.md             (the skill: pipeline, gates, behavior)
        └── references/
            ├── prd-template.md          (full PRD.md section templates)
            ├── execute-template.md      (EXECUTE.md template incl. resume/evidence rules)
            ├── status-template.md       (STATUS.md template)
            ├── question-bank.md         (product/business interrogation questions)
            ├── validation-rubric.md     (red-team mandate, checklist, report format)
            ├── research-playbook.md     (staged prior-art method, license checking)
            └── revise-playbook.md       (revise mode: load → classify → impact → validate → delta)
```

All content in English. No local paths, no personal names, no engine-specific assumptions in the skill body (engine-specific notes allowed as clearly-marked examples). After the owner approves the built skill, it may be promoted into the local cross-engine registry and symlinked into engines — promotion is a separate, explicitly-approved step per the lab's rules.

## 8. Explicitly out of scope (deferred)

- **Dashboard / UI wrapper.** The skill is the engine; a UI (e.g. as a module in an agent cockpit product) can be layered on later without changing the engine. The 4-file markdown package is deliberately dashboard-friendly.
- **Executing the PRD.** cut-once produces the package; execution is the consuming agent's job. EXECUTE.md is the bridge.
- **Reusing content from the former draft in this repo.** Owner decision: full rewrite, no files carried over.
