#!/usr/bin/env python3
# Carruseles estilo "viral golf" (fondo oscuro, titulo gigante, ilustracion plana
# grande) como las referencias tipo Scratch AI / TikTok de golf. Copy honesto:
# el CTA final no usa badges falsos de tienda (la app aun no esta publicada).
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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

def corner_glow(b,cx,cy,r,color,alpha=90):
    layer=Image.new('RGBA',(S,S),(0,0,0,0))
    ImageDraw.Draw(layer).ellipse([cx-r,cy-r,cx+r,cy+r],fill=color+(alpha,))
    layer=layer.filter(ImageFilter.GaussianBlur(r//2.2))
    b.alpha_composite(layer)

def dot_field(b,seed,n=14,box=(60,120,S-60,S-160)):
    rnd=random.Random(seed); layer=Image.new('RGBA',(S,S),(0,0,0,0)); dl=ImageDraw.Draw(layer)
    for _ in range(n):
        x=rnd.randint(box[0],box[2]); y=rnd.randint(box[1],box[3])
        r=rnd.choice([3,3,4,5,7]); col=rnd.choice([LIME,CREAM,LIME])
        a=rnd.randint(90,200)
        dl.ellipse([x-r,y-r,x+r,y+r],fill=col+(a,))
    b.alpha_composite(layer)

def dark_base(seed=1):
    b=vgrad(S,S,[DARK,DARK2]).convert('RGBA')
    corner_glow(b,60,60,260,LIME,55)
    corner_glow(b,S-40,S-120,300,(70,110,40),70)
    dot_field(b,seed)
    d=ImageDraw.Draw(b,'RGBA')
    wordmark(d,S//2,60); return b,d

def light_base():
    b=vgrad(S,S,SKY).convert('RGBA')
    corner_glow(b,S-50,40,240,(150,220,90),60)
    d=ImageDraw.Draw(b,'RGBA')
    wordmark(d,S//2,60,color=LIME,textcolor=LIMEINK); return b,d

def draw_hill(b,top_y,color,alpha=200,wave=18):
    layer=Image.new('RGBA',(S,S),(0,0,0,0)); dl=ImageDraw.Draw(layer)
    pts=[(0,S),(0,top_y+wave),(S*0.22,top_y-wave*0.6),(S*0.5,top_y+wave*0.7),
         (S*0.78,top_y-wave*0.5),(S,top_y+wave),(S,S)]
    dl.polygon(pts,fill=(color[0],color[1],color[2],alpha))
    b.alpha_composite(layer)

def draw_tree(d,cx,cy,s,color):
    d.rectangle([cx-3*s,cy-2*s,cx+3*s,cy+16*s],fill=color)
    d.ellipse([cx-20*s,cy-46*s,cx+20*s,cy-4*s],fill=color)
    d.ellipse([cx-15*s,cy-64*s,cx+15*s,cy-30*s],fill=color)

def draw_flag_scene(d,cx,cy,h,color):
    d.line([(cx,cy-h),(cx,cy+6)],fill=color,width=max(3,int(h*0.05)))
    d.polygon([(cx,cy-h),(cx+h*0.55,cy-h*0.82),(cx,cy-h*0.62)],fill=color)
    d.ellipse([cx-h*0.34,cy,cx+h*0.34,cy+h*0.12],fill=color)

def draw_ball_trail(d,x0,y0,x1,y1,n,color):
    for i in range(n):
        t=i/(n-1); x=x0+(x1-x0)*t; y=y0+(y1-y0)*t-math.sin(t*math.pi)*70
        r=max(2,7-i*0.9)
        d.ellipse([x-r,y-r,x+r,y+r],fill=color)

def golf_scene_title(b,d):
    draw_hill(b,800,(38,58,30),170,wave=22)
    draw_hill(b,860,(28,44,24),210,wave=14)
    draw_tree(d,120,930,1.15,(30,46,26))
    draw_tree(d,955,955,0.95,(26,40,22))
    draw_flag_scene(d,890,760,150,(60,84,44))
    draw_ball_trail(d,150,760,430,660,7,(90,120,55))

def golf_scene_item(b,d):
    draw_hill(b,930,(30,46,26),170,wave=16)
    draw_tree(d,90,990,0.8,(28,42,24))
    draw_flag_scene(d,970,905,110,(56,78,42))

def swipe_dots(d,n,total,cy=1006,dark=True):
    w=14; gap=22; startx=S//2-((total-1)*gap)//2
    for i in range(total):
        on=(i==n-1)
        r=6 if on else 4
        col=LIME if on else ((90,102,84) if dark else (170,190,150))
        x=startx+i*gap
        d.ellipse([x-r,cy-r,x+r,cy+r],fill=col)

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
        for i,h in enumerate([0.5,0.85,1.15]):
            x=cx-r*0.7+i*(bw+r*0.16)
            d.rounded_rectangle([x,cy+r*0.75-r*h,x+bw,cy+r*0.75],3,fill=color)
    elif kind=='flag':
        d.line([(cx-r*0.3,cy-r*0.8),(cx-r*0.3,cy+r*0.8)],fill=color,width=max(3,int(r*0.14)))
        d.polygon([(cx-r*0.3,cy-r*0.8),(cx+r*0.7,cy-r*0.5),(cx-r*0.3,cy-r*0.2)],fill=color)
    elif kind=='bolt':
        d.polygon([(cx+r*0.1,cy-r*0.9),(cx-r*0.5,cy+r*0.15),(cx-r*0.05,cy+r*0.15),(cx-r*0.15,cy+r*0.9),(cx+r*0.55,cy-r*0.1),(cx+r*0.05,cy-r*0.1)],fill=color)

def feature_chip(d,cx,y,kind,label,fg,bg=None):
    r=30
    if bg: d.ellipse([cx-r,y-r,cx+r,y+r],fill=bg)
    mini_icon(d,kind,cx,y,r*0.6,fg)
    d.ellipse([cx-r,y-r,cx+r,y+r],outline=fg,width=3)
    d.text((cx,y+r+26),label,font=BOLD(21),fill=fg,anchor='mm')

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
        sh=sh.filter(ImageFilter.GaussianBlur(18))
        base.alpha_composite(sh,(x,y))
    base.alpha_composite(im,(x,y))

ITEM_ICONS=['check','target','chart','flag','bolt']

# ---------- slide de titulo (fondo oscuro, ilustracion grande) ----------
def slide_title(kicker, title_lines, n, total):
    b,d=dark_base(seed=100); pagepill(d,n,total,dark=True)
    d.rounded_rectangle([S//2-220,150,S//2+220,204],27,fill=LIME)
    d.text((S//2,177),kicker,font=BLACK(28),fill=LIMEINK,anchor='mm')
    y=260
    for ln in title_lines:
        d.text((S//2,y),ln,font=BLACK(70),fill=CREAM,anchor='mm'); y+=82
    golf_scene_title(b,d)
    paste_char(b, 'golfer.png', S//2, 680, 330)
    feats=[('target','MIDES'),('chart','ANALIZAS'),('bolt','MEJORAS')]
    fx=[S//2-260,S//2,S//2+260]
    for x,(k,lab) in zip(fx,feats):
        feature_chip(d,x,918,k,lab,CREAM,bg=(32,44,28))
    swipe_dots(d,n,total,cy=1012,dark=True)
    footer_dark(d,'desliza →'); return fin(b)

# ---------- slide de item numerado (fondo oscuro) ----------
def slide_item(num, text, n, total):
    b,d=dark_base(seed=n*7+total); pagepill(d,n,total,dark=True)
    cy=172
    icon=ITEM_ICONS[(num-1)%len(ITEM_ICONS)]
    mini_icon(d,icon,S//2-118,cy,34,LIMEINK,bg=LIME)
    d.text((S//2+18,cy),str(num),font=BLACK(120),fill=LIME,anchor='mm')
    d.line([(S//2-70,cy+76),(S//2+70,cy+76)],fill=LIME,width=6)
    lines=wraptext(d,text,BLACK(54),860)
    total_h=len(lines)*68
    ty=430-total_h//2
    for ln in lines:
        d.text((S//2,ty),ln,font=BLACK(54),fill=CREAM,anchor='mm'); ty+=68
    golf_scene_item(b,d)
    paste_char(b, 'eagle.png', S//2, 850, 230)
    d.rounded_rectangle([S//2-186,978,S//2+186,1020],21,fill=(255,255,255,18))
    d.text((S//2,999),'PARFECT · GOLF DATA',font=BOLD(19),fill=MUT_D,anchor='mm')
    swipe_dots(d,n,total,cy=1050,dark=True)
    return fin(b)

# ---------- slide CTA final (fondo CLARO = marca real, sin badges falsos) ----------
def slide_cta(headline, sub, shotfile='shot-inicio.png', n=None, total=None):
    b,d=light_base()
    if n and total: pagepill(d,n,total,dark=False)
    d.text((S//2,150),headline,font=BLACK(54),fill=INK,anchor='mm')
    d.text((S//2,212),sub,font=BOLD(30),fill=MUT_L,anchor='mm')
    try:
        shot=Image.open(os.path.join(ASSETS,shotfile)).convert('RGBA')
        r=490/shot.height; shot=shot.resize((round(shot.width*r),490))
        fx,fy=S//2-shot.width//2, 268
        sh=Image.new('RGBA',(S,S),(0,0,0,0))
        ImageDraw.Draw(sh).rounded_rectangle([fx-14,fy+14,fx+shot.width+14,fy+shot.height+34],36,fill=(44,58,22,60))
        b.alpha_composite(sh); b.alpha_composite(shot,(fx,fy))
    except Exception:
        pass
    feats=[('target','SIN ADIVINAR'),('chart','DATOS REALES'),('check','GRATIS')]
    fx2=[S//2-260,S//2,S//2+260]
    for x,(k,lab) in zip(fx2,feats):
        feature_chip(d,x,808,k,lab,LIMEINK,bg=(219,233,183))
    d.rounded_rectangle([S//2-330,910,S//2+330,978],34,fill=LIME)
    d.text((S//2,944),'REGÍSTRATE GRATIS · LINK EN BIO',font=BLACK(26),fill=LIMEINK,anchor='mm')
    if n and total: swipe_dots(d,n,total,cy=1006,dark=False)
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
    save(slide_cta('¿Y TÚ EN QUÉ PIERDES','GOLPES SIN SABERLO?','shot-analisis.png',total,total),'carrusel1-verdades',f'{total:02d}.png')

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
    save(slide_cta('PARFECT TE DICE','QUÉ PRACTICAR HOY','shot-rondas.png',total,total),'carrusel2-bajar-hcp',f'{total:02d}.png')

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
    save(slide_cta('MIDE TU JUEGO','DE VERDAD','shot-logros.png',2,2),'carrusel3-dato','02.png')

# ============================================================
# builder generico: kicker + titulo + N items + CTA
# ============================================================
def build_carousel(folder, kicker, title_lines, items, cta_headline, cta_sub, shotfile):
    total=len(items)+2
    save(slide_title(kicker,title_lines,1,total),folder,'01.png')
    for i,t in enumerate(items):
        save(slide_item(i+1,t,i+2,total),folder,f'{i+2:02d}.png')
    save(slide_cta(cta_headline,cta_sub,shotfile,total,total),folder,f'{total:02d}.png')

CAROUSELS = [
    dict(folder='carrusel4-mitos', kicker='MITOS DEL GOLF', title_lines=['7 MITOS QUE TE','ESTÁN DETENIENDO'],
        items=[
            'Mito: necesitas pegarle más lejos para bajar tu hándicap. Falso: se ganan más golpes en el juego corto.',
            'Mito: jugar todos los días te hace mejor. Falso: practicar sin objetivo no cambia tu score.',
            'Mito: el putt es cuestión de suerte. Falso: es la parte más medible de tu juego.',
            'Mito: solo los profesionales necesitan estadísticas. Falso: entre más alto tu hándicap, más golpes hay que ganar con datos.',
            'Mito: un hándicap bajo significa que ya no hay nada que mejorar. Falso: siempre hay una fuga de golpes que no ves.',
            'Mito: comprar palos nuevos baja tu hándicap. Falso: ayuda el fitting, pero el hándicap baja con repetición medida.',
            'Mito: necesitas 18 hoyos para que cuente. Falso: hasta 9 hoyos bien anotados te dan datos reales.',
        ], cta_headline='DEJA DE CREER MITOS.', cta_sub='EMPIEZA A MEDIR.', shotfile='shot-analisis.png'),
    dict(folder='carrusel5-senales', kicker='AUTODIAGNÓSTICO', title_lines=['6 SEÑALES DE QUE','PIERDES GOLPES SIN','DARTE CUENTA'],
        items=[
            'No sabes tu porcentaje real de fairways.',
            'Cuentas solo tu score total, nunca tus putts por ronda.',
            'No sabes cuántos greens tomas en regulación.',
            'Sientes que jugaste bien, pero tu tarjeta dice otra cosa.',
            'Practicas exactamente lo mismo que hace un año.',
            'Nunca comparas tu ronda contra tu meta de hándicap.',
        ], cta_headline='DEJA DE ADIVINAR.', cta_sub='MIDE CADA RONDA.', shotfile='shot-rondas.png'),
    dict(folder='carrusel6-tabla-hcp', kicker='LA TABLA REAL', title_lines=['ASÍ JUEGA CADA','HÁNDICAP (36 → 0)'],
        items=[
            'HCP 36: 37% fairways · 8% GIR · 37 putts por ronda.',
            'HCP 18: 48% fairways · 26% GIR · 34 putts por ronda.',
            'HCP 9: 54% fairways · 45% GIR · 32 putts por ronda.',
            'HCP 0 (scratch): 60% fairways · 64% GIR · 30 putts por ronda.',
        ], cta_headline='¿EN CUÁL DE ESTAS', cta_sub='FILAS ESTÁS TÚ?', shotfile='shot-logros.png'),
    dict(folder='carrusel7-habitos', kicker='HÁBITOS', title_lines=['5 HÁBITOS DE','GOLFISTAS DE UN','SOLO DÍGITO'],
        items=[
            'Miden cada ronda, no solo el score final.',
            'Priorizan el centro del green sobre la bandera.',
            'Cuentan sus putts hoyo por hoyo.',
            'Entrenan con un objetivo, no "a lo que salga".',
            'Saben exactamente qué practicar antes de llegar al campo.',
        ], cta_headline='CONSTRUYE ESOS', cta_sub='HÁBITOS CON DATOS.', shotfile='shot-inicio.png'),
    dict(folder='carrusel8-errores-green', kicker='JUEGO CORTO', title_lines=['7 ERRORES QUE TE','CUESTAN GOLPES','EN EL GREEN'],
        items=[
            'Leer el putt desde un solo ángulo.',
            'Apuntar a la bandera en vez del centro del green en tu approach.',
            'No contar tus 3-putts.',
            'Dejar el chip corto por miedo a pasarte.',
            'No practicar los putts de 1 metro — los que "nunca fallas", hasta que fallas.',
            'Cambiar tu rutina de putt cada ronda.',
            'No medir tu up & down real.',
        ], cta_headline='MIDE TU JUEGO', cta_sub='CORTO DE VERDAD.', shotfile='shot-analisis.png'),
    dict(folder='carrusel9-preguntas', kicker='DESPUÉS DE JUGAR', title_lines=['5 PREGUNTAS TRAS','CADA RONDA'],
        items=[
            '¿Cuántos fairways pegué de verdad?',
            '¿Cuántos greens tomé en regulación?',
            '¿Cuántos putts hice por hoyo, no solo en total?',
            '¿En qué parte del campo perdí más golpes?',
            '¿Qué voy a practicar esta semana por eso?',
        ], cta_headline='PARFECT TE RESPONDE', cta_sub='LAS 5, AUTOMÁTICO.', shotfile='shot-rondas.png'),
    dict(folder='carrusel10-cambia', kicker='ANTES Y DESPUÉS', title_lines=['6 COSAS QUE CAMBIAN','CUANDO MIDES','TU GOLF'],
        items=[
            'Dejas de adivinar qué practicar.',
            'Ves patrones que no notabas (ej. siempre fallas a la derecha).',
            'Tu entrenamiento se vuelve más corto y más efectivo.',
            'Compites contra tus propios números, no contra nadie más.',
            'Tu hándicap baja más rápido.',
            'Empiezas a disfrutar más el proceso.',
        ], cta_headline='EMPIEZA A MEDIR', cta_sub='TU PRÓXIMA RONDA.', shotfile='shot-inicio.png'),
    dict(folder='carrusel11-amigos', kicker='GOLF EN GRUPO', title_lines=['5 RAZONES PARA','LLEVAR LA CUENTA','CON UNA APP'],
        items=[
            'Se acaban las peleas por el score al final de la ronda.',
            'Cada quien ve sus propias stats, no solo el resultado final.',
            'Las apuestas se liquidan solas.',
            'Puedes comparar tu ronda con la de tus amigos.',
            'Queda un historial real de cada partido.',
        ], cta_headline='ARMA TU LIGA', cta_sub='DE AMIGOS EN PARFECT.', shotfile='shot-social.png'),
    dict(folder='carrusel12-practica', kicker='ENTRENAMIENTO', title_lines=['5 FORMAS DE','APROVECHAR TU','TIEMPO DE PRÁCTICA'],
        items=[
            'Entrena lo que tu diagnóstico dice que falla, no lo que se te antoja.',
            'Pon un objetivo medible a cada sesión (ej. 7/10 en un ejercicio).',
            'Cronometra tus sesiones cortas de 20 minutos.',
            'Practica situaciones reales: chip desde el rough, no solo del tapete.',
            'Registra tu práctica igual que registras tus rondas.',
        ], cta_headline='TU PRÓXIMA SESIÓN,', cta_sub='YA ARMADA POR LA IA.', shotfile='shot-analisis.png'),
    dict(folder='carrusel13-curiosos', kicker='CURIOSIDADES', title_lines=['6 DATOS DE GOLF','QUE TE VAN A','SORPRENDER'],
        items=[
            'Un putt de 1 metro y un drive de 250 yardas valen exactamente lo mismo en tu tarjeta: un golpe.',
            'La mayoría de los golfistas amateur pierde más golpes en 50 yardas y menos que en el tee.',
            'Bajar de 100 a 90 golpes suele costar menos práctica que bajar de 90 a 80.',
            'El jugador promedio solo toma en regulación 1 de cada 3 greens.',
            'Un solo 3-putt evitado por ronda puede bajar tu hándicap más que un drive extra de 20 yardas.',
            'La mayoría de los golfistas nunca ha contado sus propios fairways en una ronda completa.',
        ], cta_headline='CONOCE TUS PROPIOS', cta_sub='NÚMEROS, NO LOS PROMEDIOS.', shotfile='shot-logros.png'),
    dict(folder='carrusel14-no-bajas-90', kicker='LA VERDAD', title_lines=['3 RAZONES POR LAS','QUE NO BAJAS DE 90'],
        items=[
            'No sabes dónde pierdes tus golpes de verdad.',
            'Practicas al azar, no lo que de verdad te está fallando.',
            'Nunca comparas tu ronda contra una meta clara.',
        ], cta_headline='ROMPE 90 CON', cta_sub='UN PLAN, NO CON SUERTE.', shotfile='shot-rondas.png'),
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
    print(f'listo: {len(CAROUSELS)+3} carruseles, {n} imagenes en total (contenido/ aplanado)')
    print('listo: carrusel1-verdades (10), carrusel2-bajar-hcp (7), carrusel3-dato (2) + contenido/ (flat)')
