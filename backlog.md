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
  - Done when receipts exist for both runs and discovered failures have regression tests.
  - Done 2026-11-17: greenfield build through every ticket to final QA, and deck review in a browser (see masterplan-slim-mermaid).

## Done

- [x] masterplan-slim-mermaid - Slim SKILL.md and make Mermaid the diagram source (completed 2026-11-17)
  - SKILL.md cut from 31.5 KB to about 20 KB with every rule kept; generator state moved to `references/decisions-template.md`; dev-cost value stated once; "proportional depth, uniform shape" made explicit for small scopes.
  - Diagrams are inline Mermaid blocks; `scripts/render-diagrams.py` renders them to SVG for the deck, with hand-authored SVG as the no-renderer fallback. Validator rejects unclosed, empty, or unknown-type Mermaid blocks.
  - Field run 2026-11-17 (receipts in the NUC sandbox `masterplan-field-20261117/`): a fresh agent planned a local read-later web app under full delegation in 23 min (7 tickets, 6 diagrams, red team found 2 real blockers); a second fresh agent given only `EXECUTE.md` built all 7 tickets to full QA in 74 min (226 tests, e2e in headless shell and Google Chrome). Both runs' friction logs were folded back: `scripts/build-deck.py`, unique SVG ids and palette theme, anchor validation, fork-and-adapt size test, Gate C start rule, shared-cache rule for validation commands, per-theme contrast tokens, full-browser QA.
  - Evidence: validator suite passes with 5 new tests; every documented Mermaid example rendered through mermaid-cli 11.4.2 with system Chrome; field package validates and its deck builds and was read at 1280 and 390 px.

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
