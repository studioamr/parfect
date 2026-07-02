#!/usr/bin/env python3
# ============================================================
# PARFECT · LINEA "THEORY" — estilo TheoryGolf (referencia de André)
# Fondo negro-verde premium, diagramas de golf con GLOW que se
# dibujan en vivo, narrativa: creencia común -> la verdad ->
# prueba visual -> CTA. Frame 1 = portada diseñada (grid pro).
#
#   python3 _build_theory.py bandera   # "Deja de tirarle a la bandera"
#   python3 _build_theory.py okay      # "No necesitas jugar perfecto"
#   python3 _build_theory.py demo      # ambos
# Salida: motion/theory-*.mp4
# ============================================================
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter
import _build_viral as V
import _build_motion as M

W,H,FPS=M.W,M.H,M.FPS
BG=(8,14,11)
PAL=dict(bg=BG, ink=(236,241,237), sub=(148,163,152))
INK=PAL['ink']; SUB=PAL['sub']
GREEN=(96,235,140)          # glow verde menta (diagramas)
GREENDIM=(24,62,42)         # superficie del green
LIME=(199,238,84)           # acento de marca (CTA)
RED=(239,96,84)
BOLD=M.BOLD; BLACK=M.BLACK; GEO=M.GEO

def canvas():
    b=Image.new('RGB',(W,H),BG).convert('RGBA')
    return b,ImageDraw.Draw(b,'RGBA')

def glow(base, draw_fn, blur=22, boost=2):
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    draw_fn(ImageDraw.Draw(layer))
    halo=layer.filter(ImageFilter.GaussianBlur(blur))
    for _ in range(boost): base.alpha_composite(halo)
    base.alpha_composite(layer)

def chrome(d,alpha=255):
    M.wordmark(d,W//2,170,INK,52,alpha=alpha)

def titlecard(frames,lines,sub,seconds,accent_idx=None):
    """portada/hook: COMPUESTA desde el frame 1 (nada de fundidos vacios)"""
    n=int(seconds*FPS)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d)
        ty=760-(len(lines)-1)*66
        for i,ln in enumerate(lines):
            col=GREEN if i==accent_idx else INK
            d.text((W//2,ty),ln,font=BLACK(92),fill=col,anchor='mm'); ty+=132
        if sub:
            pu=1+0.02*math.sin(t*math.pi*3)
            d.text((W//2,ty+40),sub,font=BOLD(int(44*pu)),fill=SUB,anchor='mm')
        def g(dd): dd.line([(W//2-330,ty+140),(W//2+330,ty+140)],fill=GREEN+(120,),width=3)
        glow(b,g,16,1)
        M.progressbar(d,0.05+0.05*t,PAL)
        frames.append(V.fin(b))

# ---------- geometría del green (vista cenital) ----------
def green_pts(cx,cy,rx,ry,n=64):
    pts=[]
    for i in range(n+1):
        a=2*math.pi*i/n
        wob=1+0.13*math.sin(a*2.3+1.1)+0.07*math.sin(a*4.7)
        pts.append((cx+math.cos(a)*rx*wob, cy+math.sin(a)*ry*wob))
    return pts

def draw_green(b,d,trace=1.0,flag_xy=None,aim=None,aim_pulse=0):
    cx,cy,rx,ry=W//2,1060,360,300
    pts=green_pts(cx,cy,rx,ry)
    if trace>=1.0:
        d.polygon(pts,fill=GREENDIM+(255,))
    k=max(2,int(len(pts)*min(trace,1.0)))
    def g(dd): dd.line(pts[:k],fill=GREEN+(230,),width=5)
    glow(b,g,20,1)
    d2=ImageDraw.Draw(b,'RGBA')
    if trace>=1.0:
        d2.ellipse([cx-rx-160,cy+60,cx-rx+30,cy+220],fill=(30,44,66,255))      # agua
        d2.ellipse([cx+rx-40,cy-190,cx+rx+150,cy-40],fill=(64,58,40,255))      # bunker
    if flag_xy and trace>=1.0:
        fx,fy=flag_xy
        d2.ellipse([fx-12,fy-6,fx+12,fy+6],fill=(10,20,14))
        d2.line([(fx,fy),(fx,fy-110)],fill=INK,width=6)
        d2.polygon([(fx,fy-110),(fx+62,fy-88),(fx,fy-66)],fill=RED)
    if aim and trace>=1.0:
        ax,ay=aim; r=42+aim_pulse*10
        def g2(dd):
            dd.ellipse([ax-r,ay-r,ax+r,ay+r],outline=GREEN+(255,),width=5)
            dd.ellipse([ax-6,ay-6,ax+6,ay+6],fill=GREEN+(255,))
        glow(b,g2,16,2)

# ============================================================
# THEORY 1 · "Deja de tirarle a la bandera"
# ============================================================
def teoria_bandera():
    rnd=random.Random(7)
    flag=(W//2+250,900)                      # bandera arrinconada (arriba-derecha)
    center=(W//2-40,1080)
    # dispersion realista (misma nube, centrada en el punto de mira)
    cloud=[(rnd.gauss(0,120),rnd.gauss(0,105)) for _ in range(12)]
    def clas(px,py):
        cx,cy,rx,ry=W//2,1060,360,300
        v=((px-cx)/(rx*1.06))**2+((py-cy)/(ry*1.06))**2
        return v<=1.0
    frames=[]
    titlecard(frames,['DEJA DE TIRARLE','A LA BANDERA.'],'(te está costando golpes)',2.6,accent_idx=1)
    # fase 1: green se dibuja
    n1=int(1.6*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,420),'Tu approach no es una línea.',font=GEO(64),fill=INK,anchor='mm')
        d.text((W//2,500),'Es una NUBE de resultados.',font=GEO(64),fill=GREEN,anchor='mm')
        draw_green(b,d,trace=t)
        M.progressbar(d,0.1+0.12*t,PAL); frames.append(V.fin(b))
    # fase 2: tiros a la BANDERA (caen uno a uno; los que fallan, rojos)
    n2=int(3.4*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,420),'12 tiros apuntando',font=GEO(60),fill=INK,anchor='mm')
        d.text((W//2,498),'a la bandera:',font=GEO(60),fill=INK,anchor='mm')
        draw_green(b,d,1.0,flag_xy=flag)
        d2=ImageDraw.Draw(b,'RGBA'); miss=0
        vis=int(len(cloud)*min(t*1.15,1))
        for i in range(vis):
            dx,dy=cloud[i]; px,py=flag[0]+dx,flag[1]+dy
            ok=clas(px,py)
            if not ok: miss+=1
            col=GREEN if ok else RED
            pop=min((t*1.15*len(cloud)-i)*3,1)
            r=11*max(pop,0.3)
            def g3(dd,px=px,py=py,col=col,r=r): dd.ellipse([px-r,py-r,px+r,py+r],fill=col+(255,))
            glow(b,g3,10,1)
        d2=ImageDraw.Draw(b,'RGBA')
        if t>0.75:
            d2.text((W//2,1560),f'{miss} de 12 FALLAN el green',font=BLACK(56),fill=RED,anchor='mm')
        M.progressbar(d,0.22+0.2*t,PAL); frames.append(V.fin(b))
    # fase 3: misma nube al CENTRO
    n3=int(3.6*FPS)
    for k in range(n3):
        t=k/(n3-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,420),'Los MISMOS 12 tiros',font=GEO(60),fill=INK,anchor='mm')
        d.text((W//2,498),'al centro del green:',font=GEO(60),fill=GREEN,anchor='mm')
        draw_green(b,d,1.0,flag_xy=flag,aim=center,aim_pulse=math.sin(t*math.pi*4)*0.5+0.5)
        miss=0
        vis=int(len(cloud)*min(t*1.15,1))
        for i in range(vis):
            dx,dy=cloud[i]; px,py=center[0]+dx,center[1]+dy
            ok=clas(px,py)
            if not ok: miss+=1
            col=GREEN if ok else RED
            r=11
            def g3(dd,px=px,py=py,col=col,r=r): dd.ellipse([px-r,py-r,px+r,py+r],fill=col+(255,))
            glow(b,g3,10,1)
        d2=ImageDraw.Draw(b,'RGBA')
        if t>0.75:
            d2.text((W//2,1560),f'{12-miss} de 12 EN el green',font=BLACK(56),fill=GREEN,anchor='mm')
        M.progressbar(d,0.42+0.2*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('El centro del green es el tiro de los que bajan handicap',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,860,'El centro del green es el tiro',72,t*1.8,INK)
        M.poptext(d,W//2,980,'de los que bajan hándicap.',72,max(t*1.8-0.2,0),GREEN)
        d.text((W//2,1200),'La bandera es marketing. El green es score.',font=BOLD(40),fill=SUB,anchor='mm')
        M.progressbar(d,0.64+0.2*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT mide tus greens reales')
    return M.render(frames,'theory-bandera')

# ============================================================
# THEORY 2 · "No necesitas jugar perfecto"
# ============================================================
def teoria_okay():
    stats=[('FAIRWAYS',56),('GREENS EN REG.',33),('UP & DOWN',41),('SIN 3-PUTTS',72)]
    frames=[]
    titlecard(frames,['NO NECESITAS','JUGAR PERFECTO.'],'(nadie juega perfecto)',2.6,accent_idx=1)
    def bars(b,d,vals,t,col):
        by=760
        for i,((lab,tgt),shown) in enumerate(zip(stats,vals)):
            d.text((150,by),lab,font=BOLD(38),fill=SUB,anchor='lm')
            x0,x1=150,W-150
            d.rounded_rectangle([x0,by+34,x1,by+58],12,fill=(255,255,255,22))
            wv=(x1-x0)*shown/100*min(t*1.3,1)
            if wv>4:
                def g(dd,wv=wv,by=by): dd.rounded_rectangle([x0,by+34,x0+wv,by+58],12,fill=col+(255,))
                glow(b,g,14,1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((x1,by),f'{int(shown*min(t*1.3,1))}%',font=BLACK(40),fill=col,anchor='rm')
            by+=170
        return by
    n1=int(3.0*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,430),'Lo que crees que necesitas:',font=GEO(58),fill=INK,anchor='mm')
        bars(b,d,[100,100,100,100],t,RED)
        d=ImageDraw.Draw(b,'RGBA')
        if t>0.7:
            d.text((W//2,1560),'NADIE juega así. Ni Tiger.',font=BLACK(54),fill=RED,anchor='mm')
        M.progressbar(d,0.1+0.22*t,PAL); frames.append(V.fin(b))
    n2=int(3.4*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,430),'Lo que tira un HCP 10 REAL:',font=GEO(58),fill=GREEN,anchor='mm')
        bars(b,d,[s[1] for s in stats],t,GREEN)
        d=ImageDraw.Draw(b,'RGBA')
        if t>0.7:
            d.text((W//2,1560),'Solo necesitas jugar OKAY.',font=BLACK(54),fill=GREEN,anchor='mm')
        M.progressbar(d,0.34+0.24*t,PAL); frames.append(V.fin(b))
    nin=int(M.dur_lectura('okay y saber exactamente donde mejorar con datos',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,840,'Jugar OKAY...',86,t*1.8,INK)
        M.poptext(d,W//2,980,'y saber DÓNDE mejorar.',86,max(t*1.8-0.25,0),GREEN)
        d.text((W//2,1200),'Eso es todo el secreto.',font=BOLD(42),fill=SUB,anchor='mm')
        M.progressbar(d,0.6+0.24*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT te dice tu DÓNDE')
    return M.render(frames,'theory-okay')

if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'demo'
    if cmd=='bandera': teoria_bandera()
    elif cmd=='okay': teoria_okay()
    else:
        teoria_bandera(); teoria_okay()
