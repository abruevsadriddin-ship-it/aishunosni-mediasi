"""AI news story cards for @aishunos_.
usage: python3 make.py news.json OUTDIR
news.json: {"date": "25.11.2026", "items": [{"title": "...", "body": "...", "source": "...", "icon": "chart|chat|music|chip|robot|shield|money|globe|code|eye"}, x3]}
Fonts: expects Montserrat[wght].ttf next to this script (fetched from google/fonts ofl/montserrat).
"""
import json, sys, os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
MONT = os.path.join(HERE, 'Montserrat[wght].ttf')
ACC = [(255, 122, 69), (90, 200, 255), (180, 120, 255)]

def font(size, w=500):
    f = ImageFont.truetype(MONT, size)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f

def wrap(d, text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def bg(acc, seed):
    r = random.Random(seed); im = Image.new('RGB', (W, H), (8, 10, 18)); d = ImageDraw.Draw(im)
    for y in range(H):  # vertical gradient
        k = y / H; d.line((0, y, W, y), fill=(int(8 + 10 * k), int(10 + 6 * k), int(22 + 18 * (1 - k))))
    for x in range(0, W, 60): d.line((x, 0, x, H), fill=(22, 26, 40))
    for y in range(0, H, 60): d.line((0, y, W, y), fill=(22, 26, 40))
    glow = Image.new('RGB', (W, H), (0, 0, 0)); g = ImageDraw.Draw(glow)
    g.ellipse((W * .15, 380, W * .85, 1060), fill=tuple(int(c * .55) for c in acc))
    glow = glow.filter(ImageFilter.GaussianBlur(170))
    import numpy as np
    return Image.fromarray(np.clip(np.asarray(im, np.int16) + np.asarray(glow, np.int16), 0, 255).astype(np.uint8))

def icon(d, kind, cx, cy, s, col):
    w = int(14 * s); S = lambda v: v * s; c = col
    if kind == 'chart':
        d.line([(cx - S(180), cy + S(140)), (cx + S(190), cy + S(140))], fill=(200, 205, 220), width=w // 2)
        pts = [(cx - S(170), cy + S(90)), (cx - S(80), cy + S(30)), (cx, cy + S(60)), (cx + S(90), cy - S(50)), (cx + S(170), cy - S(120))]
        d.line(pts, fill=c, width=w, joint='curve')
        d.polygon([(cx + S(170), cy - S(150)), (cx + S(200), cy - S(100)), (cx + S(140), cy - S(100))], fill=c)
    elif kind == 'chat':
        d.rounded_rectangle((cx - S(190), cy - S(140), cx + S(190), cy + S(90)), S(50), outline=c, width=w)
        d.polygon([(cx - S(100), cy + S(85)), (cx - S(150), cy + S(170)), (cx - S(40), cy + S(88))], fill=c)
        for i in range(3): d.ellipse((cx - S(95) + i * S(80), cy - S(45), cx - S(55) + i * S(80), cy - S(5)), fill=c)
    elif kind == 'music':
        d.line([(cx - S(60), cy + S(100)), (cx - S(60), cy - S(130)), (cx + S(110), cy - S(160)), (cx + S(110), cy + S(70))], fill=c, width=w)
        for x, y in ((cx - S(105), cy + S(100)), (cx + S(65), cy + S(70))): d.ellipse((x - S(50), y - S(38), x + S(50), y + S(38)), fill=c)
        d.line([(cx - S(200), cy - S(200)), (cx + S(200), cy + S(200))], fill=(255, 70, 70), width=w)
    elif kind == 'chip':
        d.rounded_rectangle((cx - S(130), cy - S(130), cx + S(130), cy + S(130)), S(24), outline=c, width=w)
        d.rectangle((cx - S(60), cy - S(60), cx + S(60), cy + S(60)), fill=c)
        for i in range(-2, 3):
            for (a, b, e, f_) in ((cx + S(i * 45), cy - S(130), cx + S(i * 45), cy - S(180)), (cx + S(i * 45), cy + S(130), cx + S(i * 45), cy + S(180)),
                                  (cx - S(130), cy + S(i * 45), cx - S(180), cy + S(i * 45)), (cx + S(130), cy + S(i * 45), cx + S(180), cy + S(i * 45))):
                d.line([(a, b), (e, f_)], fill=c, width=w // 2)
    elif kind == 'robot':
        d.rounded_rectangle((cx - S(150), cy - S(110), cx + S(150), cy + S(130)), S(50), outline=c, width=w)
        for x in (-60, 60): d.ellipse((cx + S(x) - S(28), cy - S(20), cx + S(x) + S(28), cy + S(36)), fill=c)
        d.line([(cx, cy - S(110)), (cx, cy - S(170))], fill=c, width=w); d.ellipse((cx - S(22), cy - S(205), cx + S(22), cy - S(160)), fill=c)
    elif kind == 'shield':
        d.polygon([(cx, cy - S(180)), (cx + S(150), cy - S(120)), (cx + S(130), cy + S(60)), (cx, cy + S(180)), (cx - S(130), cy + S(60)), (cx - S(150), cy - S(120))], outline=c, width=w)
        d.line([(cx - S(60), cy), (cx - S(10), cy + S(55)), (cx + S(75), cy - S(55))], fill=c, width=w, joint='curve')
    elif kind == 'money':
        d.ellipse((cx - S(170), cy - S(170), cx + S(170), cy + S(170)), outline=c, width=w)
        d.text((cx, cy), '$', font=font(int(S(230)), 600), fill=c, anchor='mm')
    elif kind == 'globe':
        d.ellipse((cx - S(170), cy - S(170), cx + S(170), cy + S(170)), outline=c, width=w)
        d.ellipse((cx - S(80), cy - S(170), cx + S(80), cy + S(170)), outline=c, width=w // 2)
        d.line([(cx - S(170), cy), (cx + S(170), cy)], fill=c, width=w // 2)
    elif kind == 'code':
        d.line([(cx - S(80), cy - S(110)), (cx - S(180), cy), (cx - S(80), cy + S(110))], fill=c, width=w, joint='curve')
        d.line([(cx + S(80), cy - S(110)), (cx + S(180), cy), (cx + S(80), cy + S(110))], fill=c, width=w, joint='curve')
        d.line([(cx + S(30), cy - S(140)), (cx - S(30), cy + S(140))], fill=c, width=w)
    else:  # eye
        d.ellipse((cx - S(190), cy - S(100), cx + S(190), cy + S(100)), outline=c, width=w)
        d.ellipse((cx - S(55), cy - S(55), cx + S(55), cy + S(55)), fill=c)

def card(item, i, n, date, out):
    acc = ACC[i % 3]; im = bg(acc, i); d = ImageDraw.Draw(im)
    # header (below top 15% safe area)
    d.text((80, 300), 'AI OLAMI', font=font(44, 600), fill=acc)
    d.text((W - 80, 300), f'{i + 1}/{n}', font=font(44, 500), fill=(200, 205, 220), anchor='ra')
    d.text((80, 356), date, font=font(34, 400), fill=(140, 146, 165))
    d.line((80, 415, W - 80, 415), fill=(50, 56, 78), width=3)
    icon(d, item.get('icon', 'robot'), W / 2, 700, 1.15, acc)
    y = 980
    for ln in wrap(d, item['title'], font(74, 600), W - 160):
        d.text((80, y), ln, font=font(74, 600), fill=(245, 246, 250)); y += 92
    y += 26; d.rounded_rectangle((80, y, 200, y + 8), 4, fill=acc); y += 44
    for ln in wrap(d, item['body'], font(44, 400), W - 160):
        d.text((80, y), ln, font=font(44, 400), fill=(200, 205, 220)); y += 60
    d.text((80, 1560), 'Manba: ' + item['source'], font=font(34, 400), fill=(130, 136, 155))
    d.text((W / 2, 1660), 'aishunos_', font=font(36, 500), fill=(160, 166, 185), anchor='mm')
    im.save(out, quality=94)

if __name__ == '__main__':
    data = json.load(open(sys.argv[1])); outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
    for i, it in enumerate(data['items']):
        card(it, i, len(data['items']), data['date'], os.path.join(outdir, f'news_{i + 1}.jpg'))
    print('ok', len(data['items']))
