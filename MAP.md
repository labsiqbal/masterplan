# MAP · masterplan

## What

Agent skill: idea → execution-ready masterplan package (Markdown pipeline + optional lavish visual layer).

## Open first

| Need | Open |
|---|---|
| Skill procedure (phases, gates, revise) | `skills/masterplan/SKILL.md` |
| Package templates | `skills/masterplan/references/` |
| Overview + install | `README.md` |
| Project rules | `AGENTS.md` |

## Layout

```text
skills/masterplan/       Installable skill
  SKILL.md               Six-phase pipeline + gates + revise mode
  references/            Templates, playbooks, question bank, rubric
```

## Edges

- Output package shape: `masterplan-<slug>/` with `masterplan.md`, `EXECUTE.md`, `STATUS.md`, `references/` (and optional `masterplan.html` via lavish).
- Text pipeline is source of truth; lavish is optional visual layer only.

## Ignore by default

- `.git/`, `LICENSE`
