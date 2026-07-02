#!/usr/bin/env python3
# ============================================================
# PARFECT · Motor de contenido — formatos on-demand
# Reusa el estilo de marca de _build_viral (fondo oscuro, golfista 3D, acento lima).
# Uso:
#   python3 _content_engine.py quote "texto" ["autor"]
#   python3 _content_engine.py stat "56%" "de fairways" "es lo que tira un HCP 10"
#   python3 _content_engine.py meme "setup arriba" "remate abajo" [golfer|eagle|bird]
#   python3 _content_engine.py myth "el mito" "la verdad"
#   python3 _content_engine.py challenge "RETO ROMPER 90" "meta" "paso1" "paso2" "paso3"
#   python3 _content_engine.py feature shot-analisis.png "TITULO" "beneficio en una linea"
#   python3 _content_engine.py starter        # genera un paquete de arranque variado
# Salida: contenido-extra/<tipo>/<slug>.png  (1080x1080, RGB)
# ============================================================
import os, sys, re
from PIL import Image, ImageDraw
import _build_viral as V

S = V.S
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contenido-extra')

def slug(t):
    t = re.sub(r'[^a-z0-9]+','-', t.lower()).strip('-')
    return (t[:40] or 'post')

def save(img, tipo, name):
    p = os.path.join(OUT, tipo); os.makedirs(p, exist_ok=True)
    fp = os.path.join(p, name + '.png'); img.save(fp); print('->', fp); return fp

def center_lines(d, lines, font, cy, fill, lh):
    y = cy - (len(lines)*lh)//2
    for ln in lines:
        d.text((S//2, y), ln, font=font, fill=fill, anchor='mm'); y += lh
    return y

# ---------- 1) QUOTE / mentalidad ----------
def quote(text, author=''):
    b,d = V.dark_base(seed=hash(text)%9999)
    d.text((S//2, 210), '“', font=V.BLACK(150), fill=V.LIME, anchor='mm')
    lines = V.wraptext(d, text, V.BLACK(60), 900)
    center_lines(d, lines, V.BLACK(60), 470, V.CREAM, 76)
    if author:
        d.text((S//2, 470 + (len(lines)*76)//2 + 60), '— ' + author, font=V.BOLDIT(30), fill=V.MUT_D, anchor='mm')
    V.paste_char(b, 'golfer.png', S//2, 900, 210)
    V.footer_dark(d)
    return V.fin(b)

# ---------- 2) STAT / dato del dia ----------
def stat(big, label, sub=''):
    b,d = V.dark_base(seed=hash(big+label)%9999)
    d.text((S//2, 210), 'EL DATO DE HOY', font=V.BLACK(34), fill=V.LIME, anchor='mm')
    d.rounded_rectangle([140,300,S-140,720], 40, fill=(24,32,22))
    d.text((S//2, 380), label.upper(), font=V.BOLD(34), fill=V.MUT_D, anchor='mm')
    d.text((S//2, 540), big, font=V.BLACK(190), fill=V.LIME, anchor='mm')
    if sub:
        for i,ln in enumerate(V.wraptext(d, sub, V.BOLD(30), 760)):
            d.text((S//2, 650 + i*38), ln, font=V.BOLD(30), fill=V.CREAM, anchor='mm')
    d.text((S//2, 810), 'Míde el tuyo con PARFECT', font=V.BOLDIT(30), fill=V.MUT_D, anchor='mm')
    V.paste_char(b, 'eagle.png', S//2, 930, 190)
    V.footer_dark(d)
    return V.fin(b)

# ---------- 3) MEME / relatable ----------
def meme(setup, punch, char='golfer'):
    b,d = V.dark_base(seed=hash(setup+punch)%9999)
    for i,ln in enumerate(V.wraptext(d, setup, V.BOLD(44), 900)):
        d.text((S//2, 200 + i*56), ln, font=V.BOLD(44), fill=V.CREAM, anchor='mm')
    V.paste_char(b, char + '.png', S//2, 620, 360)
    yb = 860
    d.rounded_rectangle([70, yb-56, S-70, yb+ (len(V.wraptext(d,punch,V.BLACK(50),900))*58)+10], 26, fill=V.LIME)
    for i,ln in enumerate(V.wraptext(d, punch, V.BLACK(50), 900)):
        d.text((S//2, yb + i*58), ln, font=V.BLACK(50), fill=V.LIMEINK, anchor='mm')
    V.footer_dark(d)
    return V.fin(b)

# ---------- 4) MITO vs REALIDAD ----------
def myth(m, truth):
    b,d = V.dark_base(seed=hash(m)%9999)
    d.rounded_rectangle([90,180,S-90,250],20, fill=(120,40,40))
    d.text((S//2,215),'MITO', font=V.BLACK(30), fill=(255,220,220), anchor='mm')
    ml = V.wraptext(d, m, V.BOLD(46), 900)
    y = center_lines(d, ml, V.BOLD(46), 360, V.CREAM, 58)
    d.rounded_rectangle([90,y+30,S-90,y+100],20, fill=V.LIME)
    d.text((S//2,y+65),'LA VERDAD', font=V.BLACK(30), fill=V.LIMEINK, anchor='mm')
    tl = V.wraptext(d, truth, V.BLACK(50), 900)
    center_lines(d, tl, V.BLACK(50), y+230, V.CREAM, 62)
    V.paste_char(b, 'golfer.png', S//2, 930, 190)
    V.footer_dark(d)
    return V.fin(b)

# ---------- 5) RETO / challenge ----------
def challenge(name, goal, steps):
    b,d = V.dark_base(seed=hash(name)%9999)
    d.rounded_rectangle([S//2-260,160,S//2+260,224],27, fill=V.LIME)
    d.text((S//2,192), 'RETO PARFECT', font=V.BLACK(30), fill=V.LIMEINK, anchor='mm')
    for i,ln in enumerate(V.wraptext(d, name, V.BLACK(66), 940)):
        d.text((S//2, 300 + i*76), ln, font=V.BLACK(66), fill=V.CREAM, anchor='mm')
    d.text((S//2, 470), goal, font=V.BOLDIT(32), fill=V.LIME, anchor='mm')
    y = 560
    for i,s in enumerate(steps):
        V.mini_icon(d, ['target','chart','flag','bolt','check'][i%5], 150, y+12, 26, V.LIMEINK, bg=V.LIME)
        for j,ln in enumerate(V.wraptext(d, s, V.BOLD(34), 760)):
            d.text((200, y + j*40), ln, font=V.BOLD(34), fill=V.CREAM, anchor='lm')
        y += 40*max(1,len(V.wraptext(d,s,V.BOLD(34),760))) + 34
    V.footer_dark(d, 'Súbelo a tu perfil · @parfect.golf')
    return V.fin(b)

# ---------- 6) FEATURE / spotlight de la app (fondo claro) ----------
def feature(shotfile, title, benefit):
    b,d = V.light_base()
    for i,ln in enumerate(V.wraptext(d, title, V.BLACK(56), 940)):
        d.text((S//2, 150 + i*64), ln, font=V.BLACK(56), fill=V.INK, anchor='mm')
    try:
        shot = Image.open(os.path.join(V.ASSETS, shotfile)).convert('RGBA')
        r = 520/shot.height; shot = shot.resize((round(shot.width*r),520))
        fx,fy = S//2-shot.width//2, 300
        sh = Image.new('RGBA',(S,S),(0,0,0,0))
        ImageDraw.Draw(sh).rounded_rectangle([fx-14,fy+14,fx+shot.width+14,fy+shot.height+34],36,fill=(44,58,22,60))
        b.alpha_composite(sh); b.alpha_composite(shot,(fx,fy))
    except Exception: pass
    for i,ln in enumerate(V.wraptext(d, benefit, V.BOLD(32), 900)):
        d.text((S//2, 858 + i*40), ln, font=V.BOLD(32), fill=V.MUT_L, anchor='mm')
    d.rounded_rectangle([S//2-300,940,S//2+300,1004],32, fill=V.LIME)
    d.text((S//2,972),'PRUÉBALA GRATIS · LINK EN BIO', font=V.BLACK(24), fill=V.LIMEINK, anchor='mm')
    V.footer_light(d, 'parfectapp.github.io/parfect')
    return V.fin(b)

# ---------- paquete de arranque ----------
def starter():
    quotes = [
        ('El golf no premia al que pega más lejos, sino al que falla menos.', ''),
        ('No puedes mejorar lo que no mides.', ''),
        ('Cada putt de 1 metro vale un golpe. Trátalo así.', ''),
    ]
    for t,a in quotes: save(quote(t,a),'quote', 'quote-'+slug(t))
    stats = [
        ('41%','up & down','es lo que salva un HCP 15 · ¿y tú?'),
        ('56%','de fairways','tira un HCP 10 en promedio'),
        ('32','putts por ronda','el amateur promedio · un scratch hace 30'),
    ]
    for a,b_,c in stats: save(stat(a,b_,c),'stat','stat-'+slug(a+b_))
    memes = [
        ('Cuando dices "solo tiro unas bolas"','y llevas 3 horas en el driving range','golfer'),
        ('Tu cara cuando el de al lado','te pregunta tu hándicap y no lo sabes','golfer'),
        ('Nadie:','Yo a las 5am un sábado para el tee time','eagle'),
    ]
    for su,pu,ch in memes: save(meme(su,pu,ch),'meme','meme-'+slug(su))
    myths = [
        ('Necesitas pegarle más lejos para bajar tu hándicap.','Se ganan más golpes fallando menos y con el juego corto.'),
        ('Las estadísticas son solo para profesionales.','Entre más alto tu hándicap, más golpes fáciles hay que ganar con datos.'),
    ]
    for m,t in myths: save(myth(m,t),'myth','myth-'+slug(m))
    save(challenge('RETO: ROMPER 90','7 días midiendo cada ronda',
        ['Registra tus próximas 3 rondas completas','Encuentra tu fuga #1 en Análisis IA','Entrena solo eso 20 min al día']),
        'challenge','reto-romper-90')
    feats = [
        ('shot-analisis.png','Tu coach IA lee tus rondas','Te dice exactamente dónde pierdes golpes y qué entrenar.'),
        ('shot-rondas.png','Anota tu ronda en segundos','Fairway, green, up & down y putts, hoyo por hoyo.'),
    ]
    for sf,ti,be in feats: save(feature(sf,ti,be),'feature','feature-'+slug(ti))

CMDS = {'quote':quote,'stat':stat,'meme':meme,'myth':myth,'challenge':None,'feature':feature}
if __name__=='__main__':
    if len(sys.argv)<2 or sys.argv[1]=='starter':
        starter(); print('\nPaquete de arranque listo en contenido-extra/')
    else:
        cmd = sys.argv[1]; args = sys.argv[2:]
        if cmd=='challenge':
            img = challenge(args[0], args[1], args[2:]); save(img,'challenge',slug(args[0]))
        elif cmd=='meme':
            img = meme(args[0], args[1], args[2] if len(args)>2 else 'golfer'); save(img,'meme',slug(args[0]))
        elif cmd in CMDS and CMDS[cmd]:
            img = CMDS[cmd](*args); save(img,cmd,slug(args[0]))
        else:
            print('formato no reconocido:', cmd)
