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
import os, sys, math, random, json
from PIL import Image, ImageDraw, ImageFilter
import _build_viral as V
import _build_motion as M

W,H,FPS=M.W,M.H,M.FPS
BG=(8,14,11)
PAL=dict(bg=(14,44,22), ink=(236,241,237), sub=(148,163,152))
INK=PAL['ink']; SUB=(206,223,203)
GREEN=(96,235,140)          # glow verde menta (diagramas)
GREENDIM=(24,62,42)         # superficie del green
LIME=(199,238,84)           # acento de marca (CTA)
RED=(239,96,84)
BOLD=M.BOLD; BLACK=M.BLACK; GEO=M.GEO

def _bg_img():
    """fondo 'PARFECT DAY': el mundo de la landing (cielo/sol/nubes/lomas)
    y el contenido sobre campo verde profundo (los glow leen como TV tracer)"""
    img=Image.new('RGB',(W,H),(31,82,40)).convert('RGBA')
    d=ImageDraw.Draw(img)
    for y in range(360):
        t=y/359
        d.line([(0,y),(W,y)],fill=(int(121+86*t),int(205+33*t),int(236+15*t)))
    sun=Image.new('RGBA',(W,H),(0,0,0,0))
    ImageDraw.Draw(sun).ellipse([W-320,30,W-100,250],fill=(255,224,122,225))
    img.alpha_composite(sun.filter(ImageFilter.GaussianBlur(60)))
    cl=Image.new('RGBA',(W,H),(0,0,0,0)); dc=ImageDraw.Draw(cl)
    dc.ellipse([80,110,430,215],fill=(255,255,255,215))
    dc.ellipse([610,195,880,275],fill=(255,255,255,180))
    img.alpha_composite(cl.filter(ImageFilter.GaussianBlur(14)))
    hl=Image.new('RGBA',(W,H),(0,0,0,0)); dh=ImageDraw.Draw(hl)
    dh.ellipse([-320,250,720,600],fill=(121,185,79,255))
    dh.ellipse([420,270,1420,640],fill=(93,160,66,255))
    img.alpha_composite(hl)
    fld=Image.new('RGBA',(W,H),(0,0,0,0)); df=ImageDraw.Draw(fld)
    top=(56,128,64); bot=(16,50,24)
    for y in range(395,H):
        t=(y-395)/(H-395)
        df.line([(0,y),(W,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3))+(255,))
    img.alpha_composite(fld)
    st=Image.new('RGBA',(W,H),(0,0,0,0)); ds=ImageDraw.Draw(st)
    for i,x in enumerate(range(-260,W+420,180)):
        if i%2==0: ds.polygon([(x,395),(x+180,395),(x+70,H),(x-110,H)],fill=(255,255,255,9))
    img.alpha_composite(st)
    vg=Image.new('RGBA',(W,H),(0,0,0,0))
    ImageDraw.Draw(vg).rectangle([0,H-460,W,H],fill=(0,18,8,66))
    img.alpha_composite(vg.filter(ImageFilter.GaussianBlur(150)))
    return img
BGIMG=_bg_img()

def canvas():
    b=BGIMG.copy()
    return b,ImageDraw.Draw(b,'RGBA')

def glow(base, draw_fn, blur=22, boost=2):
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    draw_fn(ImageDraw.Draw(layer))
    halo=layer.filter(ImageFilter.GaussianBlur(blur))
    for _ in range(boost): base.alpha_composite(halo)
    base.alpha_composite(layer)

DINK=(18,46,25)   # tinta bosque para el cielo
def chrome(d,alpha=255,ep=None):
    M.wordmark(d,W//2,170,DINK,52,alpha=alpha)
    if ep:
        d.text((W-84,172),f'THEORY · EP {ep:02d}',font=BOLD(27),fill=DINK+(min(alpha,220),),anchor='rm')
        d.text((84,172),'@parfectapp',font=BOLD(27),fill=DINK+(min(alpha,180),),anchor='lm')

def titlecard(frames,lines,sub,seconds,accent_idx=None):
    """portada/hook: gancho VISUAL (putt con estela al pin) + titulo, legible"""
    full=' '.join(lines)+' '+(sub or '')
    seconds=max(seconds, M.dur_lectura(full,1.0))
    n=int(seconds*FPS)
    pinx,gy=W-240,1560
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d)
        # ----- gancho visual abajo: bola rodando al hoyo -----
        def gl(dd): dd.line([(90,gy),(W-90,gy)],fill=GREEN+(80,),width=3)
        glow(b,gl,14,1)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.ellipse([pinx-40,gy-8,pinx+40,gy+10],fill=(14,24,18,255))
        d2.ellipse([pinx-14,gy-4,pinx+14,gy+6],fill=(6,10,8,255))
        wob=math.sin(t*math.pi*5)*10
        d2.line([(pinx,gy),(pinx,gy-150)],fill=INK,width=5)
        d2.polygon([(pinx,gy-150),(pinx+66+wob,gy-128),(pinx,gy-104)],fill=RED)
        bt=min(t/0.5,1.0); be=M.ease(bt)
        bx=150+(pinx-26-150)*be
        if bt<1.0:
            for j in range(6):
                tx=bx-(j+1)*26
                if tx>140:
                    def gt(dd,tx=tx,a=int(150*(1-j/6))): dd.ellipse([tx-5,gy-11,tx+5,gy-1],fill=GREEN+(a,))
                    glow(b,gt,8,1)
            d2.ellipse([bx-13,gy-19,bx+13,gy+7],fill=(250,250,246))
        else:
            rp=((t-0.5)*2.2)%1.0; rr=16+rp*55
            def gr(dd): dd.ellipse([pinx-rr,gy-6-rr*0.35,pinx+rr,gy+6+rr*0.35],outline=GREEN+(int(220*(1-rp)),),width=5)
            glow(b,gr,10,1)
        # ----- titulo con pop escalonado -----
        ty=700-(len(lines)-1)*66
        for i,ln in enumerate(lines):
            col=GREEN if i==accent_idx else INK
            M.poptext(d,W//2,ty,ln,92,(t-0.06*i)*2.4,col,font=BLACK,maxw=W-140)
            ty+=132
        if sub and t>0.28:
            d.text((W//2,ty+40),sub,font=BOLD(44),fill=SUB,anchor='mm')
        M.progressbar(d,0.05+0.05*t,PAL)
        frames.append(V.fin(b))

def titlecard_rain(frames,lines,sub,seconds,accent_idx=None):
    """gancho alternativo: LLUVIA de tiros cayendo sobre un mini-green"""
    full=' '.join(lines)+' '+(sub or '')
    seconds=max(seconds, M.dur_lectura(full,1.0))
    n=int(seconds*FPS)
    import random as _r; rnd=_r.Random(11)
    pts=[(rnd.gauss(0,120),rnd.gauss(0,80)) for _ in range(14)]
    gcx,gcy=W//2,1590
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d)
        # mini green cenital
        gp=green_pts(gcx,gcy,300,190)
        d.polygon(gp,fill=GREENDIM+(255,))
        def gg(dd): dd.line(gp,fill=GREEN+(180,),width=4)
        glow(b,gg,16,1)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.line([(gcx,gcy),(gcx,gcy-95)],fill=INK,width=5)
        d2.polygon([(gcx,gcy-95),(gcx+52,gcy-77),(gcx,gcy-59)],fill=RED)
        # tiros cayendo uno por uno
        vis=int(len(pts)*min(t*1.3,1))
        for i in range(vis):
            dx,dy=pts[i]; px,py=gcx+dx,gcy+dy
            dentro=((dx/315)**2+(dy/200)**2)<=1
            col=GREEN if dentro else RED
            pop=min((t*1.3*len(pts)-i)*3,1); r=10*max(pop,0.4)
            def gd(dd,px=px,py=py,col=col,r=r): dd.ellipse([px-r,py-r,px+r,py+r],fill=col+(255,))
            glow(b,gd,9,1)
        ty=640-(len(lines)-1)*66
        for i,ln in enumerate(lines):
            col=GREEN if i==accent_idx else INK
            M.poptext(d,W//2,ty,ln,92,(t-0.06*i)*2.4,col,font=BLACK,maxw=W-140)
            ty+=132
        if sub and t>0.28:
            d.text((W//2,ty+40),sub,font=BOLD(44),fill=SUB,anchor='mm')
        M.progressbar(d,0.05+0.05*t,PAL)
        frames.append(V.fin(b))

def ftxt(d,xy,txt,font,fill,t,anchor='mm',t_out=0.86,rise=8):
    """texto smooth SUBPIXEL: el offset fraccional se reparte entre dos draws
    ponderados -> el movimiento se ve continuo a 30fps (sin brincos de pixel)"""
    if t<=0: return
    if t<t_out:
        p=min(t*3.2,1.0); a=p*p*(3-2*p)
        off=rise*(1-p)**2
    else:
        q=min((t-t_out)/(1.0-t_out),1.0); a=1-q*q*(3-2*q)
        off=-rise*0.45*q*q
    if a<=0.02: return
    yf=xy[1]+off; y0=math.floor(yf); fr=yf-y0
    d.text((xy[0],y0),txt,font=font,fill=fill+(int(255*a*(1-fr)),),anchor=anchor,stroke_width=4,stroke_fill=(10,30,16,int(210*a*(1-fr))))
    if fr>0.04: d.text((xy[0],y0+1),txt,font=font,fill=fill+(int(255*a*fr),),anchor=anchor,stroke_width=4,stroke_fill=(10,30,16,int(210*a*fr)))

def titlecard_cone(frames,lines,sub,seconds,accent_idx=None):
    """gancho #3: ABANICO de trayectorias abriendose desde el tee"""
    full=' '.join(lines)+' '+(sub or '')
    seconds=max(seconds, M.dur_lectura(full,1.0))
    n=int(seconds*FPS)
    tee=(W//2,1830)
    angs=[-38,-25,-13,0,13,25,38]
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d)
        for i,ang in enumerate(angs):
            ft=min(max(t*2.2-i*0.12,0),1)
            if ft<=0: continue
            L=560*M.ease(ft)
            rad=math.radians(ang)
            ex,ey=tee[0]+math.sin(rad)*L, tee[1]-math.cos(rad)*L
            col=GREEN if abs(ang)<20 else RED
            def gl(dd,ex=ex,ey=ey,col=col,ft=ft):
                dd.line([tee,(ex,ey)],fill=col+(int(200*ft),),width=5)
                dd.ellipse([ex-9,ey-9,ex+9,ey+9],fill=col+(int(255*ft),))
            glow(b,gl,10,1)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.ellipse([tee[0]-14,tee[1]-8,tee[0]+14,tee[1]+10],fill=(240,240,230))
        ty=620-(len(lines)-1)*66
        for i,ln in enumerate(lines):
            col=GREEN if i==accent_idx else INK
            M.poptext(d,W//2,ty,ln,92,(t-0.06*i)*2.4,col,font=BLACK,maxw=W-140)
            ty+=132
        if sub and t>0.28:
            d.text((W//2,ty+40),sub,font=BOLD(44),fill=SUB,anchor='mm')
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
    n1=int(2.2*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,420),'Tu approach no es una línea.',font=GEO(64),fill=INK,anchor='mm')
        d.text((W//2,500),'Es una NUBE de resultados.',font=GEO(64),fill=GREEN,anchor='mm')
        draw_green(b,d,trace=t)
        M.progressbar(d,0.1+0.12*t,PAL); frames.append(V.fin(b))
    # fase 2: tiros a la BANDERA (caen uno a uno; los que fallan, rojos)
    n2=int(4.6*FPS)
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
        if t>0.55:
            d2.text((W//2,1560),f'{miss} de 12 FALLAN el green',font=BLACK(56),fill=RED,anchor='mm')
        M.progressbar(d,0.22+0.2*t,PAL); frames.append(V.fin(b))
    # fase 3: misma nube al CENTRO
    n3=int(4.8*FPS)
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
        if t>0.55:
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
    n1=int(4.2*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,430),'Lo que crees que necesitas:',font=GEO(58),fill=INK,anchor='mm')
        bars(b,d,[100,100,100,100],t,RED)
        d=ImageDraw.Draw(b,'RGBA')
        if t>0.5:
            d.text((W//2,1560),'NADIE juega así. Ni Tiger.',font=BLACK(54),fill=RED,anchor='mm')
        M.progressbar(d,0.1+0.22*t,PAL); frames.append(V.fin(b))
    n2=int(4.6*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,430),'Lo que tira un HCP 10 REAL:',font=GEO(58),fill=GREEN,anchor='mm')
        bars(b,d,[s[1] for s in stats],t,GREEN)
        d=ImageDraw.Draw(b,'RGBA')
        if t>0.5:
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

# ============================================================
# THEORY 25 · "Velocidad > linea" (hoyo efectivo por velocidad)
# ============================================================
def teoria_velocidad():
    datos=[('MURIENDO en el hoyo','4.25\"','el hoyo completo',1.00),
           ('0.5 m pasado','2.25\"','medio hoyo',0.53),
           ('1 m pasado','1.9\"','menos de la mitad',0.45),
           ('1.5 m pasado','1.4\"','más chico que la bola',0.33)]
    frames=[]
    titlecard(frames,['TU PUTT NO FALLA','POR LA LÍNEA.'],'(falla por la velocidad)',2.8,accent_idx=1)
    total=len(datos); per=3.0
    for i,(lab,size,sub2,frac) in enumerate(datos):
        n=int(per*FPS)
        for k in range(n):
            t=k/(n-1)
            b,d=canvas(); chrome(d)
            d.text((W//2,420),'El hoyo "se encoge" si pasas:',font=GEO(58),fill=INK,anchor='mm')
            ry=680
            for j in range(i+1):
                lab2,size2,sub3,frac2=datos[j]
                act=(j==i)
                a=1.0 if act else 0.55
                rr=int(95*frac2*(M.ease(t) if act else 1.0))
                col=GREEN if frac2>0.5 else (RED if frac2<0.4 else (238,205,90))
                def g(dd,rr=rr,ry=ry,col=col,a=a):
                    dd.ellipse([W//2-150-rr,ry-rr,W//2-150+rr,ry+rr],outline=col+(int(255*a),),width=6)
                glow(b,g,14,1)
                d2=ImageDraw.Draw(b,'RGBA')
                d2.ellipse([W//2-150-14,ry-14,W//2-150+14,ry+14],fill=(240,240,236,int(255*a)))
                d2.text((W//2+40,ry-26),lab2,font=BOLD(40),fill=(INK if act else SUB),anchor='lm')
                d2.text((W//2+40,ry+30),f'{size2} — {sub3}',font=BOLD(34),fill=(col if act else SUB),anchor='lm')
                ry+=250
            d=ImageDraw.Draw(b,'RGBA')
            M.progressbar(d,0.12+0.55*((i+t)/total),PAL); frames.append(V.fin(b))
    nin=int(M.dur_lectura('llega muriendo al hoyo y la linea te perdona',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,860,'Llega MURIENDO al hoyo...',80,t*1.8,INK)
        M.poptext(d,W//2,1000,'y la línea te perdona.',80,max(t*1.8-0.25,0),GREEN)
        d.text((W//2,1220),'Practica velocidad, no lecturas perfectas.',font=BOLD(40),fill=SUB,anchor='mm')
        M.progressbar(d,0.7+0.2*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT cuenta tus putts reales')
    return M.render(frames,'theory-velocidad')

# ============================================================
# THEORY 2 · "Par 5: la meta no es eagle, es evitar el bogey"
# ============================================================
def teoria_par5():
    tee=(W//2+40,1760); green_c=(W//2-40,560)
    agua=(W//2+230,1050)
    def hole(b,d,trace=1.0):
        # fairway
        fw=[(W//2-250,1780),(W//2-310,1300),(W//2-260,900),(W//2-190,640),
            (W//2+120,620),(W//2+230,880),(W//2+280,1320),(W//2+240,1780)]
        d.polygon(fw,fill=(18,42,30,255))
        def g(dd):
            k=max(2,int(len(fw)*min(trace,1)))
            dd.line(fw[:k]+([fw[0]] if trace>=1 else []),fill=GREEN+(160,),width=4)
        glow(b,g,18,1)
        d2=ImageDraw.Draw(b,'RGBA')
        # agua a la derecha a mitad de camino
        d2.ellipse([agua[0]-150,agua[1]-110,agua[0]+170,agua[1]+120],fill=(30,48,74,255))
        d2.text((agua[0]+8,agua[1]),'AGUA',font=BOLD(30),fill=(120,150,190),anchor='mm')
        # green arriba
        d2.ellipse([green_c[0]-150,green_c[1]-95,green_c[0]+150,green_c[1]+95],fill=GREENDIM)
        def g2(dd): dd.ellipse([green_c[0]-150,green_c[1]-95,green_c[0]+150,green_c[1]+95],outline=GREEN+(220,),width=4)
        glow(b,g2,16,1)
        d2.line([(green_c[0]+40,green_c[1]),(green_c[0]+40,green_c[1]-95)],fill=INK,width=5)
        d2.polygon([(green_c[0]+40,green_c[1]-95),(green_c[0]+92,green_c[1]-78),(green_c[0]+40,green_c[1]-58)],fill=RED)
        # tee
        d2.ellipse([tee[0]-16,tee[1]-16,tee[0]+16,tee[1]+16],fill=INK)
    def arco(b,pts,t,color,dash=False):
        (x0,y0),(x1,y1)=pts
        n=26; seg=[]
        for i in range(int(n*min(t,1))+1):
            u=i/n
            x=x0+(x1-x0)*u; y=y0+(y1-y0)*u-math.sin(u*math.pi)*130
            seg.append((x,y))
        if len(seg)>1:
            def g(dd): dd.line(seg,fill=color+(240,),width=7)
            glow(b,g,14,1)
        return seg[-1] if seg else pts[0]
    frames=[]
    titlecard(frames,['EN EL PAR 5 LA META','NO ES EAGLE.'],'(es evitar el BOGEY)',2.8,accent_idx=1)
    # fase 1: el mapa se dibuja
    n1=int(2.0*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,340),'El hoyo más peligroso del campo:',font=GEO(54),fill=INK,anchor='mm')
        hole(b,d,trace=t)
        M.progressbar(d,0.1+0.1*t,PAL); frames.append(V.fin(b))
    # fase 2: ruta HEROE (2 canonazos, el 2o al agua)
    n2=int(4.6*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,340),'La ruta del HÉROE: llegar en 2',font=GEO(54),fill=RED,anchor='mm')
        hole(b,d)
        p1=arco(b,[tee,(W//2-60,1180)],t*2,RED)
        if t>0.5:
            arco(b,[(W//2-60,1180),(agua[0]-10,agua[1]+10)],(t-0.5)*2.4,RED)
        d2=ImageDraw.Draw(b,'RGBA')
        if t>0.55:
            r=int(28+40*((t-0.72)/0.28))
            def gs(dd): dd.ellipse([agua[0]-10-r,agua[1]+10-r,agua[0]-10+r,agua[1]+10+r],outline=RED+(255,),width=8)
            glow(b,gs,12,1)
            d2.text((W//2,1560),'SPLASH. Doble bogey.',font=BLACK(56),fill=RED,anchor='mm')
        M.progressbar(d,0.2+0.2*t,PAL); frames.append(V.fin(b))
    # fase 3: ruta INTELIGENTE (3 tiros comodos)
    n3=int(5.0*FPS)
    for k in range(n3):
        t=k/(n3-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,340),'La ruta del que SÍ baja: 3 tiros',font=GEO(54),fill=GREEN,anchor='mm')
        hole(b,d)
        arco(b,[tee,(W//2-140,1330)],t*3,GREEN)
        if t>0.33: arco(b,[(W//2-140,1330),(W//2-190,900)],(t-0.33)*3,GREEN)
        if t>0.66: arco(b,[(W//2-190,900),green_c],(t-0.66)*3,GREEN)
        d2=ImageDraw.Draw(b,'RGBA')
        if t>0.62:
            d2.text((W//2,1560),'PAR fácil. Birdie de regalo.',font=BLACK(56),fill=GREEN,anchor='mm')
        M.progressbar(d,0.42+0.22*t,PAL); frames.append(V.fin(b))
    nin=int(M.dur_lectura('tres tiros aburridos ganan a un tiro de heroe',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,880,'3 tiros aburridos',88,t*1.8,INK)
        M.poptext(d,W//2,1020,'> 1 tiro de héroe.',88,max(t*1.8-0.25,0),GREEN)
        d.text((W//2,1240),'El eagle vende. El par paga.',font=BOLD(42),fill=SUB,anchor='mm')
        M.progressbar(d,0.66+0.2*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT mide tus pares 5 reales')
    return M.render(frames,'theory-par5')

# ============================================================
# THEORY 17 · "Un scratch hace 30 putts. Tu, ¿cuantos?"
# ============================================================
def teoria_putts30():
    tj=os.path.join(os.path.dirname(os.path.abspath(__file__)),'_voz','theory-putts30','timing.json')
    T=json.load(open(tj)) if os.path.exists(tj) else {}
    frames=[]
    titlecard(frames,['UN SCRATCH HACE','30 PUTTS.'],'(tú, ¿cuántos haces?)',T.get('title',2.8),accent_idx=1)
    filas=[('SCRATCH (HCP 0)',30,GREEN),('HCP 10',32,(238,205,90)),('HCP 20',34,(238,150,84)),('AMATEUR PROMEDIO',36,RED)]
    n1=int(T.get('bars',5.2)*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,400),'Putts por ronda:',font=GEO(60),fill=INK,anchor='mm')
        by=640
        for i,(lab,val,col) in enumerate(filas):
            ft=min(max(t*len(filas)-i,0),1)
            d.text((150,by),lab,font=BOLD(38),fill=SUB,anchor='lm')
            x0,x1=150,W-150
            d.rounded_rectangle([x0,by+34,x1,by+58],12,fill=(255,255,255,22))
            wv=(x1-x0)*(val/40)*M.ease(ft)
            if wv>4:
                def g(dd,wv=wv,by=by,col=col): dd.rounded_rectangle([x0,by+34,x0+wv,by+58],12,fill=col+(255,))
                glow(b,g,14,1)
            d2=ImageDraw.Draw(b,'RGBA')
            if ft>0: d2.text((x1,by),str(int(val*M.ease(ft))),font=BLACK(44),fill=col,anchor='rm')
            by+=170
        d=ImageDraw.Draw(b,'RGBA')
        if t>0.72:
            d.text((W//2,1500),'6 golpes de diferencia. En el GREEN.',font=BLACK(50),fill=RED,anchor='mm')
        M.progressbar(d,0.12+0.5*t,PAL); frames.append(V.fin(b))
    nin=int(max(M.dur_lectura('esos 6 golpes no estan en tu swing estan en tu putter y no los cuentas',1.2),T.get('insight',0))*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,820,'Esos 6 golpes no están',80,t*1.8,INK)
        M.poptext(d,W//2,950,'en tu swing.',80,max(t*1.8-0.2,0),INK)
        M.poptext(d,W//2,1120,'Están en tu putter.',84,max(t*1.8-0.45,0),GREEN)
        d.text((W//2,1330),'Y no los estás contando.',font=BOLD(42),fill=SUB,anchor='mm')
        M.progressbar(d,0.64+0.24*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,seconds=T.get('outro',2.8),line1='PARFECT cuenta tus putts, hoyo x hoyo')
    return M.render(frames,'theory-putts30')

# ============================================================
# THEORY 16 · "Cada 3-putt son 2 golpes regalados"
# ============================================================
def teoria_3putts():
    frames=[]
    titlecard(frames,['CADA 3-PUTT SON','2 GOLPES REGALADOS.'],'(y no los estás contando)',2.8,accent_idx=1)
    eventos=[('Hoyo 4','3 putts',2),('Hoyo 9','3 putts',4),('Hoyo 15','3 putts',6)]
    per=3.2
    for i,(hoyo,que,total) in enumerate(eventos):
        n=int(per*FPS)
        for k in range(n):
            t=k/(n-1)
            b,d=canvas(); chrome(d)
            d.text((W//2,400),'Tu ronda del sábado:',font=GEO(56),fill=INK,anchor='mm')
            d.text((W//2,620),hoyo,font=BOLD(54),fill=SUB,anchor='mm')
            sc=1.3-0.3*M.ease(min(t*2,1))
            d.text((W//2,850),que,font=BLACK(int(96*sc)),fill=RED,anchor='mm',stroke_width=3,stroke_fill=(90,30,26))
            if t>0.35:
                M.poptext(d,W//2,1050,'+2 golpes',66,(t-0.35)*2.2,RED,font=BLACK)
            d.text((W//2,1350),'REGALADOS HOY:',font=BOLD(40),fill=SUB,anchor='mm')
            val=total-2+int(2*M.ease(min(max(t*2-0.6,0),1)))
            def g(dd,val=val): dd.text((W//2,1500),str(val),font=BLACK(150),fill=GREEN+(255,),anchor='mm')
            glow(b,g,18,1)
            M.progressbar(d,0.12+0.5*((i+t)/len(eventos)),PAL); frames.append(V.fin(b))
    nin=int(M.dur_lectura('seis golpes por ronda son la diferencia entre 95 y 89 y estan en el green',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,780,'6 golpes por ronda.',88,t*1.8,INK)
        M.poptext(d,W//2,920,'La diferencia entre 95 y 89.',72,max(t*1.8-0.25,0),GREEN)
        d.text((W//2,1140),'Y todos viven en el green.',font=BOLD(42),fill=SUB,anchor='mm')
        M.progressbar(d,0.64+0.24*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT cuenta tus 3-putts solos')
    return M.render(frames,'theory-3putts')

# ============================================================
# THEORY 21 · "Tu wedge no cae donde crees" (anillos de proximidad)
# ============================================================
def teoria_wedges():
    frames=[]
    titlecard_rain(frames,['TU WEDGE NO CAE','DONDE CREES.'],'(la dispersión real duele)',3.0,accent_idx=1)
    gcx,gcy=W//2,1030
    anillos=[(95,'2 m',GREEN),(210,'5 m',(238,205,90)),(330,'8 m',RED)]
    import random as _r; rnd=_r.Random(21)
    tiros=[(rnd.gauss(0,150),rnd.gauss(0,105)) for _ in range(12)]
    def base_green(b,d,ring_t=1.0):
        gp=green_pts(gcx,gcy,430,320)
        d.polygon(gp,fill=GREENDIM+(255,))
        def gg(dd): dd.line(gp,fill=GREEN+(150,),width=4)
        glow(b,gg,16,1)
        d2=ImageDraw.Draw(b,'RGBA')
        for i,(r,lab,col) in enumerate(anillos):
            ft=min(max(ring_t*3-i,0),1)
            if ft<=0: continue
            rr=r*M.ease(ft); ry=rr*0.72
            def ga(dd,rr=rr,ry=ry,col=col): dd.ellipse([gcx-rr,gcy-ry,gcx+rr,gcy+ry],outline=col+(220,),width=4)
            glow(b,ga,10,1)
            if ft>0.9: d2.text((gcx+rr-6,gcy-ry-26),lab,font=BOLD(30),fill=col,anchor='rm')
        d2.line([(gcx,gcy),(gcx,gcy-85)],fill=INK,width=5)
        d2.polygon([(gcx,gcy-85),(gcx+48,gcy-69),(gcx,gcy-53)],fill=RED)
    n1=int(2.6*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,380),'Desde 100 yardas,',font=GEO(58),fill=INK,anchor='mm')
        d.text((W//2,458),'¿qué tan cerca la dejas?',font=GEO(58),fill=GREEN,anchor='mm')
        base_green(b,d,ring_t=t)
        M.progressbar(d,0.1+0.14*t,PAL); frames.append(V.fin(b))
    n2=int(4.8*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        d.text((W//2,380),'12 wedges del amateur',font=GEO(58),fill=INK,anchor='mm')
        d.text((W//2,458),'promedio:',font=GEO(58),fill=INK,anchor='mm')
        base_green(b,d)
        vis=int(len(tiros)*min(t*1.2,1)); cerca=0
        for i in range(vis):
            dx,dy=tiros[i]; px,py=gcx+dx,gcy+dy*0.72
            dist=(dx*dx+dy*dy)**0.5
            if dist<95: cerca+=1
            col=GREEN if dist<95 else ((238,205,90) if dist<210 else RED)
            def gd(dd,px=px,py=py,col=col): dd.ellipse([px-11,py-11,px+11,py+11],fill=col+(255,))
            glow(b,gd,9,1)
        d2=ImageDraw.Draw(b,'RGBA')
        if t>0.6:
            d2.text((W//2,1560),f'Solo {cerca} de 12 quedan a tiro de birdie',font=BLACK(48),fill=RED,anchor='mm')
        M.progressbar(d,0.24+0.3*t,PAL); frames.append(V.fin(b))
    nin=int(M.dur_lectura('el promedio queda a 8 metros planea el putt largo no el tap-in',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,800,'El wedge promedio queda',76,t*1.8,INK)
        M.poptext(d,W//2,930,'a 8 METROS del hoyo.',80,max(t*1.8-0.2,0),GREEN)
        d.text((W//2,1150),'Planea el putt largo, no el tap-in.',font=BOLD(42),fill=SUB,anchor='mm')
        M.progressbar(d,0.62+0.26*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT mide tu juego corto real')
    return M.render(frames,'theory-wedges')

# ============================================================
# THEORY 20 · "Tu drive cae en una ELIPSE, no en un punto"
# ============================================================
def teoria_drive():
    frames=[]
    titlecard_cone(frames,['TU DRIVE NO CAE','EN UN PUNTO.'],'(cae en una elipse)',3.0,accent_idx=1)
    tee=(W//2,1800)
    import random as _r; rnd=_r.Random(20)
    drives=[(rnd.gauss(0,120),rnd.gauss(0,70)) for _ in range(12)]
    cx,cy=W//2,900   # centro de aterrizaje
    def fairway(b,d):
        fw=[(W//2-210,1840),(W//2-260,1250),(W//2-215,760),(W//2-140,540),
            (W//2+150,560),(W//2+235,800),(W//2+265,1300),(W//2+220,1840)]
        d.polygon(fw,fill=(18,42,30,255))
        def g(dd): dd.line(fw+[fw[0]],fill=GREEN+(140,),width=4)
        glow(b,g,16,1)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.ellipse([tee[0]-13,tee[1]-8,tee[0]+13,tee[1]+9],fill=(240,240,230))
        return d2
    # fase 1: la fantasia (una linea recta al centro)
    n1=int(3.2*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,390),'En tu cabeza, tu drive va AQUÍ:',GEO(58),INK,t)
        fairway(b,d)
        L=M.ease(min(t*1.6,1))
        def gl(dd): dd.line([tee,(tee[0]+(cx-tee[0])*L,tee[1]+(cy-tee[1])*L)],fill=GREEN+(230,),width=6)
        glow(b,gl,12,1)
        d2=ImageDraw.Draw(b,'RGBA')
        if t>0.55:
            def gp(dd): dd.ellipse([cx-13,cy-13,cx+13,cy+13],fill=GREEN+(255,))
            glow(b,gp,10,1)
            tt=(t-0.55)/0.45
            a=min(tt*5,1.0) if tt<0.86 else max(0.0,(1.0-tt)/0.14)
            if a>0.02:
                d2.text((W//2,1560),'Un punto perfecto.',font=BLACK(50),fill=GREEN+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.1+0.16*t,PAL); frames.append(V.fin(b))
    # fase 2: la realidad (12 drives = elipse)
    n2=int(5.4*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,390),'Tus 12 drives REALES del mes:',GEO(58),INK,t)
        d2=fairway(b,d)
        fuera=0
        vis=int(len(drives)*min(t*1.25,1))
        for i in range(vis):
            dx,dy=drives[i]; px,py=cx+dx,cy+dy
            enf=abs(dx)<205
            if not enf: fuera+=1
            col=GREEN if enf else RED
            def gd(dd,px=px,py=py,col=col): dd.ellipse([px-11,py-11,px+11,py+11],fill=col+(255,))
            glow(b,gd,9,1)
        if t>0.62:
            et=(t-0.62)/0.38
            rr=290*M.ease(min(et*1.4,1)); ry=rr*0.55
            def ge(dd): dd.ellipse([cx-rr,cy-ry,cx+rr,cy+ry],outline=(238,205,90,240),width=5)
            glow(b,ge,12,1)
            d3=ImageDraw.Draw(b,'RGBA')
            a=min(et*5,1.0) if et<0.86 else max(0.0,(1.0-et)/0.14)
            if a>0.02:
                d3.text((W//2,1560),f'Esto es una ELIPSE de 40 m — {fuera} al rough',font=BLACK(44),fill=(238,205,90,int(255*a)),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.26+0.28*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('no juegues tu mejor drive juega tu elipse completa apunta donde quepa',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,780,'No juegues tu MEJOR drive.',76,t*1.8,INK)
        M.poptext(d,W//2,920,'Juega tu ELIPSE completa.',80,max(t*1.8-0.25,0),GREEN)
        if t>0.4:
            ftxt(d,(W//2,1140),'Apunta donde tu elipse quepa entera.',BOLD(42),SUB,(t-0.4)/0.6,t_out=0.92)
        M.progressbar(d,0.62+0.26*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT mide tus fairways reales')
    return M.render(frames,'theory-drive')

# ============================================================
# THEORY 23 · "Tu score vive en 100 yardas y menos" (dona)
# ============================================================
def teoria_100y():
    frames=[]
    # gancho #4: anillo dibujandose + % fantasma
    lines=['TU SCORE NO SE HACE','CON EL DRIVER.']; sub='(se hace en 100 yardas)'
    secs=max(3.0, M.dur_lectura(' '.join(lines)+' '+sub,1.0))
    n=int(secs*FPS)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d)
        ccx,ccy,rr=W//2,1520,240
        pct=int(61*M.ease(min(t*1.4,1)))
        def ga(dd):
            dd.arc([ccx-rr,ccy-rr,ccx+rr,ccy+rr],-90,-90+360*0.61*M.ease(min(t*1.4,1)),fill=GREEN+(240,),width=26)
        glow(b,ga,14,1)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.arc([ccx-rr,ccy-rr,ccx+rr,ccy+rr],0,360,fill=(255,255,255,26),width=26)
        d2.text((ccx,ccy),f'{pct}%',font=BLACK(110),fill=INK,anchor='mm')
        ty=620-66
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,90,(t-0.06*i)*2.4,GREEN if i==1 else INK,font=BLACK,maxw=W-140)
            ty+=132
        if t>0.28: d.text((W//2,ty+40),sub,font=BOLD(44),fill=SUB,anchor='mm')
        M.progressbar(d,0.05+0.06*t,PAL); frames.append(V.fin(b))
    # fase 1: la dona parte tu ronda en dos
    ccx,ccy,rr=W//2,1080,330
    n1=int(5.0*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,390),'Una ronda de 90, partida en dos:',GEO(56),INK,t)
        gt=M.ease(min(t*1.5,1))
        def g1(dd): dd.arc([ccx-rr,ccy-rr,ccx+rr,ccy+rr],-90+360*0.61*gt,-90+360*0.61*gt+360*0.39*gt,fill=(150,160,155,220),width=64)
        def g2(dd): dd.arc([ccx-rr,ccy-rr,ccx+rr,ccy+rr],-90,-90+360*0.61*gt,fill=GREEN+(250,),width=64)
        glow(b,g1,10,1); glow(b,g2,14,1)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.text((ccx,ccy-40),f'{int(55*gt)}',font=BLACK(150),fill=GREEN,anchor='mm')
        d2.text((ccx,ccy+90),'golpes',font=BOLD(40),fill=SUB,anchor='mm')
        if t>0.5:
            a=min((t-0.5)*5,1.0) if t<0.86 else max(0.0,(1.0-t)/0.14)
            d2.text((W//2,1560),'55 de 90 son de 100 yardas o MENOS',font=BLACK(46),fill=GREEN+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.12+0.24*t,PAL); frames.append(V.fin(b))
    # fase 2: desglose secuencial
    partes=[('Wedges',19),('Chips y bunker',8),('Putts',28)]
    n2=int(4.6*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,390),'¿Y dónde exactamente?',GEO(58),GREEN,t)
        by=700
        for i,(lab,val) in enumerate(partes):
            ft=min(max(t*3.2-i*0.9,0),1)
            if ft<=0: continue
            d.text((170,by),lab,font=BOLD(46),fill=SUB,anchor='lm')
            x0,x1=170,W-170
            d.rounded_rectangle([x0,by+40,x1,by+66],13,fill=(255,255,255,22))
            wv=(x1-x0)*(val/33)*M.ease(ft)
            def g(dd,wv=wv,by=by): dd.rounded_rectangle([x0,by+40,x0+wv,by+66],13,fill=GREEN+(255,))
            glow(b,g,12,1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((x1,by),f'{int(val*M.ease(ft))}',font=BLACK(48),fill=GREEN,anchor='rm')
            by+=210
        d=ImageDraw.Draw(b,'RGBA')
        if t>0.72:
            a=min((t-0.72)*5,1.0)
            d.text((W//2,1560),'¿Y tú qué practicas? El driver.',font=BLACK(48),fill=RED+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.38+0.26*t,PAL); frames.append(V.fin(b))
    nin=int(M.dur_lectura('practica donde vive tu score no donde vive tu ego',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,800,'Practica donde vive tu SCORE,',74,t*1.8,INK)
        M.poptext(d,W//2,940,'no donde vive tu ego.',78,max(t*1.8-0.25,0),GREEN)
        M.progressbar(d,0.66+0.22*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT te dice dónde vive el tuyo')
    return M.render(frames,'theory-100y')

# ============================================================
# THEORY 4 · "El lado corto es la carcel del green"
# ============================================================
def teoria_ladocorto():
    frames=[]
    # gancho #5: split-wipe rojo/verde
    lines=['EL LADO CORTO ES','LA CÁRCEL DEL GREEN.']; sub='(deja de fallar hacia la bandera)'
    secs=max(3.0, M.dur_lectura(' '.join(lines)+' '+sub,1.0))
    n=int(secs*FPS)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d)
        sx=int(W*M.ease(min(t*1.6,1)))
        d.rectangle([0,1180,max(sx//2,1),1900],fill=(60,22,20,150))
        d.rectangle([W-max(sx//2,1),1180,W,1900],fill=(60,22,20,150))
        d.rectangle([W//2-max(sx//4,1),1180,W//2+max(sx//4,1),1900],fill=(18,52,34,170))
        def gl(dd):
            dd.line([(W//2-sx//4,1180),(W//2-sx//4,1900)],fill=RED+(200,),width=4)
            dd.line([(W//2+sx//4,1180),(W//2+sx//4,1900)],fill=GREEN+(220,),width=4)
        glow(b,gl,14,1)
        d2=ImageDraw.Draw(b,'RGBA')
        if t>0.5:
            a=int(255*min((t-0.5)*4,1))
            d2.text((W//2,1400),'ANCHO',font=BLACK(54),fill=GREEN+(a,),anchor='mm')
            d2.text((170,1400),'CORTO',font=BLACK(44),fill=RED+(a,),anchor='lm')
            d2.text((W-170,1400),'CORTO',font=BLACK(44),fill=RED+(a,),anchor='rm')
        ty=560-66
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,88,(t-0.06*i)*2.4,GREEN if i==1 else INK,font=BLACK,maxw=W-120)
            ty+=132
        if t>0.28: d.text((W//2,ty+40),sub,font=BOLD(42),fill=SUB,anchor='mm')
        M.progressbar(d,0.05+0.06*t,PAL); frames.append(V.fin(b))
    # geometria: green con bandera pegada a la derecha
    gcx,gcy=W//2,1120; flag=(gcx+270,gcy-40)
    def green_lados(b,d,zonas=1.0,pulso=0.0):
        gp=green_pts(gcx,gcy,430,300)
        d.polygon(gp,fill=GREENDIM+(255,))
        def gg(dd): dd.line(gp,fill=GREEN+(150,),width=4)
        glow(b,gg,16,1)
        d2=ImageDraw.Draw(b,'RGBA')
        if zonas>0:
            a=int((90+40*pulso)*zonas)
            d2.polygon([(flag[0]+40,gcy-300),(gcx+480,gcy-300),(gcx+500,gcy+300),(flag[0]+40,gcy+300)],fill=(200,60,50,a))
            d2.polygon([(gcx-500,gcy-300),(flag[0]-60,gcy-300),(flag[0]-60,gcy+300),(gcx-520,gcy+300)],fill=(60,180,110,int(a*0.55)))
        d2.line([(flag[0],flag[1]),(flag[0],flag[1]-110)],fill=INK,width=6)
        d2.polygon([(flag[0],flag[1]-110),(flag[0]+58,flag[1]-90),(flag[0],flag[1]-70)],fill=RED)
        d2.ellipse([flag[0]-12,flag[1]-5,flag[0]+12,flag[1]+7],fill=(10,20,14))
        return d2
    n1=int(3.6*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,390),'Bandera pegada a la derecha:',GEO(58),INK,t)
        d2=green_lados(b,d,zonas=M.ease(min(max(t*1.6-0.3,0),1)),pulso=math.sin(t*math.pi*4)*0.5+0.5)
        if t>0.55:
            a=min((t-0.55)*5,1.0) if t<0.88 else max(0.0,(1.0-t)/0.12)
            d2.text((W//2,1560),'De ese lado NO hay green para trabajar',font=BLACK(44),fill=RED+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.12+0.18*t,PAL); frames.append(V.fin(b))
    # fase 2: los dos misses
    n2=int(5.0*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,390),'Mismo error, dos destinos:',GEO(58),INK,t)
        d2=green_lados(b,d,zonas=1.0)
        if t>0.1:
            ft=min((t-0.1)*2.5,1)
            mx,my=flag[0]+150,gcy+40
            def gx(dd,a=int(255*ft)): 
                dd.line([(mx-26,my-26),(mx+26,my+26)],fill=RED+(a,),width=10)
                dd.line([(mx-26,my+26),(mx+26,my-26)],fill=RED+(a,),width=10)
            glow(b,gx,10,1)
            d3=ImageDraw.Draw(b,'RGBA')
            if ft>0.6:
                a=int(255*min((ft-0.6)*3,1))
                d3.text((W//2,1500),'Miss al lado corto: bogey casi seguro',font=BLACK(42),fill=RED+(a,),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,a))
        if t>0.55:
            ft=min((t-0.55)*2.5,1)
            mx2,my2=gcx-330,gcy+20
            def gc(dd,a=int(255*ft)): dd.ellipse([mx2-22,my2-22,mx2+22,my2+22],outline=GREEN+(a,),width=9)
            glow(b,gc,10,1)
            d3=ImageDraw.Draw(b,'RGBA')
            if ft>0.6:
                a=int(255*min((ft-0.6)*3,1))
                d3.text((W//2,1600),'Miss al lado ancho: up & down fácil',font=BLACK(42),fill=GREEN+(a,),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,a))
        M.progressbar(d,0.3+0.3*t,PAL); frames.append(V.fin(b))
    nin=int(M.dur_lectura('cuando vayas a fallar falla del lado ancho el miss inteligente vale medio golpe',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,800,'Cuando vayas a fallar...',76,t*1.8,INK)
        M.poptext(d,W//2,940,'falla del lado ANCHO.',82,max(t*1.8-0.25,0),GREEN)
        if t>0.4:
            ftxt(d,(W//2,1160),'El miss inteligente vale medio golpe.',BOLD(42),SUB,(t-0.4)/0.6,t_out=0.92)
        M.progressbar(d,0.64+0.24*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT mide tus up & down reales')
    return M.render(frames,'theory-ladocorto')

# ============================================================
# THEORY 26 · "El putt de 1 metro NO es automatico"
# ============================================================
def teoria_putt1m():
    frames=[]
    # gancho #6: pendulo de putter
    lines=['EL PUTT DE 1 METRO','NO ES AUTOMÁTICO.']; sub='(y te está costando el par)'
    secs=max(3.0, M.dur_lectura(' '.join(lines)+' '+sub,1.0))
    n=int(secs*FPS)
    pvx,pvy=W//2,1150; plen=430
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d)
        ang=math.sin(t*math.pi*3)*0.55
        hx,hy=pvx+math.sin(ang)*plen, pvy+math.cos(ang)*plen
        def arc(dd):
            pts=[(pvx+math.sin(a/40-0.55)*plen, pvy+math.cos(a/40-0.55)*plen) for a in range(0,45,3)]
            for p in pts: dd.ellipse([p[0]-4,p[1]-4,p[0]+4,p[1]+4],fill=GREEN+(90,))
        glow(b,arc,8,1)
        def pend(dd):
            dd.line([(pvx,pvy),(hx,hy)],fill=INK+(230,),width=8)
            dd.rounded_rectangle([hx-52,hy-14,hx+52,hy+22],10,fill=GREEN+(255,))
        glow(b,pend,10,1)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.ellipse([pvx-90-13,pvy+plen+30-13,pvx-90+13,pvy+plen+30+13],fill=(250,250,246))
        ty=560-66
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,86,(t-0.06*i)*2.4,GREEN if i==1 else INK,font=BLACK,maxw=W-120)
            ty+=130
        if t>0.28: d.text((W//2,ty+40),sub,font=BOLD(42),fill=SUB,anchor='mm')
        M.progressbar(d,0.05+0.06*t,PAL); frames.append(V.fin(b))
    # fase 1: gauges comparativos
    n1=int(4.6*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,390),'Desde 1 metro, ¿cuántos entran?',GEO(56),INK,t)
        for i,(lab,val,col,cy) in enumerate([('UN PRO',85,GREEN,830),('TÚ',60,RED,1330)]):
            ft=min(max(t*2.2-i*0.7,0),1)
            if ft<=0: continue
            rr=200
            def ga(dd,val=val,col=col,cy=cy,ft=ft):
                dd.arc([W//2-rr,cy-rr,W//2+rr,cy+rr],180,180+180*(val/100)*M.ease(ft),fill=col+(250,),width=30)
            glow(b,ga,12,1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.arc([W//2-rr,cy-rr,W//2+rr,cy+rr],180,360,fill=(255,255,255,26),width=30)
            d2.text((W//2,cy-40),f'{int(val*M.ease(ft))}%',font=BLACK(92),fill=col,anchor='mm')
            d2.text((W//2,cy+52),lab,font=BOLD(40),fill=SUB,anchor='mm')
        M.progressbar(d,0.12+0.22*t,PAL); frames.append(V.fin(b))
    # fase 2: 10 bolitas — 4 no entran
    n2=int(4.2*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,390),'De tus 10 putts de 1 metro:',GEO(58),INK,t)
        bx0=170; gap=(W-340)/9
        for i in range(10):
            ft=min(max(t*2.6-i*0.18,0),1)
            if ft<=0: continue
            entra=i<6
            col=GREEN if entra else RED
            px=bx0+i*gap; py=900
            def gb(dd,px=px,py=py,col=col,ft=ft):
                dd.ellipse([px-26,py-26,px+26,py+26],fill=col+(int(255*ft),) if col==GREEN else (0,0,0,0),outline=col+(int(255*ft),),width=6)
                if col==RED:
                    dd.line([(px-16,py-16),(px+16,py+16)],fill=col+(int(255*ft),),width=7)
                    dd.line([(px-16,py+16),(px+16,py-16)],fill=col+(int(255*ft),),width=7)
            glow(b,gb,8,1)
        d2=ImageDraw.Draw(b,'RGBA')
        if t>0.6:
            a=min((t-0.6)*4,1.0) if t<0.88 else max(0.0,(1.0-t)/0.12)
            d2.text((W//2,1240),'4 fallados = 4 pares regalados',font=BLACK(52),fill=RED+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
            d2.text((W//2,1360),'cada ronda',font=BOLD(40),fill=SUB+(int(255*a),),anchor='mm')
        M.progressbar(d,0.34+0.28*t,PAL); frames.append(V.fin(b))
    nin=int(M.dur_lectura('no es automatico es una habilidad practicala 10 minutos al dia',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,800,'No es automático.',80,t*1.8,INK)
        M.poptext(d,W//2,940,'Es una HABILIDAD.',84,max(t*1.8-0.25,0),GREEN)
        if t>0.4:
            ftxt(d,(W//2,1160),'10 minutos al día y se vuelve tuya.',BOLD(42),SUB,(t-0.4)/0.6,t_out=0.92)
        M.progressbar(d,0.62+0.26*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT cuenta tus putts de 1 metro')
    return M.render(frames,'theory-putt1m')

# ============================================================
# THEORY 19 · "El bogey es tu amigo"
# ============================================================
def teoria_bogey():
    frames=[]
    # gancho #7: tarjeta de score dibujandose
    lines=['EL BOGEY ES','TU AMIGO.']; sub='(y te va a bajar el score)'
    secs=max(3.2, M.dur_lectura(' '.join(lines)+' '+sub,1.0))
    n=int(secs*FPS)
    scores=[5,5,4,6,5,5,4,5,5]; cw=(W-240)/9
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d)
        for i in range(9):
            ft=min(max(t*3.2-i*0.22,0),1)
            if ft<=0: continue
            x0=120+i*cw; y0=1150
            def cell(dd,x0=x0,y0=y0,ft=ft):
                dd.rectangle([x0+6,y0,x0+cw-6,y0+150],outline=GREEN+(int(230*ft),),width=4)
            glow(b,cell,7,1)
            d2=ImageDraw.Draw(b,'RGBA')
            if ft>0.5:
                col=GREEN if scores[i]==5 else INK
                d2.text((x0+cw/2,y0+75),str(scores[i]),font=BLACK(60),fill=col+(int(255*min((ft-0.5)*2,1)),),anchor='mm')
        ty=520
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,92,(t-0.06*i)*2.4,GREEN if i==1 else INK,font=BLACK,maxw=W-120)
            ty+=145
        if t>0.3: d.text((W//2,ty+40),sub,font=BOLD(42),fill=SUB,anchor='mm')
        M.progressbar(d,0.05+0.06*t,PAL); frames.append(V.fin(b))
    # fase 1: tabla tu par real por handicap
    n1=int(5.4*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,360),'Tu "par" real depende de tu hándicap:',GEO(50),INK,t)
        for i,(hcp,par,es) in enumerate([('HCP 0','72','par golf'),('HCP 9','81','bogey en la mitad'),('HCP 18','90','PURO BOGEY'),('HCP 27','99','bogey y pico')]):
            ft=min(max(t*3.0-i*0.45,0),1)
            if ft<=0: continue
            y=620+i*230; hot=(i==2); col=GREEN if hot else INK
            def lnr(dd,y=y,ft=ft,hot=hot):
                dd.line([(140,y+86),(140+(W-280)*M.ease(ft),y+86)],fill=(GREEN if hot else GREENDIM)+(170,),width=4 if hot else 3)
            glow(b,lnr,6,1)
            d2=ImageDraw.Draw(b,'RGBA'); a=int(255*ft)
            d2.text((140,y-14),hcp,font=BOLD(46),fill=(GREEN if hot else SUB)+(a,),anchor='lm')
            d2.text((W-140,y-4),par,font=BLACK(88),fill=col+(a,),anchor='rm')
            if ft>0.6:
                d2.text((140,y+44),es,font=BOLD(34),fill=(GREEN if hot else SUB)+(int(255*min((ft-0.6)*2.5,1)),),anchor='lm')
        M.progressbar(d,0.12+0.22*t,PAL); frames.append(V.fin(b))
    # fase 2: 18 bogeys -> 90
    n2=int(4.8*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,360),'18 hoyos, puro bogey:',GEO(56),INK,t)
        cw2=(W-200)/9
        for i in range(18):
            ft=min(max(t*3.0-i*0.09,0),1)
            if ft<=0: continue
            x0=100+(i%9)*cw2; y0=560+(i//9)*170
            def cel(dd,x0=x0,y0=y0,ft=ft):
                dd.rectangle([x0+5,y0,x0+cw2-5,y0+140],outline=GREEN+(int(200*ft),),width=3)
            glow(b,cel,6,1)
            d2=ImageDraw.Draw(b,'RGBA')
            if ft>0.5:
                d2.text((x0+cw2/2,y0+70),'+1',font=BLACK(42),fill=GREEN+(int(255*min((ft-0.5)*2,1)),),anchor='mm')
        cnt=int(90*M.ease(min(max((t-0.2)/0.55,0),1)))
        if cnt>0:
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((W//2,1160),str(cnt),font=BLACK(170),fill=INK+(255,),anchor='mm')
            d2.text((W//2,1300),'golpes',font=BOLD(40),fill=SUB+(255,),anchor='mm')
        if t>0.72:
            a=min((t-0.72)*5,1.0) if t<0.9 else max(0.0,(1.0-t)/0.1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((W//2,1460),'Rompiste 100. Sin UN solo par.',font=BLACK(50),fill=GREEN+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.34+0.28*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('persigue pares y haras dobles acepta el bogey y romperas 90',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,760,'Persigue pares:',64,t*1.9,SUB)
        M.poptext(d,W//2,884,'harás DOBLES.',82,max(t*1.9-0.2,0),RED)
        M.poptext(d,W//2,1090,'Acepta el bogey:',64,max(t*1.9-0.55,0),SUB)
        M.poptext(d,W//2,1216,'romperás 90.',86,max(t*1.9-0.75,0),GREEN)
        M.progressbar(d,0.62+0.26*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT calcula TU par personal')
    return M.render(frames,'theory-bogey')

# ============================================================
# THEORY 33 · "Practicar sin objetivo es pasear con palos"
# ============================================================
def teoria_practica():
    import random
    frames=[]
    # gancho #8: trazo que deambula sin rumbo
    lines=['PRACTICAR SIN OBJETIVO','ES PASEAR CON PALOS.']; sub='(50 bolas, 0 datos)'
    secs=max(3.2,M.dur_lectura(' '.join(lines)+' '+sub,1.0))
    n=int(secs*FPS)
    rnd=random.Random(7); pts=[(W//2,1520)]
    for i in range(60):
        px,py=pts[-1]
        pts.append((min(max(px+rnd.uniform(-90,90),150),W-150),min(max(py+rnd.uniform(-70,42),1040),1580)))
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d)
        m=int(len(pts)*min(t*1.6,1))
        if m>1:
            def path(dd,m=m):
                dd.line(pts[:m],fill=GREEN+(200,),width=6)
                x,y=pts[m-1]; dd.ellipse([x-13,y-13,x+13,y+13],fill=(250,250,246,255))
            glow(b,path,9,1)
        ty=520
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,72,(t-0.06*i)*2.4,GREEN if i==1 else INK,font=BLACK,maxw=W-110)
            ty+=122
        if t>0.3: d.text((W//2,ty+36),sub,font=BOLD(42),fill=SUB,anchor='mm')
        M.progressbar(d,0.05+0.06*t,PAL); frames.append(V.fin(b))
    def range_base(b,d,title,t):
        ftxt(d,(W//2,360),title,GEO(50),INK,t)
        for yy,lab in [(1180,'50'),(950,'100'),(720,'150')]:
            def dl(dd,yy=yy):
                dd.line([(150,yy),(W-190,yy)],fill=GREENDIM+(210,),width=3)
            glow(b,dl,5,1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((W-170,yy),lab,font=BOLD(32),fill=SUB+(220,),anchor='lm')
        d2=ImageDraw.Draw(b,'RGBA')
        d2.ellipse([W//2-15,1405,W//2+15,1435],fill=(250,250,246,255))
    # fase 1: bolas por todos lados
    rnd2=random.Random(11)
    dots=[(rnd2.uniform(190,W-210),rnd2.uniform(640,1330)) for _ in range(26)]
    n1=int(4.8*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        range_base(b,d,'Tu cubeta de 50 bolas, sin objetivo:',t)
        for i,(px,py) in enumerate(dots):
            ft=min(max(t*3.0-i*0.09,0),1)
            if ft<=0: continue
            def dot(dd,px=px,py=py,ft=ft):
                dd.ellipse([px-11,py-11,px+11,py+11],fill=GREEN+(int(200*ft),))
            glow(b,dot,6,1)
        if t>0.62:
            a=min((t-0.62)*5,1.0) if t<0.88 else max(0.0,(1.0-t)/0.12)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((W//2,1560),'0 objetivos. 0 datos. 0 mejora.',font=BLACK(48),fill=RED+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.12+0.22*t,PAL); frames.append(V.fin(b))
    # fase 2: con objetivo
    rnd3=random.Random(23)
    cl=[(W//2+rnd3.gauss(0,58),950+rnd3.gauss(0,52)) for _ in range(12)]
    n2=int(4.8*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        range_base(b,d,'La misma cubeta, CON objetivo:',t)
        def tgt(dd,t=t):
            e=M.ease(min(t*2.2,1))
            for rr in (46,90,134):
                r=rr*e
                dd.ellipse([W//2-r,950-r,W//2+r,950+r],outline=GREEN+(235,),width=5)
        glow(b,tgt,8,1)
        for i,(px,py) in enumerate(cl):
            ft=min(max(t*2.6-0.5-i*0.12,0),1)
            if ft<=0: continue
            def dot(dd,px=px,py=py,ft=ft):
                dd.ellipse([px-11,py-11,px+11,py+11],fill=(250,250,246,int(255*ft)))
            glow(b,dot,5,1)
        if t>0.62:
            a=min((t-0.62)*5,1.0) if t<0.88 else max(0.0,(1.0-t)/0.12)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((W//2,1560),'Cada bola = un DATO.',font=BLACK(50),fill=GREEN+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.36+0.26*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('el range no es terapia es un laboratorio 10 bolas con objetivo ganan a 50 sin rumbo',1.2)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,790,'El range no es terapia.',64,t*1.9,INK)
        M.poptext(d,W//2,920,'Es un LABORATORIO.',78,max(t*1.9-0.25,0),GREEN)
        if t>0.45:
            ftxt(d,(W//2,1140),'10 bolas con objetivo > 50 sin rumbo.',BOLD(44),SUB,(t-0.45)/0.55,t_out=0.92)
        M.progressbar(d,0.64+0.24*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT convierte tu práctica en plan')
    return M.render(frames,'theory-practica')

# ============================================================
# THEORY 41 · "La tarjeta no miente; tu memoria sí"
# ============================================================
def teoria_tarjeta():
    frames=[]
    # gancho #9: el recuerdo (88) se desvanece, la tarjeta (94) lo corrige
    lines=['LA TARJETA NO MIENTE.','TU MEMORIA SÍ.']; sub='(y por eso no bajas)'
    secs=max(3.6,M.dur_lectura(' '.join(lines)+' '+sub,1.1))
    n=int(secs*FPS)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d)
        mem_a=1.0 if t<0.30 else max(0.22,1-(t-0.30)*2.2)
        def m88(dd,mem_a=mem_a,t=t):
            wob=math.sin(t*14)*3*(1 if t<0.5 else 0)
            dd.text((W//2+wob,1180),'88',font=BLACK(220),fill=GREEN+(int(200*mem_a),),anchor='mm')
        glow(b,m88,14,1)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.text((W//2,1020),'tu recuerdo',font=BOLD(36),fill=SUB+(int(220*mem_a),),anchor='mm')
        if t>0.42:
            st=min((t-0.42)*4,1)
            fs=int(150+70*(1-M.ease(st)))
            d2.text((W//2,1470),'94',font=BLACK(fs),fill=(250,250,246,int(255*st)),anchor='mm',stroke_width=8,stroke_fill=(8,14,11,int(255*st)))
            d2.text((W//2,1610),'tu tarjeta',font=BOLD(36),fill=INK+(int(230*st),),anchor='mm')
        ty=470
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,78,(t-0.07*i)*2.2,GREEN if i==1 else INK,font=BLACK,maxw=W-110)
            ty+=126
        if t>0.32: ftxt(d,(W//2,ty+30),sub,BOLD(42),SUB,(t-0.32)/0.68,t_out=0.95)
        M.progressbar(d,0.05+0.07*t,PAL); frames.append(V.fin(b))
    # fase 1: la memoria (frases que se apagan)
    frases=['"Pegué bien el drive"','"Fallé como dos putts"','"El 7 fue pura mala suerte"']
    n1=int(M.dur_lectura(' '.join(frases),1.7)*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,380),'Tu memoria después de la ronda:',GEO(52),INK,t)
        d2=ImageDraw.Draw(b,'RGBA')
        for i,fr in enumerate(frases):
            ap=min(max(t*3.4-i*0.55,0),1)
            if ap<=0: continue
            p=ap*ap*(3-2*ap)
            dim=1.0-0.62*min(max((t*3.4-i*0.55-1.25)/0.8,0),1)
            d2.text((W//2,760+i*150+18*(1-p)**2),fr,font=GEO(54),fill=SUB+(int(255*p*dim),),anchor='mm')
        if t>0.66:
            a=min((t-0.66)*5,1.0) if t<0.9 else max(0.0,(1.0-t)/0.1)
            d2.text((W//2,1360),'Recuerdos ≠ datos.',font=BLACK(56),fill=RED+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.14+0.2*t,PAL); frames.append(V.fin(b))
    # fase 2: la tarjeta del mismo dia
    datos=[('3','three-putts que "no pasaron"'),('41%','de fairways (no "buen drive")'),('+3','en el hoyo 7 (no fue suerte)')]
    n2=int(5.4*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d)
        ftxt(d,(W//2,380),'La tarjeta del MISMO día:',GEO(54),INK,t)
        for i,(num,lab) in enumerate(datos):
            ft=min(max(t*2.8-i*0.5,0),1)
            if ft<=0: continue
            y=680+i*260
            def lnr(dd,y=y,ft=ft):
                dd.line([(150,y+96),(150+(W-300)*M.ease(ft),y+96)],fill=GREENDIM+(190,),width=3)
            glow(b,lnr,5,1)
            d2=ImageDraw.Draw(b,'RGBA'); a=int(255*(ft*ft*(3-2*ft)))
            d2.text((150,y),num,font=BLACK(92),fill=GREEN+(a,),anchor='lm')
            d2.text((W-150,y+8),lab,font=BOLD(36),fill=INK+(a,),anchor='rm')
        M.progressbar(d,0.36+0.26*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('no puedes mejorar lo que recuerdas bonito solo lo que mides',1.3)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d)
        M.poptext(d,W//2,780,'No puedes mejorar',64,t*1.9,INK)
        M.poptext(d,W//2,905,'lo que recuerdas bonito.',64,max(t*1.9-0.2,0),SUB)
        M.poptext(d,W//2,1120,'Solo lo que MIDES.',82,max(t*1.9-0.55,0),GREEN)
        M.progressbar(d,0.64+0.24*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT recuerda tu ronda por ti')
    return M.render(frames,'theory-tarjeta')

# ============================================================
# THEORY 44 · "Tus expectativas estan 10 golpes arriba de tu HCP"
# ============================================================
def teoria_brecha():
    frames=[]
    # gancho #10: compuertas que se abren revelando la brecha
    lines=['TUS EXPECTATIVAS ESTÁN','10 GOLPES ARRIBA','DE TU REALIDAD.']
    secs=max(3.8,M.dur_lectura(' '.join(lines),1.1))
    n=int(secs*FPS); cy=1210
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=17)
        gap=M.ease(min(t*1.8,1))*330
        def doors(dd,gap=gap):
            dd.line([(120,cy-gap),(W-120,cy-gap)],fill=GREEN+(235,),width=6)
            dd.line([(120,cy+gap),(W-120,cy+gap)],fill=GREEN+(235,),width=6)
        glow(b,doors,10,1)
        d2=ImageDraw.Draw(b,'RGBA')
        if gap>60:
            a=int(255*min((gap-60)/160,1))
            num=int(10*min(max((t-0.25)/0.5,0),1))
            d2.text((W//2,cy),f'+{num}',font=BLACK(185),fill=RED+(a,),anchor='mm')
        ty=470
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,64,(t-0.07*i)*2.2,GREEN if i==1 else INK,font=BLACK,maxw=W-110)
            ty+=106
        M.progressbar(d,0.05+0.07*t,PAL); frames.append(V.fin(b))
    # fase 1: la regla — cabeza vs tarjeta
    x0=340
    def y_of(sc): return 620+(sc-80)*560/20.0
    n1=int(5.6*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d,ep=17)
        ftxt(d,(W//2,380),'Tu cabeza vs tu tarjeta:',GEO(54),INK,t)
        e=M.ease(min(t*2.0,1))
        def ruler(dd,e=e):
            dd.line([(x0,620),(x0,620+560*e)],fill=GREEN+(220,),width=5)
        glow(b,ruler,8,1)
        d2=ImageDraw.Draw(b,'RGBA')
        for sc in range(80,101,5):
            if (y_of(sc)-620)<=560*e+1:
                d2.line([(x0-16,y_of(sc)),(x0,y_of(sc))],fill=SUB+(200,),width=3)
                d2.text((x0-32,y_of(sc)),str(sc),font=BOLD(30),fill=SUB+(220,),anchor='rm')
        f1=min(max((t-0.28)*3,0),1)
        if f1>0:
            a=int(255*(f1*f1*(3-2*f1)))
            d2.line([(x0,y_of(84)),(x0+230,y_of(84))],fill=INK+(a,),width=4)
            d2.text((x0+254,y_of(84)-2),'"Hoy rompo 85"',font=GEO(42),fill=INK+(a,),anchor='lm')
        f2=min(max((t-0.5)*3,0),1)
        if f2>0:
            a=int(255*(f2*f2*(3-2*f2)))
            def mk(dd,a=a):
                dd.line([(x0,y_of(94)),(x0+230,y_of(94))],fill=GREEN+(a,),width=5)
            glow(b,mk,7,1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((x0+254,y_of(94)-2),'tu promedio real: 94',font=BOLD(38),fill=GREEN+(a,),anchor='lm')
        f3=min(max((t-0.66)*3.4,0),1)
        if f3>0:
            d2.rectangle([x0+8,y_of(84)+4,x0+560,y_of(94)-4],fill=RED+(int(80*f3),))
            d2.text((x0+284,(y_of(84)+y_of(94))/2),'LA BRECHA',font=BLACK(46),fill=RED+(int(255*f3),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*f3)))
        M.progressbar(d,0.14+0.2*t,PAL); frames.append(V.fin(b))
    # fase 2: como se cobra
    pasos=['Expectativa rota en el hoyo 3','Tiros de héroe para "recuperar"','Doble. Y otro. Y otro.']
    n2=int(M.dur_lectura(' '.join(pasos),1.5)*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d,ep=17)
        ftxt(d,(W//2,380),'Y la brecha se cobra así:',GEO(54),INK,t)
        for i,p in enumerate(pasos):
            ft=min(max(t*3.2-i*0.6,0),1)
            if ft<=0: continue
            a=int(255*(ft*ft*(3-2*ft)))
            y=660+i*250; col=RED if i==2 else INK
            def chip(dd,y=y,ft=ft,col=col):
                dd.rounded_rectangle([170,y-70,W-170,y+70],26,outline=(RED if col==RED else GREEN)+(int(200*ft),),width=4)
            glow(b,chip,7,1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((W//2,y),p,font=BOLD(40),fill=col+(a,),anchor='mm')
            if i<2 and ft>0.7:
                aa=int(255*min((ft-0.7)*3.3,1))
                d2.text((W//2,y+125),'↓',font=BLACK(52),fill=SUB+(aa,),anchor='mm')
        M.progressbar(d,0.36+0.26*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('juega tu handicap de hoy no el de tus sueños la brecha se cierra midiendo no deseando',1.3)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d,ep=17)
        M.poptext(d,W//2,790,'Juega tu hándicap de HOY.',64,t*1.9,INK)
        M.poptext(d,W//2,930,'No el de tus sueños.',64,max(t*1.9-0.25,0),SUB)
        if t>0.5:
            ftxt(d,(W//2,1150),'La brecha se cierra midiendo, no deseando.',BOLD(42),GREEN,(t-0.5)/0.5,t_out=0.92)
        M.progressbar(d,0.64+0.24*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT te dice tu número REAL')
    return M.render(frames,'theory-brecha')

# ============================================================
# THEORY 14 · "El 41% que salva tu ronda: up & down" (EP 18)
# ============================================================
def teoria_updown():
    frames=[]
    # gancho #11: rescate del bunker (arena de la landing)
    lines=['FALLASTE EL GREEN.','¿Y AHORA QUÉ?']; sub='(el 41% que salva tu ronda)'
    secs=max(3.8,M.dur_lectura(' '.join(lines)+' '+sub,1.1))
    n=int(secs*FPS); gy=1560
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=18)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.ellipse([180,gy-40,560,gy+70],fill=(243,231,189,255),outline=(199,173,116,255),width=4)
        d2.ellipse([700,gy-46,1010,gy+64],fill=(20,56,34,255),outline=GREEN+(230,),width=4)
        hx=905; d2.ellipse([hx-20,gy+2,hx+20,gy+22],fill=(6,12,8,255))
        d2.line([(hx,gy+12),(hx,gy-170)],fill=(250,250,246,255),width=7)
        d2.polygon([(hx,gy-170),(hx+70,gy-148),(hx,gy-122)],fill=LIME+(255,))
        if t<0.45:
            bt=M.ease(min(t/0.45,1)); bx=110+bt*260; by=gy-10-math.sin(bt*math.pi)*330
        elif t<0.5:
            bx,by=370,gy-10
        else:
            bt=M.ease(min((t-0.5)/0.42,1)); bx=370+bt*(hx-370); by=gy-10-math.sin(bt*math.pi)*260
        def trb(dd,bx=bx,by=by):
            dd.ellipse([bx-16,by-16,bx+16,by+16],fill=(250,250,246,255))
        glow(b,trb,10,1)
        if 0.42<t<0.64:
            sp=(t-0.42)/0.22
            for i in range(7):
                ang=math.pi*(0.22+0.09*i); rr=95*M.ease(sp)
                sx,sy=370+math.cos(ang)*rr,gy-24-math.sin(ang)*rr*1.35
                d2.ellipse([sx-7,sy-7,sx+7,sy+7],fill=(243,231,189,int(235*(1-sp))))
        ty=470
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,80,(t-0.07*i)*2.3,LIME if i==1 else INK,font=BLACK,maxw=W-110)
            ty+=132
        if t>0.32: ftxt(d,(W//2,ty+34),sub,BOLD(42),SUB,(t-0.32)/0.68,t_out=0.95)
        M.progressbar(d,0.05+0.07*t,PAL); frames.append(V.fin(b))
    # fase 1: donut 41%
    cx,cy,rr=W//2,1010,300
    n1=int(5.0*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d,ep=18)
        ftxt(d,(W//2,420),'Green fallado: ¿salvas el par?',GEO(54),INK,t)
        e=M.ease(min(t*1.6,1))
        d2=ImageDraw.Draw(b,'RGBA')
        d2.arc([cx-rr,cy-rr,cx+rr,cy+rr],0,360,fill=(255,255,255,66),width=46)
        def arc(dd,e=e):
            dd.arc([cx-rr,cy-rr,cx+rr,cy+rr],-90,-90+360*0.41*e,fill=GREEN+(245,),width=46)
        glow(b,arc,12,1)
        d2.text((cx,cy-26),f'{int(41*e)}%',font=BLACK(132),fill=(250,250,246,255),anchor='mm',stroke_width=6,stroke_fill=(10,30,16,255))
        d2.text((cx,cy+86),'up & down · HCP 15',font=BOLD(38),fill=SUB+(240,),anchor='mm')
        if t>0.62:
            a=min((t-0.62)*5,1.0) if t<0.9 else max(0.0,(1.0-t)/0.1)
            d2.text((W//2,1440),'(los pros: 58%. No estás tan lejos.)',font=BOLD(40),fill=LIME+(int(255*a),),anchor='mm',stroke_width=5,stroke_fill=(10,30,16,int(255*a)))
        M.progressbar(d,0.16+0.2*t,PAL); frames.append(V.fin(b))
    # fase 2: 10 greens fallados
    n2=int(4.8*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d,ep=18)
        ftxt(d,(W//2,420),'Fallas ~10 greens por ronda:',GEO(54),INK,t)
        bx0=170; gap=(W-340)/9
        for i in range(10):
            ft=min(max(t*2.6-i*0.18,0),1)
            if ft<=0: continue
            salva=i<4; px=bx0+i*gap; py=950
            def gb(dd,px=px,py=py,ft=ft,salva=salva):
                if salva: dd.ellipse([px-26,py-26,px+26,py+26],fill=GREEN+(int(255*ft),))
                else:
                    dd.ellipse([px-26,py-26,px+26,py+26],outline=(250,250,246,int(200*ft)),width=5)
                    dd.text((px,py),'+1',font=BOLD(28),fill=(250,250,246,int(230*ft)),anchor='mm')
            glow(b,gb,7,1)
        if t>0.6:
            a=min((t-0.6)*5,1.0) if t<0.88 else max(0.0,(1.0-t)/0.12)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((W//2,1250),'4 pares salvados = tu ronda entera',font=BLACK(52),fill=LIME+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(10,30,16,int(255*a)))
        M.progressbar(d,0.38+0.26*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('el score no se salva en el tee se salva a 30 metros del hoyo',1.3)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d,ep=18)
        M.poptext(d,W//2,800,'El score no se salva en el tee.',60,t*1.9,INK)
        M.poptext(d,W//2,950,'Se salva a 30 METROS del hoyo.',66,max(t*1.9-0.3,0),GREEN)
        if t>0.5:
            ftxt(d,(W//2,1170),'Chip + putt = tu mina de oro.',BOLD(44),SUB,(t-0.5)/0.5,t_out=0.92)
        M.progressbar(d,0.66+0.22*t,PAL); frames.append(V.fin(b))
    M.cta_outro(frames,PAL,line1='PARFECT mide tus up & down')
    return M.render(frames,'theory-updown')

if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'demo'
    if cmd=='bandera': teoria_bandera()
    elif cmd=='okay': teoria_okay()
    elif cmd=='velocidad': teoria_velocidad()
    elif cmd=='par5': teoria_par5()
    elif cmd=='putts30': teoria_putts30()
    elif cmd=='3putts': teoria_3putts()
    elif cmd=='wedges': teoria_wedges()
    elif cmd=='drive': teoria_drive()
    elif cmd=='100y': teoria_100y()
    elif cmd=='ladocorto': teoria_ladocorto()
    elif cmd=='putt1m': teoria_putt1m()
    elif cmd=='bogey': teoria_bogey()
    elif cmd=='practica': teoria_practica()
    elif cmd=='tarjeta': teoria_tarjeta()
    elif cmd=='brecha': teoria_brecha()
    elif cmd=='updown': teoria_updown()
    else:
        teoria_bandera(); teoria_okay()
