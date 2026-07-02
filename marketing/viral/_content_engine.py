#!/usr/bin/env python3
# ============================================================
# PARFECT · Motor de contenido — formatos on-demand (estilo landing:
# cielo de dia, sol, nubes, pajaros, abeja, campo verde, tarjeta blanca)
# Uso:
#   python3 _content_engine.py quote "texto" ["autor"]
#   python3 _content_engine.py stat "56%" "de fairways" "contexto"
#   python3 _content_engine.py meme "setup" "remate" [golfer|eagle|bird]
#   python3 _content_engine.py myth "el mito" "la verdad"
#   python3 _content_engine.py challenge "RETO X" "meta" "paso1" "paso2" ...
#   python3 _content_engine.py feature shot-analisis.png "TITULO" "beneficio"
#   python3 _content_engine.py starter
# Salida: contenido-extra/<tipo>/<slug>.png  (1080x1080)
# ============================================================
import os, sys, re
from PIL import Image, ImageDraw
import _build_viral as V

S = V.S
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contenido-extra')
TMP = ImageDraw.Draw(Image.new('RGB',(10,10)))

def slug(t):
    t = re.sub(r'[^a-z0-9]+','-', t.lower()).strip('-'); return (t[:40] or 'post')
def save(img, tipo, name):
    p=os.path.join(OUT,tipo); os.makedirs(p,exist_ok=True)
    fp=os.path.join(p,name+'.png'); img.save(fp); print('->',fp); return fp
def wrap(text,font,maxw): return V.wraptext(TMP,text,font,maxw)

# ---------- 1) QUOTE / mentalidad ----------
def quote(text, author=''):
    b,d=V.bright_base()
    lines=wrap(text,V.BLACK(58),840); ch=150+len(lines)*72+(70 if author else 40)
    V.white_card(b,60,150,S-120,ch); d=ImageDraw.Draw(b,'RGBA')
    d.text((S//2,215),'“',font=V.BLACK(120),fill=V.LIME,anchor='mm')
    ty=300
    for ln in lines: d.text((S//2,ty),ln,font=V.BLACK(58),fill=V.INK2,anchor='mm'); ty+=72
    if author: d.text((S//2,ty+6),'— '+author,font=V.BOLDIT(30),fill=V.MUT2,anchor='mm')
    V.paste_char(b,'golfer.png',S//2,V.H-360,300)
    d.text((S//2,V.H-40),'@parfect.golf',font=V.BOLD(24),fill=V.INK2,anchor='mm')
    return V.fin(b)

# ---------- 2) STAT / dato del dia ----------
def stat(big, label, sub=''):
    b,d=V.bright_base(with_course=False)
    V.white_card(b,90,190,S-180,560); d=ImageDraw.Draw(b,'RGBA')
    d.rounded_rectangle([S//2-170,235,S//2+170,295],30,fill=V.LIME)
    d.text((S//2,265),'EL DATO DE HOY',font=V.BLACK(28),fill=V.LIMEINK,anchor='mm')
    d.text((S//2,380),label.upper(),font=V.BOLD(34),fill=V.MUT2,anchor='mm')
    d.text((S//2,540),big,font=V.BLACK(180),fill=V.GREENINK,anchor='mm')
    if sub:
        for i,ln in enumerate(wrap(sub,V.BOLD(30),740)):
            d.text((S//2,650+i*38),ln,font=V.BOLD(30),fill=V.INK2,anchor='mm')
    V.paste_char(b,'eagle.png',S//2,V.H-300,210)
    d.text((S//2,V.H-40),'Mídelo con PARFECT · @parfect.golf',font=V.BOLD(24),fill=V.INK2,anchor='mm')
    return V.fin(b)

# ---------- 3) MEME / relatable ----------
def meme(setup, punch, char='golfer'):
    b,d=V.bright_base(with_course=False)
    su=wrap(setup,V.BOLD(44),840); V.white_card(b,70,150,S-140,90+len(su)*54)
    d=ImageDraw.Draw(b,'RGBA'); ty=225
    for ln in su: d.text((S//2,ty),ln,font=V.BOLD(44),fill=V.INK2,anchor='mm'); ty+=54
    V.paste_char(b,char+'.png',S//2,640,360)
    pu=wrap(punch,V.BLACK(48),840); yb=V.H-90-len(pu)*56
    d=ImageDraw.Draw(b,'RGBA')
    d.rounded_rectangle([70,yb-40,S-70,yb+len(pu)*56+8],26,fill=V.LIME)
    for i,ln in enumerate(pu): d.text((S//2,yb+i*56),ln,font=V.BLACK(48),fill=V.LIMEINK,anchor='mm')
    return V.fin(b)

# ---------- 4) MITO vs REALIDAD ----------
def myth(m, truth):
    b,d=V.bright_base()
    ml=wrap(m,V.BOLD(44),820); tl=wrap(truth,V.BLACK(48),820)
    ch=110+len(ml)*54+90+len(tl)*60+40; V.white_card(b,70,150,S-140,ch)
    d=ImageDraw.Draw(b,'RGBA')
    d.rounded_rectangle([S//2-120,190,S//2+120,246],20,fill=(214,74,74))
    d.text((S//2,218),'MITO',font=V.BLACK(28),fill=(255,235,235),anchor='mm')
    ty=300
    for ln in ml: d.text((S//2,ty),ln,font=V.BOLD(44),fill=V.MUT2,anchor='mm'); ty+=54
    ty+=14; d.rounded_rectangle([S//2-140,ty,S//2+140,ty+56],20,fill=V.LIME)
    d.text((S//2,ty+28),'LA VERDAD',font=V.BLACK(28),fill=V.LIMEINK,anchor='mm'); ty+=100
    for ln in tl: d.text((S//2,ty),ln,font=V.BLACK(48),fill=V.INK2,anchor='mm'); ty+=60
    V.paste_char(b,'golfer.png',S//2,V.H-330,220)
    return V.fin(b)

# ---------- 5) RETO / challenge ----------
def challenge(name, goal, steps):
    b,d=V.bright_base(with_course=False)
    nm=wrap(name,V.BLACK(60),840)
    ch=120+len(nm)*72+70+sum(44*max(1,len(wrap(s,V.BOLD(34),700)))+30 for s in steps)+30
    V.white_card(b,70,150,S-140,ch); d=ImageDraw.Draw(b,'RGBA')
    d.rounded_rectangle([S//2-200,195,S//2+200,255],28,fill=V.LIME)
    d.text((S//2,225),'RETO PARFECT',font=V.BLACK(28),fill=V.LIMEINK,anchor='mm')
    ty=320
    for ln in nm: d.text((S//2,ty),ln,font=V.BLACK(60),fill=V.INK2,anchor='mm'); ty+=72
    d.text((S//2,ty),goal,font=V.BOLDIT(30),fill=V.GREENINK,anchor='mm'); ty+=64
    for i,s in enumerate(steps):
        V.mini_icon(d,['target','chart','flag','bolt','check'][i%5],150,ty+10,24,V.LIMEINK,bg=V.LIME)
        sl=wrap(s,V.BOLD(34),700)
        for j,ln in enumerate(sl): d.text((200,ty+j*40),ln,font=V.BOLD(34),fill=V.INK2,anchor='lm')
        ty+=40*max(1,len(sl))+30
    V.paste_char(b,'golfer.png',S//2,V.H-300,200)
    return V.fin(b)

# ---------- 6) FEATURE / spotlight de la app ----------
def feature(shotfile, title, benefit):
    b,d=V.bright_base(with_course=False)
    tl=wrap(title,V.BLACK(52),840); V.white_card(b,90,150,S-180,90+len(tl)*60)
    d=ImageDraw.Draw(b,'RGBA'); ty=225
    for ln in tl: d.text((S//2,ty),ln,font=V.BLACK(52),fill=V.INK2,anchor='mm'); ty+=60
    try:
        shot=Image.open(os.path.join(V.ASSETS,shotfile)).convert('RGBA')
        r=430/shot.height; shot=shot.resize((round(shot.width*r),430))
        fx,fy=S//2-shot.width//2,360
        sh=Image.new('RGBA',(S,S),(0,0,0,0))
        ImageDraw.Draw(sh).rounded_rectangle([fx-14,fy+16,fx+shot.width+14,fy+shot.height+36],36,fill=(20,45,20,70))
        sh=sh.filter(V.ImageFilter.GaussianBlur(10)); b.alpha_composite(sh); b.alpha_composite(shot,(fx,fy))
    except Exception: pass
    d=ImageDraw.Draw(b,'RGBA')
    for i,ln in enumerate(wrap(benefit,V.BOLD(30),820)):
        d.text((S//2,820+i*38),ln,font=V.BOLD(30),fill=V.MUT2,anchor='mm')
    d.rounded_rectangle([S//2-300,V.H-150,S//2+300,V.H-84],32,fill=V.LIME)
    d.text((S//2,V.H-117),'PRUÉBALA GRATIS · LINK EN BIO',font=V.BLACK(24),fill=V.LIMEINK,anchor='mm')
    d.text((S//2,V.H-40),'parfectapp.github.io/parfect',font=V.BOLD(22),fill=V.MUT2,anchor='mm')
    return V.fin(b)

def starter():
    for t,a in [('El golf no premia al que pega más lejos, sino al que falla menos.',''),
                ('No puedes mejorar lo que no mides.',''),
                ('Cada putt de 1 metro vale un golpe. Trátalo así.','')]:
        save(quote(t,a),'quote','quote-'+slug(t))
    for a,b_,c in [('41%','up & down','es lo que salva un HCP 15 · ¿y tú?'),
                   ('56%','de fairways','tira un HCP 10 en promedio'),
                   ('32','putts por ronda','el amateur promedio · un scratch hace 30')]:
        save(stat(a,b_,c),'stat','stat-'+slug(a+b_))
    for su,pu,ch in [('Cuando dices "solo tiro unas bolas"','y llevas 3 horas en el driving range','golfer'),
                     ('Tu cara cuando el de al lado','te pregunta tu hándicap y no lo sabes','golfer'),
                     ('Nadie:','Yo a las 5am un sábado por el tee time','eagle')]:
        save(meme(su,pu,ch),'meme','meme-'+slug(su))
    for m,t in [('Necesitas pegarle más lejos para bajar tu hándicap.','Se ganan más golpes fallando menos y con el juego corto.'),
                ('Las estadísticas son solo para profesionales.','Entre más alto tu hándicap, más golpes fáciles hay que ganar con datos.')]:
        save(myth(m,t),'myth','myth-'+slug(m))
    save(challenge('RETO: ROMPER 90','7 días midiendo cada ronda',
        ['Registra tus próximas 3 rondas completas','Encuentra tu fuga #1 en Análisis IA','Entrena solo eso 20 min al día']),'challenge','reto-romper-90')
    for sf,ti,be in [('shot-analisis.png','Tu coach IA lee tus rondas','Te dice dónde pierdes golpes y qué entrenar.'),
                     ('shot-rondas.png','Anota tu ronda en segundos','Fairway, green, up & down y putts, hoyo por hoyo.')]:
        save(feature(sf,ti,be),'feature','feature-'+slug(ti))

if __name__=='__main__':
    if len(sys.argv)<2 or sys.argv[1]=='starter':
        starter(); print('\nPaquete de arranque listo en contenido-extra/')
    else:
        cmd=sys.argv[1]; a=sys.argv[2:]
        if cmd=='challenge': save(challenge(a[0],a[1],a[2:]),'challenge',slug(a[0]))
        elif cmd=='meme': save(meme(a[0],a[1],a[2] if len(a)>2 else 'golfer'),'meme',slug(a[0]))
        elif cmd=='quote': save(quote(*a),'quote',slug(a[0]))
        elif cmd=='stat': save(stat(*a),'stat',slug(a[0]+a[1] if len(a)>1 else a[0]))
        elif cmd=='myth': save(myth(*a),'myth',slug(a[0]))
        elif cmd=='feature': save(feature(*a),'feature',slug(a[1] if len(a)>1 else a[0]))
        else: print('formato no reconocido:',cmd)
