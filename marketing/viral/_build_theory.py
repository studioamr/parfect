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
PAL=dict(bg=BG, ink=(236,241,237), sub=(148,163,152))
INK=PAL['ink']; SUB=PAL['sub']
GREEN=(96,235,140)          # glow verde menta (diagramas)
GREENDIM=(24,62,42)         # superficie del green
LIME=(199,238,84)           # acento de marca (CTA)
RED=(239,96,84)
BOLD=M.BOLD; BLACK=M.BLACK; GEO=M.GEO

def _bg_img():
    g=Image.new('RGB',(64,114),BG); dg=ImageDraw.Draw(g)
    top=(11,19,15); mid=BG; bot=(5,9,7)
    for y in range(114):
        t=y/113
        c=(tuple(int(top[i]+(mid[i]-top[i])*(t/0.45)) for i in range(3)) if t<0.45
           else tuple(int(mid[i]+(bot[i]-mid[i])*((t-0.45)/0.55)) for i in range(3)))
        dg.line([(0,y),(64,y)],fill=c)
    img=g.resize((W,H),Image.BILINEAR).convert('RGBA')
    hal=Image.new('RGBA',(W,H),(0,0,0,0))
    ImageDraw.Draw(hal).ellipse([W//2-640,H//2-860,W//2+640,H//2+860],fill=(17,32,23,64))
    img.alpha_composite(hal.filter(ImageFilter.GaussianBlur(230)))
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

def chrome(d,alpha=255,ep=None,serie='THEORY'):
    M.wordmark(d,W//2,170,INK,52,alpha=alpha)
    if ep:
        d.text((W-84,172),f'{serie} · EP {ep:02d}',font=BOLD(27),fill=LIME+(min(alpha,215),),anchor='rm')
        d.text((84,172),'@parfectapp',font=BOLD(27),fill=SUB+(min(alpha,170),),anchor='lm')

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
    d.text((xy[0],y0),txt,font=font,fill=fill+(int(255*a*(1-fr)),),anchor=anchor)
    if fr>0.04: d.text((xy[0],y0+1),txt,font=font,fill=fill+(int(255*a*fr),),anchor=anchor)

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
        d2.text((cx,cy-26),f'{int(41*e)}%',font=BLACK(132),fill=(250,250,246,255),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,255))
        d2.text((cx,cy+86),'up & down · HCP 15',font=BOLD(38),fill=SUB+(240,),anchor='mm')
        if t>0.62:
            a=min((t-0.62)*5,1.0) if t<0.9 else max(0.0,(1.0-t)/0.1)
            d2.text((W//2,1440),'(los pros: 58%. No estás tan lejos.)',font=BOLD(40),fill=LIME+(int(255*a),),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,int(255*a)))
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
            d2.text((W//2,1250),'4 pares salvados = tu ronda entera',font=BLACK(52),fill=LIME+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
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
    app_outro(frames,shots=('03-diagnostico.png',),line1='PARFECT te lo mide así, en TU juego:',ep=18,focus=(0.5,0.42))
    return M.render(frames,'theory-updown')

# ============================================================
# APP OUTRO · la funcion REAL de la app que corresponde al tema,
# grabada de la app viva (marketing/shots) — cierre de CADA video
# ============================================================
SHOTSDIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','shots','shots')
def app_outro(frames, flow=None, shots=None, line1='Esto, en TU juego, se ve así:',
              cta='Descárgala GRATIS', ep=None, focus=(0.5,0.4), per=4.8, serie='THEORY', labels=None):
    """SIMULACION de uso real: en cada pantalla un dedo TOCA un control
    (ripple lima) y la pantalla cambia a la siguiente con crossfade suave."""
    if flow is None:
        flow=[(sh,None) for sh in (shots or ('03-diagnostico.png',))]
    sw=620; scrh=1150
    items=[]
    for sh,tap in flow:
        im=Image.open(os.path.join(SHOTSDIR,sh)).convert('RGB')
        items.append((im.resize((sw,int(im.height*sw/im.width)),Image.LANCZOS),tap))
    px,py=(W-sw)//2,470
    mask=Image.new('L',(sw,scrh),0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,sw,scrh],44,fill=255)
    prev_end=None
    for idx,(im,tap) in enumerate(items):
        imh=im.height; maxpan=max(0,imh-scrh)
        if tap: pan_t=min(maxpan,max(0,int(tap[1]*imh-scrh*0.45)))
        else:   pan_t=maxpan
        n=int(per*FPS)
        for k in range(n):
            t=k/max(n-1,1)
            b,d=canvas(); chrome(d,ep=ep,serie=serie)
            if labels:
                lt=min(t*2.6,1.0); la=int(255*(lt*lt*(3-2*lt)))
                d2l=ImageDraw.Draw(b,'RGBA')
                tw=d2l.textlength(labels[idx],font=BLACK(44))
                d2l.rounded_rectangle([W//2-tw/2-44,300,W//2+tw/2+44,420],32,outline=LIME+(min(la,210),),width=4)
                d2l.text((W//2,360),labels[idx],font=BLACK(44),fill=LIME+(la,),anchor='mm')
            else:
                ftxt(d,(W//2,360),line1,GEO(52),INK,min(t+idx,1.0)*1.4,t_out=2.0)
            oy=int((1-M.ease(min(t*2.0,1)))*900) if idx==0 else 0
            pan=int(pan_t*M.ease(min(max((t-0.15)/0.45,0),1)))
            scr=im.crop((0,pan,sw,pan+scrh))
            if idx>0 and t<0.24 and prev_end is not None:
                p=t/0.24; scr=Image.blend(prev_end,scr,p*p*(3-2*p))
            def marco(dd,oy=oy):
                dd.rounded_rectangle([px-14,py+oy-14,px+sw+14,py+oy+scrh+14],58,outline=GREEN+(200,),width=5)
            glow(b,marco,10,1)
            b.paste(scr,(px,py+oy),mask)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.rounded_rectangle([px-2,py+oy-2,px+sw+2,py+oy+scrh+2],46,outline=(236,241,237,255),width=4)
            if tap and 0.68<t<0.94:
                rp=(t-0.68)/0.26
                fx=px+int(tap[0]*sw); fy=py+oy+int(tap[1]*imh-pan)
                if 0<tap[1]*imh-pan<scrh:
                    rr=int(20+120*M.ease(min(rp*1.6,1)))
                    aa=int(235*(1-rp))
                    d2.ellipse([fx-rr,fy-rr,fx+rr,fy+rr],outline=LIME+(aa,),width=7)
                    d2.ellipse([fx-17,fy-17,fx+17,fy+17],fill=LIME+(min(aa+40,255),))
            if idx>0 or t>0.22:
                ba=1.0 if idx>0 else min((t-0.22)*4,1)
                pulse=1+0.03*math.sin((idx*per+t*per)*2.6)
                bw2,bh2=int(430*pulse),int(96*pulse)
                byc=1755
                d2.rounded_rectangle([W//2-bw2//2,byc-bh2//2,W//2+bw2//2,byc+bh2//2],bh2//2,fill=LIME+(int(255*ba),))
                d2.text((W//2,byc),cta,font=BLACK(int(36*pulse)),fill=(12,18,12,int(255*ba)),anchor='mm')
                d2.text((W//2,byc+86),'studioamr.github.io/parfect',font=BOLD(30),fill=SUB+(int(220*ba),),anchor='mm')
            M.progressbar(d,0.78+0.22*(idx+t)/len(items),PAL); frames.append(V.fin(b))
        prev_end=im.crop((0,pan_t,sw,pan_t+scrh))
    # ---- CONCLUSION: descarga + waitlist ----
    nf=int(4.2*FPS)
    for k in range(nf):
        t=k/(nf-1)
        b,d=canvas(); chrome(d,alpha=0,ep=None)
        M.poptext(d,W//2,560,'DESCARGA',96,t*2.0,INK,font=BLACK)
        M.wordmark(d,W//2,730,INK,104,alpha=int(255*min(t*2.4,1)))
        ftxt(d,(W//2,880),'Tu golf, medido.',GEO(52),SUB,min(t*1.6,1),t_out=2.0)
        d2=ImageDraw.Draw(b,'RGBA')
        if t>0.25:
            ba=min((t-0.25)*4,1)
            pulse=1+0.035*math.sin(t*8.2)
            bw2,bh2=int(560*pulse),int(112*pulse)
            d2.rounded_rectangle([W//2-bw2//2,1170-bh2//2,W//2+bw2//2,1170+bh2//2],bh2//2,fill=LIME+(int(255*ba),))
            d2.text((W//2,1170),'DESCÁRGALA GRATIS',font=BLACK(int(40*pulse)),fill=(12,18,12,int(255*ba)),anchor='mm')
        if t>0.4:
            ftxt(d,(W//2,1330),'juega GRATIS desde hoy →',BOLD(40),SUB,(t-0.4)/0.6,t_out=2.0)
            a2=int(255*min((t-0.4)*3,1))
            d2.text((W//2,1430),'studioamr.github.io/parfect',font=BOLD(42),fill=LIME+(a2,),anchor='mm')
        M.progressbar(d,0.995+0.005*t,PAL); frames.append(V.fin(b))
    return frames

# ============================================================
# THEORY 27 · "Deja la bola DEBAJO del hoyo" (EP 19)
# ============================================================
def teoria_debajo():
    frames=[]
    # gancho #12: perfil de pendiente — el putt de bajada se pasa, el de subida muere
    lines=['DEJA LA BOLA','DEBAJO DEL HOYO.']; sub='(el putt de subida es tu amigo)'
    secs=max(4.0,M.dur_lectura(' '.join(lines)+' '+sub,1.2))
    n=int(secs*FPS)
    x0,y0,x1,y1=150,1300,930,1580; hx=620
    def y_on(x): return y0+(y1-y0)*(x-x0)/(x1-x0)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=19)
        def slope(dd):
            dd.line([(x0,y0),(x1,y1)],fill=GREEN+(235,),width=6)
        glow(b,slope,9,1)
        d2=ImageDraw.Draw(b,'RGBA')
        hy=y_on(hx)
        d2.ellipse([hx-18,hy-8,hx+18,hy+10],fill=(5,9,7,255),outline=GREEN+(200,),width=3)
        # bola 1: de ARRIBA, pasa el hoyo y sigue (roja)
        if t<0.52:
            bt=M.ease(min(t/0.5,1)); bx=200+bt*660
            col=(250,250,246) if bx<hx else RED
            def b1(dd,bx=bx,col=col):
                dd.ellipse([bx-15,y_on(bx)-32,bx+15,y_on(bx)-2],fill=col+(255,))
            glow(b,b1,9,1)
            if bx>hx+90: d2.text((760,y_on(760)-120),'se pasó 2 m',font=BOLD(38),fill=RED+(255,),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,255))
        # bola 2: de ABAJO, sube y muere en el hoyo (verde)
        if t>0.56:
            bt=M.ease(min((t-0.56)/0.34,1)); bx=900-(900-hx)*bt
            def b2(dd,bx=bx):
                dd.ellipse([bx-15,y_on(bx)-32,bx+15,y_on(bx)-2],fill=GREEN+(255,))
            glow(b,b2,9,1)
            if bt>0.96: d2.text((hx,hy-120),'muere en el hoyo',font=BOLD(38),fill=GREEN+(255,),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,255))
        ty=470
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,84,(t-0.07*i)*2.3,GREEN if i==1 else INK,font=BLACK,maxw=W-110)
            ty+=136
        if t>0.3: ftxt(d,(W//2,ty+34),sub,BOLD(42),SUB,(t-0.3)/0.7,t_out=0.95)
        M.progressbar(d,0.04+0.06*t,PAL); frames.append(V.fin(b))
    # fase 1: el mismo putt, dos mundos
    filas=[('DE SUBIDA','frena sola · tap-in tranquilo',GREEN),('DE BAJADA','resbala: 2-3 m de pasada',RED)]
    n1=int(M.dur_lectura('de subida frena sola tap in tranquilo de bajada resbala 2 a 3 metros de pasada',1.5)*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d,ep=19)
        ftxt(d,(W//2,400),'El mismo putt, dos mundos:',GEO(56),INK,t)
        for i,(tit,txt,col) in enumerate(filas):
            ft=min(max(t*2.6-i*0.55,0),1)
            if ft<=0: continue
            y=760+i*330; a=int(255*(ft*ft*(3-2*ft)))
            def box(dd,y=y,ft=ft,col=col):
                dd.rounded_rectangle([150,y-110,W-150,y+110],28,outline=col+(int(220*ft),),width=5)
            glow(b,box,8,1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((W//2,y-44),tit,font=BLACK(56),fill=col+(a,),anchor='mm')
            d2.text((W//2,y+42),txt,font=BOLD(40),fill=INK+(a,),anchor='mm')
        M.progressbar(d,0.12+0.2*t,PAL); frames.append(V.fin(b))
    # fase 2: donde apuntar el approach
    n2=int(5.0*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d,ep=19)
        ftxt(d,(W//2,400),'Bandera en pendiente: apunta AQUÍ →',GEO(50),INK,t)
        cx,cy=W//2,1050
        e=M.ease(min(t*1.8,1))
        def gr(dd,e=e):
            dd.ellipse([cx-330*e,cy-250*e,cx+330*e,cy+250*e],fill=GREENDIM+(255,),outline=GREEN+(235,),width=5)
        glow(b,gr,10,1)
        d2=ImageDraw.Draw(b,'RGBA')
        if t>0.3:
            a=min((t-0.3)*3.5,1)
            d2.ellipse([cx-320,cy-240,cx+320,cy-20],fill=RED+(int(60*a),))
            d2.text((cx,cy-130),'ARRIBA = rezar',font=BLACK(40),fill=RED+(int(255*a),),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,int(255*a)))
        if t>0.45:
            a=min((t-0.45)*3.5,1)
            d2.ellipse([cx-320,cy+20,cx+320,cy+240],fill=GREEN+(int(55*a),))
            d2.text((cx,cy+130),'DEBAJO = atacar',font=BLACK(40),fill=GREEN+(int(255*a),),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,int(255*a)))
        d2.line([(cx,cy-8),(cx,cy-190)],fill=(250,250,246,255),width=6)
        d2.polygon([(cx,cy-190),(cx+62,cy-170),(cx,cy-148)],fill=LIME+(255,))
        d2.ellipse([cx-9,cy-14,cx+9,cy-2],fill=(5,9,7,255))
        M.progressbar(d,0.34+0.24*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('de subida agresivo de bajada rezando decide desde el approach',1.3)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d,ep=19)
        M.poptext(d,W//2,790,'De subida: AGRESIVO.',68,t*1.9,GREEN)
        M.poptext(d,W//2,930,'De bajada: rezando.',64,max(t*1.9-0.25,0),RED)
        if t>0.5:
            ftxt(d,(W//2,1150),'La decisión se toma DESDE el approach.',BOLD(42),SUB,(t-0.5)/0.5,t_out=0.92)
        M.progressbar(d,0.6+0.2*t,PAL); frames.append(V.fin(b))
    app_outro(frames,shots=('03-diagnostico.png','01-inicio.png'),line1='PARFECT te entrena esto así:',ep=19,focus=(0.5,0.42),per=5.4)
    return M.render(frames,'theory-debajo')

# ============================================================
# THEORY 34 · "20 minutos CON dato > 2 horas sin rumbo" (EP 20)
# ============================================================
def teoria_20min():
    frames=[]
    # gancho #13: dos cronometros
    lines=['20 MIN CON DATO','> 2 HORAS SIN RUMBO.']; sub='(así se entrena de verdad)'
    secs=max(4.0,M.dur_lectura(' '.join(lines)+' '+sub,1.2))
    n=int(secs*FPS)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=20)
        for (cx,rr,frac,col,lab,sub2,fast) in [(300,205,0.23,SUB,'2 H','sin rumbo',False),(780,205,1.0,GREEN,'20 MIN','con dato',True)]:
            e=M.ease(min(t*(2.4 if fast else 1.1),1.0))
            d2=ImageDraw.Draw(b,'RGBA')
            d2.arc([cx-rr,1050-rr,cx+rr,1050+rr],0,360,fill=(255,255,255,46),width=26)
            def arc(dd,cx=cx,rr=rr,e=e,frac=frac,col=col):
                dd.arc([cx-rr,1050-rr,cx+rr,1050+rr],-90,-90+360*frac*e,fill=col+(245,),width=26)
            glow(b,arc,10,1)
            d2.text((cx,1010),lab,font=BLACK(56),fill=(250,250,246,255),anchor='mm')
            d2.text((cx,1086),sub2,font=BOLD(34),fill=(col if col==GREEN else SUB)+(235,),anchor='mm')
            if fast and e>=0.999:
                d2.text((cx,1050+rr+70),'✓',font=BLACK(72),fill=LIME+(255,),anchor='mm')
        ty=480
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,74,(t-0.07*i)*2.3,GREEN if i==0 else INK,font=BLACK,maxw=W-110)
            ty+=124
        if t>0.3: ftxt(d,(W//2,ty+34),sub,BOLD(42),SUB,(t-0.3)/0.7,t_out=0.95)
        M.progressbar(d,0.04+0.05*t,PAL); frames.append(V.fin(b))
    # fase 1: golpes que bajas al mes
    filas=[('Range sin rumbo · 8 h/mes',0.16,RED,'≈ 0'),('Plan con dato · 80 min/mes',0.85,GREEN,'−3')]
    n1=int(M.dur_lectura('golpes que bajas en un mes range sin rumbo 8 horas casi cero plan con dato 80 minutos menos tres',1.4)*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d,ep=20)
        ftxt(d,(W//2,400),'Golpes que bajas en un mes:',GEO(56),INK,t)
        for i,(lab,fr,col,val) in enumerate(filas):
            ft=min(max(t*2.4-i*0.5,0),1)
            if ft<=0: continue
            y=760+i*300; a=int(255*(ft*ft*(3-2*ft)))
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((150,y-64),lab,font=BOLD(40),fill=INK+(a,),anchor='lm')
            d2.rounded_rectangle([150,y,W-150,y+64],18,fill=(255,255,255,26))
            def bar(dd,y=y,ft=ft,fr=fr,col=col):
                wbar=(W-300)*fr*M.ease(ft)
                if wbar>18: dd.rounded_rectangle([150,y,150+wbar,y+64],18,fill=col+(235,))
            glow(b,bar,9,1)
            d2.text((W-150,y-64),val,font=BLACK(56),fill=col+(a,),anchor='rm')
        M.progressbar(d,0.1+0.18*t,PAL); frames.append(V.fin(b))
    # fase 2: la sesion con dato (checklist)
    items=['Objetivo medible: 5/6 al círculo','El drill exacto para TU fuga','Resultado anotado en la app']
    n2=int(M.dur_lectura(' '.join(items),1.5)*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d,ep=20)
        ftxt(d,(W//2,400),'La sesión CON dato:',GEO(58),INK,t)
        for i,it in enumerate(items):
            ft=min(max(t*2.8-i*0.55,0),1)
            if ft<=0: continue
            y=720+i*260; a=int(255*(ft*ft*(3-2*ft)))
            def box(dd,y=y,ft=ft):
                dd.rounded_rectangle([150,y-86,W-150,y+86],24,outline=GREEN+(int(210*ft),),width=4)
            glow(b,box,7,1)
            d2=ImageDraw.Draw(b,'RGBA')
            if ft>0.55:
                aa=int(255*min((ft-0.55)*3,1))
                d2.text((215,y),'✓',font=BLACK(60),fill=LIME+(aa,),anchor='mm')
            d2.text((290,y),it,font=BOLD(38),fill=INK+(a,),anchor='lm')
        M.progressbar(d,0.28+0.2*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('la practica no cuenta por horas cuenta por datos y los datos toman 20 minutos',1.3)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d,ep=20)
        M.poptext(d,W//2,780,'La práctica no cuenta por horas.',58,t*1.9,INK)
        M.poptext(d,W//2,920,'Cuenta por DATOS.',80,max(t*1.9-0.3,0),GREEN)
        if t>0.5:
            ftxt(d,(W//2,1140),'Y los datos toman 20 minutos.',BOLD(44),SUB,(t-0.5)/0.5,t_out=0.92)
        M.progressbar(d,0.48+0.3*t,PAL); frames.append(V.fin(b))
    # SIMULACION: Analisis IA -> tap Entreno -> elegir 30 min -> AI Coach
    app_outro(frames,flow=[('09-analisis.png',(0.38,0.159)),('06-entrenamiento.png',(0.28,0.394)),('10-min30.png',(0.5,0.315))],
              line1='Así se arma tu sesión en PARFECT:',ep=20,per=4.8)
    return M.render(frames,'theory-20min')

# ============================================================
# THEORY 22 · "Fairway > distancia: los numeros" (EP 21)
# ============================================================
def teoria_fairway():
    frames=[]
    # gancho #14: dos drives cenital — largo al rough (X) vs corto al fairway (✓)
    lines=['FAIRWAY','> DISTANCIA.']; sub='(los números del drive)'
    secs=max(3.8,M.dur_lectura(' '.join(lines)+' '+sub,1.2))
    n=int(secs*FPS)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=21)
        d2=ImageDraw.Draw(b,'RGBA')
        # hoyo cenital: fairway franja, rough a los lados
        d2.rounded_rectangle([340,940,740,1760],90,fill=GREENDIM+(255,))
        def fwl(dd):
            dd.rounded_rectangle([340,940,740,1760],90,outline=GREEN+(200,),width=4)
        glow(b,fwl,8,1)
        tee=(540,1740)
        d2.ellipse([tee[0]-12,tee[1]-12,tee[0]+12,tee[1]+12],fill=(250,250,246,255))
        # drive A: LARGO al rough (curva a la derecha, roja)
        e1=M.ease(min(t/0.4,1))
        if e1>0.02:
            pts=[]
            for i in range(int(30*e1)+1):
                q=i/30
                pts.append((tee[0]+q*q*330, tee[1]-q*640))
            if len(pts)>1:
                col=RED if pts[-1][0]>740 else (250,250,246)
                def tr1(dd,pts=pts,col=col):
                    dd.line(pts,fill=col+(230,),width=7)
                glow(b,tr1,8,1)
                if e1>=0.99:
                    d2.text((905,1075),'ROUGH · 285 y',font=BLACK(38),fill=RED+(255,),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,255))
        # drive B: al centro del fairway (verde)
        if t>0.45:
            e2=M.ease(min((t-0.45)/0.35,1))
            pts=[(tee[0],tee[1]-q/28*560) for q in range(int(28*e2)+1)]
            if len(pts)>1:
                def tr2(dd,pts=pts):
                    dd.line(pts,fill=GREEN+(240,),width=7)
                glow(b,tr2,9,1)
                if e2>=0.99:
                    d2.text((540,1105),'FAIRWAY · 235 y',font=BLACK(38),fill=GREEN+(255,),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,255))
        ty=470
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,96,(t-0.07*i)*2.3,GREEN if i==0 else INK,font=BLACK,maxw=W-110)
            ty+=150
        if t>0.3: ftxt(d,(W//2,ty+30),sub,BOLD(42),SUB,(t-0.3)/0.7,t_out=0.95)
        M.progressbar(d,0.04+0.05*t,PAL); frames.append(V.fin(b))
    # fase 1: promedio del hoyo segun de donde juegas el 2do
    filas=[('Segundo tiro desde FAIRWAY','4.6',GREEN),('Segundo tiro desde ROUGH','5.4',RED)]
    n1=int(M.dur_lectura('promedio del hoyo segundo tiro desde fairway 4.6 desde rough 5.4',1.5)*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d,ep=21)
        ftxt(d,(W//2,400),'Promedio del hoyo (par 4):',GEO(56),INK,t)
        for i,(lab,val,col) in enumerate(filas):
            ft=min(max(t*2.4-i*0.5,0),1)
            if ft<=0: continue
            y=780+i*320; a=int(255*(ft*ft*(3-2*ft)))
            def box(dd,y=y,ft=ft,col=col):
                dd.rounded_rectangle([150,y-110,W-150,y+110],28,outline=col+(int(215*ft),),width=5)
            glow(b,box,8,1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((190,y),lab,font=BOLD(38),fill=INK+(a,),anchor='lm')
            cnt=4.0+ (float(val)-4.0)*M.ease(ft)
            d2.text((W-190,y),f'{cnt:.1f}',font=BLACK(84),fill=col+(a,),anchor='rm')
        if t>0.62:
            aa=min((t-0.62)*5,1.0) if t<0.9 else max(0.0,(1.0-t)/0.1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((W//2,1500),'0.8 golpes de castigo. POR HOYO.',font=BLACK(50),fill=LIME+(int(255*aa),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*aa)))
        M.progressbar(d,0.1+0.18*t,PAL); frames.append(V.fin(b))
    # fase 2: la cuenta de la ronda
    n2=int(M.dur_lectura('14 drives por ronda 6 al rough son 5 golpes regalados el fairway te los devuelve',1.4)*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d,ep=21)
        ftxt(d,(W//2,400),'Tu ronda, en corto:',GEO(58),INK,t)
        d2=ImageDraw.Draw(b,'RGBA')
        cnt=int(5*M.ease(min(max((t-0.25)/0.5,0),1)))
        M.poptext(d,W//2,760,'14 drives · 6 al rough',60,t*2.0,INK)
        if t>0.25:
            d2.text((W//2,1050),f'−{cnt}',font=BLACK(210),fill=RED+(255,),anchor='mm')
            d2.text((W//2,1220),'golpes regalados por ronda',font=BOLD(40),fill=SUB+(240,),anchor='mm')
        M.progressbar(d,0.28+0.18*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('el fairway no es aburrido es la jugada agresiva disfrazada',1.3)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d,ep=21)
        M.poptext(d,W//2,800,'El fairway no es aburrido.',62,t*1.9,INK)
        M.poptext(d,W//2,950,'Es la jugada AGRESIVA disfrazada.',62,max(t*1.9-0.3,0),GREEN)
        M.progressbar(d,0.46+0.3*t,PAL); frames.append(V.fin(b))
    # demo + conclusion
    app_outro(frames,flow=[('01-inicio.png',None)],line1='PARFECT te dice TU % de fairways:',ep=21,per=5.4)
    return M.render(frames,'theory-fairway')

# ============================================================
# SERIE "ASI SE USA PARFECT" · EP 01 — Anota tu ronda en 3 taps
# ============================================================
def uso01():
    frames=[]
    # portada de serie
    n=int(3.4*FPS)
    im0=Image.open(os.path.join(SHOTSDIR,'12-nueva.png')).convert('RGB')
    sw=620; im0=im0.resize((sw,int(im0.height*sw/im0.width)),Image.LANCZOS)
    mask=Image.new('L',(sw,700),0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,sw,700],44,fill=255)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=1,serie='ASÍ SE USA')
        M.poptext(d,W//2,520,'ASÍ SE USA',104,t*2.2,INK,font=BLACK)
        M.wordmark(d,W//2,690,INK,96,alpha=int(255*min(t*2.6,1)))
        if t>0.25:
            ftxt(d,(W//2,850),'EP 01 · Anota tu ronda en 3 taps',BOLD(46),LIME,(t-0.25)/0.75,t_out=2.0)
        oy=int((1-M.ease(min(max(t-0.15,0)*1.6,1)))*760)
        def marco(dd,oy=oy):
            dd.rounded_rectangle([(W-sw)//2-14,1046+oy,(W+sw)//2+14,1046+oy+728],58,outline=GREEN+(200,),width=5)
        glow(b,marco,10,1)
        b.paste(im0.crop((0,0,sw,700)),((W-sw)//2,1060+oy),mask)
        M.progressbar(d,0.02+0.08*t,PAL); frames.append(V.fin(b))
    # pasos con taps reales
    app_outro(frames,
        flow=[('12-nueva.png',(0.5,0.447)),
              ('13-campo.png',(0.5,0.564)),
              ('14-scorecard.png',(0.72,0.503)),
              ('11-ronda.png',None)],
        labels=['PASO 1 · Elige tu campo','PASO 2 · Comenzar ronda','PASO 3 · Hoyos y salida','Tu tarjeta se analiza SOLA'],
        ep=1,serie='ASÍ SE USA',per=4.9)
    return M.render(frames,'uso01-anota')

# ============================================================
# SERIE "ASI SE USA PARFECT" · EP 02 — Tu coach IA en 1 tap
# ============================================================
def uso02():
    frames=[]
    n=int(3.4*FPS)
    im0=Image.open(os.path.join(SHOTSDIR,'09-analisis.png')).convert('RGB')
    sw=620; im0=im0.resize((sw,int(im0.height*sw/im0.width)),Image.LANCZOS)
    mask=Image.new('L',(sw,700),0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,sw,700],44,fill=255)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=2,serie='ASÍ SE USA')
        M.poptext(d,W//2,520,'ASÍ SE USA',104,t*2.2,INK,font=BLACK)
        M.wordmark(d,W//2,690,INK,96,alpha=int(255*min(t*2.6,1)))
        if t>0.25:
            ftxt(d,(W//2,850),'EP 02 · Tu coach IA en 1 tap',BOLD(46),LIME,(t-0.25)/0.75,t_out=2.0)
        oy=int((1-M.ease(min(max(t-0.15,0)*1.6,1)))*760)
        def marco(dd,oy=oy):
            dd.rounded_rectangle([(W-sw)//2-14,1046+oy,(W+sw)//2+14,1046+oy+728],58,outline=GREEN+(200,),width=5)
        glow(b,marco,10,1)
        b.paste(im0.crop((0,0,sw,700)),((W-sw)//2,1060+oy),mask)
        M.progressbar(d,0.02+0.08*t,PAL); frames.append(V.fin(b))
    app_outro(frames,
        flow=[('09-analisis.png',(0.5,0.4875)),
              ('15-diagnostico.png',None)],
        labels=['PASO 1 · Un tap: Generar análisis','La IA encuentra TU fuga y te da el plan'],
        ep=2,serie='ASÍ SE USA',per=6.2)
    return M.render(frames,'uso02-coach')

# ============================================================
# TEORIA AUTO · motor generico por especificacion (_banco30.py)
# ============================================================
def _fase_vs(frames,titulo,rows,ep,p0,p1):
    n=int(M.dur_lectura(titulo+' '+' '.join(r[0]+' '+r[1] for r in rows),1.4)*FPS)
    for k in range(n):
        t=k/(n-1)
        b,d=canvas(); chrome(d,ep=ep)
        ftxt(d,(W//2,400),titulo,GEO(52),INK,t)
        for i,(lab,val,coln) in enumerate(rows):
            col=GREEN if coln=='GREEN' else RED
            ft=min(max(t*2.4-i*0.5,0),1)
            if ft<=0: continue
            y=780+i*320; a=int(255*(ft*ft*(3-2*ft)))
            def box(dd,y=y,ft=ft,col=col):
                dd.rounded_rectangle([150,y-110,W-150,y+110],28,outline=col+(int(215*ft),),width=5)
            glow(b,box,8,1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((190,y),lab,font=BOLD(38),fill=INK+(a,),anchor='lm')
            d2.text((W-190,y),val,font=BLACK(66),fill=col+(a,),anchor='rm')
        M.progressbar(d,p0+(p1-p0)*t,PAL); frames.append(V.fin(b))

def _fase_donut(frames,spec,ep,p0,p1):
    pct,label,sub2=spec
    val=float(pct.replace('%',''))
    cx,cy,rr=W//2,1000,300
    n=int(M.dur_lectura(label+' '+sub2,1.6)*FPS)
    for k in range(n):
        t=k/(n-1)
        b,d=canvas(); chrome(d,ep=ep)
        e=M.ease(min(t*1.6,1))
        d2=ImageDraw.Draw(b,'RGBA')
        d2.arc([cx-rr,cy-rr,cx+rr,cy+rr],0,360,fill=(255,255,255,60),width=44)
        def arc(dd,e=e):
            dd.arc([cx-rr,cy-rr,cx+rr,cy+rr],-90,-90+360*(val/100)*e,fill=GREEN+(245,),width=44)
        glow(b,arc,12,1)
        d2.text((cx,cy-26),f'{int(round(val*e))}%',font=BLACK(120),fill=(250,250,246,255),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,255))
        d2.text((cx,cy+80),label,font=BOLD(38),fill=SUB+(240,),anchor='mm')
        if t>0.55:
            a=min((t-0.55)*4,1.0) if t<0.9 else max(0.0,(1.0-t)/0.1)
            d2.text((W//2,1430),sub2,font=BOLD(40),fill=LIME+(int(255*a),),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,p0+(p1-p0)*t,PAL); frames.append(V.fin(b))

def _fase_bolitas(frames,spec,ep,p0,p1,titulo=''):
    total,malas,label=spec
    n=int(M.dur_lectura(titulo+' '+label,1.8)*FPS)
    bx0=170; gap=(W-340)/(total-1)
    for k in range(n):
        t=k/(n-1)
        b,d=canvas(); chrome(d,ep=ep)
        ftxt(d,(W//2,430),titulo or label,GEO(50),INK,t)
        for i in range(total):
            ft=min(max(t*2.6-i*0.16,0),1)
            if ft<=0: continue
            mala=i<malas; px=bx0+i*gap; py=980
            def gb(dd,px=px,py=py,ft=ft,mala=mala):
                if mala:
                    dd.ellipse([px-26,py-26,px+26,py+26],outline=RED+(int(230*ft),),width=6)
                    dd.line([(px-15,py-15),(px+15,py+15)],fill=RED+(int(230*ft),),width=6)
                else:
                    dd.ellipse([px-26,py-26,px+26,py+26],fill=GREEN+(int(255*ft),))
            glow(b,gb,7,1)
        if titulo and t>0.55:
            a=min((t-0.55)*4,1.0) if t<0.9 else max(0.0,(1.0-t)/0.1)
            d2=ImageDraw.Draw(b,'RGBA')
            d2.text((W//2,1300),label,font=BOLD(42),fill=LIME+(int(255*a),),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,p0+(p1-p0)*t,PAL); frames.append(V.fin(b))

def _fase_contador(frames,spec,ep,p0,p1,titulo=''):
    big,label=spec
    n=int(M.dur_lectura(titulo+' '+big+' '+label,1.5)*FPS)
    for k in range(n):
        t=k/(n-1)
        b,d=canvas(); chrome(d,ep=ep)
        if titulo: ftxt(d,(W//2,430),titulo,GEO(52),INK,t)
        M.poptext(d,W//2,980,big,200,t*1.8,GREEN,font=BLACK)
        if t>0.35:
            ftxt(d,(W//2,1220),label,BOLD(44),INK,(t-0.35)/0.65,t_out=0.94)
        M.progressbar(d,p0+(p1-p0)*t,PAL); frames.append(V.fin(b))

def teoria_auto(spec,ep):
    frames=[]
    ganchos=[titlecard,titlecard_rain,titlecard_cone]
    ganchos[ep%3](frames,spec['lines'],spec['sub'],3.6,accent_idx=1)
    for key,(p0,p1) in (('f1',(0.12,0.36)),('f2',(0.38,0.6))):
        tipo=spec[key][0]
        if tipo=='vs': _fase_vs(frames,spec[key][1],spec[key][2],ep,p0,p1)
        elif tipo=='donut': _fase_donut(frames,spec[key][1],ep,p0,p1)
        elif tipo=='bolitas':
            it=spec[key]
            if len(it)==3: _fase_bolitas(frames,it[2],ep,p0,p1,titulo=it[1])
            else: _fase_bolitas(frames,it[1],ep,p0,p1)
        elif tipo=='contador': _fase_contador(frames,spec[key][2],ep,p0,p1,titulo=spec[key][1])
    ins=spec['ins']
    nin=int(M.dur_lectura(' '.join(ins),1.4)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d,ep=ep)
        M.poptext(d,W//2,790,ins[0],62,t*1.9,INK)
        M.poptext(d,W//2,930,ins[1],70,max(t*1.9-0.25,0),GREEN)
        if len(ins)>2 and t>0.5:
            ftxt(d,(W//2,1150),ins[2],BOLD(40),SUB,(t-0.5)/0.5,t_out=0.92)
        M.progressbar(d,0.62+0.22*t,PAL); frames.append(V.fin(b))
    app_outro(frames,flow=[(spec['shot'],None)],line1=spec['cta'],ep=ep,per=4.6)
    return M.render(frames,'theory-'+spec['slug'])

# ============================================================
# SERIE "ASI SE USA PARFECT" · EP 03 — Tu sesion de entrenamiento
# ============================================================
def uso03():
    frames=[]
    n=int(3.4*FPS)
    im0=Image.open(os.path.join(SHOTSDIR,'06-entrenamiento.png')).convert('RGB')
    sw=620; im0=im0.resize((sw,int(im0.height*sw/im0.width)),Image.LANCZOS)
    mask=Image.new('L',(sw,700),0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,sw,700],44,fill=255)
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=3,serie='ASÍ SE USA')
        M.poptext(d,W//2,520,'ASÍ SE USA',104,t*2.2,INK,font=BLACK)
        M.wordmark(d,W//2,690,INK,96,alpha=int(255*min(t*2.6,1)))
        if t>0.25:
            ftxt(d,(W//2,850),'EP 03 · Tu sesión de entrenamiento en 2 taps',BOLD(42),LIME,(t-0.25)/0.75,t_out=2.0)
        oy=int((1-M.ease(min(max(t-0.15,0)*1.6,1)))*760)
        def marco(dd,oy=oy):
            dd.rounded_rectangle([(W-sw)//2-14,1046+oy,(W+sw)//2+14,1046+oy+728],58,outline=GREEN+(200,),width=5)
        glow(b,marco,10,1)
        b.paste(im0.crop((0,0,sw,700)),((W-sw)//2,1060+oy),mask)
        M.progressbar(d,0.02+0.08*t,PAL); frames.append(V.fin(b))
    app_outro(frames,
        flow=[('09-analisis.png',(0.38,0.159)),
              ('06-entrenamiento.png',(0.28,0.394)),
              ('10-min30.png',(0.5,0.315))],
        labels=['PASO 1 · Entra a Entreno','PASO 2 · ¿Cuánto tiempo tienes?','PASO 3 · AI Coach arma tu sesión'],
        ep=3,serie='ASÍ SE USA',per=5.2)
    return M.render(frames,'uso03-entreno')

# ============================================================
# THEORY 30 · "El lag putt: tirale al circulo de 1 m" (EP 24, artesanal)
# ============================================================
def teoria_lag():
    frames=[]
    # gancho #15: putt largo serpenteante que muere en el circulo
    lines=['DESDE LEJOS NO LE','TIRES AL HOYO.']; sub='(tírale al círculo de 1 metro)'
    secs=max(4.2,M.dur_lectura(' '.join(lines)+' '+sub,1.2))
    n=int(secs*FPS)
    hx,hy=W//2,920
    import math as mt
    path=[]
    for i in range(81):
        q=i/80
        px=W//2+mt.sin(q*mt.pi*1.6+0.4)*230*(1-q*0.55)
        py=1760-q*820
        path.append((px,py))
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=24)
        d2=ImageDraw.Draw(b,'RGBA')
        # circulo de 1 m pulsando alrededor del hoyo (abajo del titulo)
        pul=1+0.05*mt.sin(t*mt.pi*4)
        def circ(dd,pul=pul):
            r=95*pul
            for a in range(0,360,14):
                x1=hx+r*mt.cos(mt.radians(a)); y1=hy+r*mt.sin(mt.radians(a))
                dd.ellipse([x1-5,y1-5,x1+5,y1+5],fill=GREEN+(200,))
        glow(b,circ,8,1)
        d2.ellipse([hx-16,hy-8,hx+16,hy+10],fill=(5,9,7,255),outline=GREEN+(220,),width=3)
        # putt avanzando con estela
        e=M.ease(min(t/0.62,1)); m=max(2,int(len(path)*e))
        def tr(dd,m=m):
            dd.line(path[:m],fill=GREEN+(210,),width=7)
        glow(b,tr,10,1)
        bx,by=path[m-1]
        d2.ellipse([bx-16,by-16,bx+16,by+16],fill=(250,250,246,255))
        if e>=1 and t>0.7:
            a=int(255*min((t-0.7)*4,1))
            d2.text((hx+270,hy-40),'muerto\na 60 cm',font=BOLD(36),fill=GREEN+(a,),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,a))
        ty=400
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,84,(t-0.07*i)*2.3,GREEN if i==1 else INK,font=BLACK,maxw=W-110)
            ty+=134
        if t>0.3: ftxt(d,(W//2,ty+26),sub,BOLD(42),SUB,(t-0.3)/0.7,t_out=0.95)
        M.progressbar(d,0.04+0.06*t,PAL); frames.append(V.fin(b))
    # fase 1: ni los pros
    n1=int(M.dur_lectura('putts de 10 metros embocados pros 9 por ciento tu 3 nadie los mete',1.5)*FPS)
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d,ep=24)
        ftxt(d,(W//2,420),'Putts de 10 metros embocados:',GEO(54),INK,t)
        d2=ImageDraw.Draw(b,'RGBA')
        for i,(lab,val,col) in enumerate([('LOS PROS','9%',GREEN),('TÚ','3%',RED)]):
            ft=min(max(t*2.4-i*0.5,0),1)
            if ft<=0: continue
            a=int(255*(ft*ft*(3-2*ft))); y=800+i*330
            d2.text((W//2,y-90),lab,font=BOLD(40),fill=SUB+(a,),anchor='mm')
            d2.text((W//2,y+40),val,font=BLACK(150),fill=col+(a,),anchor='mm')
        if t>0.62:
            aa=min((t-0.62)*5,1.0) if t<0.9 else max(0.0,(1.0-t)/0.1)
            d2.text((W//2,1500),'Nadie la mete. Deja de intentarlo.',font=BLACK(48),fill=LIME+(int(255*aa),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*aa)))
        M.progressbar(d,0.14+0.18*t,PAL); frames.append(V.fin(b))
    # fase 2: LA DIANA — al hoyo vs al circulo
    import random as rd
    r1=rd.Random(5); r2=rd.Random(9)
    cx,cy=W//2,1030
    rojos=[(cx+r1.uniform(-1,1)*250,cy+r1.uniform(-0.9,1)*240) for _ in range(6)]
    verdes=[(cx+r2.gauss(0,42),cy+r2.gauss(0,40)) for _ in range(6)]
    n2=int(6.2*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d,ep=24)
        ftxt(d,(W//2,400),'12 lag putts desde 10 metros:',GEO(54),INK,t)
        # green blob
        e=M.ease(min(t*1.8,1))
        pts=green_pts(cx,cy,380*e,300*e)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.polygon(pts,fill=GREENDIM+(255,))
        def edge(dd,pts=pts):
            dd.line(pts+[pts[0]],fill=GREEN+(220,),width=5)
        glow(b,edge,9,1)
        d2.ellipse([cx-13,cy-7,cx+13,cy+9],fill=(5,9,7,255))
        # tanda 1: al hoyo (dispersos)
        for i,(px,py) in enumerate(rojos):
            ft=min(max(t*3.2-0.5-i*0.14,0),1)
            if ft<=0: continue
            lejos=((px-cx)**2+(py-cy)**2)**0.5>150
            def dot(dd,px=px,py=py,ft=ft,lejos=lejos):
                dd.ellipse([px-13,py-13,px+13,py+13],fill=(250,250,246,int(235*ft)))
                if lejos: dd.ellipse([px-24,py-24,px+24,py+24],outline=RED+(int(220*ft),),width=4)
            glow(b,dot,6,1)
        if 0.3<t<0.55:
            a=int(255*min((t-0.3)*5,1))
            d2.text((W//2,1440),'AL HOYO: quedan a 2.1 m en promedio',font=BOLD(40),fill=RED+(a,),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,a))
        # diana + tanda 2
        if t>0.52:
            de=M.ease(min((t-0.52)*3,1))
            def diana(dd,de=de):
                for rr in (60,110):
                    r=rr*de
                    dd.ellipse([cx-r,cy-r,cx+r,cy+r],outline=LIME+(230,),width=5)
            glow(b,diana,8,1)
        if t>0.6:
            for i,(px,py) in enumerate(verdes):
                ft=min(max((t-0.6)*3.4-i*0.12,0),1)
                if ft<=0: continue
                def dg(dd,px=px,py=py,ft=ft):
                    dd.ellipse([px-13,py-13,px+13,py+13],fill=GREEN+(int(255*ft),))
                glow(b,dg,7,1)
        if t>0.78:
            a=min((t-0.78)*5,1.0) if t<0.93 else max(0.0,(1.0-t)/0.07)
            d2.text((W//2,1440),'AL CÍRCULO: 0.7 m — puro tap-in',font=BLACK(44),fill=GREEN+(int(255*a),),anchor='mm',stroke_width=6,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.34+0.28*t,PAL); frames.append(V.fin(b))
    # fase 3: el 3-putt muere aqui
    n3=int(M.dur_lectura('el 3 putt muere aqui de 36 putts a 31 por ronda',1.4)*FPS)
    for k in range(n3):
        t=k/(n3-1)
        b,d=canvas(); chrome(d,ep=24)
        ftxt(d,(W//2,480),'El 3-putt muere aquí:',GEO(58),INK,t)
        d2=ImageDraw.Draw(b,'RGBA')
        a1=int(255*min(t*2.5,1))
        d2.text((W//2-180,950),'36',font=BLACK(160),fill=SUB+(a1,),anchor='mm')
        if t>0.3:
            aa=int(255*min((t-0.3)*3,1))
            d2.line([(W//2-290,950),(W//2-70,950)],fill=RED+(aa,),width=10)
            d2.text((W//2+30,950),'→',font=BLACK(80),fill=SUB+(aa,),anchor='mm')
        if t>0.45:
            e3=M.ease(min((t-0.45)*2.6,1))
            d2.text((W//2+230,950),'31',font=BLACK(190),fill=GREEN+(int(255*e3),),anchor='mm')
        if t>0.62:
            ftxt(d,(W//2,1180),'putts por ronda con lag disciplinado',BOLD(42),SUB,(t-0.62)/0.38,t_out=0.94)
        M.progressbar(d,0.62+0.16*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('el lag putt no busca gloria busca un tap in circulo de 1 metro siempre',1.3)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d,ep=24)
        M.poptext(d,W//2,790,'El lag putt no busca gloria.',62,t*1.9,INK)
        M.poptext(d,W//2,930,'Busca un TAP-IN.',80,max(t*1.9-0.25,0),GREEN)
        if t>0.5:
            ftxt(d,(W//2,1150),'Círculo de 1 metro. Siempre.',BOLD(44),SUB,(t-0.5)/0.5,t_out=0.92)
        M.progressbar(d,0.78+0.08*t,PAL); frames.append(V.fin(b))
    app_outro(frames,flow=[('15-diagnostico.png',None)],line1='PARFECT te da los drills exactos del lag:',ep=24,per=5.0)
    return M.render(frames,'theory-lag')

# ============================================================
# THEORY 12 · "Bandera atras = FRENTE del green" (EP 25, artesanal)
# ============================================================
def teoria_bandatras():
    import math as mt
    frames=[]
    # gancho #16: PERFIL del green — el tiro largo muere atras, el corto rueda a la bandera
    lines=['BANDERA ATRÁS','= FRENTE DEL GREEN.']; sub='(la profundidad es una trampa)'
    secs=max(4.4,M.dur_lectura(' '.join(lines)+' '+sub,1.2))
    n=int(secs*FPS)
    gy=1560; gx0,gx1=180,860   # superficie del green de perfil
    fx=820                     # bandera atras
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=25)
        d2=ImageDraw.Draw(b,'RGBA')
        # suelo + green elevado de perfil
        def suelo(dd):
            dd.line([(90,gy+26),(W-90,gy+26)],fill=GREENDIM+(255,),width=6)
            dd.line([(gx0,gy),(gx1,gy)],fill=GREEN+(235,),width=7)
        glow(b,suelo,9,1)
        # rough trasero
        d2.rectangle([gx1+14,gy-8,W-100,gy+18],fill=(46,36,24,255))
        d2.text(((gx1+W-90)//2,gy+64),'rough',font=BOLD(30),fill=SUB+(210,),anchor='mm')
        # bandera atras
        d2.line([(fx,gy),(fx,gy-160)],fill=(250,250,246,255),width=6)
        d2.polygon([(fx,gy-160),(fx+62,gy-140),(fx,gy-118)],fill=RED+(255,))
        d2.ellipse([fx-9,gy-6,fx+9,gy+6],fill=(5,9,7,255))
        # tiro 1: a la bandera -> vuela largo y muere en el rough (rojo)
        if t<0.5:
            e=M.ease(min(t/0.46,1))
            pts=[]
            for i in range(int(46*e)+1):
                q=i/46
                px=140+q*(940-140); py=gy-16-mt.sin(q*mt.pi)*560
                pts.append((px,py))
            if len(pts)>1:
                col=RED if pts[-1][0]>fx else (250,250,246)
                def t1(dd,pts=pts,col=col):
                    dd.line(pts,fill=col+(230,),width=7)
                glow(b,t1,9,1)
                bx,by=pts[-1]; d2.ellipse([bx-14,by-14,bx+14,by+14],fill=(250,250,246,255))
            if e>=1:
                d2.text((950,gy-240),'muerta atrás',font=BOLD(36),fill=RED+(255,),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,255))
        # tiro 2: al FRENTE -> aterriza y rueda hasta la bandera (verde)
        if t>0.52:
            e=M.ease(min((t-0.52)/0.32,1))
            pts=[]
            for i in range(int(40*e)+1):
                q=i/40
                px=140+q*(430-140); py=gy-16-mt.sin(q*mt.pi)*470
                pts.append((px,py))
            if len(pts)>1:
                def t2(dd,pts=pts):
                    dd.line(pts,fill=GREEN+(240,),width=7)
                glow(b,t2,9,1)
            if e>=1:
                r=M.ease(min((t-0.84)/0.14,1)) if t>0.84 else 0
                rx=430+(fx-60-430)*r
                def rueda(dd,rx=rx):
                    for xx in range(440,int(rx),34):
                        dd.ellipse([xx-4,gy-22,xx+4,gy-14],fill=GREEN+(170,))
                glow(b,rueda,6,1)
                d2.ellipse([rx-14,gy-32,rx+14,gy-4],fill=(250,250,246,255))
                if r>=1: d2.text((470,gy-100),'rueda sola a la bandera',font=BOLD(36),fill=GREEN+(255,),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,255))
        ty=420
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,80,(t-0.07*i)*2.3,GREEN if i==1 else INK,font=BLACK,maxw=W-110)
            ty+=130
        if t>0.3: ftxt(d,(W//2,ty+28),sub,BOLD(42),SUB,(t-0.3)/0.7,t_out=0.95)
        M.progressbar(d,0.04+0.06*t,PAL); frames.append(V.fin(b))
    # fase 1: cenital con profundidad — 10 tiros a la bandera trasera
    import random as rd
    r1=rd.Random(13)
    cx,cy=W//2,1020
    n1=int(6.0*FPS)
    tiros=[(cx+r1.uniform(-150,150),cy+r1.uniform(-40,300)) for _ in range(7)]+[(cx+r1.uniform(-120,120),cy-r1.uniform(300,430)) for _ in range(3)]
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d,ep=25)
        ftxt(d,(W//2,400),'10 tiros a la bandera de ATRÁS:',GEO(54),INK,t)
        e=M.ease(min(t*1.8,1))
        pts=green_pts(cx,cy,300*e,390*e)
        d2=ImageDraw.Draw(b,'RGBA')
        d2.polygon(pts,fill=GREENDIM+(255,))
        def edge(dd,pts=pts):
            dd.line(pts+[pts[0]],fill=GREEN+(220,),width=5)
        glow(b,edge,9,1)
        fx2,fy2=cx,cy-300
        d2.line([(fx2,fy2),(fx2,fy2-120)],fill=(250,250,246,255),width=6)
        d2.polygon([(fx2,fy2-120),(fx2+52,fy2-104),(fx2,fy2-86)],fill=RED+(255,))
        for i,(px,py) in enumerate(tiros):
            ft=min(max(t*3.0-0.5-i*0.14,0),1)
            if ft<=0: continue
            largo=py<cy-280
            def dot(dd,px=px,py=py,ft=ft,largo=largo):
                if largo:
                    dd.ellipse([px-13,py-13,px+13,py+13],outline=RED+(int(240*ft),),width=5)
                    dd.line([(px-9,py-9),(px+9,py+9)],fill=RED+(int(240*ft),),width=5)
                else:
                    dd.ellipse([px-13,py-13,px+13,py+13],fill=(250,250,246,int(235*ft)))
            glow(b,dot,6,1)
        if t>0.68:
            a=min((t-0.68)*5,1.0) if t<0.92 else max(0.0,(1.0-t)/0.08)
            d2.text((W//2,1560),'7 quedan cortos igual. Y los 3 largos: castigo.',font=BOLD(40),fill=LIME+(int(255*a),),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.14+0.22*t,PAL); frames.append(V.fin(b))
    # fase 2: score comparado
    n2=int(M.dur_lectura('score del hoyo a la bandera atras 4.9 al centro frente 4.4 putt de subida en vez de chip imposible',1.4)*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d,ep=25)
        ftxt(d,(W//2,400),'Score promedio del hoyo:',GEO(56),INK,t)
        d2=ImageDraw.Draw(b,'RGBA')
        for i,(lab,val,col) in enumerate([('A LA BANDERA ATRÁS','4.9',RED),('AL CENTRO-FRENTE','4.4',GREEN)]):
            ft=min(max(t*2.4-i*0.5,0),1)
            if ft<=0: continue
            y=780+i*320; a=int(255*(ft*ft*(3-2*ft)))
            def box(dd,y=y,ft=ft,col=col):
                dd.rounded_rectangle([150,y-110,W-150,y+110],28,outline=col+(int(215*ft),),width=5)
            glow(b,box,8,1)
            d2.text((190,y),lab,font=BOLD(38),fill=INK+(a,),anchor='lm')
            d2.text((W-190,y),val,font=BLACK(80),fill=col+(a,),anchor='rm')
        if t>0.62:
            aa=min((t-0.62)*5,1.0) if t<0.9 else max(0.0,(1.0-t)/0.1)
            d2.text((W//2,1480),'Putt de subida > chip imposible de bajada',font=BOLD(42),fill=LIME+(int(255*aa),),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,int(255*aa)))
        M.progressbar(d,0.38+0.24*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('la bandera de atras es un anzuelo el frente del green es el tiro inteligente',1.3)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d,ep=25)
        M.poptext(d,W//2,790,'La bandera de atrás es un anzuelo.',58,t*1.9,INK)
        M.poptext(d,W//2,935,'No lo muerdas.',84,max(t*1.9-0.3,0),GREEN)
        if t>0.5:
            ftxt(d,(W//2,1150),'Frente del green. Putt de subida. Score.',BOLD(42),SUB,(t-0.5)/0.5,t_out=0.92)
        M.progressbar(d,0.64+0.2*t,PAL); frames.append(V.fin(b))
    app_outro(frames,flow=[('11-ronda.png',None)],line1='PARFECT te enseña dónde caen TUS tiros:',ep=25,per=5.0)
    return M.render(frames,'theory-bandatras')

def teoria_heroe():
    import math as mt
    frames=[]
    # gancho #17: CENITAL bola entre arboles — ruta heroe (roja, choca) vs salida lateral (lima)
    lines=['EL GOLPE HÉROE','CUESTA 3.']; sub='(la salida lateral cuesta 1)'
    secs=max(4.6,M.dur_lectura(' '.join(lines)+' '+sub,1.2))
    n=int(secs*FPS)
    bx,by=280,1480                    # bola metida en los arboles
    gcx,gcy=700,935                   # green cenital arriba-derecha
    arboles=[(380,1330,52),(478,1244,46),(418,1168,40),(566,1156,54),(520,1078,42),(618,1042,44),(330,1420,44),(452,1400,38)]
    def lerp(a,b,q): return a+(b-a)*q
    for k in range(n):
        t=k/max(n-1,1)
        b,d=canvas(); chrome(d,ep=26)
        d2=ImageDraw.Draw(b,'RGBA')
        # green con bandera
        pts=green_pts(gcx,gcy,150,185)
        d2.polygon(pts,fill=GREENDIM+(255,))
        def edge(dd,pts=pts):
            dd.line(pts+[pts[0]],fill=GREEN+(210,),width=5)
        glow(b,edge,8,1)
        d2.line([(gcx,gcy),(gcx,gcy-95)],fill=(250,250,246,255),width=5)
        d2.polygon([(gcx,gcy-95),(gcx+44,gcy-81),(gcx,gcy-67)],fill=RED+(255,))
        # calle a la derecha de la bola
        d2.rounded_rectangle([620,1400,930,1560],32,fill=(20,42,30,255))
        d2.text((775,1600),'calle',font=BOLD(30),fill=SUB+(210,),anchor='mm')
        # arboles entre bola y green
        for ax,ay,ar in arboles:
            d2.ellipse([ax-ar,ay-ar,ax+ar,ay+ar],fill=(38,68,46,255),outline=(74,118,84,255),width=3)
            d2.ellipse([ax-7,ay-7,ax+7,ay+7],fill=(96,72,44,255))
        # bola
        d2.ellipse([bx-15,by-15,bx+15,by+15],fill=(250,250,246,255))
        # ruta 1 (heroe): punteada roja hacia el green, CHOCA a 45% del camino
        if t<0.5:
            e=M.ease(min(t/0.42,1))
            q_end=0.45*e/max(e,1e-6)*e if e<1 else 0.45
            q_end=0.45*min(e,1)
            segs=int(26*min(e,1))
            for i in range(segs):
                q=0.45*i/26
                px,py=lerp(bx,gcx,q),lerp(by,gcy,q)
                def dash(dd,px=px,py=py):
                    dd.ellipse([px-5,py-5,px+5,py+5],fill=RED+(220,))
                glow(b,dash,5,1)
            if e>=1:
                ix,iy=lerp(bx,gcx,0.45),lerp(by,gcy,0.45)
                def imp(dd,ix=ix,iy=iy):
                    dd.ellipse([ix-26,iy-26,ix+26,iy+26],outline=RED+(240,),width=6)
                glow(b,imp,8,1)
                d2.text((215,1080),'choca 8 de 10',font=BOLD(36),fill=RED+(255,),anchor='lm',stroke_width=5,stroke_fill=(8,14,11,255))
        # ruta 2 (lateral): lima solida a la calle, tiro limpio
        if t>0.52:
            e=M.ease(min((t-0.52)/0.3,1))
            ex,ey=lerp(bx,775,e),lerp(by,1478,e)
            def lat(dd,ex=ex,ey=ey):
                dd.line([(bx,by),(ex,ey)],fill=LIME+(240,),width=8)
            glow(b,lat,9,1)
            if e>=1:
                d2.ellipse([775-14,1478-14,775+14,1478+14],fill=(250,250,246,255))
                d2.text((640,1650),'a la calle · tiro limpio',font=BOLD(36),fill=LIME+(255,),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,255))
        ty=420
        for i,ln in enumerate(lines):
            M.poptext(d,W//2,ty,ln,80,(t-0.07*i)*2.3,RED if i==1 else INK,font=BLACK,maxw=W-110)
            ty+=130
        if t>0.3: ftxt(d,(W//2,ty+28),sub,BOLD(42),SUB,(t-0.3)/0.7,t_out=0.95)
        M.progressbar(d,0.04+0.06*t,PAL); frames.append(V.fin(b))
    # fase 1: 10 intentos del heroe por el hueco — 8 chocan, 2 pasan
    import random as rd
    r1=rd.Random(17)
    n1=int(6.0*FPS)
    ox,oy=W//2,1600                    # origen de los tiros
    tl,tr=(410,1075,95),(700,1055,105) # dos copas con hueco estrecho
    dest=[]
    for i in range(10):
        if i in (3,7): dest.append((W//2+r1.uniform(-26,26),760,True))          # pasan por el hueco
        else:
            side=tl if i%2 else tr
            dest.append((side[0]+r1.uniform(-40,40),side[1]+r1.uniform(-30,50),False))
    for k in range(n1):
        t=k/(n1-1)
        b,d=canvas(); chrome(d,ep=26)
        ftxt(d,(W//2,400),'10 intentos del golpe héroe:',GEO(54),INK,t)
        d2=ImageDraw.Draw(b,'RGBA')
        e=M.ease(min(t*1.8,1))
        for ax,ay,ar in (tl,tr):
            rr=ar*e
            d2.ellipse([ax-rr,ay-rr,ax+rr,ay+rr],fill=(38,68,46,255),outline=(74,118,84,255),width=3)
            if e>0.9: d2.ellipse([ax-8,ay-8,ax+8,ay+8],fill=(96,72,44,255))
        d2.ellipse([ox-13,oy-13,ox+13,oy+13],fill=(250,250,246,255))
        for i,(px,py,pasa) in enumerate(dest):
            ft=min(max(t*3.0-0.5-i*0.13,0),1)
            if ft<=0: continue
            ex,ey=ox+(px-ox)*M.ease(ft),oy+(py-oy)*M.ease(ft)
            col=(250,250,246) if pasa else RED
            def tray(dd,ex=ex,ey=ey,col=col,ft=ft):
                dd.line([(ox,oy),(ex,ey)],fill=col+(int(190*ft),),width=5)
            glow(b,tray,5,1)
            if ft>=1:
                if pasa: d2.ellipse([px-12,py-12,px+12,py+12],fill=(250,250,246,235))
                else:
                    def chk(dd,px=px,py=py):
                        dd.ellipse([px-14,py-14,px+14,py+14],outline=RED+(240,),width=5)
                        dd.line([(px-9,py-9),(px+9,py+9)],fill=RED+(240,),width=5)
                    glow(b,chk,6,1)
        if t>0.68:
            a=min((t-0.68)*5,1.0) if t<0.92 else max(0.0,(1.0-t)/0.08)
            d2.text((W//2,1750),'Pasa 2 de 10. El resto: doble bogey o peor.',font=BOLD(40),fill=LIME+(int(255*a),),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,int(255*a)))
        M.progressbar(d,0.14+0.22*t,PAL); frames.append(V.fin(b))
    # fase 2: score comparado
    n2=int(M.dur_lectura('score del hoyo despues de un mal drive al heroe entre arboles 6.1 salida lateral 5.0 un golpe seguro tres de fantasia',1.4)*FPS)
    for k in range(n2):
        t=k/(n2-1)
        b,d=canvas(); chrome(d,ep=26)
        ftxt(d,(W//2,400),'Tras un mal drive, el hoyo termina en:',GEO(52),INK,t)
        d2=ImageDraw.Draw(b,'RGBA')
        for i,(lab,val,col) in enumerate([('JUGANDO AL HÉROE','6.1',RED),('SALIDA LATERAL','5.0',GREEN)]):
            ft=min(max(t*2.4-i*0.5,0),1)
            if ft<=0: continue
            y=780+i*320; a=int(255*(ft*ft*(3-2*ft)))
            def box(dd,y=y,ft=ft,col=col):
                dd.rounded_rectangle([150,y-110,W-150,y+110],28,outline=col+(int(215*ft),),width=5)
            glow(b,box,8,1)
            d2.text((190,y),lab,font=BOLD(38),fill=INK+(a,),anchor='lm')
            d2.text((W-190,y),val,font=BLACK(80),fill=col+(a,),anchor='rm')
        if t>0.62:
            aa=min((t-0.62)*5,1.0) if t<0.9 else max(0.0,(1.0-t)/0.1)
            d2.text((W//2,1480),'Un golpe seguro > tres golpes de fantasía',font=BOLD(42),fill=LIME+(int(255*aa),),anchor='mm',stroke_width=5,stroke_fill=(8,14,11,int(255*aa)))
        M.progressbar(d,0.38+0.24*t,PAL); frames.append(V.fin(b))
    # insight
    nin=int(M.dur_lectura('tu tarjeta no premia lo epico premia lo repetible bola a la calle bogey y al siguiente',1.3)*FPS)
    for k in range(nin):
        t=k/(nin-1)
        b,d=canvas(); chrome(d,ep=26)
        M.poptext(d,W//2,790,'Tu tarjeta no premia lo épico.',58,t*1.9,INK)
        M.poptext(d,W//2,935,'Premia lo repetible.',84,max(t*1.9-0.3,0),GREEN)
        if t>0.5:
            ftxt(d,(W//2,1150),'Bola a la calle. Bogey. Siguiente hoyo.',BOLD(42),SUB,(t-0.5)/0.5,t_out=0.92)
        M.progressbar(d,0.64+0.2*t,PAL); frames.append(V.fin(b))
    app_outro(frames,flow=[('09-analisis.png',None)],line1='PARFECT te dice dónde regalas golpes:',ep=26,per=5.0)
    return M.render(frames,'theory-heroe')

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
    elif cmd=='lag': teoria_lag()
    elif cmd=='bandatras': teoria_bandatras()
    elif cmd=='heroe': teoria_heroe()
    elif cmd=='debajo': teoria_debajo()
    elif cmd=='20min': teoria_20min()
    elif cmd=='fairway': teoria_fairway()
    elif cmd=='uso1': uso01()
    elif cmd=='uso2': uso02()
    elif cmd=='uso3': uso03()
    else:
        teoria_bandera(); teoria_okay()
