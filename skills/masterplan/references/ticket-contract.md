# Ticket contract

Generate one immutable local contract per execution unit under package `references/tickets/`. One ticket must fit one agent context window and be executable without reading all of `masterplan.md`. Mutable status lives only in canonical task state; contracts change only through revise mode.

## Catalog — `references/tickets/INDEX.md`

Use this exact five-column table. One row per contract, stable-ID order. Dependencies must match contract exactly.

```markdown
# Ticket catalog

| ID | Contract | Milestone | Dependencies | Status record |
|---|---|---|---|---|
| `PRJ-001` | [PRJ-001.md](PRJ-001.md) | `M1` | none | `PRJ-001` |
| `PRJ-002` | [PRJ-002.md](PRJ-002.md) | `M2` | `PRJ-001` | `PRJ-002` |
```

`Status record` is stable ID in canonical queue or fallback `STATUS.md`, not status value. Every local contract appears once; every catalog row resolves to one local contract.

## Contract — `references/tickets/<ID>.md`

Labels are parser-facing. Keep each field on one line; link longer detail docs rather than adding unlabeled prose. IDs match `[A-Z][A-Z0-9]*-[0-9]{3,}` and never change or get reused.

```markdown
# Ticket PRJ-002 — <bounded outcome>

- **ID:** `PRJ-002`
- **Goal:** <one observable outcome>
- **Milestone:** `M2`
- **Dependencies:** `PRJ-001`
- **Owned docs:** [Editor contract](../implementation/editor.md "Owned contract")
- **Linked docs:** [Decision D4](../decisions.md), [Source map](../absorption/source-target-map.md)
- **Source repository:** https://example.com/owner/repository | N/A — no source code absorption
- **Source commit:** <7–40 hex commit SHA> | N/A — no source repository
- **Source paths:** `<source path>:<symbol/range>` | N/A — no source repository
- **Target paths:** `<path list this ticket may change>`
- **Target contracts:** <interfaces, schemas, seams, invariants>
- **Exact changes:** <complete bounded implementation instructions>
- **Retained behavior:** <behavior that must stay unchanged>
- **Changed behavior:** <behavior this ticket intentionally changes>
- **Acceptance criteria:** <observable behavior-level checks>
- **Validation commands:** `python3 -m unittest tests.test_editor`; `python3 -m compileall src`
- **Expected evidence destination:** `references/evidence/PRJ-002/receipt.md`
- **License/attribution:** <license, notice/source destination> | N/A — no absorbed code
- **Rollback boundary:** Revert `<target/path>` and transaction `transaction:editor-migration`.
- **Status:** Tracked by canonical task state under `PRJ-002`; initial status `pending`.
```

Fields may say `N/A — <reason>` only where template permits. Source provenance is all-or-none: when repository is N/A, commit, source paths, and license/attribution are also N/A; otherwise repository is an `http`/`https` URL, commit is a 7–40 hex SHA, and source paths plus attribution are actionable. Validation commands contain one or more inline-code commands. Evidence destination is one exact package-relative regular-file path under `references/evidence/<ID>/`, never URL, absolute, or traversal. Rollback boundary names concrete backticked target paths or an explicit backticked `state:<identifier>` / `transaction:<identifier>`. Status declaration uses template sentence exactly; mutable current status never enters contract.

## Queue adapter/export mapping

Local contracts are execution truth. Canonical queue owns mutable status. Map any GitHub, Linear, Jira, file, database, or custom queue with these generic rules; add no provider-specific API contract:

| Local | Queue/export |
|---|---|
| Ticket `ID` | Immutable external ID/key or dedicated stable-ID field |
| Goal | Title/summary |
| Contract path | Durable link or attachment back to local contract |
| Dependencies | Blocking relationships or exported dependency-ID list |
| Status | Queue-native value mapped to `pending`, `claimed`, `blocked`, `done`, or `needs-rework` |
| Evidence destination | Evidence link/path field |

When a queue is remote, package `STATUS.md` is a read-only durable export/snapshot containing queue location, export timestamp, status vocabulary mapping, and one row per stable ticket ID with current status and evidence pointer. Regenerate it from the canonical queue; never edit it as an independent queue. Without an external queue, `STATUS.md` is canonical and uses the same rows.

## Executor protocol

1. Read workflow binding, `references/tickets/INDEX.md`, and canonical status snapshot.
2. Claim exactly one `pending` or `needs-rework` ticket whose dependencies are all `done`; atomically set it to `claimed` in canonical task state. When fallback `STATUS.md` is canonical, use one executor unless runtime binding names an external atomic claim mechanism; file edits alone do not provide safe concurrent claims.
3. Read only that ticket and its owned/linked docs. Read broader masterplan sections only when explicitly linked.
4. Change only target paths/contracts. Global decision conflicts stop execution and enter revise mode.
5. Run every validation command. Write outputs to expected evidence destination.
6. Mark `done` only when acceptance criteria pass and evidence exists; otherwise mark `blocked` with reason or roll back within stated boundary.
