# Backlog

## In flight

## Queued

- [ ] masterplan-entry-routing - Sharpen Masterplan entry and exit boundaries (kind: ship)
  - Add a lightweight capability-gap / build-versus-existing-solution check before committing to a custom product build.
  - Route multi-session strategic fog to `wayfinder`.
  - Route unresolved changes in an existing codebase to `grill-with-docs`.
  - Route already-resolved scoped implementation planning to `to-spec`.
  - For existing projects, preserve canonical domain decisions in project `CONTEXT.md` and ADRs; Masterplan links them instead of becoming a competing source of truth.
  - Done when routing examples and boundary regression checks pass without weakening greenfield Masterplan behavior.

- [ ] masterplan-beta-field-validation - Gather remaining evidence before version 1.0 (kind: test)
  - Run full-fork planning against a small MIT repository.
  - Test one-to-one GitHub Issues publish, claim, status, evidence, and dependency round-trip in a sandbox repository.
  - Build one small product through every ticket to final QA.
  - Open and review generated `masterplan.html` in a browser, including embedded SVGs and offline behavior.
  - Done when receipts exist for all four runs and discovered failures have regression tests.

## Done

- [x] masterplan-installed-activation - Install and enable Masterplan on Codex, Hermes, and Grok (completed 2026-09-10)
  - Canonical install is a symlink from `~/.agents/skills/masterplan` to lab `skills/masterplan`. Codex, Hermes user+profiles, and Grok point at that tree. Hermes `skills.disabled` no longer lists masterplan. Stale lab-profile lavish copy removed.

- [x] masterplan-artifact-first-intake - Add artifact-first entry when the owner hands a source, not an idea (completed 2026-09-10)
  - Gate A accepts a given repo/SaaS/workflow as the pitch target. Phase 2 maps that source (tree-map → logic) before keep/drop/invert. Idea-first 3-5 scan unchanged. Black-box stays pattern-only, not code-absorption. Validator requires tree-map INDEX + repo-analysis per locked source.

- [x] masterplan-portable-ticket-pipeline - Generalize Masterplan and formalize ticket-by-ticket execution (completed 2026-09-05)
  - Commit: `f60ca9adb7dc7e5c41e5151b27caa7b0c06c4e4b` on `origin/master`.
  - Added portable workflow binding, deep OSS archaeology, code absorption, Chimera seam contracts, unlimited indexed detail documents, standalone SVG diagrams, self-contained HTML, immutable ticket contracts, canonical queue mapping, and evidence-gated dependency execution.
  - Evidence: two-repository Chimera dry-run; 26 validator regression tests; ticket-flow dry-run rejecting premature successor claim; installed copy exact and validator runnable.

## Resolved — no backlog

- Canonical queue reconciliation is complete: external queue owns mutable state; `STATUS.md` is fallback or read-only export.
- Package shape stays uniform. Small projects get less content; large projects may get hundreds of documents and tickets. Separate package variants would add branches without removing required contracts.
- Proxima synchronization removed from scope: repository scan found no bundled Masterplan copy.
