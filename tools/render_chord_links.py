#!/usr/bin/env python3
"""Wrap every song in index.html's repertoire with a link to its chords.

Song titles keep whatever text they already show; this only adds the anchor.
Exact tab URLs live in EXACT — anything not listed there falls back to an
Ultimate Guitar search for the song (plus artist, when the artist is a real
act rather than a generic label like "Moroccan"), which always resolves.

    python3 tools/render_chord_links.py
"""

import html
import importlib.util
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Hand-picked links. Add entries here as better ones are found.
EXACT = {
    "Georgia on My Mind":
        "https://tabs.ultimate-guitar.com/tab/ray-charles/"
        "georgia-on-my-mind-chords-1164380",
}

# Artist values that describe a style, not a performer — searching for them
# alongside the title only muddies the results.
GENERIC = {
    "Jazz Standard", "Moroccan", "Arabic", "Moroccan / Arabic", "Arabic Pop",
    "Andalusian Classic", "Your own", "Traditional", "Latin Standard",
}


def load_sets():
    spec = importlib.util.spec_from_file_location(
        "build_repertoire_pdf", ROOT / "tools" / "build_repertoire_pdf.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SETS


def chords_url(song, artist):
    song, artist = html.unescape(song), html.unescape(artist)
    if song in EXACT:
        return EXACT[song]
    terms = song if artist in GENERIC else "%s %s" % (song, artist)
    return ("https://www.ultimate-guitar.com/search.php?search_type=title"
            "&value=" + urllib.parse.quote_plus(terms))


def main():
    path = ROOT / "index.html"
    page = path.read_text(encoding="utf-8")
    head, rest = page.split('id="repertoire"', 1)
    body, tail = rest.split('id="contact"', 1)

    songs = [row for _, rows in load_sets() for row in rows]
    cursor = {"i": 0}

    def relink(match):
        label = re.sub(r"<[^>]+>", "", match.group(1)).strip()
        song, artist = songs[cursor["i"]][0], songs[cursor["i"]][1]
        cursor["i"] += 1
        return ('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>'
                % (html.escape(chords_url(song, artist), quote=True), label))

    body = re.sub(r"<li>(.*?)</li>", relink, body, flags=re.S)

    if cursor["i"] != len(songs):
        raise SystemExit("song count mismatch: html=%d data=%d"
                         % (cursor["i"], len(songs)))

    path.write_text(head + 'id="repertoire"' + body + 'id="contact"' + tail,
                    encoding="utf-8")
    print("linked %d songs (%d exact, %d search)"
          % (len(songs),
             sum(1 for s in songs if html.unescape(s[0]) in EXACT),
             sum(1 for s in songs if html.unescape(s[0]) not in EXACT)))


if __name__ == "__main__":
    main()
