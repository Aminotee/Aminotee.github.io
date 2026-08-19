#!/usr/bin/env python3
"""Write repertoire-playlist.txt — one "Artist - Title" per line.

Paste the file into a playlist importer (TuneMyMusic, Soundiiz, Spotlistr…)
to turn the repertoire into a Spotify playlist.

    python3 tools/build_playlist.py
"""

import html
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Artists listed as a style rather than a performer: search the title alone.
GENERIC = {
    "Jazz Standard", "Moroccan", "Arabic", "Moroccan / Arabic", "Arabic Pop",
    "Andalusian Classic", "Your own", "Traditional", "Latin Standard",
}

# Where the repertoire credits differ from the recording to search for.
ARTIST_OVERRIDES = {
    "Just the Two of Us": "Grover Washington Jr.",
    "Knockin' on Heaven's Door": "Bob Dylan",
    "Mia & Sebastian's Theme": "Justin Hurwitz",
    "Idea 22": "Gibran Alcocer",       # not Einaudi, despite the PDF credit
    "Datni Skra": "Khaled",
    "Kan Enna Tahoun": "Fairuz",
}


def load_sets():
    spec = importlib.util.spec_from_file_location(
        "build_repertoire_pdf", ROOT / "tools" / "build_repertoire_pdf.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SETS


def line(song, artist):
    song, artist = html.unescape(song), html.unescape(artist)
    artist = ARTIST_OVERRIDES.get(song, artist)
    return song if artist in GENERIC else "%s - %s" % (artist, song)


def main():
    lines = [line(song, artist)
             for _, rows in load_sets() for song, artist, _, _ in rows]
    out = ROOT / "repertoire-playlist.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("%s — %d songs" % (out.name, len(lines)))


if __name__ == "__main__":
    main()
