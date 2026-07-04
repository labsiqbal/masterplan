# VERDICT template — the "don't build" outcome

Use this when the honest verdict is **don't build** (either flavour). The package is an *investigation record*, not a spec to execute: no PRD/EXECUTE/STATUS. Save as `VERDICT.md` at the package root, alongside `references/`.

Scale it to the finding — a false-premise kill can be one screen; a "deploy X instead" needs enough of the adaptation path to act on. Keep every claim grounded (cite the file/source that proves it, in `references/`).

---

# ⟨Idea name⟩ — VERDICT: DON'T BUILD ⟨/ (YET)⟩

**Date:** YYYY-MM-DD · **Status:** CLOSED, no PRD. This folder is an *investigation record*, not a spec to execute.

## The question
⟨What the user wanted, and the belief/premise behind it — in one or two lines.⟩

## What reality actually shows (verified — see `references/`)
- ⟨Grounded finding, with the file:line / product / source that proves it.⟩
- ⟨If a premise was false, state it plainly: "believed X; verified NOT X because …".⟩
- ⟨What *does* already exist that covers the need.⟩

## Why don't-build
1. ⟨The real usage vs. what's already covered.⟩
2. ⟨What the user confirmed they don't need / don't do (with date).⟩
3. ⟨Any capability the build would add that is unwanted, premature, or the riskiest part.⟩
⟨For "deploy X instead": name the product, and what adapting it costs vs. building.⟩

## Zero-build option (if the need shows up in a small way)
⟨The cheapest existing mechanism that covers a bit of the need with no build — name it, say how, note its limit. If none exists, say so.⟩

## Revisit triggers — build ONLY when one is actually felt
| Trigger (a real, felt pain — not hypothetical) | Then build |
|---|---|
| ⟨Concrete pain the user will actually notice⟩ | **Tier 1 — ⟨smallest thing that resolves it⟩** |
| ⟨A bigger pain⟩ | **Tier 2 — ⟨next increment, on top of Tier 1⟩** |
| ⟨The pain that justifies the expensive version⟩ | **Tier 3 — ⟨the heavy build⟩ (premature until then)** |

Investigation (`references/decisions.md` + any audit/scan notes) is preserved so a future build resumes with zero re-analysis.
