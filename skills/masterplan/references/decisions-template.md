# Generator state — `references/decisions.md`

The pipeline survives interruption the way the package it writes does. Create the package shell at intake in the artifact root resolved by `workflow-binding.md`, write package `references/workflow-binding.md` first, then append one block to package `references/decisions.md` as each phase completes. If Gate A rejects the pitch, remove the empty shell or keep it as an explicitly rejected investigation record, per local policy.

```markdown
## Phase 1 — Pitch (confirmed YYYY-MM-DD)
⟨the confirmed pitch paragraph; entry: idea-first | artifact-first white-box + source | artifact-first black-box + source⟩

## Phase 2 — Absorption map
⟨tree-map path + logic analysis path, or N/A for idea-first / black-box⟩
⟨absorption level + the one difference + scan summary⟩

## Phase 3 — Product decisions
⟨each Q → decision, including "agent decided: ⟨rationale⟩" entries⟩

## Phase 4 — Technical decisions
⟨stack (authority-ratified; runner-ups → §20), APIs verified, reference map, testing strategy; single-designer caveat when stacks came from one head⟩

## Phase 5 — Validation
⟨blockers → resolutions; improvements decided; rejected suggestions → §20; or "skipped by authority: tiny scope"⟩

## Phase 6 — Package written + self-review
⟨files written (incl. detail docs); placeholder scan, consistency, diagram verification method + outcome (renderer or HAND-SVG), HTML check; Gate C approval⟩
```

On session start with a partial package: read this file, state which phase you are resuming, and continue from the first incomplete phase without re-interviewing.
