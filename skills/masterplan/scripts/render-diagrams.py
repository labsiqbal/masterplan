#!/usr/bin/env python3
"""Render a package's Mermaid blocks to SVG files for the HTML deck.

Usage: render-diagrams.py <package-folder> [--dry-run]

masterplan.md block n under "## 7." becomes references/diagrams/s7-<n>.svg;
a block in any other document becomes <document-path-slug>-<n>.svg.
--dry-run prints the mapping without rendering.

Exit codes: 0 rendered (or dry run), 1 a block failed to render,
2 no Mermaid renderer available (hand-author the deck SVGs instead).
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MERMAID_CLI = "@mermaid-js/mermaid-cli@11.4.2"
BROWSERS = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
SECTION = re.compile(r"^##\s+(\d+)\.")


def load_validator():
    path = Path(__file__).with_name("validate-package.py")
    spec = importlib.util.spec_from_file_location("validate_package", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plan(root: Path) -> list[tuple[Path, int, str, Path]]:
    """(source document, opening line, Mermaid text, target SVG) per block."""
    blocks = load_validator().mermaid_blocks
    out_dir = root / "references" / "diagrams"
    jobs: list[tuple[Path, int, str, Path]] = []
    for doc in sorted(root.rglob("*.md")):
        text = doc.read_text(encoding="utf-8")
        lines = text.splitlines()
        counters: dict[str, int] = {}
        for line, body, _closed in blocks(text):
            if doc == root / "masterplan.md":
                section = "s0"
                for heading in reversed(lines[: line - 1]):
                    match = SECTION.match(heading)
                    if match:
                        section = f"s{match.group(1)}"
                        break
                prefix = section
            else:
                prefix = re.sub(r"[^a-z0-9]+", "-", doc.relative_to(root).with_suffix("").as_posix().lower()).strip("-")
            counters[prefix] = counters.get(prefix, 0) + 1
            target = out_dir / f"{prefix}-{counters[prefix]}.svg"
            jobs.append((doc, line, "\n".join(body) + "\n", target))
    return jobs


def renderer() -> tuple[list[str], dict[str, str]] | None:
    env = dict(os.environ)
    if "PUPPETEER_EXECUTABLE_PATH" not in env:
        browser = next((shutil.which(name) for name in BROWSERS if shutil.which(name)), None)
        if browser:
            env["PUPPETEER_EXECUTABLE_PATH"] = browser
    if shutil.which("mmdc"):
        return ["mmdc"], env
    if shutil.which("npx"):
        return ["npx", "-y", MERMAID_CLI], env
    return None


def main(argv: list[str]) -> int:
    if not argv or not Path(argv[0]).is_dir():
        print(__doc__)
        return 2
    root = Path(argv[0]).resolve()
    jobs = plan(root)
    for doc, line, _text, target in jobs:
        print(f"{doc.relative_to(root)}:{line} -> {target.relative_to(root)}")
    if "--dry-run" in argv or not jobs:
        return 0
    found = renderer()
    if found is None:
        print("NO RENDERER: install Node (npx) or mermaid-cli (mmdc)")
        return 2
    command, env = found
    failures = 0
    with tempfile.TemporaryDirectory() as scratch:
        config = Path(scratch) / "puppeteer.json"
        config.write_text(json.dumps({"args": ["--no-sandbox"]}), encoding="utf-8")
        for doc, line, text, target in jobs:
            source = Path(scratch) / "diagram.mmd"
            source.write_text(text, encoding="utf-8")
            target.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(
                [*command, "-i", str(source), "-o", str(target), "-t", "dark", "-b", "transparent", "-p", str(config)],
                env=env,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0 or not target.is_file():
                failures += 1
                output = (result.stderr or result.stdout).strip().splitlines()
                reason = next((entry.strip() for entry in output if "rror" in entry), output[-1] if output else "no output")
                print(f"FAIL: {doc.relative_to(root)}:{line}: {reason}")
    print("PASS: diagrams rendered" if not failures else f"FAIL: {failures} diagram(s) did not render")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
