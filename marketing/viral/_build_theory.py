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

def ftxt(d,xy,txt,font,fill,t,anchor='mm',t_out=0.86):
    """texto con fade-in/out: nunca se encima con el siguiente mensaje"""
    a=min(t*5,1.0) if t<t_out else max(0.0,(1.0-t)/(1.0-t_out))
    if a<=0.02: return
    d.text(xy,txt,font=font,fill=fill+(int(255*a),),anchor=anchor)

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
    else:
        teoria_bandera(); teoria_okay()
