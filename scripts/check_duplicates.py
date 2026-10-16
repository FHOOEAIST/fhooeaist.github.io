"""Duplicate check for _publications and _theses.

Usage:  python scripts/check_duplicates.py [--base origin/main]

Always checks (both collections, both languages):
  - every page_id exists exactly once per language, in both de/ and en/
  - permalinks are unique per language
  - no DOI / external_url is shared by several entries (hint only)
  - no two English titles are near-identical (hint only)
With --base, the entries added since that git ref are additionally compared
against all older ones by shared authors and title keywords, which catches the
same work listed under a different title.

Exit code 1 if a page_id or permalink problem is found; the other findings are
hints that need a human look (e.g. a workshop paper and its later journal
version are legitimately separate entries).
"""
import argparse, difflib, re, subprocess, sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COLLECTIONS = ("_publications", "_theses")
STOP = set("a an the of for in on and with using to from by via based its towards toward into at as".split())


def front(path):
    """Minimal front-matter reader (flat keys, folded continuation lines)."""
    fm = path.read_text(encoding="utf-8").split("---", 2)[1]
    data, key = {}, None
    for line in fm.splitlines():
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            data[key] = m.group(2)
        elif key and line.startswith(" "):
            data[key] += " " + line.strip()
    for k, v in data.items():
        v = re.sub(r"\s+#.*$", "", v).strip()
        if len(v) > 1 and v[0] == v[-1] and v[0] in "'\"":
            v = v[1:-1]
        data[k] = v
    return data


def norm(title):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9äöüß ]+", " ", title.lower())).strip()


def words(title):
    return {w for w in re.findall(r"[a-zäöüß0-9]+", title.lower()) if w not in STOP and len(w) > 2}


def authors(e):
    """Surnames from `reference` ("Lastname X., …" before the quoted title) or the thesis `student`."""
    head = re.split(r"[“„\"]", e.get("reference", ""))[0]
    names = {w.lower() for w in re.findall(r"([A-ZÄÖÜ][a-zäöüßčě]+)(?=\s+[A-Z]\.)", head)}
    if e.get("student"):
        names.add(e["student"].split()[-1].lower())
    return names


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="git ref; compare entries added since then against older ones")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    entries = []
    for coll in COLLECTIONS:
        for lang in ("de", "en"):
            for p in sorted((REPO / coll / lang).glob("*.md")):
                entries.append({"coll": coll, "lang": lang, "path": f"{coll}/{lang}/{p.name}", **front(p)})

    errors = hints = 0

    by_id = defaultdict(list)
    for e in entries:
        by_id[(e["coll"], e.get("page_id"))].append(e["lang"])
    for (coll, pid), langs in sorted(by_id.items(), key=str):
        if sorted(langs) != ["de", "en"]:
            errors += 1
            print(f"ERROR page_id {coll} {pid}: found in {sorted(langs)}")

    by_link = defaultdict(list)
    for e in entries:
        if e.get("permalink"):
            by_link[(e["lang"], e["permalink"])].append(e["path"])
    for (lang, link), paths in by_link.items():
        if len(paths) > 1:
            errors += 1
            print(f"ERROR permalink {link} used by {paths}")

    en = [e for e in entries if e["lang"] == "en"]
    for field in ("doi", "external_url"):
        seen = defaultdict(list)
        for e in en:
            if e.get(field):
                seen[e[field].lower().rstrip("/")].append(e["path"])
        for value, paths in seen.items():
            if len(paths) > 1:
                hints += 1
                print(f"HINT  same {field} {value}:\n      " + "\n      ".join(paths))

    for a, b in combinations(en, 2):
        ratio = difflib.SequenceMatcher(None, norm(a.get("title", "")), norm(b.get("title", ""))).ratio()
        if ratio >= 0.8:
            hints += 1
            print(f"HINT  similar titles ({ratio:.2f}):\n      {a['path']}\n      {b['path']}")

    if args.base:
        added = set(subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=A", f"{args.base}...HEAD", "--",
             *(f"{c}/en" for c in COLLECTIONS)],
            cwd=REPO, capture_output=True, text=True, check=True).stdout.split())
        new = [e for e in en if e["path"] in added]
        old = [e for e in en if e["path"] not in added]
        print(f"\nComparing {len(new)} entries added since {args.base} against {len(old)} older ones")
        for n in new:
            nw, na, ny = words(n.get("title", "")), authors(n), int(n["date"][:4])
            for o in old:
                ow = words(o.get("title", ""))
                jac = len(nw & ow) / max(1, len(nw | ow))
                shared = na & authors(o)
                if abs(int(o["date"][:4]) - ny) <= 2 and ((jac >= 0.3 and shared) or jac >= 0.5):
                    hints += 1
                    print(f"HINT  possible same work (title overlap {jac:.2f}, shared authors {sorted(shared)}):\n"
                          f"      new {n['path']}\n      old {o['path']}")

    print(f"\n{len(entries)} files checked: {errors} error(s), {hints} hint(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
