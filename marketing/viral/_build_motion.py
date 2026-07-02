#!/usr/bin/env python3
# ============================================================
# PARFECT · MOTOR DE VIDEO ANIMADO (formatos que venden)
# Videos cortos nativos de TikTok/Reels 1080x1920 @30fps con
# movimiento real: tipografia cinetica, numeros que cuentan,
# barras que se llenan, demo de la app con paneo, bola animada.
# Look v4 (crema/bosque, serif Georgia, lima). Outro CTA animado.
#
#   python3 _build_motion.py demo      # 4 videos de muestra
#   python3 _build_motion.py dato "41%" "up & down" "sub..."
#   python3 _build_motion.py razones "TITULO" "r1" "r2" "r3"
#   python3 _build_motion.py app       # demo de la app
#   python3 _build_motion.py meme "setup" "remate"
# Salida: motion/<slug>.mp4
# ============================================================
import os, sys, math, re, subprocess, shutil
from PIL import Image, ImageDraw, ImageFilter
import _build_viral as V
import _build_v4 as B4

HERE=os.path.dirname(os.path.abspath(__file__))
W,H,FPS=1080,1920,30
OUT=os.path.join(HERE,'motion'); os.makedirs(OUT,exist_ok=True)
TMPD=os.path.join(HERE,'_motion_frames')

GEO   = lambda s: V.ImageFont.truetype(V.FP+'Georgia Bold.ttf', s)
BOLD  = lambda s: V.ImageFont.truetype(V.FP+'Arial Bold.ttf', s)
BLACK = lambda s: V.ImageFont.truetype(V.FP+'Arial Black.ttf', s)
BOLDIT= lambda s: V.ImageFont.truetype(V.FP+'Arial Bold Italic.ttf', s)

LIME=(199,238,84); LIMEDK=(150,196,52)
CREAM=dict(bg=(242,237,224), ink=(30,58,44), sub=(112,126,104))
FOREST=dict(bg=(28,56,42), ink=(240,231,206), sub=(172,186,164))

def ease(t): return 1-(1-min(max(t,0),1))**3          # ease-out cubic
def spring(t):
    t=min(max(t,0),1); return 1+ (1.15-1)*math.sin(t*math.pi) if t<1 else 1.0
def dur_lectura(txt,base=1.1):
    return max(2.6, base + len(str(txt).split())*0.38)

def slug(t): return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')[:36] or 'video'

def canvas(pal):
    b=Image.new('RGB',(W,H),pal['bg']).convert('RGBA')
    return b,ImageDraw.Draw(b,'RGBA')

def wordmark(d,cx,y,ink,size=54,alpha=255):
    f=BOLDIT(size); txt='PARFECT'; tw=d.textlength(txt,font=f); x=cx-tw/2
    fl=size*0.95; a=(alpha,)
    d.line([(x-size*0.5,y-fl*0.5),(x-size*0.5,y+fl*0.5)],fill=ink+a,width=max(5,size//9))
    d.polygon([(x-size*0.5,y-fl*0.5),(x-size*0.5+fl*0.72,y-fl*0.22),(x-size*0.5,y-fl*0.02)],fill=LIME+a)
    d.text((x+size*0.1,y),txt,font=f,fill=ink+a,anchor='lm')

def progressbar(d,t,pal):
    d.rectangle([0,H-10,int(W*min(t,1)),H],fill=LIME)

def poptext(d,cx,cy,txt,base_fs,t,ink,font=GEO,maxw=W-160):
    """texto que entra con overshoot; t=0..1"""
    if t<=0: return
    sc=0.6+0.4*ease(t*1.4)
    if t>0.35: sc=spring(min((t-0.35)/0.65,1))*1.0
    fs=max(10,int(base_fs*min(sc,1.18)))
    f=font(fs)
    tmp=ImageDraw.Draw(Image.new('RGB',(4,4)))
    lines=V.wraptext(tmp,txt,f,maxw)
    a=int(255*min(t*3,1))
    ty=cy-(len(lines)-1)*(fs+14)//2
    for ln in lines:
        d.text((cx,ty),ln,font=f,fill=ink+(a,),anchor='mm'); ty+=fs+14

def scene_strip(d,pal,y=1840):
    gcol=(45,88,62) if pal is FOREST else (133,172,96)
    d.ellipse([-320,y-36,W+320,y+250],fill=gcol)
    B4.flagpin(d,W-160,y+40,200)
    B4.golfer(d,150,y+95,200)
    B4.tree(d,W//2+120,y+70,150)

def cta_outro(frames,pal,seconds=2.8,line1='PRUÉBALA GRATIS',line2='link en bio'):
    n=int(seconds*FPS)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(pal)
        wordmark(d,W//2,300,pal['ink'],72,alpha=int(255*min(t*4,1)))
        poptext(d,W//2,760,line1,110,t*1.6,pal['ink'])
        # boton pulsando
        pu=1+0.04*math.sin(t*math.pi*4)
        bw,bh=int(560*pu),int(150*pu)
        if t>0.25:
            d.rounded_rectangle([W//2-bw//2,1050-bh//2,W//2+bw//2,1050+bh//2],bh//2,fill=LIME)
            d.text((W//2,1050),line2.upper(),font=BLACK(52),fill=(36,48,14),anchor='mm')
        if t>0.45:
            d.text((W//2,1240),'parfectapp.github.io/parfect',font=BOLD(40),fill=pal['sub'],anchor='mm')
            d.text((W//2,1330),'@parfect.golf',font=BOLD(36),fill=pal['sub'],anchor='mm')
        progressbar(d,1.0,pal)
        frames.append(V.fin(b))

def render(frames,name):
    if os.path.isdir(TMPD): shutil.rmtree(TMPD)
    os.makedirs(TMPD)
    man=[]
    for i,fr in enumerate(frames):
        p=os.path.join(TMPD,f'f{i:05d}.png'); fr.save(p); man.append(f'{p} 1.0000')
    mp=os.path.join(TMPD,'m.txt'); open(mp,'w').write('\n'.join(man))
    outp=os.path.join(OUT,name+'.mp4')
    r=subprocess.run([os.path.join(HERE,'_encode_pro'),mp,outp],capture_output=True,text=True,cwd=HERE)
    if r.returncode!=0 or not os.path.exists(outp):
        print('encode error:',(r.stderr or r.stdout)[:300]); return None
    print('->',outp,f'({os.path.getsize(outp)//1_000_000}MB, {len(frames)/FPS:.1f}s)')
    return outp

# ============================================================
# FORMATO 1 · DATO ANIMADO (numero cuenta + barra se llena)
# ============================================================
def video_dato(big,label,sub,pal=FOREST):
    frames=[]
    m=re.match(r'^(\d+)',big.strip()); target=int(m.group(1)) if m else 0
    suf=big.strip()[len(m.group(1)):] if m else big
    # hook legible
    for k in range(int(1.6*FPS)):
        t=k/(1.6*FPS)
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        poptext(d,W//2,900,'EL DATO QUE TE',96,t*2,pal['ink'],font=BLACK)
        poptext(d,W//2,1030,'CUESTA GOLPES',96,max(t*2-0.3,0),LIME if pal is FOREST else LIMEDK,font=BLACK)
        progressbar(d,0.08*t,pal); frames.append(V.fin(b))
    # numero cuenta 2.2s + barra
    n=int(2.2*FPS)
    for k in range(n):
        t=k/(n-1)
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        d.text((W//2,560),label.upper(),font=BOLD(58),fill=pal['sub'],anchor='mm')
        val=int(target*ease(t))
        d.text((W//2,900),f'{val}{suf}',font=BLACK(300),fill=pal['ink'],anchor='mm',
               stroke_width=4,stroke_fill=LIME)
        x0,x1=140,W-140
        d.rounded_rectangle([x0,1180,x1,1210],15,fill=(255,255,255,36) if pal is FOREST else (0,0,0,26))
        pct=min(target/100.0,1.0) if '%' in suf else 0.75
        d.rounded_rectangle([x0,1180,x0+int((x1-x0)*pct*ease(t)),1210],15,fill=LIME)
        progressbar(d,0.08+0.42*t,pal); frames.append(V.fin(b))
    # sub con tiempo de lectura
    n2=int(dur_lectura(sub)*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        d.text((W//2,560),label.upper(),font=BOLD(58),fill=pal['sub'],anchor='mm')
        d.text((W//2,900),big,font=BLACK(300),fill=pal['ink'],anchor='mm',stroke_width=4,stroke_fill=LIME)
        x0,x1=140,W-140
        pct=min(target/100.0,1.0) if '%' in suf else 0.75
        d.rounded_rectangle([x0,1180,x1,1210],15,fill=(255,255,255,36) if pal is FOREST else (0,0,0,26))
        d.rounded_rectangle([x0,1180,x0+int((x1-x0)*pct),1210],15,fill=LIME)
        poptext(d,W//2,1420,sub,62,t*1.8,pal['ink'])
        progressbar(d,0.5+0.3*t,pal); frames.append(V.fin(b))
    cta_outro(frames,pal)
    return render(frames,'dato-'+slug(big+label))

# ============================================================
# FORMATO 2 · RAZONES (tipografia cinetica, una por una)
# ============================================================
def video_razones(title,items,pal=CREAM):
    frames=[]
    nin=int(dur_lectura(title,0.8)*FPS)
    for k in range(nin):
        t=k/nin
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        poptext(d,W//2,930,title,104,t*1.6,pal['ink'])
        progressbar(d,0.1*t,pal); frames.append(V.fin(b))
    for i,item in enumerate(items):
        n=int(dur_lectura(item)*FPS)
        for k in range(n):
            t=k/(n-1)
            b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
            d.text((W//2,430),f'{i+1}.',font=GEO(170),fill=LIMEDK,anchor='mm')
            poptext(d,W//2,900,item,84,t*1.7,pal['ink'])
            dots_y=1500
            for j in range(len(items)):
                r=12 if j==i else 8
                col=LIMEDK if j<=i else (pal['sub']+(120,))
                d.ellipse([W//2-(len(items)-1)*22+j*44-r,dots_y-r,
                           W//2-(len(items)-1)*22+j*44+r,dots_y+r],fill=col)
            progressbar(d,0.1+0.6*((i+t)/len(items)),pal); frames.append(V.fin(b))
    cta_outro(frames,pal)
    return render(frames,'razones-'+slug(title))

# ============================================================
# FORMATO 3 · DEMO DE LA APP (pantallas reales con paneo + pasos)
# ============================================================
def video_app(pal=FOREST,variant=0):
    HOOKS=['Así se baja el hándicap en 2026','La app que te dice qué practicar hoy',
           'Deja de adivinar por qué juegas mal','Tu coach de golf vive en tu bolsillo']
    PASOS=[[('shot-rondas.png','1. Anotas tu ronda','fairway, green y putts en segundos'),
            ('shot-analisis.png','2. La IA encuentra tu fuga','te dice dónde pierdes golpes'),
            ('shot-inicio.png','3. Entrenas lo que importa','y tu hándicap empieza a bajar')],
           [('shot-analisis.png','1. La IA lee tus rondas','encuentra tu fuga de golpes'),
            ('shot-logros.png','2. Ves tu progreso real','logros por hitos de tu juego'),
            ('shot-rondas.png','3. Cada ronda cuenta','historial completo, hoyo por hoyo')],
           [('shot-inicio.png','1. Todo tu golf en una pantalla','hándicap, tendencia y plan'),
            ('shot-social.png','2. Tu liga de amigos','scores en vivo, cero peleas'),
            ('shot-analisis.png','3. Y la IA te entrena','con tus datos, no con tips genéricos')]]
    hook=HOOKS[variant%len(HOOKS)]; pasos=PASOS[variant%len(PASOS)]
    if pal is FOREST and variant%2: pal=CREAM
    frames=[]
    for k in range(int(1.0*FPS)):
        t=k/(1.0*FPS)
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        poptext(d,W//2,900,hook,96,t*1.6,pal['ink'])
        progressbar(d,0.06*t,pal); frames.append(V.fin(b))
    for i,(shotf,cap,sub) in enumerate(pasos):
        try: shot=Image.open(os.path.join(V.ASSETS,shotf)).convert('RGBA')
        except Exception: continue
        ph=1140; r=(ph-80)/shot.height
        sc=shot.resize((round(shot.width*r),ph-80),Image.LANCZOS)
        pw=sc.width+80
        n=int(dur_lectura(cap+' '+sub,1.6)*FPS)
        for k in range(n):
            t=k/(n-1)
            b,d=canvas(pal); wordmark(d,W//2,150,pal['ink'])
            poptext(d,W//2,320,cap,72,t*2.2,pal['ink'],maxw=W-200)
            if t>0.18:
                d.text((W//2,500),sub,font=BOLD(42),fill=pal['sub'],anchor='mm')
            # telefono entra deslizando + zoom sutil
            slide=ease(min(t*1.8,1)); zz=1.0+0.05*t
            fw,fh=int(pw*zz),int(ph*zz)
            simg=sc.resize((int(sc.width*zz),int(sc.height*zz)),Image.LANCZOS)
            fx=W//2-fw//2; fy=int(560+(H-560)*(1-slide)*0.35)
            d.rounded_rectangle([fx,fy,fx+fw,fy+fh],90,fill=(24,26,30))
            b.alpha_composite(simg,(fx+40,fy+40))
            d=ImageDraw.Draw(b,'RGBA')
            # tap ripple a media escena
            if 0.45<t<0.75:
                rt=(t-0.45)/0.30; rr=int(30+90*rt)
                d.ellipse([W//2-rr,fy+fh//2-rr,W//2+rr,fy+fh//2+rr],
                          outline=LIME+(int(255*(1-rt)),),width=8)
            progressbar(d,0.06+0.64*((i+t)/len(pasos)),pal); frames.append(V.fin(b))
    cta_outro(frames,pal,line1='Gratis. Hecha en México.')
    return render(frames,f'demo-app-parfect-v{variant%3}')

# ============================================================
# FORMATO 4 · MEME ANIMADO (bola que se queda corta)
# ============================================================
def video_meme_putt(setup='POV: tu putt de 1 metro',punch='de pronto mide 4 kilómetros',pal=CREAM):
    frames=[]
    nst=int(dur_lectura(setup,0.7)*FPS)
    for k in range(nst):
        t=k/nst
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        poptext(d,W//2,820,setup,88,t*1.6,pal['ink'])
        progressbar(d,0.1*t,pal); frames.append(V.fin(b))
    n=int(4.4*FPS)
    for k in range(n):
        t=k/(n-1)
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        d.text((W//2,700),setup,font=GEO(88),fill=pal['ink'],anchor='mm')
        gy=1450
        d.ellipse([-300,gy-60,W+300,gy+220],fill=(133,172,96))
        hx=W-240
        d.ellipse([hx-60,gy+6,hx+60,gy+34],fill=(240,240,228))
        d.ellipse([hx-18,gy+12,hx+18,gy+26],fill=(30,34,32))
        d.line([(hx,gy+18),(hx,gy-190)],fill=(238,236,226),width=10)
        d.polygon([(hx,gy-190),(hx+95,gy-158),(hx,gy-126)],fill=(226,84,64))
        # bola: sale rapido, desacelera... y se queda corta
        bx=170+ (hx-170-170)*ease(min(t*1.15,1))
        d.ellipse([bx-26,gy-6,bx+26,gy+46],fill=(252,252,248))
        d.arc([bx-14,gy+6,bx+12,gy+34],20,200,fill=(200,200,192),width=3)
        if t>0.55:
            poptext(d,W//2,1050,punch,92,(t-0.55)/0.25*1.4,(178,58,46),font=BLACK,maxw=W-200)
        progressbar(d,0.1+0.6*t,pal); frames.append(V.fin(b))
    cta_outro(frames,pal,line1='Cuenta tus putts de verdad')
    return render(frames,'meme-'+slug(setup))

# ============================================================
# FORMATO 5 · QUIZ (pregunta -> opciones -> 3,2,1 -> respuesta)
# ============================================================
def video_quiz(pregunta,opciones,correcta,dato,pal=FOREST):
    frames=[]
    npre=int(dur_lectura(pregunta,1.0)*FPS)
    for k in range(npre):
        t=k/npre
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        d.rounded_rectangle([W//2-220,300,W//2+220,380],40,fill=LIME)
        d.text((W//2,340),'QUIZ DE GOLF',font=BLACK(42),fill=(36,48,14),anchor='mm')
        poptext(d,W//2,780,pregunta,88,t*1.6,pal['ink'])
        scene_strip(d,pal)
        progressbar(d,0.12*t,pal); frames.append(V.fin(b))
    nop=int(2.6*FPS)
    letras=['A','B','C']
    tmpq=ImageDraw.Draw(Image.new('RGB',(4,4)))
    fsq=68; qlines=V.wraptext(tmpq,pregunta,GEO(fsq),W-200)
    while len(qlines)>2 and fsq>48:
        fsq-=4; qlines=V.wraptext(tmpq,pregunta,GEO(fsq),W-200)
    def draw_preg(d):
        qy=560-(len(qlines)-1)*(fsq+16)//2
        for ln in qlines:
            d.text((W//2,qy),ln,font=GEO(fsq),fill=pal['ink'],anchor='mm'); qy+=fsq+16
    def draw_ops(d,hl=None,dim=False):
        oy=1050
        for j,op in enumerate(opciones):
            bg=LIME if hl==j else ((255,255,255,26) if pal is FOREST else (0,0,0,18))
            fg=(36,48,14) if hl==j else (pal['ink'] if not dim else pal['sub'])
            d.rounded_rectangle([140,oy-62,W-140,oy+62],40,fill=bg)
            d.text((210,oy),letras[j]+')',font=BLACK(52),fill=fg,anchor='lm')
            d.text((300,oy),op,font=BOLD(52),fill=fg,anchor='lm')
            oy+=170
    for k in range(nop):
        t=k/nop
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        draw_preg(d)
        draw_ops(d)
        scene_strip(d,pal)
        progressbar(d,0.12+0.2*t,pal); frames.append(V.fin(b))
    for num in (3,2,1):
        for k in range(FPS):
            t=k/FPS
            b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
            draw_preg(d)
            draw_ops(d,dim=True)
            sc=1.35-0.35*ease(t)
            d.text((W//2,560+280),str(num),font=BLACK(int(220*sc)),fill=LIME,anchor='mm',
                   stroke_width=6,stroke_fill=pal['ink'])
            scene_strip(d,pal)
            progressbar(d,0.32+0.3*((3-num)+t)/3,pal); frames.append(V.fin(b))
    nrev=int(dur_lectura(dato,1.4)*FPS)
    for k in range(nrev):
        t=k/nrev
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        draw_preg(d)
        draw_ops(d,hl=correcta)
        scene_strip(d,pal)
        poptext(d,W//2,1560,dato,54,t*1.8,pal['ink'])
        progressbar(d,0.62+0.3*t,pal); frames.append(V.fin(b))
    cta_outro(frames,pal,line1='¿Le atinaste? Mide tu golf')
    return render(frames,'quiz-'+slug(pregunta))

# ============================================================
# FORMATO 6 · VERDADERO O FALSO (con escena de campo)
# ============================================================
def video_vf(afirmacion,es_verdad,dato,pal=CREAM):
    frames=[]
    npre=int(dur_lectura(afirmacion,1.0)*FPS)
    tmpq=ImageDraw.Draw(Image.new('RGB',(4,4)))
    fsq=72; qlines=V.wraptext(tmpq,afirmacion,GEO(fsq),W-200)
    while len(qlines)>3 and fsq>52:
        fsq-=4; qlines=V.wraptext(tmpq,afirmacion,GEO(fsq),W-200)
    def draw_af(d):
        qy=560-(len(qlines)-1)*(fsq+16)//2
        for ln in qlines:
            d.text((W//2,qy),ln,font=GEO(fsq),fill=pal['ink'],anchor='mm'); qy+=fsq+16
    def draw_cards(d,hl=None,dim=False):
        for j,(tx,cx) in enumerate([('VERDADERO',W//2-250),('FALSO',W//2+250)]):
            win=(hl==0 and j==0) or (hl==1 and j==1)
            bg=LIME if win else ((255,255,255,240) if not dim else (255,255,255,150))
            fg=(36,48,14) if win else ((30,58,44) if pal is CREAM else (30,58,44))
            d.rounded_rectangle([cx-220,1040,cx+220,1220],40,fill=bg)
            d.text((cx,1130),tx,font=BLACK(52),fill=fg,anchor='mm')
    for k in range(npre):
        t=k/npre
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        d.rounded_rectangle([W//2-320,300,W//2+320,380],40,fill=LIME)
        d.text((W//2,340),'¿VERDADERO O FALSO?',font=BLACK(40),fill=(36,48,14),anchor='mm')
        poptext(d,W//2,700,afirmacion,80,t*1.6,pal['ink'])
        scene_strip(d,pal); progressbar(d,0.12*t,pal); frames.append(V.fin(b))
    for k in range(int(1.6*FPS)):
        t=k/(1.6*FPS)
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        draw_af(d); draw_cards(d)
        scene_strip(d,pal); progressbar(d,0.12+0.16*t,pal); frames.append(V.fin(b))
    for num in (3,2,1):
        for k in range(FPS):
            t=k/FPS
            b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
            draw_af(d); draw_cards(d,dim=True)
            sc=1.35-0.35*ease(t)
            d.text((W//2,1400),str(num),font=BLACK(int(190*sc)),fill=LIMEDK,anchor='mm',
                   stroke_width=6,stroke_fill=pal['ink'])
            scene_strip(d,pal); progressbar(d,0.3+0.3*((3-num)+t)/3,pal); frames.append(V.fin(b))
    nrev=int(dur_lectura(dato,1.4)*FPS)
    hl=0 if es_verdad else 1
    for k in range(nrev):
        t=k/nrev
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        draw_af(d); draw_cards(d,hl=hl)
        poptext(d,W//2,1480,dato,52,t*1.8,pal['ink'])
        scene_strip(d,pal); progressbar(d,0.62+0.3*t,pal); frames.append(V.fin(b))
    cta_outro(frames,pal,line1='Mide tu golf de verdad')
    return render(frames,'vf-'+slug(afirmacion))

# ============================================================
# FORMATO 7 · ¿ENTRA O NO ENTRA? (putt en suspenso)
# ============================================================
def video_entra(entra=True,pal=FOREST):
    frames=[]
    gy=1330
    def campo(d,bx,ball=True,celebra=0.0):
        gcol=(45,88,62) if pal is FOREST else (133,172,96)
        d.ellipse([-340,gy-60,W+340,gy+420],fill=gcol)
        hx=W-240
        d.ellipse([hx-64,gy+8,hx+64,gy+38],fill=(238,236,226))
        d.ellipse([hx-20,gy+14,hx+20,gy+30],fill=(24,28,26))
        d.line([(hx,gy+20),(hx,gy-200)],fill=(238,236,226),width=10)
        wob=math.sin(celebra*math.pi*6)*14 if celebra>0 else 0
        d.polygon([(hx,gy-200),(hx+100+wob,gy-166),(hx,gy-132)],fill=(226,84,64))
        B4.tree(d,180,gy+30,200); B4.cloud(d,260,520,70,{'cloud':(224,228,214) if pal is FOREST else (255,255,255)})
        if ball:
            d.ellipse([bx-26,gy-4,bx+26,gy+48],fill=(252,252,248))
        if celebra>0:
            import random as _r; rnd=_r.Random(9)
            for _ in range(14):
                ang=rnd.uniform(0,math.pi); rr=celebra*rnd.uniform(60,180)
                px,py=hx+math.cos(ang)*rr, gy-10-math.sin(ang)*rr
                d.ellipse([px-9,py-9,px+9,py+9],fill=LIME)
    for k in range(int(1.4*FPS)):
        t=k/(1.4*FPS)
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        poptext(d,W//2,620,'¿ENTRA O NO ENTRA?',94,t*1.6,pal['ink'],font=BLACK)
        campo(d,150); progressbar(d,0.1*t,pal); frames.append(V.fin(b))
    hx=W-240
    n1=int(2.6*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        d.text((W//2,620),'¿ENTRA O NO ENTRA?',font=BLACK(94),fill=pal['ink'],anchor='mm')
        bx=150+(hx-90-150)*ease(t*0.92)
        campo(d,bx)
        progressbar(d,0.1+0.25*t,pal); frames.append(V.fin(b))
    for k in range(int(1.8*FPS)):
        t=k/(1.8*FPS)
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        d.text((W//2,620),'¿ENTRA O NO ENTRA?',font=BLACK(94),fill=pal['ink'],anchor='mm')
        campo(d,hx-90)
        pu=1+0.12*math.sin(t*math.pi*3)
        d.text((W//2,880),'DI TU APUESTA ↓',font=BOLD(int(52*pu)),fill=LIME if pal is FOREST else LIMEDK,anchor='mm')
        progressbar(d,0.35+0.2*t,pal); frames.append(V.fin(b))
    n3=int(2.6*FPS)
    for k in range(n3):
        t=k/(n3-1)
        b,d=canvas(pal); wordmark(d,W//2,180,pal['ink'])
        if entra:
            bx=hx-90+(90-8)*min(t*2.2,1)
            vis = bx<hx-14
            campo(d,bx if vis else hx,ball=vis,celebra=max(0,(t-0.45))/0.55)
            if t>0.5:
                poptext(d,W//2,760,'¡ADENTRO!',110,(t-0.5)/0.5*1.5,pal['ink'],font=BLACK)
        else:
            bx=hx-90+(t*230)
            campo(d,bx)
            if t>0.5:
                poptext(d,W//2,760,'SE PASÓ...',110,(t-0.5)/0.5*1.5,(226,84,64),font=BLACK)
        progressbar(d,0.55+0.35*t,pal); frames.append(V.fin(b))
    cta_outro(frames,pal,line1='Cuenta tus putts de verdad')
    return render(frames,'entra-'+('si' if entra else 'no'))

if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'demo'
    a=sys.argv[2:]
    if cmd=='demo':
        video_app()
        video_dato('41%','up & down','es lo que salva un HCP 15 en sus greens fallados. ¿Y tú?')
        video_razones('Por qué no bajas de 90',
            ['No sabes dónde pierdes tus golpes de verdad.',
             'Practicas al azar, no lo que te falla.',
             'Nunca comparas tu ronda contra una meta.'])
        video_meme_putt()
    elif cmd=='dato': video_dato(a[0],a[1],a[2] if len(a)>2 else '')
    elif cmd=='razones': video_razones(a[0],a[1:])
    elif cmd=='app': video_app()
    elif cmd=='meme': video_meme_putt(*a)
    elif cmd=='quiz': video_quiz(a[0],a[1:4],int(a[4]),a[5])
    elif cmd=='vf': video_vf(a[0],a[1].lower() in ('v','true','si','1'),a[2])
    elif cmd=='entra': video_entra(a[0].lower() in ('si','1','true') if a else True)
    else: print(__doc__)
