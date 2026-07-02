#!/usr/bin/env python3
# Convierte un carrusel (PNGs 1080x1080) en frames verticales 2160x3840 para _encode.swift
# Fondo = la misma lamina llenando el canvas, con blur fuerte y oscurecida (look pro).
import os, sys
from PIL import Image, ImageFilter, ImageEnhance

W,H = 2160,3840
FPS = 30
SECS = 2.0
ZOOM0, ZOOM1 = 1.0, 1.05

folder = sys.argv[1] if len(sys.argv)>1 else 'carrusel1-verdades'
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder)
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_ss_frames')
os.makedirs(outdir, exist_ok=True)

slides = sorted(f for f in os.listdir(src) if f.endswith('.png'))
manifest = []
for i,f in enumerate(slides):
    im = Image.open(os.path.join(src,f)).convert('RGB')
    # fondo: fill + blur + oscurecer
    bg = im.resize((H,H)).crop(((H-W)//2,0,(H-W)//2+W,H))
    bg = bg.filter(ImageFilter.GaussianBlur(70))
    bg = ImageEnhance.Brightness(bg).enhance(0.5)
    # lamina centrada a todo lo ancho
    fg = im.resize((W,W), Image.LANCZOS)
    bg.paste(fg,(0,(H-W)//2))
    fp = os.path.join(outdir, f'{folder}-{i:02d}.png')
    bg.save(fp)
    n = int(FPS*SECS)
    for k in range(n):
        z = ZOOM0 + (ZOOM1-ZOOM0)*(k/(n-1))
        manifest.append(f'{fp} {z:.4f}')
mpath = os.path.join(outdir, f'{folder}.manifest.txt')
open(mpath,'w').write('\n'.join(manifest))
print(f'{len(slides)} slides, {len(manifest)} frames -> {mpath}')
