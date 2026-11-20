import base64, io, os
from PIL import Image, ImageFilter

import pathlib
ROOT = pathlib.Path(__file__).parent
W = str(ROOT / 'src') + '/'
OUT = str(ROOT / 'site') + '/'
os.makedirs(OUT, exist_ok=True)
B = lambda b: base64.b64encode(b).decode()

def webp(path, lossless=False, scale=1.0):
    im = Image.open(path)
    if scale != 1.0:
        im = im.resize((round(im.width*scale), round(im.height*scale)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'WEBP', quality=88, method=6, lossless=lossless)
    return buf.getvalue(), im.size

base, (sw, sh) = webp(W + 'sheep_base.png')
jaw, _ = webp(W + 'sheep_jaw.png', lossless=True)
x0, y0, x1, y1 = map(int, open(W + 'geom.txt').read().split())
MX = (1048 - x0) / (x1 - x0)
MY = (733 - y0) / (y1 - y0)

tuft = Image.open(W + 'tuft.png')
tb = io.BytesIO(); tuft.save(tb, 'WEBP', quality=86, method=6)

# favicon + apple-touch-icon + link preview: grass tuft on sky blue, no sheep (keep the surprise)
SKY = (135, 206, 235, 255)
def on_sky(size, frac, shadow=True):
    w, h = size
    bg = Image.new('RGBA', size, SKY)
    s = round(min(w, h) * frac)
    t = tuft.resize((s, s), Image.LANCZOS)
    pos = ((w - s)//2, (h - s)//2)
    if shadow:
        sh_ = Image.new('RGBA', size, (0,0,0,0))
        a = t.split()[3].point(lambda v: int(v*.28))
        blk = Image.new('RGBA', t.size, (20,80,130,255)); blk.putalpha(a)
        sh_.alpha_composite(blk, (pos[0], pos[1] + max(2, s//30)))
        bg.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(max(1, s//34))))
    bg.alpha_composite(t, pos)
    return bg.convert('RGB')

on_sky((1200, 630), .82).save(OUT + 'preview.png', optimize=True)
on_sky((180, 180), .92).save(OUT + 'apple-touch-icon.png', optimize=True)
fav = io.BytesIO(); tuft.resize((64, 64), Image.LANCZOS).save(fav, 'PNG', optimize=True)

t = open(ROOT / 'template.html').read()
rep = {
    '__AR__': f'{sh/sw:.5f}', '__W__': str(sw), '__H__': str(sh),
    '__MX__': f'{MX:.4f}', '__MY__': f'{MY:.4f}',
    '__BASE__': B(base), '__JAW__': B(jaw), '__TUFT__': B(tb.getvalue()), '__FAV__': B(fav.getvalue()),
    '__BITE__': B(open(W + 'snd/bite.mp3', 'rb').read()),
    '__BLEAT__': B(open(W + 'snd/bleat.mp3', 'rb').read()),
}
for k, v in rep.items():
    assert k in t, k
    t = t.replace(k, v)
assert '__' not in t.replace('__proto__', ''), [l for l in t.splitlines() if '__' in l][:3]
open(OUT + 'index.html', 'w').write(t)
print('index.html', len(t)//1024, 'KB', 'sticker', sw, sh, 'mouth', round(MX, 4), round(MY, 4))
