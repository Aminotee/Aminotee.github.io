#!/usr/bin/env python3
"""Write the repertoire out for playlist importers.

Produces repertoire-playlist.txt (one "Artist - Title" per line) and
repertoire-playlist.csv (Title,Artist columns). Feed either to an importer
such as TuneMyMusic or Soundiiz to build the Spotify playlist — those match
the real tracks, unlike a playlist generator.

    python3 tools/build_playlist.py
"""

import csv
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
    songs = [(html.unescape(song),
              ARTIST_OVERRIDES.get(html.unescape(song), html.unescape(artist)))
             for _, rows in load_sets() for song, artist, _, _ in rows]

    txt = ROOT / "repertoire-playlist.txt"
    txt.write_text("\n".join(line(s, a) for s, a in songs) + "\n",
                   encoding="utf-8")

    csv_path = ROOT / "repertoire-playlist.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Title", "Artist"])
        writer.writerows((s, "" if a in GENERIC else a) for s, a in songs)

    print("%s + %s — %d songs" % (txt.name, csv_path.name, len(songs)))


if __name__ == "__main__":
    main()
