# EXECUTE.md Template

Copy into the package's `EXECUTE.md`, filling the ⟨placeholders⟩. This file is the **single prompt**: the owner hands it (or its path) to any capable coding agent, and the build runs end-to-end. Keep it short — the PRD carries the content; this file carries the rules of engagement.

---

# Execute: ⟨project name⟩

You are building this project end-to-end. Everything you need is in this folder.

## Rules

1. **Read `PRD.md` fully before writing anything.** It contains every decision, already made. Do not re-litigate decisions or "improve" them — section 20 (Considered and rejected) explains the choices that might look like mistakes. If you find a genuine contradiction or impossibility in the PRD, stop and report it; do not improvise around it.

2. **Resume rule.** Before starting, read `STATUS.md`. If any milestones are checked, verify they actually work — run the app, run the checks, do not trust the checkmarks blindly — then continue from the first unchecked milestone. Treat any milestone marked `[!] needs rework` as unchecked: rebuild it according to its note before moving on. Never restart from zero when a partial build exists.

3. **Evidence rule.** Check a milestone off only with evidence: a passing test, a rendering page, a succeeding command — recorded in the milestone's note. "The code is written" is not evidence.

4. **Credentials rule.** Never invent or fake keys. Create `.env.example` early with every variable from PRD section 17. When a milestone needs a real credential, stop and ask the owner for it — do not stub it and continue as if it worked.

5. **Change-guard rule.** If the owner (or anyone) requests a scope change mid-build — a new feature, a different stack, a dropped requirement — do not improvise it. The PRD is the single source of truth for this build's entire life. Reply: *"That's a scope change — run it through cut-once revise mode so the PRD is updated first, then I'll continue against the updated plan."*

6. **Build order.** Follow PRD section 18 in sequence. The final milestone is always the full QA pass: every acceptance criterion in PRD section 4, verified with evidence.

## Definition of done

All milestones in `STATUS.md` checked with evidence, including the final QA pass. Nothing else counts as done.

Begin.
