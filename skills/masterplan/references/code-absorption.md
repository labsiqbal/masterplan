# Code Absorption Playbook

Use this branch when Phase 2 selects **Fork & adapt** or **Assemble (chimera)**, or when any component-reference row says `Code — adapt`. Run Stages 1–3 inside Phase 2 deep-dive; run Stages 4–7 inside Phase 4 after product decisions are known. Masterplan plans and proves the absorption; the implementation executor later performs target writes under `references/workflow-binding.md`.

## Outputs

Create under the package:

```text
references/absorption/
├── candidate-scan.md
├── repo-lock.json
├── license-report.md
├── absorption-map.md
├── source-target-map.md
├── chimera-integration.md       # chimera only
├── repo-analysis/
│   └── <source-slug>.md         # one per inspected repo
└── receipts/
    └── research-validation.md
```

`repo-lock.json` is a JSON array with one entry per `source_slug`. Each entry records upstream URL, default branch, requested tag/ref, resolved commit SHA, clone date, local temporary path, submodule URLs+SHAs, absorbed Git LFS object IDs, and separately sourced asset identities. For an archive/mirror fallback, also record original upstream, archive URL, SHA-256 digest, and the resolved upstream commit; an archive without both digest and resolved commit is not eligible for code absorption. `absorption-map.md` is the decision source. `source-target-map.md` links every absorbed source unit to target work. Target implementation state remains in the project's configured queue; `STATUS.md` is fallback only.

## Stage 1 — Acquire safely

Clone only candidates confirmed at the Phase-2 direction check. Use a temporary/sandbox location allowed by workflow binding. Pin the inspected commit:

```bash
git clone --filter=blob:none --no-checkout <url> <temporary-path>
git -C <temporary-path> checkout <commit-or-tag>
git -C <temporary-path> rev-parse HEAD
```

Treat foreign repositories as untrusted. Before static audit completes, read files only. Do not run install hooks, package-manager scripts, builds, tests, binaries, containers, Makefiles, or repository-provided commands. Clone retry: two bounded attempts; then use an official archive/package registry mirror or reject the candidate with evidence.

## Stage 2 — Repository archaeology

For every pinned repo, write `repo-analysis/<source-slug>.md` containing:

1. identity: URL, SHA, release/tag, activity date;
3. license evidence and scope, including separately licensed assets, Git LFS objects, and submodules; each absorbed submodule is independently pinned and analyzed;
3. tree, entrypoints, architecture boundaries, and module dependency graph;
4. runtime/build dependencies and all lifecycle/install hooks;
5. public APIs, internal contracts, state ownership, persistence model;
6. relevant modules/files and behavior each implements;
7. upstream tests that prove that behavior;
8. security-sensitive paths, generated code, native extensions, network calls;
9. deploy/runtime assumptions;
10. reusable units, units rejected, and why.

Completion: every candidate has all ten sections; claims cite source paths and line/symbol names. No overview-only analysis passes.

## Stage 3 — License decision per path

Apply `research-playbook.md` evidence order. `license-report.md` records each source path or asset considered, license evidence location, copyright holder, compatibility with product fate, required notice, and decision: `code`, `pattern-only`, or `reject`.

No verified license means unlicensed and therefore pattern-only. MIT generally permits use, copying, modification, distribution, sublicensing, and sale, provided copyright and permission notices accompany copies or substantial portions. Preserve required notices in the target's established third-party notice mechanism (or `THIRD_PARTY_NOTICES.md` fallback). Audit assets, fonts, datasets, model weights, submodules, trademarks, and dependencies separately; a repository-level MIT file does not automatically cover them.

## Stage 4 — Choose absorption unit

Prefer, in order: existing dependency API; maintained fork; vendored module; selective copy. Copy less code when it preserves the required behavior and maintenance path. Record why the chosen mode beats the earlier modes.

For every absorbed unit, add a record to `source-target-map.md`:

```text
Target component:
Source repository + pinned commit:
Source modules/files/symbols:
Absorption mode: dependency | fork | vendor | selective-copy | pattern-only
Behavior retained:
Behavior changed:
Target modules/files:
Public contract:
Data ownership:
Dependencies introduced:
License + evidence + notice destination:
Conflicts with other absorbed units:
Adaptation steps:
Acceptance criteria:
Validation command/observable behavior:
Rollback boundary:
```

## Stage 5 — Chimera synthesis

For Assemble (chimera), write `chimera-integration.md`. Name one canonical target contract for each seam between absorbed units:

- canonical data types/schema and conversion adapters;
- state owner and persistence owner;
- event lifecycle, ordering, idempotency;
- error propagation and retry boundary;
- authentication/authorization and trust boundary;
- dependency/runtime version conflicts;
- styling/UI ownership where components meet;
- license and attribution boundary;
- integration order and rollback boundary;
- acceptance tests proving the seam from outside.

Every pair of components that communicates has a seam record. A box-and-arrow overview without contracts fails this stage.

## Stage 6 — Derive exhaustive implementation work

Translate every source-target record and chimera seam into Section 18, immutable local ticket contracts under `references/tickets/`, and topic docs under `references/implementation/`. No ticket may say only “copy,” “adapt,” “integrate,” or “use repo X.” Each affected ticket carries:

1. exact source repository, unit, and pinned SHA;
2. target paths and contracts;
3. exact transformation;
4. stable-ID dependencies;
5. behavior retained and deliberately changed;
6. license/notice action and destination;
7. acceptance criteria, validation commands, and evidence destination;
8. rollback boundary.

Hundreds of tickets and detail documents are valid when archaeology exposes that much work. Maintain package `references/tickets/INDEX.md` per `ticket-contract.md` and package-wide `references/INDEX.md` per `detail-index-template.md`. Every absorption and implementation detail doc is reachable from its owning ticket and masterplan milestone.

## Stage 7 — Validate planning evidence

Before Gate B:

- every code absorption row maps to a pinned SHA;
- every copied path has a license decision and notice destination;
- every target component maps back to source or is explicitly fresh-built;
- every chimera edge has a seam contract;
- every adaptation record maps to one or more stable local tickets;
- every ticket has validation commands, evidence destination, and rollback boundary;
- no temporary clone is treated as durable state.

Write counts and failures to `receipts/research-validation.md`. Any missing link is a Gate-B blocker.

## Implementation handoff

Execution happens only under workflow binding. The implementation executor re-verifies pinned source identity, performs changes in the configured isolation, carries notices, ports relevant upstream behavior tests, runs target acceptance checks, and records source SHA + changed target paths + actual test output in the project's evidence system. Commit, push, publish, deploy, spending, credentials, and untrusted-script execution follow local authority policy; this playbook grants none of them.

## Model tier, research budget, and cadence

Use the runtime's normal planning model for inventory, path mapping, and license collection. Use its stronger reasoning tier for cross-repository seam design. Escalate once to the strongest available tier only when a conflict across three or more repositories remains unresolved after one documented attempt; record why and the configured spend limit in `receipts/research-validation.md`. If the runtime has no model tiers, continue sequentially and record the limitation. Clone and analyze only direction-confirmed candidates (normally 3–5); expand the set only when none can supply a required component, with the reason recorded. Run once per initial masterplan and repeat only for affected sources during revise mode — no recurring scan or monitoring.

## Failure and rollback

- Clone unavailable after retries: official mirror/archive or reject with evidence.
- License unclear/incompatible: pattern-only or select another source.
- Dependency conflict: design adapter, isolate dependency, or select another source; never force-install blindly.
- Source moved since pin: keep the pin; update only through revise mode and repeat archaeology for affected units.
- Integration plan fails red team: return to its owning stage, update maps, rerun link validation.
- Implementation failure: revert the isolated import batch using the target project's version-control mechanism; preserve planning receipts and rejection rationale.
