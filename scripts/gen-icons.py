"""Generate project icons for STOPA Command Center."""
import sys
import math
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from PIL import Image, ImageDraw
from pathlib import Path

out = Path(r'C:\Users\stock\Documents\000_NGM\STOPA\dashboard\public\icons')
out.mkdir(exist_ok=True)

projects = [
    ('monitor',   '#38bdf8', 'radar'),
    ('ngrobot',   '#c8b88a', 'quill'),
    ('adobe',     '#a855f7', 'layers'),
    ('grafik',    '#22c55e', 'brush'),
    ('kartograf', '#eab308', 'compass'),
    ('polybot',   '#ef4444', 'chart'),
    ('ftip',      '#ec4899', 'laugh'),
    ('orakulum',  '#14b8a6', 'eye'),
    ('zachvev',   '#f97316', 'wave'),
    ('rozhovor',  '#6366f1', 'mic'),
    ('dane',      '#84cc16', 'calc'),
    ('biolib',    '#06b6d4', 'leaf'),
]

BG = (8, 9, 13, 255)

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def make_icon(s, rgb, shape):
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = max(int(s * 0.19), 1)
    d.rounded_rectangle([0, 0, s-1, s-1], radius=r, fill=BG)

    c = rgb + (230,)
    cx, cy = s / 2, s / 2
    u = s / 16

    if shape == 'radar':
        for i, rad in enumerate([5.5, 4, 2.5]):
            bbox = [cx - rad*u, cy - rad*u, cx + rad*u, cy + rad*u]
            d.arc(bbox, 200, 340, fill=rgb + (140 + i*30,), width=max(int(u*0.6), 1))
        d.line([cx, cy, cx + 4*u, cy - 4*u], fill=c, width=max(int(u*0.7), 1))
        d.ellipse([cx - u*0.7, cy - u*0.7, cx + u*0.7, cy + u*0.7], fill=c)

    elif shape == 'quill':
        pts = [(cx+4*u, cy-5*u), (cx+5*u, cy-3*u), (cx-2*u, cy+4*u),
               (cx-3*u, cy+5*u), (cx-4*u, cy+5*u)]
        d.polygon(pts, fill=c)
        d.line([cx-4*u, cy+5*u, cx-5*u, cy+6*u], fill=c, width=max(int(u*0.5), 1))
        d.line([cx+3*u, cy-3*u, cx-2*u, cy+3*u], fill=BG, width=max(int(u*0.4), 1))

    elif shape == 'layers':
        for i, offset in enumerate([-3, 0, 3]):
            y = cy + offset * u
            alpha = 160 + i * 30
            pts = [(cx-4*u, y+u), (cx+3*u, y-u), (cx+4*u, y), (cx-3*u, y+2*u)]
            d.polygon(pts, fill=rgb + (alpha,))
            d.polygon(pts, outline=rgb + (200,))

    elif shape == 'brush':
        d.rounded_rectangle([cx-2.5*u, cy-5*u, cx+2.5*u, cy-u],
                            radius=max(int(u), 1), fill=c)
        d.rectangle([cx-u, cy-u, cx+u, cy+5*u], fill=rgb + (180,))
        d.rectangle([cx-1.8*u, cy-1.5*u, cx+1.8*u, cy-0.5*u], fill=rgb + (200,))

    elif shape == 'compass':
        rad = 5 * u
        d.polygon([cx, cy-rad, cx+1.5*u, cy, cx, cy+rad, cx-1.5*u, cy], fill=c)
        d.polygon([cx-rad, cy, cx, cy-1.5*u, cx+rad, cy, cx, cy+1.5*u],
                  fill=rgb + (140,))
        d.ellipse([cx-u, cy-u, cx+u, cy+u], fill=BG)

    elif shape == 'chart':
        bars = [3, 4.5, 3.5, 6, 5, 7.5]
        bw = u * 1.5
        gap = u * 0.5
        total_w = len(bars) * (bw + gap) - gap
        sx = cx - total_w / 2
        base = cy + 4 * u
        for i, h in enumerate(bars):
            x = sx + i * (bw + gap)
            alpha = 150 + int(i * 15)
            d.rectangle([x, base - h*u, x + bw, base], fill=rgb + (alpha,))
        d.line([sx, base - 3*u, sx + total_w, base - 7*u],
               fill=(255, 255, 255, 80), width=max(int(u*0.4), 1))

    elif shape == 'laugh':
        rad = 5 * u
        d.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], outline=c,
                  width=max(int(u*0.8), 1))
        er = u * 0.8
        d.ellipse([cx-2.5*u-er, cy-1.5*u-er, cx-2.5*u+er, cy-1.5*u+er], fill=c)
        d.ellipse([cx+2.5*u-er, cy-1.5*u-er, cx+2.5*u+er, cy-1.5*u+er], fill=c)
        d.arc([cx-3*u, cy-2*u, cx+3*u, cy+3.5*u], 10, 170,
              fill=c, width=max(int(u*0.7), 1))

    elif shape == 'eye':
        d.polygon([(cx-5.5*u, cy), (cx, cy-3*u), (cx+5.5*u, cy), (cx, cy+3*u)],
                  fill=rgb + (100,), outline=c)
        d.ellipse([cx-2*u, cy-2*u, cx+2*u, cy+2*u], fill=c)
        d.ellipse([cx-u, cy-u, cx+u, cy+u], fill=BG)

    elif shape == 'wave':
        w = max(int(u*0.8), 1)
        for row, amp, alpha in [(-2*u, 2.5, 140), (0, 3.5, 200), (2*u, 2, 160)]:
            pts = []
            for px in range(int(cx - 6*u), int(cx + 6*u) + 1):
                t = (px - (cx - 6*u)) / (12 * u) * math.pi * 3
                py = cy + row + math.sin(t) * amp * u
                pts.append((px, py))
            if len(pts) > 1:
                d.line(pts, fill=rgb + (alpha,), width=w)

    elif shape == 'mic':
        d.rounded_rectangle([cx-2*u, cy-5*u, cx+2*u, cy+u],
                            radius=max(int(2*u), 1), fill=c)
        d.arc([cx-3*u, cy-u, cx+3*u, cy+3*u], 0, 180,
              fill=rgb + (160,), width=max(int(u*0.6), 1))
        d.line([cx, cy+3*u, cx, cy+5.5*u], fill=rgb + (160,),
               width=max(int(u*0.6), 1))
        d.line([cx-2*u, cy+5.5*u, cx+2*u, cy+5.5*u], fill=rgb + (160,),
               width=max(int(u*0.6), 1))

    elif shape == 'calc':
        d.rounded_rectangle([cx-4*u, cy-5.5*u, cx+4*u, cy+5.5*u],
                            radius=max(int(u*0.8), 1), outline=c,
                            width=max(int(u*0.5), 1))
        d.rectangle([cx-3*u, cy-4.5*u, cx+3*u, cy-2*u], fill=rgb + (100,))
        for row in range(3):
            for col in range(3):
                bx = cx - 2.5*u + col * 2.5*u
                by = cy - 0.5*u + row * 2*u
                d.rectangle([bx-0.6*u, by-0.6*u, bx+0.6*u, by+0.6*u],
                            fill=rgb + (140 + row*20,))

    elif shape == 'leaf':
        pts = [(cx, cy-6*u), (cx+4*u, cy-2*u), (cx+3*u, cy+2*u),
               (cx, cy+5*u), (cx-3*u, cy+2*u), (cx-4*u, cy-2*u)]
        d.polygon(pts, fill=rgb + (180,))
        d.line([cx, cy-5*u, cx, cy+4*u], fill=(8, 9, 13, 120),
               width=max(int(u*0.4), 1))
        d.line([cx, cy-2*u, cx+2.5*u, cy-0.5*u], fill=(8, 9, 13, 80),
               width=max(int(u*0.3), 1))
        d.line([cx, cy+u, cx-2.5*u, cy+2*u], fill=(8, 9, 13, 80),
               width=max(int(u*0.3), 1))

    return img


for pid, color_hex, shape in projects:
    rgb = hex2rgb(color_hex)
    big = make_icon(256, rgb, shape)
    ico_path = out / f'{pid}.ico'
    big.save(str(ico_path), format='ICO',
             sizes=[(256, 256), (64, 64), (48, 48), (32, 32), (16, 16)])
    png_path = out / f'{pid}.png'
    big.save(str(png_path), format='PNG')
    print(f'  {pid:12s}  {shape:8s}  {color_hex}  {ico_path.stat().st_size:>6} B')

print(f'\nDone: {len(projects)} icons in {out}')
