# Map - masterplan

## Purpose

Skill that turns an idea into an execution-ready planning package.

## Routing

| Need | Read |
|---|---|
| Skill procedure (phases, gates, revise) | [skills/masterplan/SKILL.md](skills/masterplan/SKILL.md) |
| Package templates | [skills/masterplan/references/](skills/masterplan/references/) |
| Project rules | [AGENTS.md](AGENTS.md) |

## References

| Need | Read |
|---|---|
| Overview + install | [README.md](README.md) |

## Working artifacts

| Need | Read |
|---|---|
| Current queue and holds | [backlog.md](backlog.md) |

## Layout

```text
skills/masterplan/       Installable skill
  SKILL.md               Six-phase pipeline + gates + revise mode
  references/            Templates, playbooks, question bank, rubric
```

## Boundaries

- Output package shape: `masterplan-<slug>/` with `masterplan.md`, `masterplan.html`, `EXECUTE.md`, `STATUS.md`, `references/tickets/`, evidence, and supporting references.
- Local ticket contracts are immutable execution truth; canonical queue owns mutable status and maps 1:1 by stable ID.
- Text pipeline is source of truth; `masterplan.html` is a render, regenerated from Markdown.

## Load on demand

- `.git/`, `LICENSE`
