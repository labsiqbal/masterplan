# EXECUTE.md Template

Copy into package `EXECUTE.md`, filling placeholders. This prompt starts ticket-by-ticket execution; local ticket contracts carry work detail.

---

# Execute: ⟨project name⟩

Build this project one ticket at a time.

## Rules

1. **Bind workflow.** Read `references/workflow-binding.md`, `references/tickets/INDEX.md`, and `STATUS.md`. `STATUS.md` is canonical only in fallback mode; otherwise it is durable read-only export of configured queue. Resolve current status from canonical source before claiming work. Fallback `STATUS.md` is single-writer: run one executor unless workflow binding names an external atomic claim mechanism.
2. **Claim one ready ticket.** A ticket is ready only when status is `pending` or `needs-rework` and every dependency is `done`. Claim exactly one by stable ID using canonical queue's atomic ownership convention, or the external atomic claim mechanism named for concurrent fallback execution. If no ready ticket exists, report blockers; never skip dependencies.
3. **Load bounded context.** Read claimed `references/tickets/<ID>.md` plus its owned and linked docs. This is sufficient execution context. Do not read all of `masterplan.md` unless ticket links a required section or a contradiction demands revise mode.
4. **Honor boundary.** Change only ticket target paths/contracts; preserve its retained behavior. Local ticket contract and global decisions are immutable during execution. A contradiction, impossibility, or scope request enters masterplan revise mode; executor does not alter global decisions.
5. **Authority and credentials.** Follow workflow binding. Never invent keys or evidence. Ask resolved decision authority when required authority or credentials are absent.
6. **Validate and evidence.** Run every ticket validation command. Write actual output/artifacts to expected evidence destination. Mark `done` only when acceptance criteria pass and evidence exists. Otherwise mark `blocked` with exact reason, or roll back within ticket boundary.
7. **Design and interaction.** UI tickets follow masterplan §15 plus `references/ui-baseline.md`. Engage available frontend craft and motion skills before frontend implementation; use same discipline manually when unavailable.
8. **Continue.** Release claim, refresh canonical state/export, then claim next ready ticket. Never keep mutable status in ticket files.

## Definition of done

Every catalog ticket is `done` with evidence, including full-QA ticket. Every dependency resolves, no claim remains open, and current `STATUS.md` snapshot maps each stable ID 1:1 to canonical state.

Begin.
