#!/usr/bin/env python3
"""Validate a generated masterplan package using only Python stdlib."""
from __future__ import annotations

import datetime
import json
import re
import sys
import xml.dom.minidom
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

REQUIRED = (
    "masterplan.md",
    "masterplan.html",
    "EXECUTE.md",
    "STATUS.md",
    "references/decisions.md",
    "references/validation-report.md",
    "references/workflow-binding.md",
)
PLACEHOLDER = re.compile(r"\b(?:TBD|TODO|FIXME)\b|[⟨⟩]")
MD_LINK = re.compile(
    r"!?\[[^]\n]*]\(\s*(?:<([^>\n]+)>|([^\s)]+))"
    r"(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^()\n]*\)))?\s*\)"
)
TICKET_ID = re.compile(r"[A-Z][A-Z0-9]*-[0-9]{3,}")
TICKET_FIELD = re.compile(r"^- \*\*([^*]+):\*\*\s*(.+?)\s*$", re.MULTILINE)
INLINE_CODE = re.compile(r"`([^`\n]+)`")
CANONICAL_STATUSES = {"pending", "claimed", "blocked", "done", "needs-rework"}
TICKET_FIELDS = (
    "ID",
    "Goal",
    "Milestone",
    "Dependencies",
    "Owned docs",
    "Linked docs",
    "Source repository",
    "Source commit",
    "Source paths",
    "Target paths",
    "Target contracts",
    "Exact changes",
    "Retained behavior",
    "Changed behavior",
    "Acceptance criteria",
    "Validation commands",
    "Expected evidence destination",
    "License/attribution",
    "Rollback boundary",
    "Status",
)
NA = re.compile(r"^(?:N/A|none)(?:\b|\s*[—-])", re.IGNORECASE)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def live_markdown(text: str) -> str:
    """Remove fenced blocks while preserving line positions."""
    live: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence is None and marker:
            token = marker.group(1)
            fence = (token[0], len(token))
            live.append("\n" if line.endswith("\n") else "")
        elif fence is not None:
            if re.match(rf"^ {{0,3}}{re.escape(fence[0])}{{{fence[1]},}}\s*$", line.rstrip("\n")):
                fence = None
            live.append("\n" if line.endswith("\n") else "")
        else:
            live.append(line)
    return "".join(live)


def markdown_tables(text: str) -> list[list[tuple[str, list[str]]]]:
    tables: list[list[tuple[str, list[str]]]] = []
    current: list[tuple[str, list[str]]] = []
    for line in live_markdown(text).splitlines():
        if line.startswith("|"):
            current.append((line, [cell.strip() for cell in line.strip().strip("|").split("|")]))
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables


def table_with_headers(text: str, required: set[str]) -> list[tuple[str, list[str]]]:
    for table in markdown_tables(text):
        if any(required <= {unquote(cell).lower() for cell in cells} for _, cells in table):
            return table
    return []


def markdown_link_targets(text: str) -> list[str]:
    return [(match.group(1) or match.group(2)).strip() for match in MD_LINK.finditer(live_markdown(text))]


def is_table_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def metadata(text: str, label: str) -> str:
    match = re.search(
        rf"^\*\*{re.escape(label)}:\*\*[ \t]*(.*?)[ \t]*$",
        live_markdown(text),
        re.MULTILINE,
    )
    return match.group(1) if match else ""


def valid_http_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.hostname)
            and not parsed.username
            and not any(character.isspace() for character in value)
        )
    except ValueError:
        return False


def safe_package_path(value: str) -> PurePosixPath | None:
    try:
        if "\\" in value or "?" in value or "#" in value or urlsplit(value).scheme:
            return None
    except ValueError:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or not path.name or any(part in {"", ".", ".."} for part in path.parts):
        return None
    return path


def unquote(value: str) -> str:
    value = value.strip()
    return value[1:-1] if len(value) >= 2 and value[0] == value[-1] == "`" else value


def ids_in(value: str) -> list[str]:
    if NA.match(value):
        return []
    return re.findall(r"(?<![A-Z0-9-])[A-Z][A-Z0-9]*-[0-9]{3,}(?![A-Z0-9-])", value)


def dependency_ids(value: str, errors: list[str], source: str) -> list[str]:
    if NA.match(value):
        return []
    found = ids_in(value)
    residue = value
    for ticket_id in found:
        residue = residue.replace(ticket_id, "", 1)
    if residue.replace("`", "").replace(",", "").strip() or not found:
        fail(errors, f"invalid dependency list in {source}: {value}")
    if len(found) != len(set(found)):
        fail(errors, f"duplicate dependency in {source}: {value}")
    return found


def workflow_binding_state(root: Path, errors: list[str]) -> tuple[str, bool, str]:
    path = root / "references/workflow-binding.md"
    if not path.is_file():
        return "", False, ""
    text = live_markdown(path.read_text(encoding="utf-8"))

    def values(label: str) -> list[str]:
        return [
            value.strip()
            for value in re.findall(
                rf"^[ \t]*{re.escape(label)}:[ \t]*(.*?)[ \t]*$", text, re.MULTILINE
            )
        ]

    states = values("canonical_task_state")
    if len(states) != 1 or not states[0]:
        fail(errors, "workflow binding requires exactly one nonempty canonical_task_state")
    parallel_values = values("parallel_agents")
    parallel = len(parallel_values) == 1 and parallel_values[0].lower() == "true"
    mechanisms = values("atomic_claim_mechanism")
    return (unquote(states[0]) if len(states) == 1 else "", parallel, unquote(mechanisms[0]) if len(mechanisms) == 1 else "")


def validate_status_mapping(value: str, errors: list[str]) -> None:
    entries = [entry.strip() for entry in value.split(";") if entry.strip()]
    if not entries:
        fail(errors, "external STATUS.md export requires nonempty parseable Status mapping")
        return
    for entry in entries:
        match = re.fullmatch(r"(.+?)\s*(?:->|→)\s*`?([a-z-]+)`?", entry)
        if not match or not match.group(1).strip() or match.group(2) not in CANONICAL_STATUSES:
            fail(errors, f"external STATUS.md export has invalid Status mapping entry: {entry}")


def validate_status(
    root: Path,
    graph: dict[str, list[str]],
    evidence_destinations: dict[str, str],
    errors: list[str],
) -> None:
    ticket_ids = set(graph)
    path = root / "STATUS.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    mode = metadata(text, "Status mode")
    if mode not in {"fallback", "external-export"}:
        fail(errors, "STATUS.md requires exact Status mode: fallback or external-export")

    canonical_state = unquote(metadata(text, "Canonical task state"))
    binding_state, parallel_agents, atomic_claim = workflow_binding_state(root, errors)
    if mode == "fallback":
        if canonical_state != "STATUS.md":
            fail(errors, "fallback STATUS.md requires Canonical task state: STATUS.md")
        if binding_state != "STATUS.md":
            fail(errors, "fallback canonical task state must match workflow binding: STATUS.md")
        if parallel_agents and (not atomic_claim or atomic_claim.lower() in {"none", "n/a", "status.md"}):
            fail(errors, "fallback STATUS.md permits concurrent executors only with external atomic_claim_mechanism")
    elif mode == "external-export":
        if not canonical_state:
            fail(errors, "external STATUS.md export missing metadata: Canonical task state")
        elif canonical_state == "STATUS.md":
            fail(errors, "external STATUS.md canonical task state must not be STATUS.md")
        if not binding_state or canonical_state != binding_state:
            fail(errors, "external canonical task state must exactly match workflow binding")
        exported_at = metadata(text, "Exported at")
        try:
            if not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})",
                exported_at,
            ):
                raise ValueError
            timestamp = datetime.datetime.fromisoformat(exported_at.replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                raise ValueError
        except ValueError:
            fail(errors, "external STATUS.md Exported at must be RFC3339 timestamp with timezone")
        validate_status_mapping(metadata(text, "Status mapping"), errors)

    records: dict[str, str] = {}
    columns: dict[str, int] = {}
    in_status_table = False
    for line, cells in table_with_headers(text, {"id", "status"}):
        normalized = [unquote(cell).lower() for cell in cells]
        if "id" in normalized and "status" in normalized:
            columns = {name: normalized.index(name) for name in ("id", "status", "evidence") if name in normalized}
            in_status_table = True
            continue
        if not in_status_table or is_table_separator(cells):
            continue
        if len(cells) <= max(columns.values()):
            fail(errors, f"invalid STATUS.md data row: {line}")
            continue
        ticket_id = unquote(cells[columns["id"]])
        if not TICKET_ID.fullmatch(ticket_id):
            fail(errors, f"invalid ticket ID in STATUS.md data row: {ticket_id or '(empty)'}")
            continue
        status = unquote(cells[columns["status"]]).lower()
        evidence = cells[columns["evidence"]] if "evidence" in columns else ""
        if ticket_id in records:
            fail(errors, f"duplicate canonical status record: {ticket_id}")
        records[ticket_id] = status
        if status not in CANONICAL_STATUSES:
            fail(errors, f"invalid canonical ticket status: {ticket_id} -> {status}")
        if status == "done":
            evidence_link = re.fullmatch(r"`?([^`]+)`?", evidence)
            if not evidence_link or evidence in {"", "—", "-", "none", "N/A"}:
                fail(errors, f"done ticket requires evidence: {ticket_id}")
            else:
                evidence_rel = evidence_link.group(1)
                evidence_path = (root / evidence_rel).resolve()
                expected = unquote(evidence_destinations.get(ticket_id, ""))
                if evidence_rel != expected:
                    fail(errors, f"ticket evidence destination mismatch: {ticket_id} -> {evidence_rel}")
                if ticket_id not in Path(evidence_rel).parts:
                    fail(errors, f"done ticket evidence must be ticket-scoped: {ticket_id} -> {evidence}")
                if root not in evidence_path.parents or not evidence_path.is_file():
                    fail(errors, f"done ticket evidence missing or outside package: {ticket_id} -> {evidence}")

    for ticket_id in sorted(ticket_ids - records.keys()):
        fail(errors, f"STATUS.md missing canonical status mapping for ticket: {ticket_id}")
    for ticket_id in sorted(records.keys() - ticket_ids):
        fail(errors, f"STATUS.md has status record without local ticket: {ticket_id}")
    for ticket_id, dependencies in graph.items():
        if records.get(ticket_id) not in {"claimed", "done"}:
            continue
        for dependency in dependencies:
            if records.get(dependency) != "done":
                fail(errors, f"ticket advanced before dependencies are done: {ticket_id} -> {dependency}")


def parse_ticket_catalog(path: Path, errors: list[str]) -> dict[str, tuple[str, str, list[str]]]:
    catalog: dict[str, tuple[str, str, list[str]]] = {}
    ticket_order: list[str] = []
    rows = table_with_headers(
        path.read_text(encoding="utf-8"),
        {"id", "contract", "milestone", "dependencies", "status record"},
    )
    if not rows:
        fail(errors, "ticket catalog missing exact five-column header")
    for line, cells in rows:
        if not cells or unquote(cells[0]).lower() == "id" or is_table_separator(cells):
            continue
        if len(cells) != 5:
            fail(errors, f"invalid ticket catalog row (expected 5 columns): {line}")
            continue
        ticket_id = unquote(cells[0])
        ticket_order.append(ticket_id)
        if not TICKET_ID.fullmatch(ticket_id):
            fail(errors, f"invalid ticket ID in catalog: {ticket_id}")
            continue
        if ticket_id in catalog:
            fail(errors, f"duplicate ticket ID in catalog: {ticket_id}")
            continue
        links = markdown_link_targets(cells[1])
        target = links[0] if len(links) == 1 else ""
        if target != f"{ticket_id}.md":
            if not target:
                fail(errors, f"ticket catalog contract must be a local Markdown link: {ticket_id}")
                continue
            fail(errors, f"ticket catalog contract filename must match ID: {ticket_id} -> {target}")
        milestone = unquote(cells[2])
        if not re.fullmatch(r"M[0-9]+", milestone):
            fail(errors, f"invalid milestone in ticket catalog: {ticket_id} -> {milestone}")
        status_record = unquote(cells[4])
        if status_record != ticket_id:
            fail(errors, f"ticket status record must equal stable ID: {ticket_id} -> {status_record}")
        catalog[ticket_id] = (
            target,
            milestone,
            dependency_ids(cells[3], errors, f"catalog ticket {ticket_id}"),
        )
    if not catalog:
        fail(errors, "ticket catalog has no ticket records")
    if ticket_order != sorted(ticket_order):
        fail(errors, "ticket catalog rows must use stable-ID order")
    return catalog


def validate_masterplan_ticket_map(
    root: Path,
    catalog: dict[str, tuple[str, str, list[str]]],
    errors: list[str],
) -> None:
    path = root / "masterplan.md"
    if not path.is_file():
        return
    text = live_markdown(path.read_text(encoding="utf-8"))
    section_match = re.search(r"^##\s+18\.\s+.*?(?=^##\s+19\.|\Z)", text, re.MULTILINE | re.DOTALL)
    if not section_match:
        fail(errors, "masterplan.md missing §18 build-order section")
        return
    rows = table_with_headers(section_match.group(0), {"milestone", "ticket ids"})
    columns: dict[str, int] = {}
    mapped: dict[str, str] = {}
    for line, cells in rows:
        normalized = [unquote(cell).lower() for cell in cells]
        if "milestone" in normalized and "ticket ids" in normalized:
            columns = {name: normalized.index(name) for name in ("milestone", "ticket ids")}
            continue
        if not columns or is_table_separator(cells):
            continue
        if len(cells) <= max(columns.values()):
            fail(errors, f"invalid masterplan §18 milestone row: {line}")
            continue
        milestone_match = re.search(r"(?<![A-Z0-9])M[0-9]+(?![A-Z0-9])", unquote(cells[columns["milestone"]]))
        if not milestone_match:
            fail(errors, f"invalid masterplan §18 milestone: {cells[columns['milestone']]}")
            continue
        milestone = milestone_match.group(0)
        row_ids = ids_in(cells[columns["ticket ids"]])
        if not row_ids:
            fail(errors, f"masterplan §18 milestone has no ticket IDs: {milestone}")
        for ticket_id in row_ids:
            if ticket_id in mapped:
                fail(errors, f"duplicate ticket in masterplan §18: {ticket_id}")
            mapped[ticket_id] = milestone
    if not columns:
        fail(errors, "masterplan §18 requires Milestone and Ticket IDs table")
    for ticket_id in sorted(set(catalog) - set(mapped)):
        fail(errors, f"catalog ticket missing from masterplan §18: {ticket_id}")
    for ticket_id in sorted(set(mapped) - set(catalog)):
        fail(errors, f"masterplan §18 has unknown ticket ID: {ticket_id}")
    for ticket_id in sorted(set(catalog) & set(mapped)):
        if catalog[ticket_id][1] != mapped[ticket_id]:
            fail(errors, f"ticket milestone mismatch between catalog and masterplan §18: {ticket_id}")


def validate_ticket_doc_links(root: Path, path: Path, label: str, value: str, errors: list[str]) -> None:
    targets = markdown_link_targets(value)
    relative = path.relative_to(root)
    if not targets:
        fail(errors, f"{relative} {label} must contain a Markdown link")
        return
    for target in targets:
        try:
            parsed = urlsplit(target)
            target_path = PurePosixPath(parsed.path)
            resolved = (path.parent / target_path).resolve()
            valid = (
                not parsed.scheme
                and not parsed.netloc
                and not target_path.is_absolute()
                and target_path.suffix.lower() == ".md"
                and root in resolved.parents
                and resolved.is_file()
            )
        except ValueError:
            valid = False
        if not valid:
            fail(errors, f"{relative} {label} link must resolve to package-local Markdown file: {target}")


def validate_evidence_destination(root: Path, path: Path, ticket_id: str, value: str, errors: list[str]) -> None:
    relative = path.relative_to(root)
    raw = unquote(value)
    target = safe_package_path(raw)
    prefix = ("references", "evidence", ticket_id)
    if target is None or target.parts[:3] != prefix or len(target.parts) < 4:
        fail(errors, f"{relative} Expected evidence destination must be exact package-relative references/evidence/{ticket_id}/... regular-file path")


def validate_rollback_boundary(
    root: Path, path: Path, value: str, target_value: str, errors: list[str]
) -> None:
    rollback_targets = INLINE_CODE.findall(value)
    target_paths = set(INLINE_CODE.findall(target_value))
    valid = any(
        target in target_paths
        or re.fullmatch(r"(?:state|transaction):[A-Za-z0-9._/-]+", target)
        for target in rollback_targets
    )
    if not valid:
        fail(errors, f"{path.relative_to(root)} Rollback boundary must name backticked target path or state/transaction identifier")


def validate_source_provenance(root: Path, path: Path, fields: dict[str, str], errors: list[str]) -> None:
    relative = path.relative_to(root)
    labels = ("Source repository", "Source commit", "Source paths", "License/attribution")
    inactive = {label: bool(NA.match(fields.get(label, ""))) for label in labels}
    if inactive["Source repository"]:
        if not all(inactive.values()):
            fail(errors, f"{relative} source provenance must be all active or all N/A")
        return
    if any(inactive.values()):
        fail(errors, f"{relative} source provenance must be all active or all N/A")
    source = unquote(fields.get("Source repository", ""))
    if not valid_http_url(source):
        fail(errors, f"{relative} Source repository must be valid http/https URL")
    sha = unquote(fields.get("Source commit", ""))
    if not re.fullmatch(r"[0-9a-fA-F]{7,40}", sha):
        fail(errors, f"{relative} Source commit must be a pinned SHA")
    source_paths = INLINE_CODE.findall(fields.get("Source paths", ""))
    if inactive["Source paths"] or not source_paths or not all(
        safe_package_path(source_path.split(":", 1)[0]) for source_path in source_paths
    ):
        fail(errors, f"{relative} Source paths required when source code is absorbed")
    if inactive["License/attribution"] or not fields.get("License/attribution", "").strip():
        fail(errors, f"{relative} License/attribution required when source code is absorbed")



def validate_tickets(root: Path, errors: list[str]) -> None:
    tickets = root / "references" / "tickets"
    index = tickets / "INDEX.md"
    if not tickets.is_dir():
        fail(errors, "missing required ticket directory: references/tickets")
        return
    if not index.is_file():
        fail(errors, "missing required ticket catalog: references/tickets/INDEX.md")
        return

    catalog = parse_ticket_catalog(index, errors)
    validate_masterplan_ticket_map(root, catalog, errors)
    files = sorted(path for path in tickets.glob("*.md") if path.name != "INDEX.md")
    if not files:
        fail(errors, "ticket catalog has no local ticket contracts")

    contracts: dict[str, tuple[Path, dict[str, str], list[str]]] = {}
    catalog_files = {Path(target).name for target, _, _ in catalog.values()}
    for path in files:
        text = path.read_text(encoding="utf-8")
        pairs = TICKET_FIELD.findall(live_markdown(text))
        fields: dict[str, str] = {}
        for label, value in pairs:
            if label in fields:
                fail(errors, f"{path.relative_to(root)} duplicate field: {label}")
            fields[label] = value.strip()
        for label in TICKET_FIELDS:
            if not fields.get(label):
                fail(errors, f"{path.relative_to(root)} missing required field: {label}")

        ticket_id = unquote(fields.get("ID", ""))
        if not TICKET_ID.fullmatch(ticket_id):
            fail(errors, f"{path.relative_to(root)} invalid ticket ID: {ticket_id or '(missing)'}")
        elif ticket_id in contracts:
            fail(errors, f"duplicate ticket ID: {ticket_id}")
        else:
            dependencies = dependency_ids(
                fields.get("Dependencies", "none"), errors, str(path.relative_to(root))
            )
            contracts[ticket_id] = (path, fields, dependencies)
        if ticket_id and path.name != f"{ticket_id}.md":
            fail(errors, f"ticket contract filename does not match ID: {path.name} -> {ticket_id}")
        if path.name not in catalog_files:
            fail(errors, f"ticket contract not listed in catalog: {path.name}")

        actionable = (
            "Goal",
            "Milestone",
            "Owned docs",
            "Linked docs",
            "Target paths",
            "Target contracts",
            "Exact changes",
            "Retained behavior",
            "Changed behavior",
            "Acceptance criteria",
            "Validation commands",
            "Expected evidence destination",
            "Rollback boundary",
            "Status",
        )
        for label in actionable:
            value = fields.get(label, "")
            if not value or NA.match(value):
                fail(errors, f"{path.relative_to(root)} {label} must be actionable")
        for label in ("Owned docs", "Linked docs"):
            validate_ticket_doc_links(root, path, label, fields.get(label, ""), errors)
        if not INLINE_CODE.findall(fields.get("Validation commands", "")):
            fail(errors, f"{path.relative_to(root)} Validation commands must contain inline-code command entries")
        if ticket_id:
            validate_evidence_destination(
                root, path, ticket_id, fields.get("Expected evidence destination", ""), errors
            )
            expected_status = f"Tracked by canonical task state under `{ticket_id}`; initial status `pending`."
            if fields.get("Status") != expected_status:
                fail(errors, f"{path.relative_to(root)} Status must equal immutable declaration: {expected_status}")
        validate_rollback_boundary(
            root,
            path,
            fields.get("Rollback boundary", ""),
            fields.get("Target paths", ""),
            errors,
        )
        validate_source_provenance(root, path, fields, errors)

    for ticket_id, (target, index_milestone, index_dependencies) in catalog.items():
        target_path = tickets / target
        if not target_path.is_file():
            fail(errors, f"ticket catalog references missing contract: {target}")
            continue
        contract = contracts.get(ticket_id)
        if contract is None:
            actual = next((item for item, data in contracts.items() if data[0].resolve() == target_path.resolve()), None)
            if actual:
                fail(errors, f"catalog ID {ticket_id} does not match contract ID {actual}")
            continue
        if contract[0].resolve() != target_path.resolve():
            fail(errors, f"ticket catalog path mismatch for {ticket_id}: {target}")
        contract_milestone = unquote(contract[1].get("Milestone", ""))
        if contract_milestone != index_milestone:
            fail(errors, f"ticket milestone mismatch between catalog and contract: {ticket_id}")
        if contract[2] != index_dependencies:
            fail(errors, f"ticket dependency mismatch between catalog and contract: {ticket_id}")

    known = set(contracts)
    graph: dict[str, list[str]] = {}
    for ticket_id, (_, _, dependencies) in contracts.items():
        graph[ticket_id] = dependencies
        for dependency in dependencies:
            if dependency not in known:
                fail(errors, f"missing dependency: {ticket_id} -> {dependency}")
            if dependency == ticket_id:
                fail(errors, f"ticket dependency cycle: {ticket_id} -> {ticket_id}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(ticket_id: str, trail: list[str]) -> None:
        if ticket_id in visiting:
            start = trail.index(ticket_id)
            fail(errors, "ticket dependency cycle: " + " -> ".join(trail[start:]))
            return
        if ticket_id in visited:
            return
        visiting.add(ticket_id)
        for dependency in graph.get(ticket_id, []):
            if dependency in graph:
                visit(dependency, trail + [dependency])
        visiting.remove(ticket_id)
        visited.add(ticket_id)

    for ticket_id in graph:
        if ticket_id not in visited:
            visit(ticket_id, [ticket_id])

    evidence_destinations = {
        ticket_id: fields.get("Expected evidence destination", "")
        for ticket_id, (_, fields, _) in contracts.items()
    }
    validate_status(root, graph, evidence_destinations, errors)


def main(root_arg: str) -> int:
    root = Path(root_arg).resolve()
    errors: list[str] = []
    if not root.is_dir():
        print(f"FAIL: package directory missing: {root}")
        return 2

    for rel in REQUIRED:
        if not (root / rel).is_file():
            fail(errors, f"missing required artifact: {rel}")

    validate_tickets(root, errors)

    markdown = sorted(root.rglob("*.md"))
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        for match in PLACEHOLDER.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            fail(errors, f"placeholder: {path.relative_to(root)}:{line}: {match.group()}")
        for raw in markdown_link_targets(text):
            target = raw.split("#", 1)[0].strip()
            if not target or re.match(r"(?:https?|mailto):", target):
                continue
            resolved = (path.parent / target).resolve()
            if root not in resolved.parents and resolved != root:
                fail(errors, f"link escapes package: {path.relative_to(root)} -> {target}")
            elif not resolved.exists():
                fail(errors, f"broken link: {path.relative_to(root)} -> {target}")

    for path in sorted((root / "references" / "diagrams").glob("*.svg")):
        try:
            xml.dom.minidom.parse(str(path))
        except Exception as exc:  # parser gives exact malformed-XML reason
            fail(errors, f"invalid SVG XML: {path.relative_to(root)}: {exc}")

    references = root / "references"
    core_reference_names = {
        "INDEX.md",
        "decisions.md",
        "validation-report.md",
        "workflow-binding.md",
        "ui-baseline.md",
    }
    tickets = references / "tickets"
    evidence = references / "evidence"
    detail_files = [
        path
        for path in markdown
        if references in path.parents
        and tickets not in path.parents
        and evidence not in path.parents
        and path.name not in core_reference_names
    ]
    index = references / "INDEX.md"
    if detail_files:
        if not index.is_file():
            fail(errors, "detail documents exist but references/INDEX.md is missing")
        else:
            index_text = index.read_text(encoding="utf-8")
            for path in detail_files:
                rel = path.relative_to(root).as_posix()
                short_rel = path.relative_to(references).as_posix()
                if rel not in index_text and short_rel not in index_text:
                    fail(errors, f"orphan detail document not listed in references/INDEX.md: {rel}")

    absorption = root / "references" / "absorption"
    if absorption.exists():
        for name in ("repo-lock.json", "license-report.md", "absorption-map.md", "source-target-map.md", "receipts/research-validation.md"):
            if not (absorption / name).is_file():
                fail(errors, f"incomplete code-absorption package: references/absorption/{name}")
        lock = absorption / "repo-lock.json"
        if lock.is_file():
            try:
                entries = json.loads(lock.read_text(encoding="utf-8"))
                if not isinstance(entries, list) or not entries:
                    raise ValueError("expected non-empty JSON array")
                source_slugs: set[str] = set()
                for pos, entry in enumerate(entries):
                    for key in ("source_slug", "url", "commit", "clone_date"):
                        if not isinstance(entry, dict) or not entry.get(key):
                            fail(errors, f"repo-lock.json[{pos}] missing {key}")
                    if not isinstance(entry, dict):
                        continue
                    slug = str(entry.get("source_slug", ""))
                    if slug in source_slugs:
                        fail(errors, f"repo-lock.json[{pos}] duplicate source_slug: {slug}")
                    source_slugs.add(slug)
                    if entry.get("commit") and not re.fullmatch(r"[0-9a-fA-F]{7,40}", str(entry["commit"])):
                        fail(errors, f"repo-lock.json[{pos}] invalid commit SHA")
                    if entry.get("archive_url") and not re.fullmatch(r"[0-9a-fA-F]{64}", str(entry.get("archive_sha256", ""))):
                        fail(errors, f"repo-lock.json[{pos}] archive requires SHA-256 digest")
                    for subpos, submodule in enumerate(entry.get("submodules", [])):
                        if not isinstance(submodule, dict) or not submodule.get("url") or not re.fullmatch(r"[0-9a-fA-F]{7,40}", str(submodule.get("commit", ""))):
                            fail(errors, f"repo-lock.json[{pos}].submodules[{subpos}] requires url + commit SHA")
            except (json.JSONDecodeError, ValueError) as exc:
                fail(errors, f"invalid repo-lock.json: {exc}")

    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"PASS: {root} ({len(markdown)} Markdown file(s))")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate-package.py <masterplan-package>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
