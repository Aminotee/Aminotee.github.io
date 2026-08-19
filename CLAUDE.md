# Aminotee.github.io — working notes

Single-page portfolio for Aminotee, a jazz/lounge pianist. No build step:
`index.html` is hand-written, with media in `assets/` and `videos/`.

## Repertoire must stay in sync with the source PDF

The repertoire section in `index.html` mirrors `hotel_piano_repertoire.pdf`,
kept in the repo root as the source of truth. **They must always match.**

- When a new version of the PDF is provided, replace the copy in the repo root,
  then diff it against the site and update `index.html` so every set, song, and
  ordering matches the PDF exactly.
- When a song is added or removed on either side, apply the same change to the
  other, and report any drift found.
- Keep the six set names and their order as they appear in the PDF:
  Jazz Standards · Sentimental Classics · Smooth Lounge · Classical ·
  Andalusian & Arabic (signature) · Special Occasions.
- Update the song count in `README.md` whenever the total changes.

Current total: 63 songs.

After editing the song data in `tools/build_repertoire_pdf.py`, run:

```
python3 tools/build_repertoire_pdf.py   # regenerate the PDF
python3 tools/render_chord_links.py     # re-link song titles to their chords
python3 tools/check_sync.py             # confirm the PDF and site agree
python3 tools/build_playlist.py         # refresh the playlist import list
```

Each song title on the site links to its chords. Exact URLs go in the `EXACT`
map in `render_chord_links.py` — any chord site is fine (Ultimate Guitar,
Chordify, e-chords). Songs not listed there fall back to an Ultimate Guitar
search, which always resolves.

## Deploying

GitHub Pages serves this repo. Push to both `main` and the active working
branch; the site is live at https://aminotee.github.io.

## Video files

Clips come from an iPhone as HEVC/QuickTime, which browsers can't play. Convert
to H.264 before committing, cropping any baked-in letterboxing, and set each
`<video>` element's `style="aspect-ratio:W/H"` to the clip's real dimensions:

```
ffmpeg -i in.mp4 -vf "crop=W:H:X:Y" -c:v libx264 -crf 24 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart videos/out.mp4
```

Use `cropdetect` to find the crop box, and generate a poster frame into
`assets/<name>-poster.jpg`.
