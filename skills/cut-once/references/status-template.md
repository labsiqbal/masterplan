# STATUS.md Template

Copy into the package's `STATUS.md`, pre-filled with the build order from PRD section 18. cut-once creates it; the **executing agent** maintains it; the owner reads it any time to see progress without asking anyone.

**Marker convention:**
- `[ ]` pending
- `[x]` done — only with evidence in the note (evidence rule in EXECUTE.md)
- `[!]` needs rework — set by revise mode when a change invalidates a built milestone. Never silently uncheck history; `[!]` preserves the fact that it was built once.

---

# Status: ⟨project name⟩

**PRD version:** v1.0
**Started:** ⟨YYYY-MM-DD⟩
**Last updated:** ⟨YYYY-MM-DD⟩ by ⟨agent/owner⟩

## Milestones

- [ ] **M1 — Scaffold** — ⟨what M1 covers, from PRD §18⟩
  - Note: —
  - Evidence: —
- [ ] **M2 — Data layer** — ⟨…⟩
  - Note: —
  - Evidence: —
- [ ] **M⟨n⟩ — …**
  - Note: —
  - Evidence: —
- [ ] **M⟨last⟩ — Full QA pass** — run every acceptance criterion from the PRD end-to-end and record evidence.
  - Note: —
  - Evidence: —

## Blockers

*(none)* — when blocked, record: what, since when, what is needed to unblock, and which milestone it stops.
