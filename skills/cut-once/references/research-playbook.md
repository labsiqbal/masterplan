# Research Playbook (prior-art, phase 2)

Research is the most expensive phase — in tokens, time, and attention. The discipline: **spend nothing until the pitch is locked (GATE A), spend little until the direction is confirmed, and only then go deep.** A wrong guess at the scan stage costs a paragraph; a wrong guess at the deep-dive stage costs the whole afternoon.

## Stage 1 — Quick scan (cheap)

Find the **3–5 existing products/projects closest to the pitch**. Search broadly: commercial products, open-source projects, and "X alternative" / "open source X" queries. For each candidate, write exactly one paragraph:

- What it is and who uses it.
- Its core flow in one sentence.
- Open source or proprietary (with license if visible at a glance).

Do not go deeper yet. No feature matrices, no repo reading.

## Stage 2 — Direction check (with the user)

Present the candidates: *"Your idea resembles X and Y. Their flow works like ⟨summary⟩ — is that what you have in mind?"*

Classify every divergence between the user's mental model and the prior art:

- **Deliberate differentiation** — the user knows the pattern and wants to differ. Record it; it feeds "the one difference".
- **Unknown pattern** — the user simply hadn't seen how the proven products do it. Offer the proven pattern with the reason it won; let them choose knowingly.

Only proceed when the user confirms which candidates are actually the relevant comparison set.

## Stage 3 — Deep-dive (only after confirmation)

For the confirmed candidates: user flows and page structures (what screens exist, in what order), tech stacks where discoverable, open-source repos (activity, quality, license), pricing models. This material becomes PRD §2 (differentiation table), §5–6 (flows and pages worth absorbing), and §14 (reference map). Save raw notes to the package's `references/` folder.

## Stage 4 — The verdict

Decide honestly:

```
Does a deployable product already cover the pitch (including "the one difference")?
├─ YES → DON'T BUILD.
│        The package becomes a setup/adaptation document for that product:
│        PRD sections re-aim at configuring/deploying/extending it, the build
│        order becomes a setup order. Say it plainly: "deploy X, save months."
└─ NO → Is there meaningful prior art?
    ├─ YES → BUILD WITH DIFFERENTIATION.
    │        PRD §2 must state THE one difference in a single sentence.
    │        If you cannot write that sentence, the verdict is "don't build."
    └─ NO → BUILD FRESH.
             Rare. Components still get anchored to references where possible —
             even a novel product is assembled from proven parts.
```

Deliver the verdict before interrogation (phase 3): it changes which questions matter.

## License table

Checked per reference **before** it enters the map. When unsure, learn the pattern, don't copy the code.

| License family | Examples | Rule |
|---|---|---|
| Permissive | MIT, Apache-2.0, BSD | Adapt code freely; keep attribution/notice as required. |
| Weak copyleft | MPL, LGPL | Adapt within file/library boundaries; modifications to the covered parts stay open. |
| Strong copyleft | GPL, AGPL | Do **not** absorb code into a closed-source product. Pattern-learning only. AGPL binds even network-served use. |
| Proprietary / no license | closed products, unlicensed repos | Pattern only. An unlicensed public repo is NOT free to copy. |

Cross-check against the product's fate (PRD §21): an open-source (compatible-licensed) product may absorb more; a commercial closed product is strictest.

## Reference map format

Feeds PRD §14 directly:

| Component | Reference (repo/product) | License | Absorb |
|---|---|---|---|
| ⟨component⟩ | ⟨URL or product name⟩ | ⟨license⟩ | Code — adapt directly / Pattern only |

**"Absorb" is a decision, not a note** — the executing agent will act on it literally: "Code" means open the repo and adapt; "Pattern" means study the approach and re-implement.
