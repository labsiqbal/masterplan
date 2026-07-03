# cut-once Skill Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the publishable `cut-once` skill package — a 6-phase, 3-gate pipeline that turns raw product ideas into complete, one-shot-executable PRD packages.

**Architecture:** A pure-markdown skill package: one `SKILL.md` orchestrator that carries the pipeline, gates, and behavioral rules, plus seven `references/` files it points to for templates and playbooks (progressive disclosure — SKILL.md stays lean, detail lives in references). No code except doc content.

**Tech Stack:** Markdown + YAML frontmatter only. Git for history. Verification via `grep` portability audits and content checklists.

**Source of truth:** `docs/2026-07-03-cut-once-design.md` (approved). Where this plan and the design doc conflict, the design doc wins — flag the conflict, don't improvise.

**Hard rules for every file in this package:**
- English only. Plain prose an agent on ANY platform can follow.
- Zero hardcoded local paths (`/home/`, `~/_build`, `~/_agent`, `kuya`, usernames).
- Zero engine lock-in in normative text. Engine names (Claude Code, Codex, Hermes, Gemini CLI) may appear ONLY in clearly-marked example/install notes.
- No "TBD"/"TODO" anywhere in shipped files.
- Tone: imperative instructions to the executing agent ("Ask one question per turn"), not essays.

---

### Task 1: Repo skeleton + LICENSE

**Files:**
- Create: `LICENSE`
- Create: `.gitignore`
- Directories: `skills/cut-once/references/`, `docs/plans/` (already exists)

- [ ] **Step 1: Create directories**

```bash
mkdir -p skills/cut-once/references
```

- [ ] **Step 2: Write LICENSE** — standard MIT text, copyright line:

```
MIT License

Copyright (c) 2026 cut-once contributors
```

(full standard MIT body follows — use the canonical text verbatim)

- [ ] **Step 3: Write `.gitignore`**

```
.DS_Store
*.swp
node_modules/
```

- [ ] **Step 4: Verify**

Run: `ls skills/cut-once/references LICENSE .gitignore` — all exist.

- [ ] **Step 5: Commit** — `chore: repo skeleton + MIT license`

---

### Task 2: `skills/cut-once/SKILL.md` — the orchestrator

**Files:**
- Create: `skills/cut-once/SKILL.md`

This is the core deliverable. Target length: 250–400 lines. It must be readable top-to-bottom as the complete operating procedure; references carry the bulk detail.

- [ ] **Step 1: Write frontmatter**

```yaml
---
name: cut-once
description: Use when turning a product idea — from a one-sentence thought to a long messy chat — into a complete, execution-ready PRD package that a coding agent can build end-to-end from a single prompt. Covers idea clarification, prior-art research with an honest build/don't-build verdict, product interrogation, technical decisions with per-component reference maps, adversarial validation, and revision of existing packages. Also use when the user asks to add features or change scope on a project that already has a cut-once package (revise mode).
version: 1.0.0
license: MIT
metadata:
  tags: [prd, requirements, planning, one-shot, product]
---
```

- [ ] **Step 2: Write body sections, in this order:**

1. **Motto & overview** — "Measure twice, cut once." 3–5 sentences: what it produces (the 4-file package), for whom, and the one-shot execution goal.
2. **Core principles** — the 7 from design doc §3, each one line: decisions-not-discussion; honest consultant; chimera principle (nothing from scratch without a reason); cheap-before-expensive; user answers product questions, agent decides technical; not a yes-man; scale the document to the project.
3. **When to use / when not to use** — use: new idea → PRD package; existing package + change request → revise mode. Not: tiny bugfixes, projects that already have a final PRD and only need coding (point to an implementation-planning skill), pure copywriting.
4. **Pipeline map** — the 6-phase / 3-gate ASCII diagram from design doc §4, verbatim.
5. **Phase 1 — Intake** — clarification loop rules: conversation + model knowledge ONLY, no web research, no tools; researchable-pitch definition (what / for whom / core action); GATE A wording: "Do not begin research until the user confirms the pitch."
6. **Phase 2 — Prior-art** — staged: quick scan (3–5 candidates) → direction check with user → deep-dive → honest verdict. The three verdicts verbatim: **Don't build** (deploy X; package becomes a setup/adaptation document), **Build with differentiation** (must state THE one difference), **Build fresh**. Point to `references/research-playbook.md`.
7. **Phase 3 — Interrogation** — product/business questions only (~a dozen); agent corrects with evidence from phase 2; question style block (one per turn; multiple choice preferred; recommended option marked with one-line reason; ALWAYS a "you decide" escape hatch that converts to a recorded agent decision). Point to `references/question-bank.md`.
8. **Phase 4 — Technical research** — agent decides stack/db/architecture/security with written rationale; verify external APIs alive + priced within budget; per-component reference map with license check (warn on incompatible licenses, e.g. GPL into closed-source).
9. **Phase 5 — Validate** — spawn a FRESH agent with no conversation context; send the decision summary, never the transcript; adversarial mandate "find what is wrong, not what is good"; 🔴 Blocker / 🟡 Improvement / 🟢 Nice-to-have; GATE B: "Do not write the PRD while blockers remain." Fallback for platforms without subagents: run the same rubric as a self-review in a clean context. Default ON, skippable for tiny projects. Report saved to `references/validation-report.md` in the output package. Point to `references/validation-rubric.md`.
10. **Phase 6 — Write the package** — the 4-file package layout; write section by section; self-review (placeholder scan, consistency, ambiguity); GATE C: user reviews. Point to the three template references.
11. **Generator state** — after each phase, append confirmed outcomes to the package's `references/decisions.md`; on session start, if a partial package exists, resume from the first incomplete phase instead of re-interviewing.
12. **Revise mode** — the 5-step flow from design doc §6 (load state → classify change & run only affected phases → impact analysis → scaled-down validation → write the delta: bump version, changelog, new milestones, mark invalidated ones *needs rework*, never silently uncheck). Point to `references/revise-playbook.md`.
13. **Output location note** — package folder `prd-<slug>/` created per the conventions of the workspace the skill runs in; project-local by default; never a fixed path.

- [ ] **Step 3: Verify content**

Checklist — every item must be answerable "yes, and I can point to the line":
- [ ] All 3 gates present with explicit "do not proceed" wording?
- [ ] All 3 verdicts present?
- [ ] Escape-hatch rule present?
- [ ] Subagent fallback present?
- [ ] Revise mode present with all 5 steps?
- [ ] Every `references/*.md` pointer matches a file this plan creates?

Run: `grep -nE '/home/|kuya|~/_' skills/cut-once/SKILL.md` — Expected: no matches.

- [ ] **Step 4: Commit** — `feat: cut-once SKILL.md orchestrator`

---

### Task 3: `references/prd-template.md`

**Files:**
- Create: `skills/cut-once/references/prd-template.md`

- [ ] **Step 1: Write the template** — all 22 sections from design doc §5, in order, each with: an H2 heading, a one-line instruction of what belongs there, and a concrete mini-example or skeleton. Non-negotiable details:
  - §2 Prior-art & differentiation: a markdown table skeleton `| Product | What it does | What we absorb | License |` plus a required single-sentence field: **"The one difference: …"**
  - §4 Features: per-feature block skeleton with `Acceptance criteria:` as a checkbox list.
  - §5 User flows: a small mermaid `flowchart TD` example.
  - §7 Data model: a real example schema (SQL `CREATE TABLE` or equivalent) — instruction says "write the actual schema, not 'needs a database'".
  - §8 API contracts: route + request/response JSON example.
  - §15 Design direction: register (brand vs product), mood words, 2–3 look-references, and a required **"Must NOT look like: …"** line.
  - §16 Content & seed data: source (AI-generated / user-provided / imported) + minimum quantities.
  - §17 Required credentials: table `| Credential | Used by | Needed at milestone |`.
  - §20 Considered-and-rejected: `| Suggestion | Source (validation/interrogation) | Why rejected |`.
  - §22 Version & changelog: `## v1.0 — YYYY-MM-DD — initial` list format.
  - Global banner at top of template: "Every section resolves to a DECISION with a short rationale. No option lists. No TBD."

- [ ] **Step 2: Verify** — count H2 sections = 22; `grep -c '^## ' …` Expected: 22 (+0 tolerance). Portability grep as in Task 2.

- [ ] **Step 3: Commit** — `feat: PRD template (22 sections)`

---

### Task 4: `references/execute-template.md` + `references/status-template.md`

**Files:**
- Create: `skills/cut-once/references/execute-template.md`
- Create: `skills/cut-once/references/status-template.md`

- [ ] **Step 1: Write execute-template.md** — the EXECUTE.md skeleton the skill fills in. Must contain, as numbered rules addressed to the executing agent:
  1. Read PRD.md fully; do not re-litigate decisions; considered-and-rejected explains deliberate choices.
  2. **Resume rule** — read STATUS.md first; verify checked items actually work before trusting them; continue from first unchecked.
  3. **Evidence rule** — check a milestone only with evidence (test passing / page rendering / command succeeding), never "code is written".
  4. **Credentials rule** — never invent keys; create `.env.example` early; stop and ask the owner when a milestone needs a real credential (per PRD §17).
  5. **Change-guard rule** — refuse ad-hoc scope changes; direct them to cut-once revise mode; the PRD is the single source of truth for the build's life.
  6. Build order reference + definition of done = the final QA milestone.

- [ ] **Step 2: Write status-template.md** — skeleton: header (project, PRD version, started date), milestone checkbox list mirroring PRD build order, per-milestone note + evidence line, `Blockers:` section, and the mandatory final milestone verbatim: **"Full QA pass — run every acceptance criterion from the PRD end-to-end and record evidence."** Plus the marker convention: `[x]` done with evidence, `[ ]` pending, `[!]` needs rework (set by revise mode, never silently unchecked).

- [ ] **Step 3: Verify** — both files: portability grep; execute-template contains all 5 named rules; status-template contains `[!]` convention and the QA milestone.

- [ ] **Step 4: Commit** — `feat: EXECUTE and STATUS templates`

---

### Task 5: `references/question-bank.md`

**Files:**
- Create: `skills/cut-once/references/question-bank.md`

- [ ] **Step 1: Write the bank** — organized by phase:
  - **Phase 1 (clarification):** ~6 question patterns for locking the pitch (what is it / who is it for / core action / closest analogy / one-sentence success).
  - **Phase 3 (interrogation):** ~12 core questions grouped: audience & problem (2–3), features & flows (3–4), business (monthly infra/API budget, revenue model) (2–3), fate: open source / commercial / internal (1), design taste (register + 2 look-references) (2), content on day one (1).
  - Each question written in the multiple-choice format with a marked recommended option example and the mandatory final option: `You decide — make the call and record your rationale in the PRD.`
  - **Adaptive rules:** which answers eliminate which later questions (e.g. "internal tool, just me" → skip pricing/onboarding/marketing questions).
  - Cap note: "Aim for ~12 questions total; the bank is a menu, not a script."

- [ ] **Step 2: Verify** — every listed question includes the "You decide" option; portability grep.

- [ ] **Step 3: Commit** — `feat: question bank`

---

### Task 6: `references/validation-rubric.md`

**Files:**
- Create: `skills/cut-once/references/validation-rubric.md`

- [ ] **Step 1: Write the rubric** — three parts:
  1. **The validator prompt template** (verbatim, fill-in-the-blanks): fresh agent; receives decision summary only; mandate: "Your job is to find what is wrong, not what is good. You get no credit for approval."
  2. **Checklist** — the 5 axes with concrete sub-prompts: Completeness (auth, payments, email, backups, legal/privacy, error handling, mobile); Consistency; Feasibility (APIs exist? at that price?); Optimization (simpler/cheaper path?); Risk (what breaks a one-shot run midway?).
  3. **Report format** — 🔴 Blocker / 🟡 Improvement / 🟢 Nice-to-have with a required `Why + suggested fix` per finding; disposition rules (blockers → return to owning phase; improvements → decide with user; rejected → record in PRD §20).
  Plus: scaled-down variant for revise mode (validator sees change + impact analysis only), and the no-subagent fallback instruction.

- [ ] **Step 2: Verify** — contains prompt template, 5 axes, 3 levels, fallback, revise variant; portability grep.

- [ ] **Step 3: Commit** — `feat: validation rubric`

---

### Task 7: `references/research-playbook.md`

**Files:**
- Create: `skills/cut-once/references/research-playbook.md`

- [ ] **Step 1: Write the playbook** — stages with cost discipline stated explicitly:
  1. **Quick scan** (cheap): find 3–5 closest products/projects; one paragraph each: what it is, its core flow, open-source or not.
  2. **Direction check**: present to user; classify each divergence as deliberate differentiation vs unknown-pattern.
  3. **Deep-dive** (only after confirmation): flows, page structures, stacks, repos, licenses.
  4. **Verdict**: decision tree for the three verdicts, incl. what the package becomes under "don't build" (setup/adaptation document).
  5. **License table**: permissive (MIT/Apache/BSD → adapt freely with attribution), weak copyleft (MPL/LGPL → boundaries apply), strong copyleft (GPL/AGPL → do NOT absorb into closed-source; pattern-learning only) — one-line guidance each, with "when unsure, learn the pattern, don't copy the code".
  6. **Reference map format**: `| Component | Reference (repo/product) | License | What to absorb (pattern vs code) |`.

- [ ] **Step 2: Verify** — 3 stages + verdict tree + license table + map format present; portability grep.

- [ ] **Step 3: Commit** — `feat: research playbook`

---

### Task 8: `references/revise-playbook.md`

**Files:**
- Create: `skills/cut-once/references/revise-playbook.md`

- [ ] **Step 1: Write the playbook** — the 5 steps from design doc §6, each with concrete instructions:
  1. **Load state** — read PRD.md, STATUS.md, references/decisions.md; summarize what is built vs pending.
  2. **Classify** — table mapping change types → phases to rerun (new user-facing feature → phases 2+3 slice; stack/infra change → phase 4; copy/content tweak → none, straight to delta).
  3. **Impact analysis** — output format: affected PRD sections list + invalidated milestones list, shown to user before writing anything.
  4. **Validate** — significance test (touches data model, security, external APIs, or >2 PRD sections → validate; else skip), using the rubric's scaled-down variant.
  5. **Write the delta** — update sections; bump version (minor = additive, major = changes built behavior); append changelog entry; append new milestones to STATUS.md; flag invalidated ones `[!] needs rework` — never silently uncheck; append the revision decisions to decisions.md.
  Closing note: pair with EXECUTE.md's change-guard rule — quote it once so the playbook stands alone.

- [ ] **Step 2: Verify** — 5 steps present; `[!]` convention consistent with Task 4's status-template; version bump rules present; portability grep.

- [ ] **Step 3: Commit** — `feat: revise playbook`

---

### Task 9: `README.md`

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README** — sections:
  1. Name + motto + one-paragraph pitch (what you get: the 4-file package; the one-shot goal).
  2. **How it works** — the 6-phase/3-gate diagram + one line per phase.
  3. **The output package** — the `prd-<slug>/` tree with one-line explanations.
  4. **What makes it different** — honest consultant verdict; chimera/reference-map; machine-executable PRD; revise mode vs stale docs; resumable both ways (generator + executor).
  5. **Install** — generic: "copy `skills/cut-once/` into your agent's skill directory"; engine-specific paths as a clearly-marked examples table (Claude Code `~/.claude/skills/`, etc.) — this is the ONLY place engine paths may appear.
  6. **Package layout** (repo tree) + License (MIT).

- [ ] **Step 2: Verify** — portability grep on normative sections (engine names allowed only inside the install examples table); no reference to the owner's private workspace.

- [ ] **Step 3: Commit** — `docs: README`

---

### Task 10: Package-wide audit

**Files:**
- Modify: any file that fails a check

- [ ] **Step 1: Portability audit**

```bash
grep -rnE '/home/|kuya|~/_build|~/_agent|minarflow|hermes-profile' --include='*.md' . | grep -v docs/
```
Expected: no matches (docs/ = internal design/plan, exempt).

- [ ] **Step 2: Placeholder audit**

```bash
grep -rniE 'TBD|TODO|FIXME|fill in|later' skills/ README.md
```
Expected: no matches (except legitimate uses inside instruction prose — judge each hit; "later" may appear in normative rules like "never 'implement later'").

- [ ] **Step 3: Cross-reference audit** — every `references/…` pointer in SKILL.md resolves to an existing file; every template/playbook is pointed to at least once; the 22-section count in SKILL.md, prd-template.md, and README agree; `[!]` convention identical in status-template and revise-playbook.

- [ ] **Step 4: Frontmatter check** — SKILL.md frontmatter is valid YAML (`python3 -c "import yaml,sys; yaml.safe_load(open('skills/cut-once/SKILL.md').read().split('---')[1])"`).

- [ ] **Step 5: Fix anything found, then commit** — `chore: package audit fixes`

---

### Task 11: Fresh-eyes design-conformance review

- [ ] **Step 1: Dispatch a fresh reviewer** (subagent) with: the design doc + the built package. Question: "Does the package implement every requirement in the design doc? List gaps and contradictions. Do not praise."
- [ ] **Step 2: Triage findings** — fix real gaps; record rejected suggestions in the commit message.
- [ ] **Step 3: Final commit** — `fix: design-conformance review fixes`

---

## Self-review notes

- Spec coverage: design doc §3 principles → Task 2 step 2.2; §4 phases → Task 2 steps 2.4–2.10 + Tasks 5–7; §5 package → Tasks 3–4; §6 revise → Task 8 (+ Task 2 step 2.12); §7 repo layout → Tasks 1, 9; §8 out-of-scope → nothing to build (correct).
- The plan intentionally contains outlines + non-negotiable verbatim fragments rather than full file text: the deliverables ARE prose, and duplicating them here would make the plan the product. Each task carries enough structure that a zero-context writer produces conforming files, and Tasks 10–11 catch drift.
- Commits are per-task; nothing is pushed anywhere.
