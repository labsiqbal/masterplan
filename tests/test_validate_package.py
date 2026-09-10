#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "skills/masterplan/scripts/validate-package.py"


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


ABSORPTION_DOCS = (
    "license-report.md",
    "absorption-map.md",
    "source-target-map.md",
    "receipts/research-validation.md",
)


def absorption_index_rows(*extra: str) -> str:
    return "\n".join(
        f"| `absorption/{relative}` | absorption | source | §2/§4 | none | check |"
        for relative in list(ABSORPTION_DOCS) + list(extra)
    )


def write_source_maps(root: Path, slug: str) -> None:
    write(root, f"references/absorption/repo-analysis/{slug}.md", f"# {slug}\n")
    write(
        root,
        f"references/absorption/tree-map/{slug}/INDEX.md",
        "# Tree map\n\n"
        "| Path | Kind | Role | Card |\n"
        "|---|---|---|---|\n"
        "| `.` | first-party | root | - |\n",
    )


def ticket(ticket_id: str, dependencies: str = "none") -> str:
    return f"""# Ticket {ticket_id} — walking skeleton

- **ID:** `{ticket_id}`
- **Goal:** Deliver one runnable vertical slice.
- **Milestone:** `M1`
- **Dependencies:** {dependencies}
- **Owned docs:** [Decisions](../decisions.md)
- **Linked docs:** [Workflow binding](../workflow-binding.md)
- **Source repository:** N/A — no source code absorption
- **Source commit:** N/A — no source repository
- **Source paths:** N/A — no source repository
- **Target paths:** `src/app.py`, `tests/test_app.py`
- **Target contracts:** CLI prints a deterministic result.
- **Exact changes:** Add CLI entry point and behavior-level test.
- **Retained behavior:** Existing commands remain unchanged.
- **Changed behavior:** New command becomes available.
- **Acceptance criteria:** Command exits zero and prints `ready`.
- **Validation commands:** `python3 -m unittest`
- **Expected evidence destination:** `references/evidence/{ticket_id}/validation.txt`
- **License/attribution:** N/A — no absorbed code
- **Rollback boundary:** Revert `src/app.py` and `tests/test_app.py` only.
- **Status:** Tracked by canonical task state under `{ticket_id}`; initial status `pending`.
"""


def ticket_index(rows: str) -> str:
    return (
        "# Ticket catalog\n\n"
        "| ID | Contract | Milestone | Dependencies | Status record |\n"
        "|---|---|---|---|---|\n"
        f"{rows}\n"
    )


def masterplan_ticket_map(rows: str) -> str:
    return (
        "# Masterplan\n\n![Architecture](references/diagrams/architecture.svg)\n\n"
        "## 18. Build order\n\n"
        "| Milestone | Outcome | Ticket IDs | Depends on |\n"
        "|---|---|---|---|\n"
        f"{rows}\n\n## 19. Non-goals\n"
    )


def base_package(root: Path) -> None:
    files = {
        "masterplan.md": masterplan_ticket_map(
            "| `M1` — Walking skeleton | Runnable slice | `MP-001` | none |"
        ),
        "masterplan.html": "<!doctype html><html><body><svg></svg></body></html>\n",
        "EXECUTE.md": "# Execute\n",
        "STATUS.md": (
            "# Status\n\n**Status mode:** fallback\n"
            "**Canonical task state:** STATUS.md\n\n"
            "| ID | Status | Evidence |\n|---|---|---|\n"
            "| `MP-001` | pending | — |\n"
        ),
        "references/decisions.md": "# Decisions\n",
        "references/validation-report.md": "# Validation\n",
        "references/workflow-binding.md": (
            "# Workflow binding\n\ncanonical_task_state: STATUS.md\n"
            "parallel_agents: false\natomic_claim_mechanism: N/A\n"
        ),
        "references/tickets/INDEX.md": ticket_index(
            "| `MP-001` | [MP-001.md](MP-001.md) | `M1` | none | `MP-001` |"
        ),
        "references/tickets/MP-001.md": ticket("MP-001"),
        "references/diagrams/architecture.svg": (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            '<text x="1" y="10">Architecture</text></svg>\n'
        ),
    }
    for relative, content in files.items():
        write(root, relative, content)


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(VALIDATOR), str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_base_passes() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        result = run(root)
        assert result.returncode == 0, result.stdout + result.stderr


def test_orphan_detail_fails_then_index_passes() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(root, "references/implementation/editor.md", "# Editor\n")
        failed = run(root)
        assert failed.returncode == 1
        assert "references/INDEX.md is missing" in failed.stdout
        write(
            root,
            "references/INDEX.md",
            "# Index\n\n| Document | Scope | Source decisions/evidence | Owning section/milestones | Dependencies | Validator |\n"
            "|---|---|---|---|---|---|\n"
            "| `implementation/editor.md` | editor | source map | §18, M2 | M1 | tests |\n",
        )
        passed = run(root)
        assert passed.returncode == 0, passed.stdout + passed.stderr


def test_absorption_contract_and_lock_are_enforced() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(root, "references/absorption/repo-lock.json", "[]\n")
        write(
            root,
            "references/INDEX.md",
            "# Index\n\n| Document | Scope | Source decisions/evidence | Owning section/milestones | Dependencies | Validator |\n"
            "|---|---|---|---|---|---|\n",
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "incomplete code-absorption package" in failed.stdout
        assert "expected non-empty JSON array" in failed.stdout

        for relative in ABSORPTION_DOCS:
            write(root, f"references/absorption/{relative}", f"# {relative}\n")
        lock = [{"source_slug": "example", "url": "https://example.test/repo.git", "commit": "abcdef1", "clone_date": "2026-09-05"}]
        write(root, "references/absorption/repo-lock.json", json.dumps(lock))
        missing_map = run(root)
        assert missing_map.returncode == 1
        assert "tree-map/example/INDEX.md" in missing_map.stdout
        write_source_maps(root, "example")
        write(
            root,
            "references/INDEX.md",
            "# Index\n\n| Document | Scope | Source decisions/evidence | Owning section/milestones | Dependencies | Validator |\n"
            "|---|---|---|---|---|---|\n"
            + absorption_index_rows("repo-analysis/example.md", "tree-map/example/INDEX.md")
            + "\n",
        )
        passed = run(root)
        assert passed.returncode == 0, passed.stdout + passed.stderr


def test_ticket_layer_is_required() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        (root / "references/tickets/MP-001.md").unlink()
        (root / "references/tickets/INDEX.md").unlink()
        (root / "references/tickets").rmdir()
        failed = run(root)
        assert failed.returncode == 1
        assert "missing required ticket directory: references/tickets" in failed.stdout


def test_ticket_contract_required_fields_and_catalog_match_are_enforced() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        (root / "references/tickets/MP-001.md").unlink()
        write(root, "references/tickets/BAD.md", "# Ticket BAD\n\n- **ID:** `bad id`\n")
        failed = run(root)
        assert failed.returncode == 1
        assert "ticket catalog references missing contract: MP-001.md" in failed.stdout
        assert "invalid ticket ID" in failed.stdout
        assert "missing required field: Goal" in failed.stdout
        assert "ticket contract not listed in catalog: BAD.md" in failed.stdout


def test_duplicate_ticket_id_fails() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(root, "references/tickets/MP-002.md", ticket("MP-001"))
        write(
            root,
            "references/tickets/INDEX.md",
            ticket_index(
                "| `MP-001` | [MP-001.md](MP-001.md) | `M1` | none | `MP-001` |\n"
                "| `MP-002` | [MP-002.md](MP-002.md) | `M1` | none | `MP-002` |"
            ),
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "duplicate ticket ID: MP-001" in failed.stdout
        assert "ticket contract filename does not match ID: MP-002.md -> MP-001" in failed.stdout


def test_missing_ticket_dependency_fails() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(root, "references/tickets/MP-001.md", ticket("MP-001", "`MP-999`"))
        write(
            root,
            "references/tickets/INDEX.md",
            ticket_index("| `MP-001` | [MP-001.md](MP-001.md) | `M1` | `MP-999` | `MP-001` |"),
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "missing dependency: MP-001 -> MP-999" in failed.stdout


def test_ticket_dependency_cycle_fails() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(root, "references/tickets/MP-001.md", ticket("MP-001", "`MP-002`"))
        write(root, "references/tickets/MP-002.md", ticket("MP-002", "`MP-001`"))
        write(
            root,
            "references/tickets/INDEX.md",
            ticket_index(
                "| `MP-001` | [MP-001.md](MP-001.md) | `M1` | `MP-002` | `MP-001` |\n"
                "| `MP-002` | [MP-002.md](MP-002.md) | `M1` | `MP-001` | `MP-002` |"
            ),
        )
        write(
            root,
            "masterplan.md",
            masterplan_ticket_map(
                "| `M1` — Walking skeleton | Runnable slices | `MP-001`, `MP-002` | none |"
            ),
        )
        write(
            root,
            "STATUS.md",
            "# Status\n\n**Status mode:** fallback\n**Canonical task state:** STATUS.md\n\n"
            "| ID | Status | Evidence |\n|---|---|---|\n"
            "| `MP-001` | pending | — |\n| `MP-002` | pending | — |\n",
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "ticket dependency cycle:" in failed.stdout
        assert "MP-001" in failed.stdout and "MP-002" in failed.stdout


def test_ticket_bad_doc_link_fails() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        content = ticket("MP-001").replace(
            "[Decisions](../decisions.md)", "[Missing](../missing.md)"
        )
        write(root, "references/tickets/MP-001.md", content)
        failed = run(root)
        assert failed.returncode == 1
        assert "broken link: references/tickets/MP-001.md -> ../missing.md" in failed.stdout


def test_global_link_checker_ignores_fences_and_supports_titles() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(
            root,
            "masterplan.md",
            (root / "masterplan.md").read_text(encoding="utf-8")
            + '\n[Decisions](references/decisions.md "Record")\n'
            + '```markdown\n[Example](missing-example.md)\n```\n',
        )
        passed = run(root)
        assert passed.returncode == 0, passed.stdout + passed.stderr


def test_ticket_execution_safety_fields_cannot_be_na() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        content = ticket("MP-001")
        content = content.replace("`python3 -m unittest`", "N/A")
        content = content.replace("`references/evidence/MP-001/validation.txt`", "N/A")
        content = content.replace("Revert `src/app.py` and `tests/test_app.py` only.", "N/A")
        write(root, "references/tickets/MP-001.md", content)
        failed = run(root)
        assert failed.returncode == 1
        assert "Validation commands must be actionable" in failed.stdout
        assert "Expected evidence destination must be actionable" in failed.stdout
        assert "Rollback boundary must name backticked target path" in failed.stdout


def test_absorbed_source_ticket_requires_pin_paths_and_attribution() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        content = ticket("MP-001")
        content = content.replace("N/A — no source code absorption", "https://example.test/repo.git")
        content = content.replace("N/A — no source repository", "N/A — omitted", 2)
        content = content.replace("N/A — no absorbed code", "N/A — omitted")
        write(root, "references/tickets/MP-001.md", content)
        failed = run(root)
        assert failed.returncode == 1
        assert "Source commit must be a pinned SHA" in failed.stdout
        assert "Source paths required when source code is absorbed" in failed.stdout
        assert "License/attribution required when source code is absorbed" in failed.stdout


def test_status_cannot_advance_before_dependencies_or_without_evidence() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(root, "references/tickets/MP-002.md", ticket("MP-002", "`MP-001`"))
        write(
            root,
            "references/tickets/INDEX.md",
            ticket_index(
                "| `MP-001` | [MP-001.md](MP-001.md) | `M1` | none | `MP-001` |\n"
                "| `MP-002` | [MP-002.md](MP-002.md) | `M1` | `MP-001` | `MP-002` |"
            ),
        )
        write(
            root,
            "masterplan.md",
            masterplan_ticket_map(
                "| `M1` — Walking skeleton | Runnable slices | `MP-001`, `MP-002` | none |"
            ),
        )
        write(
            root,
            "STATUS.md",
            "# Status\n\n**Status mode:** fallback\n**Canonical task state:** STATUS.md\n\n"
            "| ID | Status | Evidence |\n|---|---|---|\n"
            "| `MP-001` | pending | — |\n"
            "| `MP-002` | claimed | — |\n",
        )
        blocked = run(root)
        assert blocked.returncode == 1
        assert "ticket advanced before dependencies are done: MP-002 -> MP-001" in blocked.stdout

        write(
            root,
            "STATUS.md",
            "# Status\n\n**Status mode:** fallback\n**Canonical task state:** STATUS.md\n\n"
            "| ID | Status | Evidence |\n|---|---|---|\n"
            "| `MP-001` | done | — |\n"
            "| `MP-002` | pending | — |\n",
        )
        no_evidence = run(root)
        assert no_evidence.returncode == 1
        assert "done ticket requires evidence: MP-001" in no_evidence.stdout

        write(root, "references/evidence/MP-001/validation.txt", "PASS\n")
        write(
            root,
            "STATUS.md",
            "# Status\n\n**Status mode:** fallback\n**Canonical task state:** STATUS.md\n\n"
            "| ID | Status | Claimed by | Updated | Evidence | Blocker/note |\n"
            "|---|---|---|---|---|---|\n"
            "| `MP-001` | done | agent-a | 2026-09-05T10:00:00Z | `references/evidence/MP-001/validation.txt` | — |\n"
            "| `MP-002` | claimed | agent-b | 2026-09-05T10:01:00Z | — | — |\n",
        )
        passed = run(root)
        assert passed.returncode == 0, passed.stdout + passed.stderr

        write(root, "references/evidence/MP-001/other.txt", "PASS\n")
        write(
            root,
            "STATUS.md",
            "# Status\n\n**Status mode:** fallback\n**Canonical task state:** STATUS.md\n\n"
            "| ID | Status | Evidence |\n|---|---|---|\n"
            "| `MP-001` | done | `references/evidence/MP-001/other.txt` |\n"
            "| `MP-002` | pending | — |\n",
        )
        mismatch = run(root)
        assert mismatch.returncode == 1
        assert "ticket evidence destination mismatch: MP-001" in mismatch.stdout


def test_external_queue_requires_durable_one_to_one_status_export() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(
            root,
            "references/workflow-binding.md",
            "# Workflow binding\n\ncanonical_task_state: https://queue.example/project\n"
            "parallel_agents: true\natomic_claim_mechanism: queue compare-and-set\n",
        )
        write(
            root,
            "STATUS.md",
            "# Status\n\n**Status mode:** external-export\n"
            "**Canonical task state:** https://queue.example/project\n"
            "**Exported at:** 2026-09-05T10:00:00Z\n\n"
            "| ID | Status | Evidence |\n|---|---|---|\n"
            "| `MP-001` | ready | — |\n| `MP-001` | pending | — |\n",
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "invalid canonical ticket status: MP-001 -> ready" in failed.stdout
        assert "duplicate canonical status record: MP-001" in failed.stdout

        write(
            root,
            "STATUS.md",
            "# Status\n\n**Status mode:** external-export\n"
            "**Canonical task state:** https://queue.example/project\n"
            "**Exported at:** 2026-09-05T10:00:00Z\n"
            "**Status mapping:** Open -> pending; Started -> claimed; Closed -> done\n\n"
            "| ID | Status | Evidence |\n|---|---|---|\n"
            "| `MP-001` | pending | — |\n",
        )
        passed = run(root)
        assert passed.returncode == 0, passed.stdout + passed.stderr


def test_fenced_ticket_structures_do_not_satisfy_schema() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(root, "references/tickets/MP-001.md", "```markdown\n" + ticket("MP-001") + "```\n")
        failed = run(root)
        assert failed.returncode == 1
        assert "missing required field: ID" in failed.stdout

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        original = (root / "references/tickets/INDEX.md").read_text(encoding="utf-8")
        write(root, "references/tickets/INDEX.md", "```markdown\n" + original + "```\n")
        failed = run(root)
        assert failed.returncode == 1
        assert "ticket catalog has no ticket records" in failed.stdout

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(
            root,
            "STATUS.md",
            "# Status\n\n**Status mode:** fallback\n**Canonical task state:** STATUS.md\n\n"
            "```markdown\n| ID | Status | Evidence |\n|---|---|---|\n| `MP-001` | pending | — |\n```\n",
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "STATUS.md missing canonical status mapping for ticket: MP-001" in failed.stdout


def test_status_mode_requires_full_value_match() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        path = root / "STATUS.md"
        write(root, "STATUS.md", path.read_text(encoding="utf-8").replace("fallback", "fallback | external-export", 1))
        failed = run(root)
        assert failed.returncode == 1
        assert "requires exact Status mode" in failed.stdout


def test_invalid_status_data_row_id_fails() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        path = root / "STATUS.md"
        write(
            root,
            "STATUS.md",
            path.read_text(encoding="utf-8").replace(
                "| `MP-001` | pending | — |", "| bad-id | pending | — |"
            ),
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "invalid ticket ID in STATUS.md data row: bad-id" in failed.stdout


def test_ticket_actionability_requires_structured_values() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        content = ticket("MP-001")
        content = content.replace("`python3 -m unittest`", "Run the tests thoroughly.")
        content = content.replace(
            "`references/evidence/MP-001/validation.txt`", "https://example.test/validation.txt"
        )
        content = content.replace(
            "Revert `src/app.py` and `tests/test_app.py` only.", "Revert the changed files."
        )
        write(root, "references/tickets/MP-001.md", content)
        failed = run(root)
        assert failed.returncode == 1
        assert "Validation commands must contain inline-code command entries" in failed.stdout
        assert "Expected evidence destination must be exact package-relative" in failed.stdout
        assert "Rollback boundary must name backticked target path" in failed.stdout

    for bad_path in ("`/tmp/receipt.md`", "`references/evidence/MP-001/../../receipt.md`"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_package(root)
            content = ticket("MP-001").replace(
                "`references/evidence/MP-001/validation.txt`", bad_path
            )
            write(root, "references/tickets/MP-001.md", content)
            failed = run(root)
            assert failed.returncode == 1
            assert "Expected evidence destination must be exact package-relative" in failed.stdout


def test_source_provenance_url_and_all_or_none_are_enforced() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        content = ticket("MP-001")
        content = content.replace("N/A — no source code absorption", "git@example.test:repo.git")
        content = content.replace("N/A — no source repository", "`abcdef1`", 1)
        content = content.replace("N/A — no source repository", "`src/core.py:run`", 1)
        content = content.replace("N/A — no absorbed code", "MIT; preserve NOTICE")
        write(root, "references/tickets/MP-001.md", content)
        failed = run(root)
        assert failed.returncode == 1
        assert "Source repository must be valid http/https URL" in failed.stdout

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        content = ticket("MP-001").replace("N/A — no source repository", "`abcdef1`", 1)
        write(root, "references/tickets/MP-001.md", content)
        failed = run(root)
        assert failed.returncode == 1
        assert "source provenance must be all active or all N/A" in failed.stdout


def test_contract_status_is_exact_immutable_declaration() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        content = ticket("MP-001").replace(
            "Tracked by canonical task state under `MP-001`; initial status `pending`.",
            "Current status `done` for `MP-001`.",
        )
        write(root, "references/tickets/MP-001.md", content)
        failed = run(root)
        assert failed.returncode == 1
        assert "Status must equal immutable declaration" in failed.stdout


def test_ticket_doc_links_support_titles_and_reject_directories_and_escapes() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        content = ticket("MP-001").replace(
            "[Decisions](../decisions.md)", '[Decisions](../decisions.md "Decision record")'
        )
        write(root, "references/tickets/MP-001.md", content)
        passed = run(root)
        assert passed.returncode == 0, passed.stdout + passed.stderr

    for bad_link in ("[References](..)", "[Escape](../../../outside.md)"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_package(root)
            content = ticket("MP-001").replace("[Decisions](../decisions.md)", bad_link)
            write(root, "references/tickets/MP-001.md", content)
            failed = run(root)
            assert failed.returncode == 1
            assert "Owned docs link must resolve to package-local Markdown file" in failed.stdout


def test_workflow_status_binding_parity_and_external_metadata() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(root, "references/workflow-binding.md", "canonical_task_state: https://queue.example/other\n")
        write(
            root,
            "STATUS.md",
            "# Status\n\n**Status mode:** external-export\n"
            "**Canonical task state:** https://queue.example/project\n"
            "**Exported at:** not-a-timestamp\n"
            "**Status mapping:**\n\n"
            "| ID | Status | Evidence |\n|---|---|---|\n| `MP-001` | pending | — |\n",
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "external canonical task state must exactly match workflow binding" in failed.stdout
        assert "Exported at must be RFC3339" in failed.stdout
        assert "requires nonempty parseable Status mapping" in failed.stdout

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(root, "references/workflow-binding.md", "# No binding value\n")
        failed = run(root)
        assert failed.returncode == 1
        assert "workflow binding requires exactly one nonempty canonical_task_state" in failed.stdout


def test_masterplan_section_18_must_match_catalog() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(
            root,
            "masterplan.md",
            masterplan_ticket_map("| `M2` — stale | Stale map | `MP-999` | none |"),
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "catalog ticket missing from masterplan §18: MP-001" in failed.stdout
        assert "masterplan §18 has unknown ticket ID: MP-999" in failed.stdout

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(
            root,
            "masterplan.md",
            masterplan_ticket_map("| `M2` — stale | Stale milestone | `MP-001` | none |"),
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "ticket milestone mismatch between catalog and masterplan §18: MP-001" in failed.stdout


def test_fallback_concurrency_requires_external_atomic_claim() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        write(
            root,
            "references/workflow-binding.md",
            "canonical_task_state: STATUS.md\nparallel_agents: true\natomic_claim_mechanism: N/A\n",
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "permits concurrent executors only with external atomic_claim_mechanism" in failed.stdout

        write(
            root,
            "references/workflow-binding.md",
            "canonical_task_state: STATUS.md\nparallel_agents: true\n"
            "atomic_claim_mechanism: database compare-and-set service\n",
        )
        passed = run(root)
        assert passed.returncode == 0, passed.stdout + passed.stderr


def test_executor_docs_keep_needs_rework_claimable() -> None:
    docs = (
        ROOT / "skills/masterplan/references/execute-template.md",
        ROOT / "skills/masterplan/references/ticket-contract.md",
    )
    for path in docs:
        text = path.read_text(encoding="utf-8")
        assert "`pending` or `needs-rework`" in text, path


def test_repo_lock_provenance_fails_closed() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        base_package(root)
        for relative in ABSORPTION_DOCS:
            write(root, f"references/absorption/{relative}", f"# {relative}\n")
        write_source_maps(root, "repo")
        bad_lock = [{
            "source_slug": "repo",
            "url": "https://example.test/repo.git",
            "commit": "abcdef1",
            "clone_date": "2026-09-05",
            "archive_url": "https://example.test/repo.tar.gz",
            "submodules": [{"url": "https://example.test/sub.git", "commit": "bad"}],
        }]
        write(root, "references/absorption/repo-lock.json", json.dumps(bad_lock))
        write(
            root,
            "references/INDEX.md",
            "# Index\n\n| Document | Scope | Source decisions/evidence | Owning section/milestones | Dependencies | Validator |\n"
            "|---|---|---|---|---|---|\n"
            + absorption_index_rows("repo-analysis/repo.md", "tree-map/repo/INDEX.md")
            + "\n",
        )
        failed = run(root)
        assert failed.returncode == 1
        assert "archive requires SHA-256 digest" in failed.stdout
        assert "requires url + commit SHA" in failed.stdout


if __name__ == "__main__":
    test_base_passes()
    test_orphan_detail_fails_then_index_passes()
    test_absorption_contract_and_lock_are_enforced()
    test_ticket_layer_is_required()
    test_ticket_contract_required_fields_and_catalog_match_are_enforced()
    test_duplicate_ticket_id_fails()
    test_missing_ticket_dependency_fails()
    test_ticket_dependency_cycle_fails()
    test_ticket_bad_doc_link_fails()
    test_global_link_checker_ignores_fences_and_supports_titles()
    test_ticket_execution_safety_fields_cannot_be_na()
    test_absorbed_source_ticket_requires_pin_paths_and_attribution()
    test_status_cannot_advance_before_dependencies_or_without_evidence()
    test_external_queue_requires_durable_one_to_one_status_export()
    test_fenced_ticket_structures_do_not_satisfy_schema()
    test_status_mode_requires_full_value_match()
    test_invalid_status_data_row_id_fails()
    test_ticket_actionability_requires_structured_values()
    test_source_provenance_url_and_all_or_none_are_enforced()
    test_contract_status_is_exact_immutable_declaration()
    test_ticket_doc_links_support_titles_and_reject_directories_and_escapes()
    test_workflow_status_binding_parity_and_external_metadata()
    test_masterplan_section_18_must_match_catalog()
    test_fallback_concurrency_requires_external_atomic_claim()
    test_executor_docs_keep_needs_rework_claimable()
    test_repo_lock_provenance_fails_closed()
    print("PASS: validate-package tests")
