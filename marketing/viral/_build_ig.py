#!/usr/bin/env python3
# ============================================================
# PARFECT · Kit de lanzamiento de INSTAGRAM
# Genera: avatar, portadas de highlights, tiles nuevos del grid
# (manifiesto + marca), grid inicial 3x3 (checkerboard navy/papel),
# preview del feed, e historias 1080x1920 (bienvenida, cómo
# funciona x3, encuesta, reto).
# Salida: instagram/
# ============================================================
import os, math
from PIL import Image, ImageDraw, ImageFilter
import _build_viral as V
import _content_engine as E

S=V.S; M=V.M
HERE=os.path.dirname(os.path.abspath(__file__))
IG=os.path.join(HERE,'instagram')
def out(sub=''):
    p=os.path.join(IG,sub) if sub else IG
    os.makedirs(p,exist_ok=True); return p

# ---------- AVATAR (foto de perfil, se ve en círculo) ----------
def avatar():
    b=V.vgrad(S,S,[V.NAVY,V.NAVY2]).convert('RGBA')
    V.soft_glow(b,S//2,S//2,420,V.LIME,22)
    d=ImageDraw.Draw(b,'RGBA')
    d.ellipse([120,120,S-120,S-120],outline=V.LIME,width=8)
    # bandera de la marca, grande y centrada
    px,py=S//2-60,S//2+190
    d.line([(px,py),(px,py-420)],fill=V.INKW,width=26)
    d.polygon([(px,py-420),(px+330,py-310),(px,py-200)],fill=V.LIME)
    d.ellipse([px-90,py-24,px+90,py+30],outline=V.LIME,width=10)
    img=V.fin(b); img.save(os.path.join(out(),'avatar.png')); return img

# ---------- PORTADAS DE HIGHLIGHTS (icono centrado, círculo) ----------
def highlight(nombre,icono):
    b=V.vgrad(S,S,[V.NAVY,V.NAVY2]).convert('RGBA')
    d=ImageDraw.Draw(b,'RGBA')
    d.ellipse([S//2-330,S//2-330,S//2+330,S//2+330],outline=(255,255,255,40),width=3)
    V.mini_icon(d,icono,S//2,S//2-40,120,V.LIME)
    V.mono_label(d,S//2,S//2+200,nombre.upper(),34,V.INKW,anchor='m',ls=10)
    img=V.fin(b); img.save(os.path.join(out('highlights'),f'hl-{nombre.lower()}.png'))

# ---------- TILE A · MANIFIESTO ----------
def tile_manifiesto():
    b,d=V.base_navy()
    V.kicker_row(d,280,'PARFECT · GOLF · DATOS')
    for i,ln in enumerate(['TU GOLF,','MEDIDO.']):
        d.text((M+40,388+i*118),ln,font=V.BLACK(104),fill=V.INKW if i==0 else V.LIME,anchor='lm')
    for i,ln in enumerate(['Anota tu ronda. La IA encuentra dónde','pierdes golpes. Entrena solo eso.']):
        d.text((M+44,620+i*42),ln,font=V.BOLD(30),fill=V.MUTW,anchor='lm')
    V.traj(b,d,M+70,V.H-250,S-M-150,V.H-290,arc=120)
    d=ImageDraw.Draw(b,'RGBA')
    V.footer(d,True,right='HECHO EN MORELIA · MX')
    return V.fin(b)

# ---------- TILE E · MARCA (centro del grid) ----------
def tile_marca():
    b,d=V.base_navy()
    f=V.BOLDIT(110); txt='PARFECT'
    tw=d.textlength(txt,font=f); x=S//2-tw/2
    d.line([(x-56,S//2-52),(x-56,S//2+52)],fill=V.INKW,width=12)
    d.polygon([(x-56,S//2-52),(x+26,S//2-22),(x-56,S//2+8)],fill=V.LIME)
    d.text((x+4,S//2),txt,font=f,fill=V.INKW,anchor='lm')
    V.mono_label(d,S//2,S//2+120,'GOLF · DATOS · MX',28,V.MUTW,anchor='m',ls=9)
    d.rectangle([S//2-70,S//2+180,S//2+70,S//2+188],fill=V.LIME)
    V.footer(d,True,right='EST. 2026')
    return V.fin(b)

# ---------- GRID INICIAL 3x3 (checkerboard navy/papel) ----------
# El grid de IG muestra el más NUEVO arriba-izquierda → se publica en
# orden inverso (09 primero, 01 al final).
def grid():
    gdir=out('feed-01')
    piezas=[
        ('01', tile_manifiesto()),                                             # navy
        ('02', E.quote('No puedes mejorar lo que no mides.')),                 # papel
        ('03', E.stat('41%','up & down','es lo que salva un HCP 15 en sus greens fallados. ¿Y tú?')),  # navy
        ('04', E.meme('Cuando dices "solo tiro unas bolas"','y llevas 3 horas en el driving range')),  # papel
        ('05', tile_marca()),                                                  # navy
        ('06', E.challenge('RETO: ROMPER 90','7 días midiendo cada ronda',
              ['Registra tus próximas 3 rondas completas','Encuentra tu fuga #1 en Análisis IA','Entrena solo eso 20 min al día'])),  # papel
        ('07', E.feature('shot-analisis.png','Tu coach IA lee tus rondas','Te dice dónde pierdes golpes y qué entrenar.')),  # navy
        ('08', E.quote('El score se hace en 100 yardas y menos.')),            # papel
        ('09', V.slide_title('LA TABLA REAL',['ASÍ JUEGA','CADA HÁNDICAP','(36 → 0)'],1,1)),  # navy
    ]
    for n,img in piezas:
        img.save(os.path.join(gdir,f'{n}.png'))
    # preview del feed 3x3
    t=340; prev=Image.new('RGB',(t*3+8,t*3+8),(10,10,14))
    for i,(n,img) in enumerate(piezas):
        x=(i%3)*(t+3)+1; y=(i//3)*(t+3)+1
        prev.paste(img.resize((t,t),Image.LANCZOS),(x,y))
    prev.save(os.path.join(out(),'PREVIEW-GRID.png'))

# ---------- HISTORIAS 1080x1920 ----------
SW,SH=1080,1920
def story_base(dark=True):
    stops=[V.NAVY,V.NAVY2] if dark else [V.PAPER,V.PAPER2]
    b=V.vgrad(SW,SH,stops).convert('RGBA')
    d=ImageDraw.Draw(b,'RGBA')
    hair=V.HAIRW if dark else V.HAIRD
    d.rectangle([M,M+120,SW-M,SH-M-120],outline=hair,width=2)
    tk=20
    for cx,cy,dx,dy in [(M,M+120,1,1),(SW-M,M+120,-1,1),(M,SH-M-120,1,-1),(SW-M,SH-M-120,-1,-1)]:
        d.line([(cx,cy),(cx+tk*dx,cy)],fill=V.LIME,width=4)
        d.line([(cx,cy),(cx,cy+tk*dy)],fill=V.LIME,width=4)
    V.wordmark_left(d,M+30,M+170,size=34,ink=V.INKW if dark else V.INKD)
    return b,d

def story_save(b,name):
    V.fin(b).save(os.path.join(out('stories'),name+'.png'))

def st_bienvenida():
    b,d=story_base()
    V.kicker_row(d,560,'YA ESTAMOS AQUÍ')
    for i,ln in enumerate(['TU GOLF,','MEDIDO.']):
        d.text((M+44,680+i*128),ln,font=V.BLACK(112),fill=V.INKW if i==0 else V.LIME,anchor='lm')
    for i,ln in enumerate(['La app que te dice dónde pierdes','golpes de verdad. Gratis.']):
        d.text((M+48,950+i*46),ln,font=V.BOLD(34),fill=V.MUTW,anchor='lm')
    V.traj(b,d,M+80,1450,SW-M-170,1390,arc=160)
    d=ImageDraw.Draw(b,'RGBA')
    d.rounded_rectangle([SW//2-300,1600,SW//2+300,1680],40,fill=V.LIME)
    d.text((SW//2,1640),'LINK EN BIO',font=V.BLACK(30),fill=V.LIMEINK,anchor='mm')
    story_save(b,'01-bienvenida')

def st_paso(n,titulo,sub,shot,name):
    b,d=story_base()
    d.text((M+40,420),f'{n:02d}',font=V.BLACK(170),fill=V.NAVY3,anchor='lm',stroke_width=3,stroke_fill=V.LIME)
    d.text((M+44,600),titulo,font=V.BLACK(56),fill=V.INKW,anchor='lm')
    d.text((M+48,668),sub,font=V.BOLD(30),fill=V.MUTW,anchor='lm')
    try:
        shot_im=Image.open(os.path.join(V.ASSETS,shot)).convert('RGBA')
        hpx=880; r=hpx/shot_im.height
        shot_im=shot_im.resize((round(shot_im.width*r),hpx),Image.LANCZOS)
        fx=SW//2-shot_im.width//2; fy=760
        b.alpha_composite(shot_im,(fx,fy))
        ImageDraw.Draw(b).rounded_rectangle([fx-3,fy-3,fx+shot_im.width+3,fy+hpx+3],18,outline=V.LIME,width=3)
    except Exception: pass
    story_save(b,name)

def st_encuesta():
    b,d=story_base()
    V.kicker_row(d,500,'PREGUNTA DEL DÍA')
    for i,ln in enumerate(['¿CUÁNTOS PUTTS','HICISTE EN TU','ÚLTIMA RONDA?']):
        d.text((M+44,620+i*86),ln,font=V.BLACK(72),fill=V.INKW,anchor='lm')
    d.rounded_rectangle([M+60,1050,SW-M-60,1330],30,outline=(255,255,255,60),width=3)
    V.mono_label(d,SW//2,1170,'PON AQUÍ EL STICKER',26,V.MUTW,anchor='m')
    V.mono_label(d,SW//2,1220,'DE ENCUESTA (–30 / 30–36 / +36 / NI IDEA)',22,V.MUTW,anchor='m')
    d.text((M+48,1450),'El promedio amateur: 32. Un scratch: 30.',font=V.BOLD(30),fill=V.MUTW,anchor='lm')
    story_save(b,'05-encuesta')

def st_reto():
    b,d=story_base(dark=False)
    d.rounded_rectangle([M+40,470,M+320,530],12,fill=V.LIME)
    V.mono_label(d,M+180,500,'RETO PARFECT',24,V.LIMEINK,anchor='m')
    for i,ln in enumerate(['ROMPER 90','EN 7 DÍAS.']):
        d.text((M+44,640+i*110),ln,font=V.BLACK(96),fill=V.INKD,anchor='lm')
    pasos=['Registra tus próximas 3 rondas','Encuentra tu fuga #1 en Análisis IA','Entrena solo eso 20 min al día']
    ty=980
    for i,p in enumerate(pasos):
        d.rounded_rectangle([M+48,ty-20,M+88,ty+20],10,outline=V.INKD,width=3)
        if i==0: V.mini_icon(d,'check',M+68,ty,15,V.LIMEINK)
        d.text((M+116,ty),p,font=V.BOLD(34),fill=V.INKD,anchor='lm'); ty+=92
    d.rounded_rectangle([SW//2-330,1560,SW//2+330,1644],42,fill=V.INKD)
    d.text((SW//2,1602),'COMPARTE TU AVANCE →',font=V.BLACK(28),fill=V.PAPER,anchor='mm')
    story_save(b,'06-reto')

if __name__=='__main__':
    avatar()
    for nm,ic in [('la-app','flag'),('datos','chart'),('retos','target'),('humor','bolt'),('comunidad','check')]:
        highlight(nm,ic)
    grid()
    st_bienvenida()
    st_paso(1,'ANOTA TU RONDA','Fairway, green, up & down y putts. En segundos.','shot-rondas.png','02-paso1')
    st_paso(2,'LA IA ENCUENTRA TU FUGA','Te dice exactamente dónde pierdes golpes.','shot-analisis.png','03-paso2')
    st_paso(3,'ENTRENA LO QUE IMPORTA','Tu plan de práctica, armado por tus datos.','shot-inicio.png','04-paso3')
    st_encuesta()
    st_reto()
    print('kit de instagram listo en instagram/')
