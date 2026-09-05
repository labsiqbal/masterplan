# Detail-document index

Use when the package has any overflow detail documents. Every detail file must appear here and be linked from its owning masterplan section or milestone. This prevents a hundred-document package becoming an unsearchable dump.

| Document | Scope | Source decisions/evidence | Owning section/milestones | Dependencies | Validator |
|---|---|---|---|---|---|
| `references/<topic>.md` | <one bounded module/flow/domain> | <decision or source record links> | §<n>, M<n> | <documents/milestones> | <deterministic check> |

Validation: listed paths exist; every detail `.md` is listed; every row names an owning section and milestone; every milestone points back to the exact documents it needs; every detail doc links back to its owning section or states it in frontmatter; no two rows claim canonical ownership of the same fact. Run the package validator for path/orphan checks, then review ownership/backlinks/duplicate canonical facts during Phase 6 consistency review.
