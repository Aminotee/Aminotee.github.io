#!/usr/bin/env python3
"""Verify the repertoire in index.html matches the data in build_repertoire_pdf.py.

    python3 tools/check_sync.py

Exits non-zero and prints the drift if the two lists disagree. The site lists
song titles only, except for a few lesser-known tracks written "Song — Artist";
both forms count as a match.
"""

import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_sets():
    spec = importlib.util.spec_from_file_location(
        "build_repertoire_pdf", ROOT / "tools" / "build_repertoire_pdf.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SETS


def unescape(text):
    return text.replace("&amp;", "&").replace("&nbsp;", " ")


def site_sets():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    section = html[html.index('id="repertoire"'):html.index('id="contact"')]
    found = re.findall(
        r'<h3>(.*?)</h3>\s*<ul>(.*?)</ul>', section, re.S)
    return [(unescape(name),
             [unescape(x) for x in re.findall(r"<li>(.*?)</li>", body)])
            for name, body in found]


def matches(site_entry, song, artist):
    """A site line matches if it is the song title, or "Song — Artist"."""
    return site_entry in (song, "%s — %s" % (song, artist))


def main():
    data, site = load_sets(), site_sets()
    drift = []

    if len(data) != len(site):
        drift.append("set count differs: pdf=%d site=%d" % (len(data), len(site)))

    for (name, rows), (site_name, entries) in zip(data, site):
        remaining = list(entries)
        for song, artist, _, _ in rows:
            song, artist = unescape(song), unescape(artist)
            hit = next((e for e in remaining if matches(e, song, artist)), None)
            if hit is None:
                drift.append("%s: missing from site — %s" % (site_name, song))
            else:
                remaining.remove(hit)
        for leftover in remaining:
            drift.append("%s: on site but not in PDF — %s"
                         % (site_name, leftover))

    total_pdf = sum(len(rows) for _, rows in data)
    total_site = sum(len(e) for _, e in site)

    if drift:
        print("OUT OF SYNC (pdf=%d, site=%d)" % (total_pdf, total_site))
        for line in drift:
            print("  -", line)
        return 1

    print("in sync — %d songs across %d sets" % (total_pdf, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
