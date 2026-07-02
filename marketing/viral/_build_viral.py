#!/usr/bin/env python3
# ============================================================
# PARFECT · Sistema de diseño "EDITORIAL DE DATOS" (v3, pro)
# Concepto: analytics deportivo premium (Whoop/Strava): navy
# profundo, tipografia gigante, UN acento lima, retícula fina,
# motivos de datos reales (barras, trayectoria de bola punteada).
# Serie hermana "PAPEL" (editorial claro) para quotes/memes.
# Sin personajes caricatura. Sin ruido.
# ============================================================
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, '..', '..', 'assets'))
OUT    = HERE
S = 1080
H = S
M = 56                      # margen de la retícula

FP='/System/Library/Fonts/Supplemental/'
BLACK  = lambda s: ImageFont.truetype(FP+'Arial Black.ttf', s)
BOLD   = lambda s: ImageFont.truetype(FP+'Arial Bold.ttf', s)
BOLDIT = lambda s: ImageFont.truetype(FP+'Arial Bold Italic.ttf', s)
GEO    = lambda s: ImageFont.truetype(FP+'Georgia Bold.ttf', s)
GEOIT  = lambda s: ImageFont.truetype(FP+'Georgia Bold Italic.ttf', s)
def MONO(s):
    try: return ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', s, index=1)
    except Exception: return ImageFont.truetype(FP+'Courier New Bold.ttf', s)

# --- tokens ---
NAVY=(11,17,36); NAVY2=(15,23,48); NAVY3=(26,36,70)
PAPER=(246,246,241); PAPER2=(238,239,230)
INKW=(240,243,235)          # texto sobre navy
INKD=(17,24,46)             # texto sobre papel
MUTW=(136,146,174)          # apagado sobre navy
MUTP=(122,127,118)          # apagado sobre papel
LIME=(199,238,84); LIMEINK=(36,48,14)
HAIRW=(255,255,255,30); HAIRD=(17,24,46,42)
RED=(226,88,74)

# compat con codigo previo
INK2=INKD; GREENINK=(29,105,58); MUT2=MUTP

def lerp(a,b,t): return tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def vgrad(w,h,stops):
    col=Image.new('RGB',(1,h)); px=col.load(); n=len(stops)-1
    for y in range(h):
        t=y/(h-1); seg=min(int(t*n),n-1); lt=t*n-seg
        px[0,y]=lerp(stops[seg],stops[seg+1],lt)
    return col.resize((w,h))

def wraptext(d,text,font,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def mono_label(d,x,y,txt,size,fill,ls=5,anchor='l'):
    f=MONO(size)
    wt=sum(d.textlength(c,font=f)+ls for c in txt)-ls
    cx = x-wt/2 if anchor=='m' else (x-wt if anchor=='r' else x)
    for c in txt:
        d.text((cx,y),c,font=f,fill=fill,anchor='lm')
        cx+=d.textlength(c,font=f)+ls
    return wt

def soft_glow(b,cx,cy,r,color,alpha):
    layer=Image.new('RGBA',(S,S),(0,0,0,0))
    ImageDraw.Draw(layer).ellipse([cx-r,cy-r,cx+r,cy+r],fill=color+(alpha,))
    layer=layer.filter(ImageFilter.GaussianBlur(r//2))
    b.alpha_composite(layer)

def wordmark_left(d,x,y,size=30,ink=INKW):
    f=BOLDIT(size); fl=int(size*0.95)
    d.line([(x,y-fl*0.5),(x,y+fl*0.5)],fill=ink,width=max(3,int(size*0.11)))
    d.polygon([(x,y-fl*0.5),(x+fl*0.72,y-fl*0.28),(x,y-fl*0.08)],fill=LIME)
    d.text((x+int(size*0.55),y),'PARFECT',font=f,fill=ink,anchor='lm')

def frame(b,d,dark=True,idx=None,total=None):
    hair = HAIRW if dark else HAIRD
    ink  = INKW if dark else INKD
    mut  = MUTW if dark else MUTP
    d.rectangle([M,M,S-M,H-M],outline=hair,width=2)
    tk=18
    for cx,cy,dx,dy in [(M,M,1,1),(S-M,M,-1,1),(M,H-M,1,-1),(S-M,H-M,-1,-1)]:
        d.line([(cx,cy),(cx+tk*dx,cy)],fill=LIME,width=4)
        d.line([(cx,cy),(cx,cy+tk*dy)],fill=LIME,width=4)
    wordmark_left(d,M+30,M+46,ink=ink)
    if idx and total:
        mono_label(d,S-M-28,M+46,f'{idx:02d}/{total:02d}',24,mut,anchor='r')

def footer(d,dark=True,n=None,total=None,right='GOLF · DATOS · MX'):
    mut = MUTW if dark else MUTP
    hair= HAIRW if dark else HAIRD
    d.line([(M+28,H-M-92),(S-M-28,H-M-92)],fill=hair,width=2)
    mono_label(d,M+28,H-M-58,'@PARFECT.GOLF',20,mut)
    mono_label(d,S-M-28,H-M-58,right,20,mut,anchor='r')
    if n and total:
        x0,x1=M+28,S-M-28
        d.rounded_rectangle([x0,H-M-30,x1,H-M-24],3,fill=hair)
        fw=(x1-x0)*(n/total)
        d.rounded_rectangle([x0,H-M-30,x0+fw,H-M-24],3,fill=LIME)

def traj(b,d,x0,y0,x1,y1,arc=150,ndots=26):
    for i in range(ndots):
        t=i/(ndots-1)
        x=x0+(x1-x0)*t; y=y0+(y1-y0)*t-math.sin(t*math.pi)*arc
        r=3.6-2.0*t
        a=int(255-120*t)
        d.ellipse([x-r,y-r,x+r,y+r],fill=LIME+(a,))
    # pin minimal
    d.ellipse([x1-16,y1-5,x1+16,y1+7],outline=LIME,width=3)
    d.line([(x1,y1),(x1,y1-86)],fill=INKW,width=4)
    d.polygon([(x1,y1-86),(x1+46,y1-70),(x1,y1-52)],fill=LIME)

def bars_motif(d,x,y,dark=True,hs=(18,30,44,24,52),bw=10,gap=8):
    mut = MUTW if dark else MUTP
    for i,hh in enumerate(hs):
        col = LIME if hh==max(hs) else mut
        d.rounded_rectangle([x+i*(bw+gap),y-hh,x+i*(bw+gap)+bw,y],3,fill=col)

def base_navy(idx=None,total=None):
    b=vgrad(S,S,[NAVY,NAVY2]).convert('RGBA')
    soft_glow(b,S-120,80,340,LIME,16)
    soft_glow(b,60,H-60,320,(40,70,140),26)
    d=ImageDraw.Draw(b,'RGBA')
    frame(b,d,True,idx,total)
    return b,d

def base_paper(idx=None,total=None):
    b=vgrad(S,S,[PAPER,PAPER2]).convert('RGBA')
    d=ImageDraw.Draw(b,'RGBA')
    frame(b,d,False,idx,total)
    return b,d

# alias de compatibilidad (motor de contenido viejo)
def bright_base(with_course=True): return base_navy()
def white_card(b,x,y,w,h,r=24):
    sh=Image.new('RGBA',(S,S),(0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([x,y+8,x+w,y+h+10],r,fill=(0,0,0,80))
    sh=sh.filter(ImageFilter.GaussianBlur(10)); b.alpha_composite(sh)
    ImageDraw.Draw(b).rounded_rectangle([x,y,x+w,y+h],r,fill=(255,255,255,250))

def mini_icon(d,kind,cx,cy,r,color,bg=None):
    if bg: d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=bg)
    if kind=='check':
        d.line([(cx-r*0.5,cy),(cx-r*0.1,cy+r*0.4),(cx+r*0.55,cy-r*0.45)],fill=color,width=max(4,int(r*0.22)),joint='curve')
    elif kind=='target':
        d.ellipse([cx-r*0.9,cy-r*0.9,cx+r*0.9,cy+r*0.9],outline=color,width=max(3,int(r*0.14)))
        d.ellipse([cx-r*0.45,cy-r*0.45,cx+r*0.45,cy+r*0.45],outline=color,width=max(3,int(r*0.14)))
        d.ellipse([cx-r*0.12,cy-r*0.12,cx+r*0.12,cy+r*0.12],fill=color)
    elif kind=='chart':
        bw=r*0.34
        for i,hh in enumerate([0.5,0.85,1.15]):
            x=cx-r*0.7+i*(bw+r*0.16)
            d.rounded_rectangle([x,cy+r*0.75-r*hh,x+bw,cy+r*0.75],3,fill=color)
    elif kind=='flag':
        d.line([(cx-r*0.3,cy-r*0.8),(cx-r*0.3,cy+r*0.8)],fill=color,width=max(3,int(r*0.14)))
        d.polygon([(cx-r*0.3,cy-r*0.8),(cx+r*0.7,cy-r*0.5),(cx-r*0.3,cy-r*0.2)],fill=color)
    elif kind=='bolt':
        d.polygon([(cx+r*0.1,cy-r*0.9),(cx-r*0.5,cy+r*0.15),(cx-r*0.05,cy+r*0.15),(cx-r*0.15,cy+r*0.9),(cx+r*0.55,cy-r*0.1),(cx+r*0.05,cy-r*0.1)],fill=color)

def paste_char(base,name,cx,cy,h,glow=False):
    im=Image.open(os.path.join(ASSETS,name)).convert('RGBA')
    r=h/im.height; im=im.resize((round(im.width*r),h))
    base.alpha_composite(im,(round(cx-im.width/2),round(cy-im.height/2)))

def paste_shot(b,shotfile,cy,hpx):
    """screenshot real de la app con borde fino lima y sombra"""
    try:
        shot=Image.open(os.path.join(ASSETS,shotfile)).convert('RGBA')
    except Exception:
        return None
    r=hpx/shot.height; shot=shot.resize((round(shot.width*r),hpx),Image.LANCZOS)
    fx,fy=S//2-shot.width//2,cy
    sh=Image.new('RGBA',(S,S),(0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([fx-10,fy+18,fx+shot.width+10,fy+shot.height+34],30,fill=(0,0,0,120))
    sh=sh.filter(ImageFilter.GaussianBlur(14)); b.alpha_composite(sh)
    b.alpha_composite(shot,(fx,fy))
    ImageDraw.Draw(b).rounded_rectangle([fx-3,fy-3,fx+shot.width+3,fy+shot.height+3],18,outline=LIME,width=3)
    return (fx,fy,shot.width,shot.height)

def fin(b): return b.convert('RGB')

def kicker_row(d,y,txt,dark=True):
    d.rectangle([M+40,y-7,M+54,y+7],fill=LIME)
    mono_label(d,M+72,y,txt.upper(),25,LIME if dark else LIMEINK,ls=7)

# ============================================================
# SLIDES DE CARRUSEL
# ============================================================
def slide_title(kicker, title_lines, n, total):
    b,d=base_navy(n,total)
    kicker_row(d,300,kicker)
    ty=372
    fs=88 if max(len(l) for l in title_lines)<=16 else 76
    for ln in title_lines:
        d.text((M+40,ty),ln,font=BLACK(fs),fill=INKW,anchor='lm'); ty+=fs+14
    d.rectangle([M+40,ty+4,M+180,ty+12],fill=LIME)
    traj(b,d,M+70,H-260,S-M-150,H-300,arc=130)
    d=ImageDraw.Draw(b,'RGBA')
    # pill DESLIZA
    px0,px1=S-M-262,S-M-28
    d.rounded_rectangle([px0,H-232,px1,H-176],28,outline=LIME,width=3)
    mono_label(d,(px0+px1)//2,H-204,'DESLIZA →',22,INKW,anchor='m')
    footer(d,True,n,total)
    return fin(b)

def slide_item(num, text, n, total, serie=''):
    b,d=base_navy(n,total)
    ns=f'{num:02d}'
    d.text((M+36,168),ns,font=BLACK(200),fill=NAVY3,anchor='lt',stroke_width=3,stroke_fill=LIME)
    nw=d.textlength(ns,font=BLACK(200))
    if serie:
        mono_label(d,M+60+nw,352,serie.upper(),22,MUTW)
    d.line([(M+40,430),(S-M-40,430)],fill=HAIRW,width=2)
    tmp=ImageDraw.Draw(Image.new('RGB',(10,10)))
    fs=52; lines=wraptext(tmp,text,BLACK(fs),S-2*M-88)
    while len(lines)*(fs+16)>380 and fs>38:
        fs-=4; lines=wraptext(tmp,text,BLACK(fs),S-2*M-88)
    ty=505
    for ln in lines:
        d.text((M+44,ty),ln,font=BLACK(fs),fill=INKW,anchor='lm'); ty+=fs+16
    bars_motif(d,S-M-130,H-140)
    footer(d,True,n,total)
    return fin(b)

def slide_cta(headline, sub, shotfile='shot-inicio.png', n=None, total=None):
    b,d=base_navy(n,total)
    d.text((S//2,225),headline,font=BLACK(50),fill=INKW,anchor='mm')
    d.text((S//2,290),sub,font=BLACK(50),fill=LIME,anchor='mm')
    paste_shot(b,shotfile,352,430)
    d=ImageDraw.Draw(b,'RGBA')
    d.rounded_rectangle([S//2-330,H-238,S//2+330,H-170],34,fill=LIME)
    d.text((S//2,H-204),'PRUÉBALA GRATIS · LINK EN BIO',font=BLACK(26),fill=LIMEINK,anchor='mm')
    footer(d,True,n,total,right='PARFECTAPP.GITHUB.IO/PARFECT')
    return fin(b)

def save(img,folder,name):
    p=os.path.join(OUT,folder); os.makedirs(p,exist_ok=True)
    img.save(os.path.join(p,name))

# ============================================================
# CARRUSELES
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
    save(slide_title('GOLF · DATOS',['8 VERDADES','DEL GOLF QUE','NADIE TE DICE'],1,total),'carrusel1-verdades','01.png')
    for i,t in enumerate(C1_TRUTHS):
        save(slide_item(i+1,t,i+2,total,serie='VERDADES'),'carrusel1-verdades',f'{i+2:02d}.png')
    save(slide_cta('¿Y TÚ EN QUÉ PIERDES','GOLPES SIN SABERLO?','shot-analisis.png',total,total),'carrusel1-verdades',f'{total:02d}.png')

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
        save(slide_item(i+1,t,i+2,total,serie='MÉTODO'),'carrusel2-bajar-hcp',f'{i+2:02d}.png')
    save(slide_cta('PARFECT TE DICE','QUÉ PRACTICAR HOY','shot-rondas.png',total,total),'carrusel2-bajar-hcp',f'{total:02d}.png')

def build_c3():
    b,d=base_navy(1,2)
    kicker_row(d,270,'EL DATO DE HOY')
    d.text((M+40,360),'UP & DOWN',font=BLACK(58),fill=INKW,anchor='lm')
    d.text((M+36,560),'41%',font=BLACK(230),fill=INKW,anchor='lm',stroke_width=2,stroke_fill=LIME)
    x0,x1=M+44,S-M-44
    d.rounded_rectangle([x0,712,x1,724],6,fill=HAIRW)
    d.rounded_rectangle([x0,712,x0+(x1-x0)*0.41,724],6,fill=LIME)
    d.text((M+44,790),'de tus greens fallados — y ni te habías',font=BOLD(32),fill=MUTW,anchor='lm')
    d.text((M+44,834),'dado cuenta de cuántos golpes cuesta.',font=BOLD(32),fill=MUTW,anchor='lm')
    footer(d,True,1,2)
    save(fin(b),'carrusel3-dato','01.png')
    save(slide_cta('MIDE TU JUEGO','DE VERDAD','shot-logros.png',2,2),'carrusel3-dato','02.png')

def build_carousel(folder, kicker, title_lines, items, cta_headline, cta_sub, shotfile, serie=''):
    total=len(items)+2
    save(slide_title(kicker,title_lines,1,total),folder,'01.png')
    for i,t in enumerate(items):
        save(slide_item(i+1,t,i+2,total,serie=serie or kicker),folder,f'{i+2:02d}.png')
    save(slide_cta(cta_headline,cta_sub,shotfile,total,total),folder,f'{total:02d}.png')

CAROUSELS = [
    dict(folder='carrusel4-mitos', kicker='MITOS DEL GOLF', title_lines=['7 MITOS QUE','TE ESTÁN','DETENIENDO'],
        items=[
            'Mito: necesitas pegarle más lejos para bajar tu hándicap. Falso: se ganan más golpes en el juego corto.',
            'Mito: jugar todos los días te hace mejor. Falso: practicar sin objetivo no cambia tu score.',
            'Mito: el putt es cuestión de suerte. Falso: es la parte más medible de tu juego.',
            'Mito: solo los profesionales necesitan estadísticas. Falso: entre más alto tu hándicap, más golpes hay que ganar con datos.',
            'Mito: un hándicap bajo significa que ya no hay nada que mejorar. Falso: siempre hay una fuga de golpes que no ves.',
            'Mito: comprar palos nuevos baja tu hándicap. Falso: ayuda el fitting, pero el hándicap baja con repetición medida.',
            'Mito: necesitas 18 hoyos para que cuente. Falso: hasta 9 hoyos bien anotados te dan datos reales.',
        ], cta_headline='DEJA DE CREER MITOS.', cta_sub='EMPIEZA A MEDIR.', shotfile='shot-analisis.png', serie='MITO'),
    dict(folder='carrusel5-senales', kicker='AUTODIAGNÓSTICO', title_lines=['6 SEÑALES DE','QUE PIERDES','GOLPES SIN','DARTE CUENTA'],
        items=[
            'No sabes tu porcentaje real de fairways.',
            'Cuentas solo tu score total, nunca tus putts por ronda.',
            'No sabes cuántos greens tomas en regulación.',
            'Sientes que jugaste bien, pero tu tarjeta dice otra cosa.',
            'Practicas exactamente lo mismo que hace un año.',
            'Nunca comparas tu ronda contra tu meta de hándicap.',
        ], cta_headline='DEJA DE ADIVINAR.', cta_sub='MIDE CADA RONDA.', shotfile='shot-rondas.png', serie='SEÑAL'),
    dict(folder='carrusel6-tabla-hcp', kicker='LA TABLA REAL', title_lines=['ASÍ JUEGA','CADA HÁNDICAP','(36 → 0)'],
        items=[
            'HCP 36: 37% fairways · 8% GIR · 37 putts por ronda.',
            'HCP 18: 48% fairways · 26% GIR · 34 putts por ronda.',
            'HCP 9: 54% fairways · 45% GIR · 32 putts por ronda.',
            'HCP 0 (scratch): 60% fairways · 64% GIR · 30 putts por ronda.',
        ], cta_headline='¿EN CUÁL DE ESTAS', cta_sub='FILAS ESTÁS TÚ?', shotfile='shot-logros.png', serie='NIVEL'),
    dict(folder='carrusel7-habitos', kicker='HÁBITOS', title_lines=['5 HÁBITOS DE','GOLFISTAS DE','UN SOLO DÍGITO'],
        items=[
            'Miden cada ronda, no solo el score final.',
            'Priorizan el centro del green sobre la bandera.',
            'Cuentan sus putts hoyo por hoyo.',
            'Entrenan con un objetivo, no "a lo que salga".',
            'Saben exactamente qué practicar antes de llegar al campo.',
        ], cta_headline='CONSTRUYE ESOS', cta_sub='HÁBITOS CON DATOS.', shotfile='shot-inicio.png', serie='HÁBITO'),
    dict(folder='carrusel8-errores-green', kicker='JUEGO CORTO', title_lines=['7 ERRORES QUE','TE CUESTAN','GOLPES EN','EL GREEN'],
        items=[
            'Leer el putt desde un solo ángulo.',
            'Apuntar a la bandera en vez del centro del green en tu approach.',
            'No contar tus 3-putts.',
            'Dejar el chip corto por miedo a pasarte.',
            'No practicar los putts de 1 metro — los que "nunca fallas", hasta que fallas.',
            'Cambiar tu rutina de putt cada ronda.',
            'No medir tu up & down real.',
        ], cta_headline='MIDE TU JUEGO', cta_sub='CORTO DE VERDAD.', shotfile='shot-analisis.png', serie='ERROR'),
    dict(folder='carrusel9-preguntas', kicker='DESPUÉS DE JUGAR', title_lines=['5 PREGUNTAS','TRAS CADA','RONDA'],
        items=[
            '¿Cuántos fairways pegué de verdad?',
            '¿Cuántos greens tomé en regulación?',
            '¿Cuántos putts hice por hoyo, no solo en total?',
            '¿En qué parte del campo perdí más golpes?',
            '¿Qué voy a practicar esta semana por eso?',
        ], cta_headline='PARFECT TE RESPONDE', cta_sub='LAS 5, AUTOMÁTICO.', shotfile='shot-rondas.png', serie='PREGUNTA'),
    dict(folder='carrusel10-cambia', kicker='ANTES Y DESPUÉS', title_lines=['6 COSAS QUE','CAMBIAN CUANDO','MIDES TU GOLF'],
        items=[
            'Dejas de adivinar qué practicar.',
            'Ves patrones que no notabas (ej. siempre fallas a la derecha).',
            'Tu entrenamiento se vuelve más corto y más efectivo.',
            'Compites contra tus propios números, no contra nadie más.',
            'Tu hándicap baja más rápido.',
            'Empiezas a disfrutar más el proceso.',
        ], cta_headline='EMPIEZA A MEDIR', cta_sub='TU PRÓXIMA RONDA.', shotfile='shot-inicio.png', serie='CAMBIO'),
    dict(folder='carrusel11-amigos', kicker='GOLF EN GRUPO', title_lines=['5 RAZONES PARA','LLEVAR LA CUENTA','CON UNA APP'],
        items=[
            'Se acaban las peleas por el score al final de la ronda.',
            'Cada quien ve sus propias stats, no solo el resultado final.',
            'Las apuestas se liquidan solas.',
            'Puedes comparar tu ronda con la de tus amigos.',
            'Queda un historial real de cada partido.',
        ], cta_headline='ARMA TU LIGA', cta_sub='DE AMIGOS EN PARFECT.', shotfile='shot-social.png', serie='RAZÓN'),
    dict(folder='carrusel12-practica', kicker='ENTRENAMIENTO', title_lines=['5 FORMAS DE','APROVECHAR TU','PRÁCTICA'],
        items=[
            'Entrena lo que tu diagnóstico dice que falla, no lo que se te antoja.',
            'Pon un objetivo medible a cada sesión (ej. 7/10 en un ejercicio).',
            'Cronometra tus sesiones cortas de 20 minutos.',
            'Practica situaciones reales: chip desde el rough, no solo del tapete.',
            'Registra tu práctica igual que registras tus rondas.',
        ], cta_headline='TU PRÓXIMA SESIÓN,', cta_sub='YA ARMADA POR LA IA.', shotfile='shot-analisis.png', serie='FORMA'),
    dict(folder='carrusel13-curiosos', kicker='CURIOSIDADES', title_lines=['6 DATOS DE','GOLF QUE TE VAN','A SORPRENDER'],
        items=[
            'Un putt de 1 metro y un drive de 250 yardas valen exactamente lo mismo en tu tarjeta: un golpe.',
            'La mayoría de los golfistas amateur pierde más golpes en 50 yardas y menos que en el tee.',
            'Bajar de 100 a 90 golpes suele costar menos práctica que bajar de 90 a 80.',
            'El jugador promedio solo toma en regulación 1 de cada 3 greens.',
            'Un solo 3-putt evitado por ronda puede bajar tu hándicap más que un drive extra de 20 yardas.',
            'La mayoría de los golfistas nunca ha contado sus propios fairways en una ronda completa.',
        ], cta_headline='CONOCE TUS PROPIOS', cta_sub='NÚMEROS, NO LOS PROMEDIOS.', shotfile='shot-logros.png', serie='DATO'),
    dict(folder='carrusel14-no-bajas-90', kicker='LA VERDAD', title_lines=['3 RAZONES POR','LAS QUE NO','BAJAS DE 90'],
        items=[
            'No sabes dónde pierdes tus golpes de verdad.',
            'Practicas al azar, no lo que de verdad te está fallando.',
            'Nunca comparas tu ronda contra una meta clara.',
        ], cta_headline='ROMPE 90 CON', cta_sub='UN PLAN, NO CON SUERTE.', shotfile='shot-rondas.png', serie='RAZÓN'),
]

def flatten():
    dest=os.path.join(OUT,'contenido')
    os.makedirs(dest,exist_ok=True)
    for f in os.listdir(dest):
        if f.endswith('.png'): os.remove(os.path.join(dest,f))
    folders=['carrusel1-verdades','carrusel2-bajar-hcp','carrusel3-dato']+[c['folder'] for c in CAROUSELS]
    for folder in folders:
        src=os.path.join(OUT,folder)
        for f in sorted(os.listdir(src)):
            if f.endswith('.png'):
                Image.open(os.path.join(src,f)).save(os.path.join(dest,f'{folder}-{f}'))

if __name__=='__main__':
    build_c1(); build_c2(); build_c3()
    for spec in CAROUSELS:
        build_carousel(**spec)
    flatten()
    n=sum(len(c['items'])+2 for c in CAROUSELS) + 10 + 7 + 2
    print(f'listo: {len(CAROUSELS)+3} carruseles, {n} imagenes (estilo EDITORIAL DE DATOS v3)')
