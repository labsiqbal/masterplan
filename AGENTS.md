# masterplan

Source of the `masterplan` skill: idea or given source to execution-ready
planning package. Procedure: [skills/masterplan/SKILL.md](skills/masterplan/SKILL.md);
overview, package shape and install: [README.md](README.md); queue and holds:
[backlog.md](backlog.md). Shared rules: [Work rules](../../../.standards/work-rules.md).

Delivery: direct-PR to `labsiqbal/masterplan`.

## Gotchas

- Maintaining this skill differs from using it. A planning run writes its
  package in the receiving project, under that project's contract; nothing
  lands here.
- This checkout is live: `~/.agents/skills/masterplan` links to
  `skills/masterplan/`, so check consumers before changing the skill payload.
- A changed phase or gate carries through its templates in
  `skills/masterplan/references/`, the validator and the tests; check with
  `python3 tests/test_validate_package.py`.
- The owner approves material phase or gate changes. Installation, symlink
  updates, publication and writes to other profile homes need explicit scope.
