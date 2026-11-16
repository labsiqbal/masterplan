#!/usr/bin/env python3
"""Build the self-contained HTML deck from a masterplan package.

Usage: build-deck.py <package-folder> [--theme <file.css>]

Renders masterplan.md (or VERDICT.md on a false-premise stop) plus every
package document under references/ (evidence excluded) into one offline HTML
file next to the source. Mermaid blocks become the SVGs written by
render-diagrams.py; local .md links become in-deck anchors. The theme is
references/deck-theme.css when present (CSS custom properties from §15),
else --theme, else the built-in dark theme.

Exit codes: 0 deck written and complete, 1 deck written with problems
(missing render, duplicate SVG ids, external request), 2 bad input.
Python 3 stdlib only.
"""
from __future__ import annotations

import base64
import html
import importlib.util
import mimetypes
import posixpath
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def load(name: str):
    path = Path(__file__).with_name(name)
    spec = importlib.util.spec_from_file_location(name.replace("-", "_")[:-3], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load("validate-package.py")
RENDER = load("render-diagrams.py")
slugify = VALIDATOR.heading_slug

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*([^\s`]*)")
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
HR = re.compile(r"^ {0,3}([-*_])(?:\s*\1){2,}\s*$")
LIST = re.compile(r"^(\s*)([-*+]|\d{1,9}[.)])\s+(.*)$")
QUOTE = re.compile(r"^ {0,3}> ?(.*)$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(?:\|\s*:?-{1,}:?\s*)*\|?\s*$")
SVG_ID = re.compile(r"\sid=\"([^\"]+)\"")

CSS = """
:root{--bg:#020617;--surface:#0f172a;--text:#e2e8f0;--muted:#94a3b8;--accent:#22d3ee;
--border:#1e293b;--code:#0b1222;--font:system-ui,-apple-system,"Segoe UI",sans-serif;
--mono:"JetBrains Mono",ui-monospace,monospace}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 var(--font)}
a{color:var(--accent)}
.layout{display:grid;grid-template-columns:minmax(0,1fr)}
nav{position:sticky;top:0;z-index:2;background:var(--surface);border-bottom:1px solid var(--border);padding:8px 16px;max-height:85vh;overflow-y:auto}
nav summary{cursor:pointer;font-weight:600}
nav ol{list-style:none;margin:4px 0;padding-left:12px;font-size:14px}
nav a{color:var(--text);text-decoration:none}nav a:hover,nav a:focus-visible{color:var(--accent)}
main{min-width:0;padding:0 16px 64px;max-width:960px;width:100%;margin:0 auto}
section.block{border-bottom:1px solid var(--border);padding:24px 0}
h1,h2,h3,h4{line-height:1.25;scroll-margin-top:64px}
h1{font-size:2rem}h2{font-size:1.5rem}h3{font-size:1.2rem}
code{font-family:var(--mono);font-size:.9em;background:var(--code);padding:.1em .3em;border-radius:4px}
pre{background:var(--code);border:1px solid var(--border);border-radius:8px;padding:12px;overflow-x:auto}
pre code{background:none;padding:0}
.scroll{overflow-x:auto;margin:16px 0}
table{border-collapse:collapse;min-width:100%;font-size:14px}
th,td{border:1px solid var(--border);padding:6px 10px;text-align:left;vertical-align:top}
th{background:var(--surface)}
blockquote{margin:16px 0;padding:4px 16px;border-left:3px solid var(--accent);color:var(--muted)}
figure.diagram{margin:16px 0;padding:12px;background:var(--surface);border:1px solid var(--border);border-radius:8px;overflow-x:auto}
figure.diagram svg{display:block;margin:0 auto;height:auto;max-width:100%}
li.task{list-style:none;margin-left:-1.2em}
.doc-path{color:var(--muted);font:12px var(--mono)}
@media (min-width:1100px){.layout{grid-template-columns:280px minmax(0,1fr)}
nav{height:100vh;overflow-y:auto;border-bottom:0;border-right:1px solid var(--border);padding:16px}}
"""


class Deck:
    def __init__(self, root: Path, docs: list[Path]):
        self.root = root
        self.docs = {doc.relative_to(root).as_posix(): doc for doc in docs}
        self.ids = {rel: ("mp" if rel in {"masterplan.md", "VERDICT.md"} else slugify(rel[:-3].replace("/", "-"))) for rel in self.docs}
        self.renders: dict[str, list[Path]] = {}
        for doc, _line, _text, target in RENDER.plan(root):
            self.renders.setdefault(doc.relative_to(root).as_posix(), []).append(target)
        self.problems: list[str] = []
        self.svg_ids: dict[str, str] = {}
        self.current = ""
        self.seen_slugs: dict[str, int] = {}
        self.diagram_count = 0
        self.diagram_counts: dict[str, int] = {}

    # ---- links and assets -------------------------------------------------
    def href(self, target: str) -> str:
        if re.match(r"(?:[a-z]+:|#)", target, re.I):
            if target.startswith("#"):
                return f"#{self.ids[self.current]}--{target[1:]}"
            return target
        path, _, anchor = target.partition("#")
        rel = posixpath.normpath(posixpath.join(posixpath.dirname(self.current), path))
        if rel in self.docs:
            return f"#{self.ids[rel]}--{anchor}" if anchor else f"#{self.ids[rel]}"
        return rel

    def svg(self, path: Path, origin: str) -> str:
        if not path.is_file():
            self.problems.append(f"missing diagram render {path.relative_to(self.root)} ({origin}); run render-diagrams.py")
            return ""
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", text).strip()
        clashes: dict[str, int] = {}
        for svg_id in set(SVG_ID.findall(text)):
            owner = self.svg_ids.setdefault(svg_id, path.name)
            if owner != path.name:
                clashes[owner] = clashes.get(owner, 0) + 1
        for owner, count in clashes.items():
            self.problems.append(f"{count} SVG id(s) in {path.name} also used by {owner}; re-render with render-diagrams.py")
        return text

    def image(self, alt: str, target: str) -> str:
        if re.match(r"[a-z]+:", target, re.I):
            self.problems.append(f"external image {target} in {self.current}")
            return f'<img alt="{alt}" src="{target}">'
        rel = posixpath.normpath(posixpath.join(posixpath.dirname(self.current), target))
        path = self.root / rel
        if path.suffix.lower() == ".svg":
            return f'<figure class="diagram" role="img" aria-label="{alt}">{self.svg(path, self.current)}</figure>'
        if not path.is_file():
            self.problems.append(f"missing image {rel} in {self.current}")
            return ""
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        data = base64.b64encode(path.read_bytes()).decode()
        return f'<img alt="{alt}" src="data:{mime};base64,{data}">'

    # ---- inline -----------------------------------------------------------
    def inline(self, text: str) -> str:
        codes: list[str] = []

        def stash(match: re.Match) -> str:
            codes.append(f"<code>{html.escape(match.group(2).strip())}</code>")
            return f"\x00{len(codes) - 1}\x00"

        def keep(markup: str) -> str:
            codes.append(markup)
            return f"\x00{len(codes) - 1}\x00"

        text = re.sub(r"(`+)(.+?)\1", stash, text)
        text = html.escape(text, quote=False)
        text = re.sub(
            r"!\[([^\]]*)\]\(\s*(?:&lt;)?([^\s)&]+)(?:&gt;)?(?:\s+\"[^\"]*\")?\s*\)",
            lambda m: keep(self.image(html.escape(m.group(1)), html.unescape(m.group(2)))),
            text,
        )
        text = re.sub(
            r"\[([^\]]+)\]\(\s*(?:&lt;([^\s>]+)&gt;|([^\s)]+))(?:\s+\"[^\"]*\")?\s*\)",
            lambda m: keep(f'<a href="{html.escape(self.href(html.unescape(m.group(2) or m.group(3))))}">') + m.group(1) + "</a>",
            text,
        )
        text = re.sub(r"&lt;(https?://[^\s&]+)&gt;", lambda m: keep(f'<a href="{m.group(1)}">{m.group(1)}</a>'), text)
        text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<![*\w])\*(?=\S)(.+?)(?<=\S)\*(?![*\w])", r"<em>\1</em>", text)
        text = re.sub(r"(?<!\w)_(?=\S)(.+?)(?<=\S)_(?!\w)", r"<em>\1</em>", text)
        text = re.sub(r"~~(.+?)~~", r"<del>\1</del>", text)
        return re.sub("\x00(\\d+)\x00", lambda m: codes[int(m.group(1))], text)

    # ---- blocks -----------------------------------------------------------
    def starts_block(self, lines: list[str], i: int) -> bool:
        line = lines[i]
        return bool(
            FENCE.match(line) or HEADING.match(line) or HR.match(line) or LIST.match(line) or QUOTE.match(line)
            or ("|" in line and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1]) and "-" in lines[i + 1])
        )

    def heading(self, level: int, raw: str) -> str:
        slug = slugify(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw))
        count = self.seen_slugs.get(slug, 0)
        self.seen_slugs[slug] = count + 1
        anchor = slug if count == 0 else f"{slug}-{count}"
        return f'<h{level} id="{self.ids[self.current]}--{anchor}">{self.inline(raw)}</h{level}>'

    def cells(self, line: str) -> list[str]:
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|") and not line.endswith("\\|"):
            line = line[:-1]
        return [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", line)]

    def blocks(self, lines: list[str]) -> str:
        out: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            fence = FENCE.match(line)
            if fence:
                token, lang = fence.group(1), fence.group(2).lower()
                body: list[str] = []
                i += 1
                while i < len(lines) and not re.match(rf"^ {{0,3}}{re.escape(token[0])}{{{len(token)},}}\s*$", lines[i]):
                    body.append(lines[i])
                    i += 1
                i += 1
                if lang == "mermaid":
                    out.append(self.mermaid(body))
                else:
                    cls = f' class="language-{html.escape(lang)}"' if lang else ""
                    out.append(f"<pre><code{cls}>{html.escape(chr(10).join(body))}</code></pre>")
                continue
            heading = HEADING.match(line)
            if heading:
                out.append(self.heading(len(heading.group(1)), heading.group(2)))
                i += 1
                continue
            if HR.match(line) and not LIST.match(line):
                out.append("<hr>")
                i += 1
                continue
            if "|" in line and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1]) and "-" in lines[i + 1]:
                head = self.cells(line)
                rows: list[list[str]] = []
                i += 2
                while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                    rows.append(self.cells(lines[i]))
                    i += 1
                thead = "".join(f"<th>{self.inline(cell)}</th>" for cell in head)
                tbody = "".join(
                    "<tr>" + "".join(f"<td>{self.inline(cell)}</td>" for cell in row) + "</tr>" for row in rows
                )
                out.append(f'<div class="scroll"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>')
                continue
            if QUOTE.match(line):
                quoted: list[str] = []
                while i < len(lines) and QUOTE.match(lines[i]):
                    quoted.append(QUOTE.match(lines[i]).group(1))
                    i += 1
                out.append(f"<blockquote>{self.blocks(quoted)}</blockquote>")
                continue
            if LIST.match(line):
                rendered, i = self.list_block(lines, i)
                out.append(rendered)
                continue
            para = [line.strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not self.starts_block(lines, i):
                para.append(lines[i].strip())
                i += 1
            out.append(f"<p>{self.inline(' '.join(para))}</p>")
        return "\n".join(out)

    def list_block(self, lines: list[str], i: int) -> tuple[str, int]:
        first = LIST.match(lines[i])
        base = len(first.group(1).expandtabs(4))
        ordered = first.group(2)[0].isdigit()
        items: list[str] = []
        while i < len(lines):
            match = LIST.match(lines[i])
            if not match or len(match.group(1).expandtabs(4)) != base or match.group(2)[0].isdigit() != ordered:
                break
            content_indent = base + len(match.group(2)) + 1
            item = [match.group(3)]
            loose = False
            i += 1
            while i < len(lines):
                line = lines[i]
                indent = len(line.expandtabs(4)) - len(line.expandtabs(4).lstrip())
                if not line.strip():
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    nxt = lines[j] if j < len(lines) else ""
                    if nxt and len(nxt.expandtabs(4)) - len(nxt.expandtabs(4).lstrip()) > base:
                        item.append("")
                        loose = True
                        i += 1
                        continue
                    break
                if indent > base:
                    item.append(line.expandtabs(4)[min(indent, content_indent):])
                    i += 1
                    continue
                if self.starts_block(lines, i):
                    break
                item.append(line.strip())
                i += 1
            task = re.match(r"\[([ xX])\]\s+(.*)", item[0])
            cls = ""
            if task:
                checked = " checked" if task.group(1) != " " else ""
                item[0] = task.group(2)
                cls = ' class="task"'
            body = self.blocks(item)
            if not loose and body.startswith("<p>"):
                body = re.sub(r"^<p>(.*?)</p>", r"\1", body, count=1, flags=re.S)
            if task:
                body = f'<input type="checkbox" disabled{checked} aria-label="done"> {body}'
            items.append(f"<li{cls}>{body}</li>")
        tag = "ol" if ordered else "ul"
        return f"<{tag}>{''.join(items)}</{tag}>", i

    def mermaid(self, body: list[str]) -> str:
        renders = self.renders.get(self.current, [])
        index = self.diagram_counts.get(self.current, 0)
        self.diagram_counts[self.current] = index + 1
        if index >= len(renders):
            self.problems.append(f"Mermaid block {index + 1} in {self.current} has no render")
            return f"<pre><code>{html.escape(chr(10).join(body))}</code></pre>"
        self.diagram_count += 1
        svg = self.svg(renders[index], self.current)
        if not svg:
            return f"<pre><code>{html.escape(chr(10).join(body))}</code></pre>"
        return f'<figure class="diagram">{svg}</figure>'

    # ---- document ---------------------------------------------------------
    def render_doc(self, rel: str) -> tuple[str, list[tuple[int, str, str]]]:
        self.current = rel
        self.seen_slugs = {}
        text = self.docs[rel].read_text(encoding="utf-8")
        body = self.blocks(text.splitlines())
        toc = [
            (int(level[1]), anchor, re.sub(r"<[^>]+>", "", label))
            for level, anchor, label in re.findall(r'<(h[1-3]) id="([^"]+)">(.*?)</h[1-3]>', body)
        ]
        return body, toc


def main(argv: list[str]) -> int:
    if not argv or not Path(argv[0]).is_dir():
        print(__doc__)
        return 2
    root = Path(argv[0]).resolve()
    source = root / "masterplan.md"
    if not source.is_file():
        source = root / "VERDICT.md"
    if not source.is_file():
        print("FAIL: neither masterplan.md nor VERDICT.md found")
        return 2
    theme = root / "references" / "deck-theme.css"
    if "--theme" in argv:
        theme = Path(argv[argv.index("--theme") + 1])
    evidence = root / "references" / "evidence"
    docs = [source] + sorted(
        path for path in (root / "references").rglob("*.md") if evidence not in path.parents
    ) if (root / "references").is_dir() else [source]
    deck = Deck(root, docs)

    sections: list[str] = []
    nav: list[str] = []
    main_body, main_toc = deck.render_doc(source.name)
    title = next((label for level, _a, label in main_toc if level == 1), source.stem)
    sections.append(f'<section class="block" id="mp">{main_body}</section>')
    nav.append("<li><strong>" + html.escape(title) + "</strong><ol>" + "".join(
        f'<li><a href="#{anchor}">{label}</a></li>' for level, anchor, label in main_toc if level == 2
    ) + "</ol></li>")

    groups: dict[str, list[str]] = {}
    for rel in deck.docs:
        if rel == source.name:
            continue
        body, toc = deck.render_doc(rel)
        label = next((text for level, _a, text in toc if level == 1), rel)
        sections.append(
            f'<section class="block" id="{deck.ids[rel]}"><p class="doc-path">{html.escape(rel)}</p>{body}</section>'
        )
        group = posixpath.dirname(rel) or "."
        groups.setdefault(group, []).append(f'<li><a href="#{deck.ids[rel]}">{label}</a></li>')
    for group, links in groups.items():
        nav.append(f"<li><strong>{html.escape(group)}/</strong><ol>{''.join(links)}</ol></li>")

    css = CSS + ("\n" + theme.read_text(encoding="utf-8") if theme.is_file() else "")
    page = (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{html.escape(title)}</title><style>{css}</style></head><body><div class=\"layout\">"
        f"<nav aria-label=\"Contents\"><details id=\"toc\"><summary>Contents</summary><ol>{''.join(nav)}</ol></details></nav>"
        f"<main>{''.join(sections)}</main></div>"
        "<script>if(matchMedia('(min-width:1100px)').matches)document.getElementById('toc').open=true;"
        "document.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>{"
        "if(!matchMedia('(min-width:1100px)').matches)document.getElementById('toc').open=false}))</script>"
        "</body></html>\n"
    )
    external = sorted(set(re.findall(r"(?:src|href)=\"(https?://[^\"]+)\"", page)) - set(
        re.findall(r"<a href=\"(https?://[^\"]+)\"", page)
    ))
    for url in external:
        deck.problems.append(f"external request: {url}")
    if re.search(r"@import|url\(\s*['\"]?https?:", css):
        deck.problems.append("theme loads an external resource (@import or remote url())")

    target = root / f"{source.stem}.html"
    target.write_text(page, encoding="utf-8")
    print(f"{target.relative_to(root)}: {len(page) // 1024} KB, {len(deck.docs)} document(s), {deck.diagram_count} diagram(s)")
    for problem in deck.problems:
        print(f"FAIL: {problem}")
    print("PASS: deck built" if not deck.problems else f"FAIL: {len(deck.problems)} problem(s)")
    return 1 if deck.problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
