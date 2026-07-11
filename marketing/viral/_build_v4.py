#!/usr/bin/env python3
# ============================================================
# PARFECT · v4 "ILUSTRADO EDITORIAL" — estilo Scratch AI
# 4K (2160x2160): fondos crema / verde bosque, titulo serif
# gigante, ilustracion plana grande (golfista sin rostro con
# gorra lima, carrito, perro, arbol, bandera, flecha), numero
# grande por item + spot illustration. Sin caras, sin neon.
# Reusa el copy de _build_viral (C1/C2/CAROUSELS).
# Salida: v4-<carpeta>/  (mismos nombres de carpeta con prefijo)
# ============================================================
import os, math
from PIL import Image, ImageDraw, ImageFilter
import _build_viral as V

HERE=os.path.dirname(os.path.abspath(__file__))
S=2160
GEO   = lambda s: V.ImageFont.truetype(V.FP+'Georgia Bold.ttf', s)
BOLD  = lambda s: V.ImageFont.truetype(V.FP+'Arial Bold.ttf', s)
BLACK = lambda s: V.ImageFont.truetype(V.FP+'Arial Black.ttf', s)
BOLDIT= lambda s: V.ImageFont.truetype(V.FP+'Arial Bold Italic.ttf', s)

LIME=(199,238,84); LIMEDK=(150,196,52)
CREAM=dict(bg=(242,237,224), ink=(30,58,44), sub=(112,126,104),
    gA=(133,172,96), gB=(101,146,77), sky=None, cloud=(255,255,255),
    sun=(255,224,138), pill=(30,58,44), pilltx=(242,237,224))
FOREST=dict(bg=(28,56,42), ink=(240,231,206), sub=(172,186,164),
    gA=(45,88,62), gB=(60,108,75), sky=None, cloud=(224,228,214),
    sun=(246,222,140), pill=(240,231,206), pilltx=(28,56,42))
SKIN=(224,181,132); OUTFIT=(28,30,34); TRUNK=(124,86,52)
DOG=(219,141,76); CARTB=(248,246,238); WHEEL=(40,42,46)

def base(pal):
    b=Image.new('RGB',(S,S),pal['bg']).convert('RGBA')
    d=ImageDraw.Draw(b,'RGBA')
    return b,d

def wordmark(d,cx,y,ink,size=64):
    f=BOLDIT(size); txt='PARFECT'; tw=d.textlength(txt,font=f)
    x=cx-tw/2
    fl=size*0.95
    d.line([(x-size*0.55,y-fl*0.5),(x-size*0.55,y+fl*0.5)],fill=ink,width=max(6,size//9))
    d.polygon([(x-size*0.55,y-fl*0.5),(x-size*0.55+fl*0.75,y-fl*0.22),(x-size*0.55,y-fl*0.02)],fill=LIME)
    d.text((x+size*0.1,y),txt,font=f,fill=ink,anchor='lm')

def pagepill(d,n,total,pal):
    f=BOLD(44)
    d.rounded_rectangle([S-300,96,S-110,180],42,fill=pal['pill'])
    d.text((S-205,138),f'{n}/{total}',font=f,fill=pal['pilltx'],anchor='mm')

def footer(d,pal):
    d.text((S//2,S-84),'@parfect.golf',font=BOLD(42),fill=pal['sub'],anchor='mm')

# ---------------- ILUSTRACION PLANA ----------------
def sun(d,cx,cy,r,pal):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=pal['sun'])
def cloud(d,cx,cy,s,pal):
    for dx,dy,r in [(-1.1,0.1,0.62),(0,-0.28,0.8),(1.05,0.06,0.6)]:
        rr=r*s; d.ellipse([cx+dx*s-rr,cy+dy*s-rr,cx+dx*s+rr,cy+dy*s+rr],fill=pal['cloud'])
    d.rounded_rectangle([cx-1.6*s,cy,cx+1.6*s,cy+0.62*s],int(0.31*s),fill=pal['cloud'])

def ground(d,ytop,pal):
    d.ellipse([-S*0.55,ytop,S*0.75,ytop+S*0.95],fill=pal['gA'])
    d.ellipse([S*0.35,ytop+40,S*1.55,ytop+S*0.9],fill=pal['gB'])
    d.rectangle([0,min(ytop+S*0.32,S-2),S,S],fill=pal['gB'])
    d.ellipse([-S*0.2,ytop+S*0.16,S*0.85,ytop+S*0.75],fill=pal['gA'])

def tree(d,x,y,s):
    d.rounded_rectangle([x-0.05*s,y-0.55*s,x+0.05*s,y],int(0.05*s),fill=TRUNK)
    d.ellipse([x-0.42*s,y-1.25*s,x+0.18*s,y-0.55*s],fill=(58,104,66))
    d.ellipse([x-0.18*s,y-1.45*s,x+0.44*s,y-0.62*s],fill=(77,130,82))

def flagpin(d,x,y,s,flagcolor=(226,84,64)):
    d.ellipse([x-0.30*s,y-0.055*s,x+0.30*s,y+0.075*s],fill=(240,240,228))
    d.ellipse([x-0.085*s,y-0.03*s,x+0.085*s,y+0.03*s],fill=(30,34,32))
    d.line([(x,y),(x,y-1.05*s)],fill=(238,236,226),width=max(6,int(0.045*s)))
    d.polygon([(x,y-1.05*s),(x+0.52*s,y-0.87*s),(x,y-0.70*s)],fill=flagcolor)

def dog(d,x,y,s):
    d.rounded_rectangle([x-0.36*s,y-0.30*s,x+0.30*s,y+0.02*s],int(0.16*s),fill=DOG)
    for lx in (-0.26,-0.12,0.08,0.2):
        d.rounded_rectangle([x+lx*s,y-0.06*s,x+(lx+0.08)*s,y+0.22*s],int(0.03*s),fill=DOG)
    d.ellipse([x+0.20*s,y-0.56*s,x+0.52*s,y-0.24*s],fill=DOG)
    d.polygon([(x+0.26*s,y-0.52*s),(x+0.34*s,y-0.72*s),(x+0.40*s,y-0.5*s)],fill=(184,110,54))
    d.ellipse([x+0.44*s,y-0.40*s,x+0.54*s,y-0.30*s],fill=(66,42,26))
    p=[(x-0.34*s,y-0.28*s),(x-0.52*s,y-0.52*s),(x-0.44*s,y-0.24*s)]
    d.polygon(p,fill=DOG)

def cart(d,x,y,s):
    d.rounded_rectangle([x-0.62*s,y-0.44*s,x+0.62*s,y-0.02*s],int(0.10*s),fill=CARTB)
    d.rounded_rectangle([x-0.66*s,y-1.02*s,x+0.66*s,y-0.92*s],int(0.05*s),fill=OUTFIT)
    d.line([(x-0.52*s,y-0.92*s),(x-0.52*s,y-0.44*s)],fill=OUTFIT,width=max(6,int(0.05*s)))
    d.line([(x+0.52*s,y-0.92*s),(x+0.52*s,y-0.44*s)],fill=OUTFIT,width=max(6,int(0.05*s)))
    d.rounded_rectangle([x-0.30*s,y-0.78*s,x+0.06*s,y-0.44*s],int(0.06*s),fill=(214,208,190))
    for wx in (-0.40,0.40):
        d.ellipse([x+wx*s-0.15*s,y-0.15*s,x+wx*s+0.15*s,y+0.15*s],fill=WHEEL)
        d.ellipse([x+wx*s-0.06*s,y-0.06*s,x+wx*s+0.06*s,y+0.06*s],fill=(210,210,206))
    d.rounded_rectangle([x+0.30*s,y-0.86*s,x+0.46*s,y-0.5*s],int(0.05*s),fill=(178,58,46))

def golfer(d,x,y,s,outfit=OUTFIT):
    """flat, sin rostro, top-of-backswing; gorra lima = firma de marca"""
    lw=max(8,int(0.070*s))
    d.rounded_rectangle([x-0.20*s,y-0.52*s,x-0.04*s,y],int(0.045*s),fill=outfit)          # pierna izq
    d.rounded_rectangle([x+0.02*s,y-0.52*s,x+0.18*s,y],int(0.045*s),fill=outfit)          # pierna der
    d.rounded_rectangle([x-0.26*s,y-0.06*s,x-0.02*s,y+0.02*s],int(0.03*s),fill=(250,250,246))  # zapato
    d.rounded_rectangle([x+0.0*s,y-0.06*s,x+0.24*s,y+0.02*s],int(0.03*s),fill=(250,250,246))
    d.rounded_rectangle([x-0.22*s,y-1.08*s,x+0.20*s,y-0.46*s],int(0.11*s),fill=outfit)    # torso
    # brazos cortos hacia arriba (backswing) + palo, detras de la cabeza
    d.line([(x-0.02*s,y-0.94*s),(x-0.26*s,y-1.18*s)],fill=SKIN,width=lw)
    d.line([(x+0.10*s,y-0.94*s),(x-0.22*s,y-1.22*s)],fill=SKIN,width=lw)
    d.line([(x-0.25*s,y-1.21*s),(x-0.68*s,y-1.50*s)],fill=(120,124,130),width=max(6,int(0.042*s)))
    d.rounded_rectangle([x-0.78*s,y-1.58*s,x-0.64*s,y-1.48*s],int(0.03*s),fill=(70,74,80))
    d.ellipse([x-0.13*s,y-1.44*s,x+0.13*s,y-1.18*s],fill=SKIN)                            # cabeza
    d.pieslice([x-0.15*s,y-1.49*s,x+0.15*s,y-1.19*s],180,360,fill=LIMEDK)                 # gorra lima
    d.rounded_rectangle([x+0.06*s,y-1.37*s,x+0.30*s,y-1.30*s],int(0.03*s),fill=LIMEDK)    # visera
    d.ellipse([x-0.56*s,y-0.045*s,x-0.48*s,y+0.035*s],fill=(252,252,248))                 # bola

def arrow_up(d,x,y,s,color):
    w=0.16*s
    d.line([(x-0.75*s,y),(x+0.15*s,y-0.75*s)],fill=color,width=int(w))
    d.polygon([(x+0.02*s,y-0.94*s),(x+0.42*s,y-0.94*s),(x+0.42*s,y-0.54*s)],fill=color)

def balls(d,x,y,s):
    d.polygon([(x-0.4*s,y),(x+0.4*s,y),(x+0.3*s,y-0.55*s),(x-0.3*s,y-0.55*s)],fill=(198,190,168))
    for i,(dx,dy) in enumerate([(-0.16,-0.62),(0,-0.7),(0.16,-0.62),(-0.08,-0.56),(0.08,-0.56)]):
        d.ellipse([x+dx*s-0.07*s,y+dy*s-0.07*s,x+dx*s+0.07*s,y+dy*s+0.07*s],fill=(252,252,248))

def chartbars(d,x,y,s,pal):
    hs=[0.34,0.52,0.74,1.0]
    for i,h in enumerate(hs):
        col=LIMEDK if i==len(hs)-1 else pal['sub']
        d.rounded_rectangle([x+i*0.30*s,y-h*s,x+i*0.30*s+0.22*s,y],int(0.04*s),fill=col)
    arrow_up(d,x+1.35*s,y-0.1*s,s*0.85,LIMEDK)

def trophy(d,x,y,s):
    gold=(233,183,74)
    d.rounded_rectangle([x-0.30*s,y-0.85*s,x+0.30*s,y-0.35*s],int(0.10*s),fill=gold)
    d.polygon([(x-0.30*s,y-0.60*s),(x-0.48*s,y-0.80*s),(x-0.34*s,y-0.42*s)],fill=gold)
    d.polygon([(x+0.30*s,y-0.60*s),(x+0.48*s,y-0.80*s),(x+0.34*s,y-0.42*s)],fill=gold)
    d.rounded_rectangle([x-0.07*s,y-0.38*s,x+0.07*s,y-0.16*s],int(0.03*s),fill=gold)
    d.rounded_rectangle([x-0.22*s,y-0.16*s,x+0.22*s,y],int(0.04*s),fill=(150,112,42))

def putt_scene(d,x,y,s,pal):
    d.ellipse([x-1.1*s,y-0.30*s,x+1.1*s,y+0.16*s],fill=pal['gA'])
    flagpin(d,x+0.5*s,y-0.05*s,s*0.9)
    for i in range(5):
        t=i/4.0; bx=x-0.9*s+t*(1.2*s); by=y-0.02*s-math.sin(t*math.pi)*0.12*s
        r=0.035*s*(1-t*0.4); d.ellipse([bx-r,by-r,bx+r,by+r],fill=(252,252,248))

SPOTS=['golf','cart','putt','balls','chart','trophy','dogtree']
def spot(d,kind,cy,pal):
    cx=S//2
    if kind=='golf':
        golfer(d,cx+30,cy,400); flagpin(d,cx+560,cy-20,360); tree(d,cx-640,cy-10,360)
    elif kind=='cart':
        cart(d,cx,cy-40,420); tree(d,cx-720,cy,360)
    elif kind=='putt':
        putt_scene(d,cx,cy-70,460,pal)
    elif kind=='balls':
        balls(d,cx-180,cy,420); golfer(d,cx+400,cy,340)
    elif kind=='chart':
        chartbars(d,cx-460,cy,380,pal)
    elif kind=='trophy':
        trophy(d,cx,cy,420); cloud(d,cx-660,cy-520,70,pal); cloud(d,cx+620,cy-460,60,pal)
    elif kind=='dogtree':
        dog(d,cx-200,cy-30,340); tree(d,cx+540,cy,380); cloud(d,cx-720,cy-540,70,pal)

# ---------------- SLIDES ----------------
def slide_title(kicker,title_lines,n,total,pal,flip=False):
    b,d=base(pal)
    # --- ESCENA primero (banda inferior estricta: nada sube de y=1150) ---
    gy=S-620                                   # horizonte
    sun(d,S-330,1290,105,pal)
    cloud(d,400,1250,90,pal); cloud(d,1150,1360,65,pal)
    ground(d,gy,pal)
    tree(d,220,gy+420,470)
    golfer(d,680,gy+560,590)
    dog(d,1040,gy+560,330)
    cart(d,1560,gy+580,440)
    flagpin(d,S-200,gy+370,400)
    # --- TEXTO al final, siempre encima, en su banda (termina antes de 1120) ---
    wordmark(d,S//2,190,pal['ink']); pagepill(d,n,total,pal)
    d.text((S//2,330),kicker.upper(),font=BOLD(52),fill=pal['sub'],anchor='mm')
    tmp=ImageDraw.Draw(Image.new('RGB',(10,10)))
    fs=185
    while True:
        wide=max(tmp.textlength(l,font=GEO(fs)) for l in title_lines)
        hgt=len(title_lines)*(fs+34)
        if (wide<=S-260 and 445+hgt<=1160) or fs<=110: break
        fs-=5
    ty=445+fs//2
    for ln in title_lines:
        d.text((S//2,ty),ln,font=GEO(fs),fill=pal['ink'],anchor='mm'); ty+=fs+34
    footer(d,pal)
    return V.fin(b)

def slide_item(num,text,n,total,pal):
    b,d=base(pal)
    wordmark(d,S//2,190,pal['ink']); pagepill(d,n,total,pal)
    d.text((S//2,450),f'{num}.',font=GEO(220),fill=pal['ink'],anchor='mm')
    tmp=ImageDraw.Draw(Image.new('RGB',(10,10)))
    fs=96; lines=V.wraptext(tmp,text,GEO(fs),S-520)
    while len(lines)*(fs+30)>620 and fs>62:
        fs-=6; lines=V.wraptext(tmp,text,GEO(fs),S-520)
    ty=640+fs//2
    for ln in lines:
        d.text((S//2,ty),ln,font=GEO(fs),fill=pal['ink'],anchor='mm'); ty+=fs+30
    spot(d,SPOTS[(num-1)%len(SPOTS)],S-220,pal)
    footer(d,pal)
    return V.fin(b)

def slide_cta(headline,sub,shotfile,n,total,pal):
    b,d=base(pal)
    wordmark(d,S//2,190,pal['ink']); pagepill(d,n,total,pal)
    tmp=ImageDraw.Draw(Image.new('RGB',(10,10)))
    fs=120
    while tmp.textlength(headline,font=GEO(fs))>S-240 and fs>72: fs-=5
    d.text((S//2,380),headline,font=GEO(fs),fill=pal['ink'],anchor='mm')
    fs2=56
    while tmp.textlength(sub,font=BOLD(fs2))>S-260 and fs2>38: fs2-=4
    d.text((S//2,510),sub,font=BOLD(fs2),fill=pal['sub'],anchor='mm')
    # telefono con screenshot real
    try:
        shot=Image.open(os.path.join(V.ASSETS,shotfile)).convert('RGBA')
        ph=1130; r=(ph-90)/shot.height
        shot=shot.resize((round(shot.width*r),ph-90),Image.LANCZOS)
        pw=shot.width+90
        fx,fy=S//2-pw//2,620
        d.rounded_rectangle([fx,fy,fx+pw,fy+ph],110,fill=(24,26,30))
        b.alpha_composite(shot,(fx+45,fy+45))
        d=ImageDraw.Draw(b,'RGBA')
        d.rounded_rectangle([S//2-130,fy+18,S//2+130,fy+40],12,fill=(24,26,30))
    except Exception: pass
    d.rounded_rectangle([S//2-620,S-370,S//2+620,S-220],75,fill=pal['ink'])
    d.text((S//2,S-295),'PRUÉBALA GRATIS · LINK EN BIO',font=BLACK(58),fill=pal['bg'],anchor='mm')
    d.text((S//2,S-150),'studioamr.github.io/parfect',font=BOLD(46),fill=pal['sub'],anchor='mm')
    footer(d,pal)
    return V.fin(b)

def build(folder,kicker,title_lines,items,cta_headline,cta_sub,shotfile,pal):
    total=len(items)+2
    V.save(slide_title(kicker,title_lines,1,total,pal),'v4-'+folder,'01.png')
    for i,t in enumerate(items):
        V.save(slide_item(i+1,t,i+2,total,pal),'v4-'+folder,f'{i+2:02d}.png')
    V.save(slide_cta(cta_headline,cta_sub,shotfile,total,total,pal),'v4-'+folder,f'{total:02d}.png')

if __name__=='__main__':
    pals=[CREAM,FOREST]
    build('carrusel1-verdades','Golf · Datos',['8 verdades del golf','que nadie','te dice'],V.C1_TRUTHS,
          '¿Dónde pierdes golpes?','PARFECT te lo dice con tus propios datos.','shot-analisis.png',FOREST)
    build('carrusel2-bajar-hcp','Baja tu hándicap',['5 formas de','mejorar tu golf','más rápido'],V.C2_TIPS,
          'Qué practicar hoy','PARFECT arma tu plan con tus rondas reales.','shot-rondas.png',CREAM)
    for i,spec in enumerate(V.CAROUSELS):
        tl=[l.title() if l.isupper() else l for l in spec['title_lines']]
        tl=[l.capitalize() for l in [x.lower() for x in spec['title_lines']]]
        build(spec['folder'],spec['kicker'].title(),tl,spec['items'],
              spec['cta_headline'].title().rstrip('.'),spec['cta_sub'].capitalize(),
              spec['shotfile'],pals[i%2])
    print('v4 listo: 13 carruseles ilustrados en 4K (v4-*/)')
