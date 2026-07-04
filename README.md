# masterplan

> *Measure twice, cut once.*

An agent skill that turns a product idea — a one-sentence thought or a long messy chat — into a **PRD package**: a folder any capable coding agent can build end-to-end from a single prompt, with resumable progress if a run is interrupted.

## How it works

A six-phase pipeline with three review gates:

```
1. Intake + clarification loop ── GATE A: researchable pitch confirmed
2. Prior-art: quick scan → direction confirmed → deep-dive → honest verdict
3. Product/business interrogation
4. Technical research + per-component reference map
5. Validate: fresh red-team agent ── GATE B: zero blockers
6. Write the package ── GATE C: user reviews package
```

1. **Intake** — clarifies the idea in conversation until it locks into a confirmed pitch: what it is, who it's for, and the core action.
2. **Prior-art** — staged research into what already exists, ending in one verdict: *don't build* (deploy the existing thing), *build with differentiation*, or *build fresh*.
3. **Interrogation** — asks the user product and business questions (multiple choice, with a "you decide" option on every one); technical calls are the agent's to make.
4. **Technical research** — chooses the stack, data model, and architecture; verifies external APIs are live and within budget; anchors each major component to a proven reference implementation with its license checked.
5. **Validate** — a fresh agent with no prior context red-teams the decision set before anything is written; blockers must be cleared.
6. **Write** — produces the package section by section, self-reviews, and hands it to the user for approval.

## The output package

```
prd-<slug>/
├── PRD.md        ← every decision made: schema, API contracts, acceptance
│                   criteria, design direction, build order
├── EXECUTE.md    ← the single prompt handed to the executing agent
├── STATUS.md     ← milestone checklist the executor updates with evidence
└── references/   ← research notes, decisions.md, validation-report.md
```

Hand `EXECUTE.md` to any capable coding agent and the build runs end-to-end. If a run stops midway, the next session resumes from `STATUS.md`.

## Revise mode

When a project that already has a package needs a change, the skill runs only the affected phases, shows which sections and milestones are impacted, bumps the version, and appends to the changelog — so the PRD stays current as the product changes.

## Worked example

A complete package produced by the skill — the recorded decisions, the red-team validation report, and the final PRD / EXECUTE / STATUS — is in [`examples/prd-ai-tools-affiliate/`](examples/prd-ai-tools-affiliate/).

## Install

Copy `skills/masterplan/` into your agent's skill directory. The skill is plain English with no engine-specific dependencies.

| System | Location |
|---|---|
| Claude Code (user) | `~/.claude/skills/masterplan/` |
| Claude Code (project) | `.claude/skills/masterplan/` |
| Codex-style CLIs | `~/.codex/skills/masterplan/` |
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
            ├── prd-template.md          (the full PRD structure)
            ├── execute-template.md      (the single execution prompt)
            ├── status-template.md       (milestone checklist)
            ├── verdict-template.md      (the don't-build investigation record)
            ├── question-bank.md         (interrogation menu)
            ├── validation-rubric.md     (red-team mandate + report format)
            ├── research-playbook.md     (staged prior-art method + license table)
            └── revise-playbook.md       (change → impact → delta)
```

## License

MIT — see [LICENSE](LICENSE).
