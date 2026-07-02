#!/usr/bin/env python3
# Slideshow PRO: transiciones crossfade + Ken Burns suave + pacing por rol.
# Genera frames 1080x1920 (fondo blur oscurecido + lamina), reusa base en holds
# y guarda solo los frames de transicion (crossfade). Escribe manifest para _encode.
import os, sys
from PIL import Image, ImageFilter, ImageEnhance, Image as IM

W,H = 2160,3840
FPS = 30
XF = 10                 # frames de crossfade (~0.33s)
folder = sys.argv[1] if len(sys.argv)>1 else 'carrusel1-verdades'
HERE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(HERE, folder)
outdir = os.path.join(HERE, '_pro_frames'); os.makedirs(outdir, exist_ok=True)
for f in os.listdir(outdir):
    if f.startswith(folder): os.remove(os.path.join(outdir,f))

slides = sorted(f for f in os.listdir(src) if f.endswith('.png'))

def base_frame(path):
    im = Image.open(path).convert('RGB')
    bg = im.resize((H,H)).crop(((H-W)//2,0,(H-W)//2+W,H)).filter(ImageFilter.GaussianBlur(110))
    bg = ImageEnhance.Brightness(bg).enhance(0.45)
    fg = im.resize((W,W), Image.LANCZOS)
    bg.paste(fg,(0,(H-W)//2))
    return bg

bases=[]
for i,f in enumerate(slides):
    bf = base_frame(os.path.join(src,f))
    p = os.path.join(outdir, f'{folder}-base-{i:02d}.png'); bf.save(p); bases.append((p,bf))

def hold_for(i):
    if i==0: return int(FPS*3.2)          # gancho aguanta
    if i==len(slides)-1: return int(FPS*3.4)  # CTA aguanta
    return int(FPS*2.3)

manifest=[]
z0,z1 = 1.0,1.06
for i,(p,bf) in enumerate(bases):
    n=hold_for(i)
    for k in range(n):
        z=z0+(z1-z0)*(k/max(1,n-1))
        manifest.append(f'{p} {z:.4f}')
    if i < len(bases)-1:                    # crossfade hacia el siguiente
        nxt=bases[i+1][1]
        for t in range(1,XF+1):
            a=t/(XF+1)
            blend=Image.blend(bf,nxt,a)
            fp=os.path.join(outdir,f'{folder}-xf-{i:02d}-{t:02d}.png'); blend.save(fp)
            manifest.append(f'{fp} 1.0000')
mpath=os.path.join(outdir,f'{folder}.manifest.txt'); open(mpath,'w').write('\n'.join(manifest))
print(f'{len(slides)} slides, {len(manifest)} frames -> {mpath}')
