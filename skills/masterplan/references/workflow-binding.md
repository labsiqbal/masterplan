# Workflow Binding

Masterplan defines the work contract; each project/runtime decides who performs it, where state lives, and which actions need approval. Resolve this binding at intake from project instructions (`AGENTS.md`, `CLAUDE.md`, policies, configured queue, runtime capabilities). Do not hardcode profile names, vendors, or one person's workflow.

Record the result as plain, unfenced values in `references/workflow-binding.md` inside package. This fenced block is source-skill example only; generated package omits fences:

```yaml
decision_authority: user | named role | configured policy
research_executor: current agent | named role/capability
implementation_executor: current agent | named role/capability
final_reviewer: user | named role | configured policy
workspace_isolation: project convention | temporary clone | branch | worktree | sandbox
canonical_task_state: project queue path/URL | STATUS.md
atomic_claim_mechanism: queue-native claim/CAS | external lock service | N/A
artifact_root: project-local path
approval_policy_source: path/URL | safe fallback
capabilities:
  parallel_agents: true | false
  network_research: true | false
  repository_clone: true | false
  browser_preview: true | false
authority:
  read_public_sources: allowed | approval-required | forbidden
  write_target: allowed | approval-required | forbidden
  execute_untrusted_source: allowed | approval-required | forbidden
  add_dependencies: allowed | approval-required | forbidden
  publish_deploy_spend_credentials: allowed | approval-required | forbidden
```

## Resolution rules

1. Project/runtime policy wins. Cite its source in the binding.
2. Use capability classes, not product-specific role names: decision authority, research executor, implementation executor, reviewer.
3. Use the project's configured queue as canonical mutable task state. Always generate immutable local ticket contracts under `references/tickets/` and map them 1:1 by stable ID. Generate `STATUS.md` as canonical status when no queue is configured; otherwise generate it as a durable read-only export/snapshot with queue location, RFC3339 export timestamp, parseable status mapping, and one row per ticket. Binding `canonical_task_state` and STATUS metadata must match exactly: both `STATUS.md` in fallback mode, same non-STATUS location in external mode. Fallback is single-writer unless runtime supplies and names an external atomic claim mechanism. See `ticket-contract.md`; never make remote queue the only copy of execution prose.
4. Use the project's isolation method. If none exists, use a temporary clone for research and an isolated branch/workspace for target changes.
5. If no authority policy exists, safe fallback requires explicit user approval before target writes, executing untrusted repository scripts, adding dependencies, publishing/deploying, spending, or credential/access changes. Public-source reading and static inspection remain read-only.
6. Re-resolve on revise mode only when policy, runtime, or project location changed.

## Validation

Before Phase 2, every field above has one value and every configured path exists or is marked `fallback`. `atomic_claim_mechanism` is N/A only for single-writer fallback; concurrent fallback names an external mechanism. Contradictions (for example `write_target: forbidden` with an execution package promising target writes) block the pipeline until scope or binding changes.
