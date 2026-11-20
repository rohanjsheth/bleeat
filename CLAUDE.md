# blee.eat

Sister site to simin.eat: one sticker, one button, one gag. A real sheep photo cut out as a paper-bordered sticker on a sky-blue background. Tapping **feed** flies a clump of grass (a real photo, with dirt) up to its mouth, and it eats it in four bites ("nom, nom, NOM, NOM!!"), then swallows, chews, gets fatter (each bite inflates its belly with a WebGL bulge warp centred on the body, so the belly swells and sags out of the sticker and jiggles; the face barely moves; caps out after ~4 meals, resets on reload, plain sticker if WebGL is unavailable) and bleats (same baa + text as a poke). Pokes during a meal are ignored; a feed tapped during a poke-bleat waits for it. The calorie counter at the top goes up 6 cal per bite. Tapping the sheep makes it bleat, and "BLEEEAT!" (0–2 extra E's at random) pops up white with a black outline, same style as simin.eat's BURP. Spacebar feeds, B bleats. Extra feed taps queue up (max 5).

## Files
- `template.html` is the page source. Images and sounds are inlined as base64 via `__PLACEHOLDER__` tokens.
- `build.py` fills the template and writes `site/index.html`, `site/preview.png` and `site/apple-touch-icon.png`. Run it with `python3 build.py` (needs Pillow).
- `site/` is what gets deployed. Upload that folder (or a zip of its 3 files) as a new Cloudflare Pages deployment, same as simin.eat.
- `src/sticker.py` rebuilds `sheep_base.png` (sheep + paper border, with a dark mouth hole where the jaw is) and `sheep_jaw.png` (just the chin) from `sheep_photo.png` and `sheep_cutout_raw.png` (rembg isnet-general-use output). The jaw polygon is in photo pixel coords. Run it from inside `src/` (needs opencv-python, numpy, Pillow).
- `src/tuft.png` is `grass_photo.png` (already transparent) cropped, scaled and centered on a 480×480 canvas. `BITES` in the template are the canvas rows it gets bitten at.
- `src/snd/` has `bleat.mp3` ("Sheep Baa" by AntumDeluge from a recording by mikewest, CC0, OpenGameArt) and `bite.mp3` ("Crunchy bite", CC0, OpenGameArt). Both are trimmed and loudness-normalized.

## Style (kept the same as simin.eat)
- Font: Outfit 800/900 (a free stand-in for Crumbl Sans), loaded from Google Fonts. It's used everywhere, including the bleat text.
- Black pill "feed" button at bottom center, round black mute button top right (remembered in localStorage as `blee-muted`).
- Text styles are copied from simin.eat: black "nom"s that grow, "+6 cal" pops and the BLEEEAT in white with a black outline and hard black shadow. The counter sits on top of the sticker, tilted -4° and sized to it.
- Background `#87CEEB`, with blue-tinted drop shadows.
- Tuning knobs at the top of the script: `OPEN`/`WIDE` (jaw drop, % of sticker height), `CAL_PER_BITE`, `BITES` (tuft rows bitten), `FAT_PER_BITE`/`FAT_PER_MEAL`/`FAT_MAX` (bulge growth and cap), `BC`/`BR` (bulge centre/radius in sticker units), `PAD` (how far the warp canvas overhangs the sticker), the tuft size (`size:r.width*0.3` in `geom()`), and the sticker size (the `.8` and `.72` factors in `.sticker{height:...}`).

## Link preview
It's spoiler-free on purpose: the title is just "blee.eat" and the image is only the grass clump on sky blue.
