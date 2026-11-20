# blee.eat

Sister site to simin.eat: one sticker, one button, one gag. A real sheep photo cut out as a paper-bordered sticker on a sky-blue background. Tapping **feed** flies a clump of grass (a real photo, with dirt) up to its mouth, and it eats it in four bites ("nom, nom, NOM, NOM!!"), then swallows, chews and bleats (same bubble + baa as a poke). Pokes during a meal are ignored; a feed tapped during a poke-bleat waits for it. The calorie counter at the top goes up 6 cal per bite. Tapping the sheep makes it bleat, with a spiky shout bubble saying "BLEEEAT!" (0–2 extra E's at random) in the site's normal bold font. Spacebar feeds, B bleats. Extra feed taps queue up (max 5).

## Files
- `template.html` is the page source. Images and sounds are inlined as base64 via `__PLACEHOLDER__` tokens.
- `build.py` fills the template and writes `site/index.html`, `site/preview.png` and `site/apple-touch-icon.png`. Run it with `python3 build.py` (needs Pillow).
- `site/` is what gets deployed. Upload that folder (or a zip of its 3 files) as a new Cloudflare Pages deployment, same as simin.eat.
- `src/sticker.py` rebuilds `sheep_base.png` (sheep + paper border, with a dark mouth hole where the jaw is) and `sheep_jaw.png` (just the chin) from `sheep_photo.png` and `sheep_cutout_raw.png` (rembg isnet-general-use output). The jaw polygon is in photo pixel coords. Run it from inside `src/` (needs opencv-python, numpy, Pillow).
- `src/tuft.png` is `grass_photo.png` (already transparent) cropped, scaled and centered on a 480×480 canvas. `BITES` in the template are the canvas rows it gets bitten at.
- `src/snd/` has `bleat.mp3` ("Sheep Baa" by AntumDeluge from a recording by mikewest, CC0, OpenGameArt) and `bite.mp3` ("Crunchy bite", CC0, OpenGameArt). Both are trimmed and loudness-normalized.

## Style (kept the same as simin.eat)
- Font: Outfit 800/900 (a free stand-in for Crumbl Sans), loaded from Google Fonts. It's used everywhere, including the bleat bubble.
- Black pill "feed" button at bottom center, round black mute button top right (remembered in localStorage as `blee-muted`).
- Counter: white with a black outline and shadow, tilted -3°.
- Background `#87CEEB`, with blue-tinted drop shadows.
- Tuning knobs at the top of the script: `OPEN`/`WIDE` (jaw drop, % of sticker height), `CAL_PER_BITE`, `BITES` (tuft rows bitten), the tuft size (`size:r.width*0.3` in `geom()`), and the sticker size (the `.8` and `.72` factors in `.sticker{height:...}`).

## Link preview
It's spoiler-free on purpose: the title is just "blee.eat" and the image is only the grass clump on sky blue.
