# STATUS.md Template

Generate in every build package. Mutable ticket prose belongs nowhere here; contracts live under `references/tickets/`.

- **Fallback mode:** `STATUS.md` is canonical mutable state and single-writer. Run one executor unless workflow binding names an external atomic claim mechanism.
- **External queue mode:** `STATUS.md` is durable read-only export/snapshot. Regenerate from canonical queue after state changes; never hand-edit as second queue.

---

# Status: ⟨project name⟩

**Masterplan version:** v1.0
**Status mode:** ⟨exactly `fallback` or `external-export`⟩
**Canonical task state:** `STATUS.md` | ⟨exact queue path/URL matching workflow binding⟩
**Exported at:** ⟨external mode: RFC3339 timestamp such as 2026-09-05T10:00:00Z; fallback: N/A⟩
**Status mapping:** ⟨external mode: semicolon-separated mappings such as Open -> pending; In progress -> claimed; fallback: N/A⟩

| ID | Status | Claimed by | Updated | Evidence | Blocker/note |
|---|---|---|---|---|---|
| `PRJ-001` | pending | — | ⟨timestamp⟩ | `references/evidence/PRJ-001/receipt.md` | — |
| `PRJ-002` | pending | — | ⟨timestamp⟩ | `references/evidence/PRJ-002/receipt.md` | waits for `PRJ-001` |

Every ID in `references/tickets/INDEX.md` appears exactly once. `done` requires evidence at ticket destination. `needs-rework` preserves prior completion history after revise mode invalidates work. External exports include queue location and export timestamp so offline contract validation remains deterministic; execution still requires queue access.
