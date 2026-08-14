# Aminotee.github.io — working notes

Single-page portfolio for Aminotee, a jazz/lounge pianist. No build step:
`index.html` is hand-written, with media in `assets/` and `videos/`.

## Repertoire must stay in sync with the source PDF

The repertoire section in `index.html` mirrors Aminotee's
`hotel_piano_repertoire.pdf`. **They must always match.**

- When a new version of the PDF is provided, diff it against the site and update
  `index.html` so every set, song, and ordering matches the PDF exactly.
- When a song is added or removed on either side, apply the same change to the
  other, and report any drift found.
- Keep the six set names and their order as they appear in the PDF:
  Jazz Standards · Sentimental Classics · Smooth Lounge · Classical ·
  Andalusian & Arabic (signature) · Special Occasions.
- Update the song count in `README.md` whenever the total changes.

Current total: 60 songs.

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
