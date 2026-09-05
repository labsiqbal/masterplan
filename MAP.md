# MAP · masterplan

## What

Agent skill: idea → ticket-executable masterplan package (Markdown contracts + self-contained HTML walkthrough deck).

## Open first

| Need | Open |
|---|---|
| Skill procedure (phases, gates, revise) | [skills/masterplan/SKILL.md](skills/masterplan/SKILL.md) |
| Package templates | [skills/masterplan/references/](skills/masterplan/references/) |
| Overview + install | [README.md](README.md) |
| Current queue and holds | [backlog.md](backlog.md) |
| Project rules | [AGENTS.md](AGENTS.md) |

## Layout

```text
skills/masterplan/       Installable skill
  SKILL.md               Six-phase pipeline + gates + revise mode
  references/            Templates, playbooks, question bank, rubric
```

## Edges

- Output package shape: `masterplan-<slug>/` with `masterplan.md`, `masterplan.html`, `EXECUTE.md`, `STATUS.md`, `references/tickets/`, evidence, and supporting references.
- Local ticket contracts are immutable execution truth; canonical queue owns mutable status and maps 1:1 by stable ID.
- Text pipeline is source of truth; `masterplan.html` is a render, regenerated from Markdown.

## Ignore by default

- `.git/`, `LICENSE`
