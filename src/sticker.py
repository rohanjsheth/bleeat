import cv2, numpy as np
from PIL import Image

SRC = 'sheep_photo.png'
CUT = 'sheep_cutout_raw.png'
BOTTOM = 1215          # flat bottom edge (photo y)
R = 30                 # paper border thickness (px)

rgb = np.array(Image.open(SRC).convert('RGB')).astype(np.float32)
al = np.array(Image.open(CUT))[..., 3].astype(np.float32) / 255
H, W = al.shape

# ---- clean mask: drop thin grass blades, keep the sheep blob
b = (al > 0.5).astype(np.uint8)
b[BOTTOM:] = 0
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))
op = cv2.morphologyEx(b, cv2.MORPH_OPEN, k)
n, lab, st, _ = cv2.connectedComponentsWithStats(op)
big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
body = (lab == big).astype(np.uint8)
# fill holes
ff = body.copy(); m = np.zeros((H + 2, W + 2), np.uint8); cv2.floodFill(ff, m, (0, 0), 1)
body = body | (1 - ff)
keep = cv2.dilate(body, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
alpha = al * keep
alpha[BOTTOM:] = 0
# soften the flat bottom cut by 1px
alpha[BOTTOM - 1] *= 0.5

# ---- edge decontamination (photo bg is dark green)
dist = cv2.distanceTransform((alpha > 0.5).astype(np.uint8), cv2.DIST_L2, 5)
inside = (dist > 7).astype(np.uint8)
fillmask = ((alpha > 0.01) & (inside == 0)).astype(np.uint8)
def bleed(sig):
    m = inside.astype(np.float32)
    num = cv2.GaussianBlur(rgb * m[..., None], (0, 0), sig)
    den = cv2.GaussianBlur(m, (0, 0), sig)[..., None]
    return num / np.maximum(den, 1e-4), den
c1, d1 = bleed(4); c2, _ = bleed(14)
inp = np.where(d1 > 0.02, c1, c2)
w_in = np.clip((dist - 2) / 6, 0, 1)[..., None]        # trust real pixels only when nearly opaque
rgb = np.where(fillmask[..., None] > 0, rgb * w_in + inp * (1 - w_in), rgb)
# lift the outer fuzz a touch so the halo reads as backlit wool, not shadow
rgb = np.where(fillmask[..., None] > 0, rgb * 0.85 + np.array([238, 232, 222]) * 0.15, rgb)

# ---- paper border
solid = (alpha > 0.35).astype(np.uint8)
solid = cv2.morphologyEx(solid, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
bd = cv2.dilate(solid, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * R + 1, 2 * R + 1))).astype(np.float32)
bd = cv2.GaussianBlur(bd, (0, 0), 6)
bd = np.clip((bd - 0.5) * 6 + 0.5, 0, 1)              # smooth rounded outline, soft AA
rng = np.random.default_rng(7)
grain = rng.normal(0, 1, (H, W)).astype(np.float32)
fib = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 3) * 3
blot = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 28) * 18
tex = 1 + 0.018 * grain + 0.012 * fib + 0.02 * blot
paper = np.stack([251 * tex, 247 * tex, 238 * tex], -1)
# faint warm edge just inside the outline
edge = cv2.GaussianBlur((bd > 0.5).astype(np.float32), (0, 0), 2.5)
paper *= (0.93 + 0.07 * np.clip((edge - 0.5) * 2, 0, 1))[..., None]

# ---- jaw region (photo coords)
jaw_poly = np.array([(1012, 727), (1030, 730), (1047, 735), (1064, 731), (1086, 725),
                     (1088, 736), (1080, 749), (1066, 758), (1048, 763), (1030, 759),
                     (1018, 749), (1011, 737)], np.int32)
jm = np.zeros((H, W), np.uint8); cv2.fillPoly(jm, [jaw_poly], 1)
jaw_a = cv2.GaussianBlur(jm.astype(np.float32), (0, 0), 1.0)
hole = cv2.erode(jm, np.ones((5, 5), np.uint8)).astype(np.float32)
hole = cv2.GaussianBlur(hole, (0, 0), 1.0)

# mouth inside: dark, a bit of pink tongue near the bottom
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
t = np.clip((yy - 728) / 36, 0, 1)
inner = np.stack([26 + 52 * t, 10 + 14 * t, 12 + 16 * t], -1)
tongue = np.exp(-(((xx - 1048) / 20) ** 2 + ((yy - 770) / 9) ** 2))
inner = inner * (1 - tongue[..., None] * .7) + np.array([170, 78, 88]) * tongue[..., None] * .7

def compose(rgbimg, a_sheep):
    out_rgb = paper * (1 - a_sheep[..., None]) + rgbimg * a_sheep[..., None]
    out_a = np.maximum(bd, a_sheep)
    return out_rgb, out_a

base_rgb = rgb * (1 - hole[..., None]) + inner * hole[..., None]
full_rgb, full_a = compose(rgb, alpha)
base_rgb, base_a = compose(base_rgb, alpha)
jaw_rgb, jaw_a2 = rgb, alpha * jaw_a

ys, xs = np.where(full_a > 0.01)
x0, x1, y0, y1 = xs.min() - 4, xs.max() + 5, ys.min() - 4, ys.max() + 5
print('crop', x0, y0, x1, y1, 'size', x1 - x0, y1 - y0)
print('mouth frac', (1048 - x0) / (x1 - x0), (733 - y0) / (y1 - y0))

def save(name, c, a):
    im = np.dstack([np.clip(c, 0, 255), np.clip(a, 0, 1) * 255]).astype(np.uint8)[y0:y1, x0:x1]
    Image.fromarray(im, 'RGBA').save(name)

save('sheep_full.png', full_rgb, full_a)
save('sheep_base.png', base_rgb, base_a)
save('sheep_jaw.png', jaw_rgb, jaw_a2)
open('geom.txt', 'w').write(f'{x0} {y0} {x1} {y1}')
