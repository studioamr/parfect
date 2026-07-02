#!/usr/bin/env python3
# ============================================================
# PARFECT · Motor de contenido — formatos on-demand
# Sistema "EDITORIAL DE DATOS" v3: navy+lima para datos/mitos/
# features, serie PAPEL editorial para quotes/memes/retos.
# Uso:
#   python3 _content_engine.py quote "texto" ["autor"]
#   python3 _content_engine.py stat "56%" "de fairways" "contexto"
#   python3 _content_engine.py meme "setup" "remate"
#   python3 _content_engine.py myth "el mito" "la verdad"
#   python3 _content_engine.py challenge "RETO X" "meta" "paso1" ...
#   python3 _content_engine.py feature shot-analisis.png "TITULO" "beneficio"
#   python3 _content_engine.py starter
# Salida: contenido-extra/<tipo>/<slug>.png (1080x1080)
# ============================================================
import os, sys, re
from PIL import Image, ImageDraw
import _build_viral as V

S=V.S; H=V.H; M=V.M
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contenido-extra')
TMP = ImageDraw.Draw(Image.new('RGB',(10,10)))

def slug(t):
    t = re.sub(r'[^a-z0-9]+','-', t.lower()).strip('-'); return (t[:40] or 'post')
def save(img, tipo, name):
    p=os.path.join(OUT,tipo); os.makedirs(p,exist_ok=True)
    fp=os.path.join(p,name+'.png'); img.save(fp); print('->',fp); return fp
def wrap(text,font,maxw): return V.wraptext(TMP,text,font,maxw)

# ---------- 1) QUOTE (papel editorial) ----------
def quote(text, author=''):
    b,d=V.base_paper()
    d.text((M+34,300),'“',font=V.GEO(210),fill=V.LIME,anchor='lt',
           stroke_width=2,stroke_fill=V.LIMEINK)
    fs=60; lines=wrap(text,V.GEOIT(fs),S-2*M-120)
    while len(lines)*(fs+22)>430 and fs>40:
        fs-=4; lines=wrap(text,V.GEOIT(fs),S-2*M-120)
    ty=470
    for ln in lines:
        d.text((M+60,ty),ln,font=V.GEOIT(fs),fill=V.INKD,anchor='lm'); ty+=fs+22
    d.rectangle([M+60,ty+16,M+200,ty+24],fill=V.LIME)
    if author:
        V.mono_label(d,M+60,ty+70,('— '+author).upper(),22,V.MUTP)
    V.footer(d,False,right='MENTALIDAD · GOLF')
    return V.fin(b)

# ---------- 2) STAT / dato del dia (navy) ----------
def stat(big, label, sub=''):
    b,d=V.base_navy()
    V.kicker_row(d,270,'EL DATO DE HOY')
    d.text((M+40,360),label.upper(),font=V.BLACK(54),fill=V.INKW,anchor='lm')
    d.text((M+36,565),big,font=V.BLACK(230),fill=V.INKW,anchor='lm',
           stroke_width=2,stroke_fill=V.LIME)
    pct=None
    mnum=re.match(r'^(\d+(?:\.\d+)?)\s*%$',big.strip())
    if mnum: pct=min(1.0,float(mnum.group(1))/100.0)
    x0,x1=M+44,S-M-44
    if pct is not None:
        d.rounded_rectangle([x0,716,x1,728],6,fill=V.HAIRW)
        d.rounded_rectangle([x0,716,x0+(x1-x0)*pct,728],6,fill=V.LIME)
        suby=790
    else:
        V.bars_motif(d,x0,760,hs=(26,44,62,38,74),bw=14,gap=12); suby=800
    if sub:
        for i,ln in enumerate(wrap(sub,V.BOLD(32),S-2*M-100)):
            d.text((M+44,suby+i*44),ln,font=V.BOLD(32),fill=V.MUTW,anchor='lm')
    V.footer(d,False if False else True,right='MÍDELO CON PARFECT')
    return V.fin(b)

# ---------- 3) MEME (papel, texto grande estilo marcador) ----------
def meme(setup, punch, char=None):
    b,d=V.base_paper()
    V.mono_label(d,M+40,230,'#COSASDEGOLFISTAS',24,V.MUTP,ls=6)
    fs=46; su=wrap(setup,V.GEOIT(fs),S-2*M-110)
    ty=330
    for ln in su:
        d.text((M+48,ty),ln,font=V.GEOIT(fs),fill=V.INKD,anchor='lm'); ty+=fs+18
    d.line([(M+40,ty+26),(S-M-40,ty+26)],fill=V.HAIRD,width=2)
    fp=58; pu=wrap(punch,V.BLACK(fp),S-2*M-130)
    while len(pu)*(fp+26)>330 and fp>40:
        fp-=4; pu=wrap(punch,V.BLACK(fp),S-2*M-130)
    py=ty+110
    for ln in pu:
        wpx=TMP.textlength(ln,font=V.BLACK(fp))
        d.rectangle([M+44,py-fp*0.62,M+44+wpx+26,py+fp*0.62],fill=V.LIME)
        d.text((M+58,py),ln,font=V.BLACK(fp),fill=V.INKD,anchor='lm')
        py+=fp+30
    V.footer(d,False,right='HUMOR · GOLF')
    return V.fin(b)

# ---------- 4) MITO vs REALIDAD (navy, split) ----------
def myth(m, truth):
    b,d=V.base_navy()
    d.rounded_rectangle([M+40,214,M+204,266],10,outline=V.MUTW,width=3)
    V.mono_label(d,M+122,240,'✕ MITO',22,V.MUTW,anchor='m')
    fs=42; ml=wrap(m,V.BOLD(fs),S-2*M-100); ty=330
    for ln in ml:
        d.text((M+44,ty),ln,font=V.BOLD(fs),fill=V.MUTW,anchor='lm'); ty+=fs+16
    d.line([(M+40,ty+34),(S-M-40,ty+34)],fill=V.HAIRW,width=2)
    ry=ty+100
    d.rounded_rectangle([M+40,ry-26,M+266,ry+26],10,fill=V.LIME)
    V.mono_label(d,M+153,ry,'✓ REALIDAD',22,V.LIMEINK,anchor='m')
    fs2=52; tl=wrap(truth,V.BLACK(fs2),S-2*M-100)
    while (ry+70)+len(tl)*(fs2+16)>H-M-110 and fs2>38:
        fs2-=4; tl=wrap(truth,V.BLACK(fs2),S-2*M-100)
    ty=ry+92
    for ln in tl:
        d.text((M+44,ty),ln,font=V.BLACK(fs2),fill=V.INKW,anchor='lm'); ty+=fs2+16
    V.footer(d,True,right='MITOS · GOLF')
    return V.fin(b)

# ---------- 5) RETO (papel, checklist) ----------
def challenge(name, goal, steps):
    b,d=V.base_paper()
    d.rounded_rectangle([M+40,206,M+300,258],10,fill=V.LIME)
    V.mono_label(d,M+170,232,'RETO PARFECT',22,V.LIMEINK,anchor='m')
    fs=64; nm=wrap(name,V.BLACK(fs),S-2*M-100); ty=340
    for ln in nm:
        d.text((M+44,ty),ln,font=V.BLACK(fs),fill=V.INKD,anchor='lm'); ty+=fs+14
    V.mono_label(d,M+46,ty+26,goal.upper(),22,V.MUTP)
    ty+=100
    for i,s in enumerate(steps):
        bx=M+46
        d.rounded_rectangle([bx,ty-18,bx+36,ty+18],8,outline=V.INKD,width=3)
        if i==0: V.mini_icon(d,'check',bx+18,ty,14,V.LIMEINK)
        sl=wrap(s,V.BOLD(34),S-2*M-190)
        for j,ln in enumerate(sl):
            d.text((bx+62,ty+j*42),ln,font=V.BOLD(34),fill=V.INKD,anchor='lm')
        ty+=42*max(1,len(sl))+34
    V.footer(d,False,right='RETO · 7 DÍAS')
    return V.fin(b)

# ---------- 6) FEATURE de la app (navy + screenshot real) ----------
def feature(shotfile, title, benefit):
    b,d=V.base_navy()
    V.kicker_row(d,220,'DENTRO DE PARFECT')
    fs=52; tl=wrap(title,V.BLACK(fs),S-2*M-90); ty=296
    for ln in tl:
        d.text((M+44,ty),ln,font=V.BLACK(fs),fill=V.INKW,anchor='lm'); ty+=fs+12
    V.paste_shot(b,shotfile,ty+26,H-M-260-(ty+26))
    d=ImageDraw.Draw(b,'RGBA')
    for i,ln in enumerate(wrap(benefit,V.BOLD(28),S-2*M-120)):
        d.text((S//2,H-M-170+i*36),ln,font=V.BOLD(28),fill=V.MUTW,anchor='mm')
    V.footer(d,True,right='GRATIS · LINK EN BIO')
    return V.fin(b)

def starter():
    for t,a in [('El golf no premia al que pega más lejos, sino al que falla menos.',''),
                ('No puedes mejorar lo que no mides.',''),
                ('Cada putt de 1 metro vale un golpe. Trátalo así.','')]:
        save(quote(t,a),'quote','quote-'+slug(t))
    for a,b_,c in [('41%','up & down','es lo que salva un HCP 15 en sus greens fallados. ¿Y tú?'),
                   ('56%','de fairways','es lo que tira un HCP 10 en promedio.'),
                   ('32','putts por ronda','el amateur promedio. Un scratch hace 30.')]:
        save(stat(a,b_,c),'stat','stat-'+slug(a+b_))
    for su,pu in [('Cuando dices "solo tiro unas bolas"','y llevas 3 horas en el driving range'),
                  ('Tu cara cuando te preguntan tu hándicap','y no lo sabes ni tú'),
                  ('Nadie:','Yo a las 5am un sábado por el tee time')]:
        save(meme(su,pu),'meme','meme-'+slug(su))
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
        elif cmd=='meme': save(meme(a[0],a[1]),'meme',slug(a[0]))
        elif cmd=='quote': save(quote(*a),'quote',slug(a[0]))
        elif cmd=='stat': save(stat(*a),'stat',slug(a[0]+a[1] if len(a)>1 else a[0]))
        elif cmd=='myth': save(myth(*a),'myth',slug(a[0]))
        elif cmd=='feature': save(feature(*a),'feature',slug(a[1] if len(a)>1 else a[0]))
        else: print('formato no reconocido:',cmd)
