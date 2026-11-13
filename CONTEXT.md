# Context — Masterplan skill source

## Inputs

- [Rules](AGENTS.md), [Map](MAP.md), [backlog](backlog.md).
- [Procedure](skills/masterplan/SKILL.md), only relevant [reference](skills/masterplan/references/).
- [Validator](skills/masterplan/scripts/validate-package.py), [tests](tests/test_validate_package.py).
- For running the skill: approved idea/source and receiving project's own contract.

## Process

1. Distinguish changing this skill from using it to plan another project.
2. For source maintenance, trace changed phase/gate to templates, validator and tests.
   Preserve source Markdown versus generated HTML; do not duplicate ticket status.
3. For a planning run, use installed skill method; outputs belong in the receiving
   project's existing planning package. Local ticket contracts stay immutable;
   that project's canonical queue owns mutable state.
4. Record source-maintenance evidence here in backlog. Installed symlinks may make
   source changes immediately visible; inspect consumers before changing skill payload.

## Outputs

Approved source/template/validator changes and task evidence, or a routed receiving
project package. This contract creates no template copy and no alternative planner.

## Verification

For validator changes: `python3 tests/test_validate_package.py` from this root.
Walk affected phase input, output, owner gate and template; validate an isolated
fixture package. This documentation rollout does not change installable skill payload.

## Human check

Owner approves material phase/gate changes and planning transitions. Installation,
symlink updates, publication and writes to other profile homes need explicit scope.
