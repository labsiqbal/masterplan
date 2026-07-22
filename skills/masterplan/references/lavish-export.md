# Lavish Export Playbook

The package doubles as a **presentation**. lavish-axi owns the visual layer: interactive review during the gates and the final portable artifact.

- `masterplan.md` → `masterplan.html` (via `lavish-axi export`)
- `VERDICT.md` → `VERDICT.html` (same treatment, on a false-premise stop)

The Markdown stays the single source of truth — the HTML is a render of it, regenerated whenever it changes (revise mode step 6). Never hand-edit the export as the master.

## The flow

1. **Author the artifact HTML** driven by the masterplan's §15 Design direction — lavish injects no design system, so the deck previews the product's own look, not a generic theme.
2. **Open it for review:** `lavish-axi <file>` — the reviewer reads, annotates, and sketches on it during Gates A/B/C. (If the bare `lavish-axi` bin is absent, every command here runs as `npx -y lavish-axi ...`.)
3. **Collect feedback:** `lavish-axi poll <file>` — annotations come back as prompts; whiteboard edits come back as a whiteboard prompt. This is a **long-poll with a discipline**, not a one-shot check:
   - It stays **silent until the user acts** (feedback, session end, or a browser-proven severe layout failure). Silence is normal - never read it as "no feedback" and move on.
   - Run it in the **foreground** and let it return feedback directly. Background polling only via a harness-native tracked facility that notifies this same agent on completion - never `nohup`, shell `&`, or any fire-and-forget.
   - If the poll is **killed or times out** (harness command timeouts will do this), just **re-run it** - queued feedback is never lost. Keep re-running until feedback arrives or the user ends the session.
   - On the first poll, prefer `--agent-reply "<one-line summary of what to review>"` so the reviewer's panel opens with context; after applying feedback, poll again with `--agent-reply` to keep the loop going.
   - "Send & End" delivers its final feedback once; after that, stop polling and do not reopen the session uninvited.
4. **Ship:** `lavish-axi export` writes the portable self-contained HTML next to the Markdown; `lavish-axi share` optionally produces a link.

## Diagrams

Author diagrams as **Mermaid** in `.mermaid` containers so lavish converts them to **editable Excalidraw whiteboards** — a reviewer redraws the flow instead of describing the change. Every type the template uses (flowchart, erDiagram, sequenceDiagram) converts.

## Without lavish

On a runtime without lavish-axi, skip this file entirely: the text package is complete on its own, and Mermaid sources render natively on GitHub and most Markdown viewers. Rich HTML export is simply unavailable there — say so honestly rather than hand-rolling a substitute pipeline.
