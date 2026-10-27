"""Write the project assignments from the /tools/project-links/ page into the
front matter of publications and theses.

Usage:  python scripts/apply_project_links.py project_links.json [--dry-run]

TEMPORARY, like the page itself (PR #21): removed again before the PR is
merged. The JSON maps every entry's page_id to a project page_id or null,
e.g. {"pub:...": "projects:bambi", "thesis:...": null}. For each entry the DE
and the EN file get `projects: [<id>]` (an existing line is replaced in place,
a new one goes after `categories:` or before the closing `---`), and a null
removes the line. Unknown entry or project ids are reported and skipped;
files that already match stay as they are.
"""
import argparse, json, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COLLECTIONS = ("_publications", "_theses")


def page_id(text):
    m = re.search(r"^page_id:\s*(\S+)\s*$", text.split("---", 2)[1], re.M)
    return m.group(1) if m else None


def set_projects(text, project):
    """Replace an existing `projects:` line in place, insert one after
    `categories:` (or before the closing ---), or drop it for None."""
    _, fm, body = text.split("---", 2)
    lines = fm.split("\n")
    new = f"projects: [{project}]" if project else None
    at = next((i for i, l in enumerate(lines) if re.match(r"^projects:", l)), None)
    if at is not None:
        if new:
            lines[at] = new
        else:
            del lines[at]
    elif new:
        at = next((i + 1 for i, l in enumerate(lines) if re.match(r"^categories:", l)), None)
        if at is None:  # before the trailing empty line that precedes the closing ---
            at = len(lines) - 1 if lines and lines[-1] == "" else len(lines)
        lines.insert(at, new)
    return "---" + "\n".join(lines) + "---" + body


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("mapping", type=Path)
    ap.add_argument("--dry-run", action="store_true", help="only report what would change")
    args = ap.parse_args()

    mapping = json.loads(args.mapping.read_text(encoding="utf-8"))
    projects = {page_id(p.read_text(encoding="utf-8")) for p in (REPO / "_projects").glob("*/*.md")}

    files = {}
    for coll in COLLECTIONS:
        for path in sorted((REPO / coll).glob("*/*.md")):
            files.setdefault(page_id(path.read_text(encoding="utf-8")), []).append(path)

    changed = problems = 0
    for entry, project in mapping.items():
        if project is not None and project not in projects:
            print(f"unknown project {project!r} for {entry}", file=sys.stderr)
            problems += 1
            continue
        paths = files.get(entry)
        if not paths:
            print(f"no files for {entry}", file=sys.stderr)
            problems += 1
            continue
        for path in paths:
            old = path.read_text(encoding="utf-8")
            new = set_projects(old, project)
            if new != old:
                changed += 1
                print(f"{'would update' if args.dry_run else 'updated'} {path.relative_to(REPO)} -> {project}")
                if not args.dry_run:
                    path.write_text(new, encoding="utf-8")

    print(f"{changed} file(s) {'to change' if args.dry_run else 'changed'}, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
