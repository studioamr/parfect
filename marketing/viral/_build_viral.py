#!/usr/bin/env python3
# Carruseles estilo "viral golf" (fondo oscuro, titulo gigante, ilustracion plana
# grande) como las referencias tipo Scratch AI / TikTok de golf. Copy honesto:
# el CTA final no usa badges falsos de tienda (la app aun no esta publicada).
import os, math
from PIL import Image, ImageDraw, ImageFont

HERE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, '..', '..', 'assets'))
OUT    = HERE
S = 1080

FP='/System/Library/Fonts/Supplemental/'
BLACK  = lambda s: ImageFont.truetype(FP+'Arial Black.ttf', s)
BOLD   = lambda s: ImageFont.truetype(FP+'Arial Bold.ttf', s)
BOLDIT = lambda s: ImageFont.truetype(FP+'Arial Bold Italic.ttf', s)

DARK=(15,20,15); DARK2=(22,30,20)
INK=(27,42,24); MUT_D=(150,166,140); MUT_L=(111,126,96)
LIME=(199,238,84); LIMEINK=(44,58,22)
WHITE=(255,255,255); CREAM=(240,238,224)
SKY=[(238,246,223),(225,239,198),(206,229,166)]

def lerp(a,b,t): return tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def vgrad(w,h,stops):
    col=Image.new('RGB',(1,h)); px=col.load(); n=len(stops)-1
    for y in range(h):
        t=y/(h-1); seg=min(int(t*n),n-1); lt=t*n-seg
        px[0,y]=lerp(stops[seg],stops[seg+1],lt)
    return col.resize((w,h))

def wordmark(d,cx,y,size=38,color=LIME,textcolor=WHITE):
    f=BOLDIT(size); txt='PARFECT'; tw=d.textlength(txt,font=f); fl=int(size*0.95)
    px=cx-tw/2-int(size*1.05)
    d.line([(px,y-fl*0.5),(px,y+fl*0.5)],fill=textcolor,width=max(3,int(size*0.10)))
    d.polygon([(px,y-fl*0.5),(px+fl*0.7,y-fl*0.30),(px,y-fl*0.10)],fill=color)
    d.text((cx+int(size*0.18),y),txt,font=f,fill=textcolor,anchor='lm')

def dark_base():
    b=vgrad(S,S,[DARK,DARK2]).convert('RGBA'); d=ImageDraw.Draw(b)
    wordmark(d,S//2,60); return b,d

def light_base():
    b=vgrad(S,S,SKY).convert('RGBA'); d=ImageDraw.Draw(b)
    wordmark(d,S//2,60,color=LIME,textcolor=LIMEINK); return b,d

def pagepill(d,n,total,dark=True):
    txt=f'{n}/{total}'
    fill=(255,255,255,235) if dark else (44,58,22,230)
    fg = INK if dark else WHITE
    d.rounded_rectangle([S-140,32,S-40,78],23,fill=fill)
    d.text((S-90,55),txt,font=BOLD(24),fill=fg,anchor='mm')

def wraptext(d,text,font,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def footer_dark(d,sub='@parfect.golf'):
    d.text((S//2,1044),sub,font=BOLD(24),fill=MUT_D,anchor='mm')
def footer_light(d,sub='@parfect.golf'):
    d.text((S//2,1044),sub,font=BOLD(24),fill=MUT_L,anchor='mm')
def fin(b): return b.convert('RGB')

# ---------- personaje 3D REAL de la marca (assets/*.png), no ilustracion a mano ----------
def paste_char(base, name, cx, cy, h, glow=True):
    im=Image.open(os.path.join(ASSETS,name)).convert('RGBA')
    r=h/im.height; im=im.resize((round(im.width*r),h))
    x,y=round(cx-im.width/2),round(cy-im.height/2)
    if glow:
        a=im.split()[3].point(lambda p: min(255,int(p*0.55)))
        sh=Image.new('RGBA',im.size,LIME+(0,)); sh.putalpha(a)
        sh=sh.filter(__import__('PIL.ImageFilter',fromlist=['ImageFilter']).GaussianBlur(18))
        base.alpha_composite(sh,(x,y))
    base.alpha_composite(im,(x,y))

# ---------- slide de titulo (fondo oscuro, ilustracion grande) ----------
def slide_title(kicker, title_lines, n, total):
    b,d=dark_base(); pagepill(d,n,total,dark=True)
    d.rounded_rectangle([S//2-220,150,S//2+220,204],27,fill=LIME)
    d.text((S//2,177),kicker,font=BLACK(28),fill=LIMEINK,anchor='mm')
    y=260
    for ln in title_lines:
        d.text((S//2,y),ln,font=BLACK(70),fill=CREAM,anchor='mm'); y+=82
    paste_char(b, 'golfer.png', S//2, 760, 400)
    footer_dark(d,'desliza → · @parfect.golf'); return fin(b)

# ---------- slide de item numerado (fondo oscuro) ----------
def slide_item(num, text, n, total):
    b,d=dark_base(); pagepill(d,n,total,dark=True)
    cy=175
    d.text((S//2,cy),str(num),font=BLACK(140),fill=LIME,anchor='mm')
    d.line([(S//2-70,cy+84),(S//2+70,cy+84)],fill=LIME,width=6)
    lines=wraptext(d,text,BLACK(54),860)
    total_h=len(lines)*68
    ty=440-total_h//2
    for ln in lines:
        d.text((S//2,ty),ln,font=BLACK(54),fill=CREAM,anchor='mm'); ty+=68
    paste_char(b, 'eagle.png', S//2, 870, 260)
    footer_dark(d); return fin(b)

# ---------- slide CTA final (fondo CLARO = marca real, sin badges falsos) ----------
def slide_cta(headline, sub, shotfile='shot-inicio.png'):
    b,d=light_base()
    d.text((S//2,150),headline,font=BLACK(54),fill=INK,anchor='mm')
    d.text((S//2,212),sub,font=BOLD(30),fill=MUT_L,anchor='mm')
    try:
        shot=Image.open(os.path.join(ASSETS,shotfile)).convert('RGBA')
        r=560/shot.height; shot=shot.resize((round(shot.width*r),560))
        fx,fy=S//2-shot.width//2, 300
        sh=Image.new('RGBA',(S,S),(0,0,0,0))
        ImageDraw.Draw(sh).rounded_rectangle([fx-14,fy+14,fx+shot.width+14,fy+shot.height+34],36,fill=(44,58,22,60))
        b.alpha_composite(sh); b.alpha_composite(shot,(fx,fy))
    except Exception:
        pass
    d.rounded_rectangle([S//2-330,910,S//2+330,978],34,fill=LIME)
    d.text((S//2,944),'REGÍSTRATE GRATIS · LINK EN BIO',font=BLACK(26),fill=LIMEINK,anchor='mm')
    footer_light(d,'parfectapp.github.io/parfect'); return fin(b)

def save(img,folder,name):
    p=os.path.join(OUT,folder); os.makedirs(p,exist_ok=True)
    img.save(os.path.join(p,name))

# ============================================================
# CARRUSEL 1 — "8 verdades del golf que nadie te dice"
# ============================================================
C1_TRUTHS = [
    'Tu problema no es el swing. Son los 3-putts que ni siquiera ves venir.',
    'Pegar más lejos no baja tu hándicap. Fallar menos fairways sí.',
    'El golpe que más te cuesta no es el drive: es el chip que dejas corto.',
    'Jugar más rondas no te mejora. Practicar lo que de verdad falla, sí.',
    'Un putt de 1 metro pesa lo mismo en tu tarjeta que un drive de 250 yardas.',
    'Nadie baja de hándicap adivinando qué practicar la próxima vez.',
    'Tu hándicap no miente. Pero si no lo mides hoyo por hoyo, no sabes en qué.',
    'Los datos no son solo para pros: son para cualquiera que quiera mejorar rápido.',
]
def build_c1():
    total=len(C1_TRUTHS)+2
    save(slide_title('GOLF · DATOS',['8 VERDADES DEL','GOLF QUE NADIE','TE DICE'],1,total),'carrusel1-verdades','01.png')
    for i,t in enumerate(C1_TRUTHS):
        save(slide_item(i+1,t,i+2,total),'carrusel1-verdades',f'{i+2:02d}.png')
    save(slide_cta('¿Y TÚ EN QUÉ PIERDES','GOLPES SIN SABERLO?','shot-analisis.png'),'carrusel1-verdades',f'{total:02d}.png')

# ============================================================
# CARRUSEL 2 — "5 formas de bajar tu hándicap rápido"
# ============================================================
C2_TIPS = [
    'Deja de adivinar qué practicar: mide primero, entrena después.',
    'Prioriza greens en regulación antes que pegarle más lejos.',
    'Cuenta tus putts hoyo por hoyo, no solo el total al final.',
    'Entrena 20 minutos con un objetivo claro, no 2 horas sin rumbo.',
    'Compara cada ronda contra el hándicap al que quieres llegar.',
]
def build_c2():
    total=len(C2_TIPS)+2
    save(slide_title('BAJA TU HÁNDICAP',['5 FORMAS DE','MEJORAR TU GOLF','MÁS RÁPIDO'],1,total),'carrusel2-bajar-hcp','01.png')
    for i,t in enumerate(C2_TIPS):
        save(slide_item(i+1,t,i+2,total),'carrusel2-bajar-hcp',f'{i+2:02d}.png')
    save(slide_cta('PARFECT TE DICE','QUÉ PRACTICAR HOY','shot-rondas.png'),'carrusel2-bajar-hcp',f'{total:02d}.png')

# ============================================================
# CARRUSEL 3 — gancho de un solo dato
# ============================================================
def build_c3():
    b,d=dark_base()
    d.text((S//2,180),'EL DATO QUE MÁS',font=BLACK(56),fill=CREAM,anchor='mm')
    d.text((S//2,248),'GOLPES TE CUESTA',font=BLACK(56),fill=CREAM,anchor='mm')
    d.rounded_rectangle([140,360,S-140,760],40,fill=(24,32,22))
    d.text((S//2,428),'UP & DOWN',font=BOLD(32),fill=MUT_D,anchor='mm')
    d.text((S//2,600),'41%',font=BLACK(190),fill=LIME,anchor='mm')
    d.text((S//2,708),'de tus greens fallados',font=BOLD(28),fill=CREAM,anchor='mm')
    d.text((S//2,860),'y ni te habías dado cuenta',font=BOLDIT(32),fill=MUT_D,anchor='mm')
    footer_dark(d); save(fin(b),'carrusel3-dato','01.png')
    save(slide_cta('MIDE TU JUEGO','DE VERDAD','shot-logros.png'),'carrusel3-dato','02.png')

def flatten():
    dest=os.path.join(OUT,'contenido')
    os.makedirs(dest,exist_ok=True)
    for f in os.listdir(dest):
        if f.endswith('.png'): os.remove(os.path.join(dest,f))
    for folder in ('carrusel1-verdades','carrusel2-bajar-hcp','carrusel3-dato'):
        src=os.path.join(OUT,folder)
        for f in sorted(os.listdir(src)):
            if f.endswith('.png'):
                Image.open(os.path.join(src,f)).save(os.path.join(dest,f'{folder}-{f}'))

if __name__=='__main__':
    build_c1(); build_c2(); build_c3(); flatten()
    print('listo: carrusel1-verdades (10), carrusel2-bajar-hcp (7), carrusel3-dato (2) + contenido/ (flat)')
