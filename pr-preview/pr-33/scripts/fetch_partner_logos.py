#!/usr/bin/env python3
"""Crawl the logos of the project partners in _data/partners.yml.

For every partner with a `url` but no `logo`, the start page is fetched and
the most likely logo is picked, in this order:

  1. an <img> or inline <svg> inside <header>/<nav> whose src, class, id or
     alt mentions "logo" (or "brand")
  2. any such <img>/<svg> on the page
  3. the apple-touch-icon / largest icon link (square, last resort)

The file is saved to assets/images/partners/<slug>.<ext> and a `logo:` line
is added below the partner's `url:` in _data/partners.yml (the rest of the
file, comments included, is left as is). Check every logo by eye before
committing: crawling can pick a wrong image, and logos are trademarks (see
issue #19).

Usage (from the repository root, needs network access, standard library only):

    python3 scripts/fetch_partner_logos.py            # all partners without logo
    python3 scripts/fetch_partner_logos.py --force    # re-fetch existing ones too
    python3 scripts/fetch_partner_logos.py --only "karriere.at"
"""

import argparse
import html.parser
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data" / "partners.yml"
OUT = ROOT / "assets" / "images" / "partners"
WEB_PATH = "/assets/images/partners/"
UA = "Mozilla/5.0 (X11; Linux x86_64) AIST-website logo crawler"
TYPES = {
    "image/svg+xml": "svg",
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/webp": "webp",
    "image/gif": "gif",
}
LOGO_RE = re.compile(r"logo|brand", re.I)


def slugify(name):
    s = name.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("&", "and")):
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


def fetch(url):
    # Percent-encode non-ASCII characters (e.g. "logo_weiß.png"), keep the rest.
    url = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~")
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.geturl(), r.headers.get_content_type(), r.read()


class LogoFinder(html.parser.HTMLParser):
    """Collects (score, kind, value) candidates; higher score wins."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.candidates = []
        self.depth_header = 0
        self.svg = None  # [score, depth, chunks] while inside a logo <svg>

    def _attrs_text(self, attrs):
        return " ".join(v or "" for k, v in attrs if k in ("src", "class", "id", "alt", "href", "aria-label", "title", "data-src"))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("header", "nav"):
            self.depth_header += 1
        if self.svg is not None:
            self.svg[1] += 1
            self.svg[2].append(self.get_starttag_text() or "")
            return
        text = self._attrs_text(attrs)
        bonus = 10 if self.depth_header else 0
        if tag == "img":
            src = a.get("src") or a.get("data-src") or ""
            if src and not src.startswith("data:") and LOGO_RE.search(text):
                self.candidates.append((20 + bonus, "url", src))
        elif tag == "svg" and LOGO_RE.search(text):
            self.svg = [20 + bonus + 1, 1, [self.get_starttag_text() or ""]]
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            href = a.get("href")
            if href and "apple-touch-icon" in rel:
                self.candidates.append((5, "url", href))
            elif href and "icon" in rel and (href.endswith(".svg") or "192" in (a.get("sizes") or "")):
                self.candidates.append((4, "url", href))

    def handle_startendtag(self, tag, attrs):
        was_in_svg = self.svg is not None
        self.handle_starttag(tag, attrs)
        if self.svg is None:
            return
        if was_in_svg:
            self.svg[1] -= 1  # self-closing child: no end tag follows
        else:
            self.svg = None  # empty <svg/>: nothing to save

    def handle_endtag(self, tag):
        if tag in ("header", "nav") and self.depth_header:
            self.depth_header -= 1
        if self.svg is not None:
            self.svg[2].append(f"</{tag}>")
            self.svg[1] -= 1
            if self.svg[1] == 0:
                markup = "".join(self.svg[2])
                if "xmlns" not in markup.split(">", 1)[0]:
                    markup = markup.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
                self.candidates.append((self.svg[0], "svg", markup))
                self.svg = None

    def handle_data(self, data):
        if self.svg is not None:
            self.svg[2].append(data)


def find_logo(url):
    base, ctype, body = fetch(url)
    finder = LogoFinder()
    finder.feed(body.decode("utf-8", "replace"))
    # Stable sort: the first candidate of the best score wins.
    for score, kind, value in sorted(finder.candidates, key=lambda c: -c[0]):
        if kind == "svg":
            return "svg", value.encode("utf-8")
        try:
            _, ctype, data = fetch(urllib.parse.urljoin(base, value))
        except Exception as e:  # try the next candidate
            print(f"    skip {value}: {e}", file=sys.stderr)
            continue
        ext = TYPES.get(ctype) or Path(urllib.parse.urlparse(value).path).suffix.lstrip(".").lower()
        if ext in TYPES.values() and len(data) > 200:
            return ext, data
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="re-fetch partners that already have a logo")
    ap.add_argument("--only", help="only the partner with this name")
    args = ap.parse_args()

    lines = DATA.read_text(encoding="utf-8").splitlines(keepends=True)
    # Parse the simple "- name: / url: / logo:" list by hand so comments survive.
    entries, cur = [], None
    for i, line in enumerate(lines):
        m = re.match(r"- name:\s*(.+?)\s*$", line)
        if m:
            cur = {"name": m.group(1), "line": i}
            entries.append(cur)
            continue
        m = re.match(r"\s+(url|logo):\s*(.+?)\s*$", line)
        if cur and m:
            cur[m.group(1)] = m.group(2)
            cur[m.group(1) + "_line"] = i

    OUT.mkdir(parents=True, exist_ok=True)
    inserts, replaces, failed = {}, {}, []
    for e in entries:
        if "url" not in e or (args.only and e["name"] != args.only):
            continue
        if "logo" in e and not args.force:
            continue
        print(f"{e['name']}  <{e['url']}>")
        try:
            found = find_logo(e["url"])
        except Exception as ex:
            found = None
            print(f"    error: {ex}", file=sys.stderr)
        if not found:
            failed.append(e["name"])
            continue
        ext, data = found
        fname = f"{slugify(e['name'])}.{ext}"
        (OUT / fname).write_bytes(data)
        print(f"    -> {WEB_PATH}{fname} ({len(data)} bytes)")
        if "logo_line" in e:
            replaces[e["logo_line"]] = f"  logo: {WEB_PATH}{fname}\n"
        else:
            inserts[e["url_line"]] = f"  logo: {WEB_PATH}{fname}\n"

    out = []
    for i, line in enumerate(lines):
        out.append(replaces.get(i, line))
        if i in inserts:
            out.append(inserts[i])
    DATA.write_text("".join(out), encoding="utf-8")

    if failed:
        print("\nNo logo found (add one by hand):\n  " + "\n  ".join(failed))
    print("\nReview the files in assets/images/partners/ before committing.")


if __name__ == "__main__":
    main()
