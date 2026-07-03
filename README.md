# cut-once

> **Measure twice, cut once.**

An agent skill that turns a raw product idea — a one-sentence thought or a long messy chat — into a **PRD package**: a folder any capable coding agent can pick up and build **end-to-end from a single prompt**, with resumable progress if the run is interrupted. The interrogation is thorough so the execution can be one-shot.

## How it works

```
1. Intake + clarification loop ── GATE A: researchable pitch confirmed
2. Prior-art: quick scan → direction confirmed → deep-dive → honest verdict
3. Product/business interrogation with evidence-based correction
4. Technical research + per-component reference map
5. Validate: fresh red-team agent ── GATE B: zero blockers
6. Write the package (+ final self-review) ── GATE C: user reviews package
```

1. **Intake** — the idea is clarified in cheap conversation (no research) until it locks into a confirmed pitch: what, for whom, core action.
2. **Prior-art** — staged research into what already exists, ending in an honest verdict: *don't build* (deploy the existing thing), *build with differentiation* (the one difference stated), or *build fresh*.
3. **Interrogation** — the user answers only product and business questions (~a dozen, multiple choice, always with a "you decide" escape hatch); the agent challenges vague flows with evidence, not opinion.
4. **Technical research** — the agent decides stack, data model, and architecture itself, verifies APIs are alive and priced within budget, and anchors every major component to a proven reference implementation (license-checked).
5. **Validate** — a fresh agent with no conversation context red-teams the decision set before a single page is written. Blockers block.
6. **Write** — the package is written section by section, self-reviewed, and handed to the user for final approval.

## The output package

```
prd-<slug>/
├── PRD.md        ← every decision, already made — real schema, API contracts,
│                   acceptance criteria, design direction, build order (22 sections)
├── EXECUTE.md    ← the single prompt: rules of engagement for the executing agent
├── STATUS.md     ← milestone checklist the executor maintains with evidence;
│                   the owner reads progress here without asking anyone
└── references/   ← research notes, decisions.md, validation-report.md
```

Hand `EXECUTE.md` to any capable coding agent, and the build runs end-to-end. If the run dies midway, the next session resumes from `STATUS.md` instead of starting over.

## What makes it different

- **Decisions, not discussion.** A PRD full of options and "TBD"s makes the executing agent guess. Every section here resolves to one chosen answer with a rationale — chosen stack, real schema, concrete contracts.
- **An honest consultant, not a PRD machine.** If research shows the idea already exists as a deployable product, the verdict is "don't build — deploy X," and the package becomes a setup document. Saving you three months is a success.
- **The chimera principle.** Nothing gets built from scratch without a reason. Every major component is anchored to a proven implementation — adapt the code where the license allows, learn the pattern where it doesn't.
- **Revise mode vs. stale docs.** Changes enter through the front door: impact analysis, version bump, changelog, invalidated milestones flagged for rework. The executor refuses ad-hoc scope changes (the change-guard rule), so the PRD stays truthful for the build's entire life.
- **Resumable both ways.** The generator checkpoints its decisions as it goes; the executor checkpoints its milestones with evidence. Neither a dead session nor a dead build run starts over.

## Worked example

A complete package produced by this skill — including the recorded decisions, the red-team validation report (4 blockers caught and resolved before writing), and the final PRD/EXECUTE/STATUS — lives in [`examples/prd-ai-tools-affiliate/`](examples/prd-ai-tools-affiliate/).

## Install

Copy `skills/cut-once/` into your agent's skill directory. The skill is plain English with no engine-specific dependencies; any skill-capable agent system (or a human with patience) can follow it.

Examples of common skill directories:

| System | Typical location |
|---|---|
| Claude Code (user) | `~/.claude/skills/cut-once/` |
| Claude Code (project) | `.claude/skills/cut-once/` |
| Codex-style CLIs | `~/.codex/skills/cut-once/` |
| Other agent runtimes | wherever that runtime discovers `SKILL.md` files |

## Package layout

```
cut-once/
├── README.md
├── LICENSE                      (MIT)
├── docs/                        (design doc + implementation plan)
└── skills/
    └── cut-once/
        ├── SKILL.md             (the pipeline: phases, gates, rules, revise mode)
        └── references/
            ├── prd-template.md          (the 22-section PRD)
            ├── execute-template.md      (the single execution prompt)
            ├── status-template.md       (milestone checklist + marker convention)
            ├── question-bank.md         (interrogation menu + adaptive rules)
            ├── validation-rubric.md     (red-team mandate, axes, report format)
            ├── research-playbook.md     (staged prior-art method + license table)
            └── revise-playbook.md       (change classification → impact → delta)
```

## License

MIT — see [LICENSE](LICENSE).
