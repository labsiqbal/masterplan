# masterplan

> *Every decision made before the first line of code.*

An agent skill that turns a product idea, a given repo/product/workflow, or a long messy chat into a **masterplan package**: a folder any capable coding agent can build end-to-end from a single prompt, with resumable progress if a run is interrupted. Given a readable repo, it maps folders one by one and reconstructs logic before deciding what our version keeps, drops, or changes.

The core is a **portable text pipeline** — plain Markdown, diagrams as hand-authored SVG files (dark tech design system, semantic colors, no rendering library) — that runs on any agent runtime. The finished package carries `masterplan.html`: a self-contained walkthrough render with the SVGs inlined, offline-openable, styled by the product's own design direction.

## How it works

A six-phase pipeline with three review gates:

```
1. Intake + clarification loop ── GATE A: researchable pitch confirmed
   (idea-first or artifact-first)
2. Research: map the source (or prior art) before any adapt
3. Product/business interrogation
4. Technical research + per-component reference map
5. Validate: fresh red-team agent ── GATE B: zero blockers
6. Write the package ── GATE C: resolved reviewer approves package
```

1. **Intake** - clarifies an idea, or a given repo/product/workflow, until it locks into a confirmed pitch: what it is, who it's for, and the core action.
2. **Research** - map first, adapt later. Idea-first scans 3-5 closest products then deep-dives. Artifact-first deep-dives the given source: pin the repo, walk first-party folders one by one into a tree-map, reconstruct logic, then decide absorption (*fork & adapt*, *assemble*, *differentiate*, or *fresh* - all build outcomes). Confirmed open-source that may contribute code is cloned into temporary isolation and statically excavated before any foreign code runs. The one brake: a request resting on a factually false premise stops honestly with an investigation record instead.
3. **Interrogation** — asks the user product and business questions (multiple choice, with a "you decide" option on every one), challenging vague or contradicted choices with evidence from the research.
4. **Technical research** — compares 2–3 genuinely different stacks and recommends one for the resolved decision authority to ratify; decides data model and architecture; verifies external APIs; and completes code-absorption planning: path-level licenses, source→target mappings, every chimera seam, exhaustive implementation steps, validators, provenance, and rollback boundaries.
5. **Validate** — a fresh agent with no prior context red-teams the decision set before anything is written; blockers must be cleared.
6. **Write** — produces the package section by section, self-reviews, and hands it to the user for approval.

## The output package

```
masterplan-<slug>/
├── masterplan.md    ← every decision made: schema, API contracts, acceptance
│                      criteria, design direction, build order
├── masterplan.html  ← self-contained walkthrough deck (render of masterplan.md)
├── EXECUTE.md       ← ticket-by-ticket executor prompt
├── STATUS.md        ← canonical fallback status or durable external-queue export
└── references/      ← research, decisions, diagrams, detail docs,
                       tickets/INDEX.md + immutable tickets/<ID>.md contracts,
                       evidence/<ID>/* execution receipts
```

Hand `EXECUTE.md` to any capable coding agent. It claims one dependency-ready stable ID, reads only that local ticket contract and linked docs, validates, writes evidence, and updates canonical status. External queues own mutable status but map 1:1 to immutable local contracts. Package contracts and deterministic validation remain offline; external-mode execution requires access to configured queue. Text files are source of truth; HTML deck is their render.

## Revise mode

When a project that already has a package needs a change, the skill runs only the affected phases, shows which sections and milestones are impacted, bumps the version, and appends to the changelog — so the masterplan stays current as the product changes.

## Install

Copy `skills/masterplan/` into your agent's skill directory. The core skill is plain English with no engine-specific dependencies — the text pipeline completes on any runtime. The HTML walkthrough deck is authored directly by the agent (single file, inline CSS, diagrams inlined as SVG); no external tooling required.

| System | Location |
|---|---|
| Shared canonical | `~/.agents/skills/masterplan/` (symlink to this repo's `skills/masterplan/`) |
| Claude Code (user) | `~/.claude/skills/masterplan/` |
| Claude Code (project) | `.claude/skills/masterplan/` |
| Codex | `~/.codex/skills/masterplan/` |
| Hermes (user) | `~/.hermes/skills/masterplan/` |
| Hermes profiles | `~/.hermes/profiles/<name>/skills/masterplan/` |
| Grok | `~/.grok/skills/masterplan/` |
| Other runtimes | wherever that runtime discovers `SKILL.md` |

## Package layout

```
masterplan/
├── README.md
├── LICENSE                      (MIT)
└── skills/
    └── masterplan/
        ├── SKILL.md             (the pipeline: phases, gates, rules, revise mode)
        └── references/
            ├── masterplan-template.md   (the full masterplan.md structure)
            ├── execute-template.md      (ticket-by-ticket execution prompt)
            ├── status-template.md       (canonical fallback / queue export)
            ├── ticket-contract.md       (local contract, catalog, queue mapping)
            ├── verdict-template.md      (the false-premise investigation record)
            ├── question-bank.md         (interrogation menu)
            ├── validation-rubric.md     (red-team mandate + report format)
            ├── research-playbook.md     (staged prior-art method + license table)
            ├── code-absorption.md       (clone, folder tree-map, logic, provenance, fork/chimera planning)
            ├── workflow-binding.md      (portable roles, authority, queue, capabilities)
            ├── detail-index-template.md (navigation for large multi-doc packages)
            ├── revise-playbook.md       (change → impact → delta)
            ├── ui-baseline.md           (standing UI interaction standard)
            ├── diagrams.md              (SVG diagram system + verification)
            └── html-export.md           (self-contained HTML walkthrough deck)
        └── scripts/
            └── validate-package.py      (deterministic package validator)
```

## License

MIT — see [LICENSE](LICENSE).
