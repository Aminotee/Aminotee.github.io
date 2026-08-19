#!/usr/bin/env python3
"""Regenerate hotel_piano_repertoire.pdf from the song data below.

The repertoire lives here as the single source of truth: edit SETS, run this
script, and update the matching list in index.html so the two stay in sync.

    python3 tools/build_repertoire_pdf.py
"""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

# ---------------------------------------------------------------- palette ---
INK = colors.HexColor("#1A1A2E")
GREY = colors.HexColor("#555555")
TEAL = colors.HexColor("#085041")
MINT = colors.HexColor("#E1F5EE")
RULE = colors.HexColor("#DDDDDD")
HEAD_BG = colors.HexColor("#F5F5F5")
HEAD_INK = colors.HexColor("#000444")
ALT_BG = colors.HexColor("#FAFAFA")

LEVEL = {
    "Easy": (colors.HexColor("#EAF3DE"), colors.HexColor("#3B6D11")),
    "Medium": (colors.HexColor("#FAEEDA"), colors.HexColor("#854F0B")),
    "Advanced": (colors.HexColor("#FAECE7"), colors.HexColor("#993C1D")),
}

BULLET = '<font face="ZapfDingbats">n</font>'

# ------------------------------------------------------------------- data ---
# (song, artist, notes, level)
SETS = [
    ("Jazz Standards", [
        ("Fly Me to the Moon", "Frank Sinatra",
         "Perfect opener — guests recognize it in 2 seconds.", "Easy"),
        ("Autumn Leaves", "Jazz Standard",
         "Minor key, melancholic. Great for quieter moments.", "Easy"),
        ("Just the Two of Us", "Bill Withers / Grover Washington Jr.",
         "Smooth and warm. Sophisticated groove that fits perfectly in a hotel lounge.", "Easy"),
        ("Feeling Good", "Nina Simone",
         "Powerful mid-set moment. Build dynamics gradually.", "Medium"),
        ("Take Five", "Dave Brubeck",
         "Iconic 5/4 groove. Even non-jazz fans recognize it.", "Medium"),
        ("Georgia on My Mind", "Ray Charles",
         "Soulful and slow. Stunning as a solo piano ballad.", "Easy"),
        ("Sway", "Dean Martin",
         "Elegant Latin-infused swing. Perfect for a lively moment in the set.", "Easy"),
        ("Ain't No Sunshine", "Bill Withers",
         "Soulful and slow. One of the most emotional jazz-blues pieces you can play.", "Easy"),
        ("Back to Black", "Amy Winehouse",
         "Dark, soulful groove. Modern classic that sits beautifully in a lounge.", "Medium"),
        ("Hit the Road Jack", "Ray Charles",
         "Upbeat and fun — lifts the energy instantly. Great contrast after a ballad.", "Easy"),
        ("Dancing in Wartime", "Miles Laroque",
         "Cool and laid-back. Smooth mid-tempo feel.", "Medium"),
        ("I've Got a Woman", "Ray Charles",
         "Gospel-influenced groove. Energetic and joyful — crowd pleaser.", "Easy"),
        ("Careless Whisper", "George Michael",
         "Iconic melody. Never fails to get a reaction.", "Easy"),
    ]),
    ("Sentimental Classics", [
        ("Stand By Me", "Ben E. King",
         "Simple chord loop, iconic melody. Slows beautifully.", "Easy"),
        ("Knockin' on Heaven's Door", "Bob Dylan / Guns N' Roses",
         "Simple and deeply moving. Guests always recognize it.", "Easy"),
        ("Can't Help Falling in Love", "Elvis Presley",
         "Waltz (3/4). One of the best solo piano hotel songs.", "Easy"),
        ("Imagine", "John Lennon",
         "Simple and profound. Always lands perfectly.", "Easy"),
        ("Ain't No Mountain High Enough", "Marvin Gaye &amp; Tammi Terrell",
         "Joyful and uplifting. Great energy shift in a set.", "Easy"),
        ("Hotel California", "Eagles",
         "Instantly recognizable intro. Guests always react to this one.", "Medium"),
        ("Can't Take My Eyes Off You", "Frankie Valli",
         "Joyful and uplifting. Guests love the energy of this classic.", "Easy"),
        ("What a Wonderful World", "Louis Armstrong",
         "Warm and universally loved — tourists adore this one.", "Easy"),
        ("I'm Not the Only One", "Sam Smith",
         "Slow soul groove. Warm and easy to sing along to.", "Easy"),
    ]),
    ("Smooth Lounge / Modern", [
        ("Perfect", "Ed Sheeran",
         "Every couple loves this — works brilliantly as solo piano.", "Easy"),
        ("City of Stars", "La La Land",
         "Film fans will recognize and appreciate it.", "Easy"),
        ("A Thousand Years", "Christina Perri",
         "Romantic and flowing. Very popular request.", "Easy"),
        ("Say Something", "A Great Big World",
         "Sparse and emotional — effective as a quiet moment.", "Easy"),
        ("Someone Like You", "Adele",
         "Powerful ballad that draws attention in a room.", "Easy"),
        ("Fix You", "Coldplay",
         "Builds from quiet to powerful — great set arc.", "Medium"),
        ("Chasing Cars", "Snow Patrol",
         "Minimal and dreamy. Works as soft background music.", "Easy"),
        ("Stay With Me", "Sam Smith",
         "Simple gospel-influenced ballad. Very recognizable.", "Easy"),
        ("Sex, Drugs, Etc.", "Beach Weather",
         "Moody and cool. Younger guests love the vibe of this one.", "Easy"),
        ("Mad About You", "Hooverphonic",
         "Cinematic and dreamy. Elegant slow-burn lounge feel.", "Easy"),
        ("Creep", "Radiohead",
         "Hauntingly emotional. Solo piano version is stunning and unexpected.", "Easy"),
        ("Wicked Game", "Chris Isaak",
         "Dark and seductive. One of the most atmospheric solo piano songs.", "Easy"),
        ("Listen Before I Go", "Billie Eilish",
         "Sparse and haunting. A striking quiet moment late in the set.", "Easy"),
        ("Happier Than Ever", "Billie Eilish",
         "Starts gentle, then builds — a great dynamic arc on solo piano.", "Medium"),
        ("The Night We Met", "Lord Huron",
         "Melancholic and hypnotic. Younger guests recognize it instantly.", "Easy"),
    ]),
    ("Classical", [
        ("Experience", "Ludovico Einaudi",
         "Minimal contemporary classical. Sophisticated atmosphere.", "Medium"),
        ("Idea 22", "Ludovico Einaudi",
         "Gentle and repetitive. Quietly mesmerizing for a lounge.", "Easy"),
        ("Only If I Could Tell", "Ludovico Einaudi",
         "Tender and introspective. Beautiful slow-burn piece.", "Easy"),
        ("Una Mattina", "Ludovico Einaudi",
         "One of Einaudi's most beloved pieces. Guests always respond.", "Easy"),
        ("Valse Sentimentale", "Tchaikovsky",
         "Elegant waltz. Romantic and timeless — a true classic.", "Medium"),
        ("Je te laisserai des mots", "Patrick Watson",
         "Delicate and poetic. French title adds a sophisticated touch.", "Easy"),
        ("Solas", "Joep Beving",
         "Deeply meditative. Perfect for creating a peaceful atmosphere.", "Medium"),
        ("Mia &amp; Sebastian's Theme", "La La Land / Justin Hurwitz",
         "Iconic film piano piece. Instantly recognizable and romantic.", "Easy"),
    ]),
    ("Andalusian / Arabic", [
        ("Lamma Bada Yatathanna", "Andalusian Classic",
         "Most iconic muwashshah. Stops people in their tracks.", "Medium"),
        ("Habibi Ya Nour El Ain", "Amr Diab",
         "Modern and lighter. Moroccan guests love this one.", "Easy"),
        ("Ahwak", "Abdel Halim Hafez",
         "Egyptian classic. Slow, romantic, and instantly familiar.", "Medium"),
        ("Kan Enna Tahoun", "Moroccan / Arabic",
         "Nostalgic and deeply Moroccan. Guests will feel at home.", "Medium"),
        ("Talat Daqat", "Arabic Pop",
         "Modern Arabic hit. Younger Moroccan guests love this.", "Easy"),
        ("3ahd Asdikae", "Arabic",
         "Warm and sentimental. Evokes nostalgia in Arab audiences.", "Medium"),
        ("Win", "Halim Yousfi",
         "Poetic and emotional. A beautiful slow lounge arrangement.", "Medium"),
        ("Diroulha Laaka / Nti Sbabi", "Moroccan",
         "Two beloved Moroccan classics — pair them as a medley.", "Easy"),
        ("A Girl Within My Soul", "Yanni",
         "Cinematic and orchestral feel. Impresses on solo piano.", "Medium"),
        ("Asabaka 3ichqon", "Arabic",
         "Romantic and flowing. Resonates deeply with Arab guests.", "Easy"),
    ]),
    ("Special Occasions", [
        ("Smooth", "Santana ft. Rob Thomas",
         "Instantly recognizable. Brings a warm Latin groove to the set.", "Medium"),
        ("Tum Hi Ho", "Arijit Singh",
         "Beloved Bollywood ballad. Indian guests will love it — very emotional.", "Easy"),
        ("Kan Kitshabhoum", "Shayfeen",
         "Popular Moroccan song. Local guests will light up hearing this.", "Easy"),
        ("Brm Brm Brm", "Moroccan",
         "Fun and energetic Moroccan track. Great mood lifter.", "Easy"),
        ("Maak", "Draganov",
         "Bold and recognizable. Local crowd will love it.", "Easy"),
        ("Briya", "Djam",
         "Smooth and modern Moroccan sound. Great crowd pleaser.", "Easy"),
        ("Datni Skra", "Moroccan",
         "Energetic and fun. Gets the room going instantly.", "Easy"),
    ]),
]

# ----------------------------------------------------------------- styles ---
title = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=22,
                       leading=26, textColor=INK, alignment=TA_CENTER)
subtitle = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=11,
                          leading=14, textColor=colors.HexColor("#666666"),
                          alignment=TA_CENTER)
tip = ParagraphStyle("tip", fontName="Helvetica-Oblique", fontSize=9,
                     leading=12, textColor=TEAL)
section = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=13,
                         leading=18, textColor=colors.white)
th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8, leading=12,
                    textColor=HEAD_INK)
song = ParagraphStyle("song", fontName="Helvetica-Bold", fontSize=9,
                      leading=12, textColor=INK)
meta = ParagraphStyle("meta", fontName="Helvetica", fontSize=8.5, leading=12,
                      textColor=GREY)
note = ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8.5,
                      leading=12, textColor=GREY)
foot = ParagraphStyle("foot", fontName="Helvetica-Oblique", fontSize=9,
                      leading=12, textColor=colors.HexColor("#666666"),
                      alignment=TA_CENTER)
stat_n = ParagraphStyle("stat_n", fontName="Helvetica-Bold", fontSize=15,
                        leading=18, textColor=TEAL, alignment=TA_CENTER)
stat_l = ParagraphStyle("stat_l", fontName="Helvetica", fontSize=8, leading=11,
                        textColor=GREY, alignment=TA_CENTER)

COLS = [113.3858, 90.7087, 209.7638, 51.0236]
WIDTH = sum(COLS)


def level_cell(value):
    style = ParagraphStyle("lv", fontName="Helvetica-Bold", fontSize=7.5,
                           leading=10, textColor=LEVEL[value][1],
                           alignment=TA_CENTER)
    return Paragraph(value, style)


def build():
    total = sum(len(rows) for _, rows in SETS)
    doc = SimpleDocTemplate(
        "hotel_piano_repertoire.pdf", pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2.3 * cm, bottomMargin=2 * cm,
        title="Hotel Piano Repertoire", author="Aminotee",
    )
    story = [
        Paragraph("Hotel Piano Repertoire", title),
        Spacer(1, 6),
        Paragraph("Jazz · Lounge · Sentimental · Andalusian "
                  "— %d Songs" % total, subtitle),
        Spacer(1, 10),
        HRFlowable(width="100%", thickness=1, color=RULE, spaceAfter=14),
    ]

    hint = Table([[Paragraph(
        "%s &nbsp;Aim for 25–30 songs per 3-hour set. Play each 3–4 min, "
        "repeat favourites with different arrangements." % BULLET, tip)]],
        colWidths=[WIDTH])
    hint.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MINT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story += [hint, Spacer(1, 16)]

    for name, rows in SETS:
        bar = Table([[Paragraph("%s &nbsp;%s" % (BULLET, name), section)]],
                    colWidths=[WIDTH])
        bar.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), TEAL),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))

        data = [[Paragraph(h, th) for h in ("Song", "Artist", "Notes", "Level")]]
        for s, a, n, lv in rows:
            data.append([Paragraph(s, song), Paragraph(a, meta),
                         Paragraph(n, note), level_cell(lv)])

        table = Table(data, colWidths=COLS, repeatRows=1)
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
            ("GRID", (0, 0), (-1, -1), 0.3, RULE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
        for i, (_, _, _, lv) in enumerate(rows, start=1):
            if i % 2 == 0:
                style.append(("BACKGROUND", (0, i), (2, i), ALT_BG))
            style.append(("BACKGROUND", (3, i), (3, i), LEVEL[lv][0]))
        table.setStyle(TableStyle(style))

        story += [bar, table, Spacer(1, 18)]

    stats = Table([[
        Paragraph("%d" % total, stat_n), Paragraph("~3–4h", stat_n),
        Paragraph("%d" % len(SETS), stat_n), Paragraph("~75%", stat_n),
    ], [
        Paragraph("Songs total", stat_l), Paragraph("Full set length", stat_l),
        Paragraph("Categories", stat_l), Paragraph("Easy / Medium", stat_l),
    ]], colWidths=[WIDTH / 4.0] * 4)
    stats.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
        ("LINEABOVE", (0, 0), (-1, 0), 1, RULE),
    ]))
    story += [stats, Spacer(1, 10), Paragraph(
        "Generated for hotel lounge performance use · Good luck at Plaza!",
        foot)]

    doc.build(story)
    print("hotel_piano_repertoire.pdf — %d songs, %d sets"
          % (total, len(SETS)))


if __name__ == "__main__":
    build()
