#!/usr/bin/env python3
"""Refresh <lastmod> in sitemap.xml from git: the date a page's VISIBLE TEXT last changed.

    python3 build-sitemap.py          # run after build-i18n.py / build-files.py, before committing

Why visible text: commits that only touch CSS, scripts or the analytics tag (e.g. the 25 Oct 2026 beacon
change on every page) should not tell Google the content changed. Uncommitted text changes count as today.
Only <lastmod> values are rewritten; the URL list, changefreq and priority stay hand-edited.
"""
import datetime, html, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITEMAP = ROOT / "sitemap.xml"


def visible_text(src):
    src = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", src)
    src = re.sub(r"(?s)<!--.*?-->", " ", src)
    title = " ".join(re.findall(r"(?is)<title>(.*?)</title>", src))
    desc = " ".join(re.findall(r'(?i)<meta name="description" content="([^"]*)"', src))
    body = re.sub(r"(?s)<[^>]+>", " ", src)
    return re.sub(r"\s+", " ", html.unescape(title + " " + desc + " " + body)).strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def lastmod(rel):
    path = ROOT / rel
    if not path.exists():
        return None
    today = datetime.date.today().isoformat()
    revs = [l.split(" ", 1) for l in git("log", "--format=%H %cs", "--", rel).splitlines() if l]
    if not revs:
        return today
    cur = visible_text(path.read_text(encoding="utf-8"))
    head = visible_text(git("show", f"{revs[0][0]}:{rel}"))
    if cur != head:
        return today
    # walk back until the text differs from the newer revision; the newer one is the last real change
    newer_text, newer_date = head, revs[0][1]
    for h, d in revs[1:]:
        t = visible_text(git("show", f"{h}:{rel}"))
        if t != newer_text:
            return newer_date
        newer_text, newer_date = t, d
    return newer_date


def main():
    sm = SITEMAP.read_text(encoding="utf-8")
    changed = 0

    def repl(m):
        nonlocal changed
        loc, old = m.group(1), m.group(3)
        p = loc.replace("https://eraybalat.com/", "", 1)
        rel = (p + "index.html") if (p == "" or p.endswith("/")) else p
        new = lastmod(rel) or old
        if new != old:
            changed += 1
            print(f"  {loc}: {old} -> {new}")
        return m.group(0).replace(f"<lastmod>{old}</lastmod>", f"<lastmod>{new}</lastmod>")

    sm2 = re.sub(r"<loc>([^<]+)</loc>(\s*)<lastmod>([^<]+)</lastmod>", repl, sm)
    SITEMAP.write_text(sm2, encoding="utf-8")
    print(f"sitemap.xml: {changed} lastmod value(s) updated")


if __name__ == "__main__":
    sys.exit(main())
