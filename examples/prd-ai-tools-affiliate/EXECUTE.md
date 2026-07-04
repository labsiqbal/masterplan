# Execute: ai-tools-affiliate

You are building this project end-to-end. Everything you need is in this folder.

## Rules

1. **Read `PRD.md` fully before writing anything.** It contains every decision, already made. Do not re-litigate decisions or "improve" them — section 20 (Considered and rejected) explains the choices that might look like mistakes (yes, the affiliate URLs are supposed to be plain vendor URLs at launch; yes, there is deliberately no newsletter). If you find a genuine contradiction or impossibility in the PRD, stop and report it; do not improvise around it.

2. **Resume rule.** Before starting, read `STATUS.md`. If any milestones are checked, verify they actually work — run the build, hit the pages, do not trust the checkmarks blindly — then continue from the first unchecked milestone. Treat any milestone marked `[!] needs rework` as unchecked: rebuild it according to its note before moving on. Never restart from zero when a partial build exists.

3. **Evidence rule.** Check a milestone off only with evidence: a passing build, a rendering page, a logged redirect — recorded in the milestone's note. "The code is written" is not evidence.

4. **Credentials rule.** Never invent or fake keys. Create `.env.example` early with every variable from PRD section 17. When you reach M7 (deploy), stop and ask the owner for Cloudflare and domain access — do not stub the deploy and continue as if it worked. Affiliate accounts are explicitly NOT needed for any milestone (PRD §4.3).

5. **Content rule (this project's sharpest edge).** No tool fact — price, feature, verdict — may appear anywhere unless it exists in `data/tools.json`. If seed data for the 5 articles + 15 profiles is missing or incomplete, stop and ask the owner for the verified facts; generating plausible-sounding tool facts is the one way to destroy this product (PRD §1, §20).

6. **Change-guard rule.** If the owner (or anyone) requests a scope change mid-build — a new feature, a different stack, a dropped requirement — do not improvise it. The PRD is the single source of truth for this build's entire life. Reply: *"That's a scope change — run it through masterplan revise mode so the PRD is updated first, then I'll continue against the updated plan."*

7. **Build order.** Follow PRD section 18 in sequence: M1 scaffold → M2 schemas → M3 redirect layer → M4 layouts → M5 legal & SEO → M6 pipeline + seed batch → M7 deploy → M8 full QA pass.

## Definition of done

All milestones in `STATUS.md` checked with evidence, including M8: every acceptance criterion in PRD §4 verified, Lighthouse ≥90 performance / ≥95 SEO, layouts verified at 375px. Nothing else counts as done.

Begin.
