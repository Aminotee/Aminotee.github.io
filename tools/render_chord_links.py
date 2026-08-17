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

# Direct links to a specific chord sheet. Anything missing here falls back to
# an Ultimate Guitar search, so this map can grow one song at a time.
UG = "https://tabs.ultimate-guitar.com/tab/"
EXACT = {
    # Jazz Standards
    "Fly Me to the Moon": UG + "frank-sinatra/fly-me-to-the-moon-chords-327721",
    "Autumn Leaves": UG + "misc-traditional/autumn-leaves-chords-1966069",
    "Just the Two of Us": UG + "grover-washington-jr-/just-the-two-of-us-chords-663141",
    "What a Wonderful World": UG + "louis-armstrong/what-a-wonderful-world-chords-7427",
    "Feeling Good": UG + "nina-simone/feeling-good-chords-280078",
    "Take Five": UG + "the-dave-brubeck-quartet/take-five-chords-1196457",
    "Georgia on My Mind": UG + "ray-charles/georgia-on-my-mind-chords-1164380",
    "Sway": UG + "dean-martin/sway-quien-sera-chords-819964",
    "Ain't No Sunshine": UG + "bill-withers/aint-no-sunshine-chords-468744",
    "Back to Black": UG + "amy-winehouse/back-to-black-chords-467281",
    "Hit the Road Jack": UG + "ray-charles/hit-the-road-jack-chords-168021",
    "I've Got a Woman": UG + "ray-charles/ive-got-a-woman-chords-4356752",
    # Sentimental Classics
    "Stand By Me": UG + "ben-e-king/stand-by-me-chords-73005",
    "Knockin' on Heaven's Door": UG + "bob-dylan/knockin-on-heavens-door-chords-66587",
    "Can't Help Falling in Love": UG + "elvis-presley/cant-help-falling-in-love-chords-1086983",
    "My Heart Will Go On": UG + "celine-dion/my-heart-will-go-on-chords-14976",
    "Imagine": UG + "john-lennon/imagine-chords-9306",
    "Careless Whisper": UG + "george-michael/careless-whisper-chords-45782",
    "Ain't No Mountain High Enough":
        UG + "marvin-gaye/aint-no-mountain-high-enough-chords-660108",
    "Hotel California": UG + "eagles/hotel-california-chords-46190",
    "Can't Take My Eyes Off You":
        UG + "frankie-valli/cant-take-my-eyes-off-you-chords-439357",
    # Smooth Lounge / Modern
    "Perfect": UG + "ed-sheeran/perfect-chords-1956589",
    "City of Stars": UG + "misc-soundtrack/la-la-land-city-of-stars-chords-1860368",
    "A Thousand Years": UG + "christina-perri/a-thousand-years-chords-1101795",
    "Say Something": UG + "a-great-big-world/say-something-chords-1416487",
    "Someone Like You": UG + "adele/someone-like-you-chords-1006751",
    "Fix You": UG + "coldplay/fix-you-chords-202592",
    "Chasing Cars": UG + "snow-patrol/chasing-cars-chords-355425",
    "Stay With Me": UG + "sam-smith/stay-with-me-chords-1473600",
    "I'm Not the Only One": UG + "sam-smith/im-not-the-only-one-chords-1489018",
    "Sex, Drugs, Etc.": UG + "beach-weather/sex-drugs-etc-chords-2737914",
    "Mad About You": UG + "hooverphonic/mad-about-you-chords-827610",
    "Creep": UG + "radiohead/creep-chords-4169",
    "Wicked Game": UG + "chris-isaak/wicked-game-chords-11066",
    "Listen Before I Go": UG + "billie-eilish/listen-before-i-go-chords-2591907",
    "Happier Than Ever": UG + "billie-eilish/happier-than-ever-chords-3592094",
    "The Night We Met": UG + "lord-huron/the-night-we-met-chords-1709964",
    # Classical
    "Experience": UG + "ludovico-einaudi/experience-tabs-2027143",
    "Idea 22": UG + "gibran-alcocer/idea-22-chords-5199567",
    "Una Mattina": UG + "ludovico-einaudi/una-mattina-official-chords-2646672",
    "Je te laisserai des mots":
        UG + "patrick-watson/je-te-laisserai-des-mots-chords-1820643",
    "Mia &amp; Sebastian's Theme":
        UG + "misc-soundtrack/la-la-land-mia-and-sebastians-theme-chords-3488813",
    # Andalusian / Arabic
    "Lamma Bada Yatathanna":
        UG + "lena-chamamyan/lamma-bada-yatathanna-chords-1818953",
    "Habibi Ya Nour El Ain": "https://tabs.ultimate-guitar.com/tab/6047888",
    "Ahwak": UG + "abdel-halim-hafez/ahwak-chords-3623948",
    "Talat Daqat": UG + "misc-unsigned-bands/talat-daqat-chords-2303431",
    "Kan Enna Tahoun": UG + "fairuz/kan-enna-tahoun-chords-1832169",
    "3ahd Asdikae": "https://tabs.ultimate-guitar.com/tab/3105149",
    "Asabaka 3ichqon": "https://tabs.ultimate-guitar.com/tab/1859566",
    "Win": UG + "halim-yousfi/win-chords-3113915",
    "A Girl Within My Soul": "https://tabs.ultimate-guitar.com/tab/4168996",
    # Special Occasions
    "Smooth": UG + "santana/smooth-chords-210966",
    "Tum Hi Ho": UG + "misc-soundtrack/aashiqui-2-tum-hi-ho-chords-1244521",
    "Briya": UG + "djam/briya-chords-5746646",
    "Maak": "https://chordify.net/chords/"
            "draganov-maak-dragagalessfdar-2-mr-draganov",
    "Datni Skra": "https://www.e-chords.com/chords/khaled/detni-essekra",
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
