# masterplan

> *Every decision made before the first line of code.*

An agent skill that turns a product idea — a one-sentence thought or a long messy chat — into a **masterplan package**: a folder any capable coding agent can build end-to-end from a single prompt, with resumable progress if a run is interrupted.

The core is a **portable text pipeline** — plain Markdown, diagrams as Mermaid source — that runs on any agent runtime. Where [lavish-axi](https://github.com/kunchenguid/lavish-axi) is available, it adds the **visual layer**: interactive interrogation and gate reviews, diagrams as editable Excalidraw whiteboards, and a portable HTML export of the finished package.

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
masterplan-<slug>/
├── masterplan.md    ← every decision made: schema, API contracts, acceptance
│                      criteria, design direction, build order
├── masterplan.html  ← portable walkthrough deck, exported by lavish-axi
│                      (only where lavish is available)
├── EXECUTE.md       ← the single prompt handed to the executing agent
├── STATUS.md        ← milestone checklist the executor updates with evidence
└── references/      ← research notes, decisions.md, validation-report.md
```

Hand `EXECUTE.md` to any capable coding agent and the build runs end-to-end. If a run stops midway, the next session resumes from `STATUS.md`. The text files are the source of truth; the HTML deck is a render of them.

## Revise mode

When a project that already has a package needs a change, the skill runs only the affected phases, shows which sections and milestones are impacted, bumps the version, and appends to the changelog — so the masterplan stays current as the product changes.

## Install

Copy `skills/masterplan/` into your agent's skill directory. The core skill is plain English with no engine-specific dependencies — the text pipeline completes on any runtime. The visual layer (interactive review, editable diagrams, HTML export) uses `lavish-axi` where installed; without it, diagrams remain Mermaid source (rendered natively by GitHub and most Markdown viewers) and rich HTML export is unavailable.

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
            ├── masterplan-template.md   (the full masterplan.md structure)
            ├── execute-template.md      (the single execution prompt)
            ├── status-template.md       (milestone checklist)
            ├── verdict-template.md      (the false-premise investigation record)
            ├── question-bank.md         (interrogation menu)
            ├── validation-rubric.md     (red-team mandate + report format)
            ├── research-playbook.md     (staged prior-art method + license table)
            ├── revise-playbook.md       (change → impact → delta)
            ├── ui-baseline.md           (standing UI interaction standard)
            └── lavish-export.md         (review + export via lavish-axi)
```

## License

MIT — see [LICENSE](LICENSE).

HTML export & interactive review powered by [lavish-axi](https://github.com/kunchenguid/lavish-axi) (MIT).
