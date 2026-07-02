#!/usr/bin/env python3
# ============================================================
# PARFECT · DEPARTAMENTO DE MARKETING AUTOMÁTICO
# Un solo comando prepara la publicación del día completa:
# imagen (estilo Editorial de Datos v3) + video vertical con
# transiciones + caption con hashtags + hora sugerida + QC.
# También lleva métricas y recomienda qué formato escalar.
#
#   python3 _dept.py hoy                  # prepara el post de hoy
#   python3 _dept.py preparar 2026-07-04  # prepara una fecha
#   python3 _dept.py semana               # prepara los próximos 7 días
#   python3 _dept.py proximos             # muestra el plan 14 días
#   python3 _dept.py registrar 2026-07-02 1200 80 14 6   # vistas likes com comp
#   python3 _dept.py reporte              # qué funciona, qué matar
#
# Salida: outbox/<fecha>-<slug>/  → video.mp4, imagen .png,
#         caption.txt, CHECKLIST.md
# ============================================================
import os, sys, csv, subprocess, shutil, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _build_viral as V
import _content_engine as E
from PIL import Image

HERE   = os.path.dirname(os.path.abspath(__file__))
OUTBOX = os.path.join(HERE,'outbox')
METR   = os.path.join(HERE,'metrica.csv')
EPOCH  = dt.date(2026,7,2)          # arranque del plan
HORA   = {0:'19:30',1:'13:00',2:'19:30',3:'13:00',4:'17:00',5:'11:00',6:'18:00'}

# lunes=carrusel; resto formatos sueltos (variedad = algoritmo contento)
PLAN_SEMANAL = {0:'carrusel',1:'theory',2:'quiz',3:'theory',4:'feature',5:'entra',6:'theory'}

COLA_CARRUSELES = ['v4-carrusel2-bajar-hcp','v4-carrusel4-mitos','v4-carrusel5-senales',
    'v4-carrusel6-tabla-hcp','v4-carrusel7-habitos','v4-carrusel8-errores-green',
    'v4-carrusel9-preguntas','v4-carrusel10-cambia','v4-carrusel11-amigos',
    'v4-carrusel12-practica','v4-carrusel13-curiosos','v4-carrusel14-no-bajas-90',
    'v4-carrusel1-verdades']

GANCHO_CARRUSEL = {
    'v4-carrusel2-bajar-hcp':'5 formas de bajar tu hándicap más rápido (sin pegarle más lejos) 👇',
    'v4-carrusel4-mitos':'7 mitos del golf que te están deteniendo 🚫',
    'v4-carrusel5-senales':'6 señales de que pierdes golpes sin darte cuenta 👀',
    'v4-carrusel6-tabla-hcp':'Así juega cada hándicap, del 36 al scratch 📊',
    'v4-carrusel7-habitos':'5 hábitos de golfistas de un solo dígito 🎯',
    'v4-carrusel8-errores-green':'7 errores que te cuestan golpes en el green ⛳',
    'v4-carrusel9-preguntas':'5 preguntas que debes hacerte después de cada ronda 🤔',
    'v4-carrusel10-cambia':'6 cosas que cambian cuando empiezas a medir tu golf 📈',
    'v4-carrusel11-amigos':'5 razones para llevar la cuenta con una app cuando juegas con amigos 🍺',
    'v4-carrusel12-practica':'5 formas de aprovechar mejor tu tiempo de práctica ⏱️',
    'v4-carrusel13-curiosos':'6 datos de golf que te van a sorprender 🤯',
    'v4-carrusel14-no-bajas-90':'3 razones por las que no bajas de 90 (y no es tu swing) 🔥',
    'v4-carrusel3-dato':'El dato que más golpes te cuesta y ni te habías dado cuenta 👀',
    'v4-carrusel1-verdades':'8 verdades del golf que nadie te dice (la 5 me dolió) ⛳',
}

# --- bancos de contenido (rotan solos; agrega más cuando quieras) ---
MEMES=[('Cuando dices "solo tiro unas bolas"','y llevas 3 horas en el driving range'),
 ('Tu cara cuando te preguntan tu hándicap','y no lo sabes ni tú'),
 ('Nadie:','Yo a las 5am un sábado por el tee time'),
 ('Mi swing en el rango:','Mi swing en el tee del hoyo 1: desconocido'),
 ('Yo después de UN par:','"creo que ya le entendí al golf"'),
 ('El palo no era.','Tampoco el anterior. Ni el que sigue.'),
 ('POV: tu putt de 1 metro','de pronto mide 4 kilómetros'),
 ('"Última bola y nos vamos"','— nadie se fue, temporada 47')]
STATS=[('56%','de fairways','es lo que tira un HCP 10 en promedio.'),
 ('32','putts por ronda','el amateur promedio. Un scratch hace 30.'),
 ('8%','de GIR','es todo lo que tiene un HCP 36. La mejora está ahí.'),
 ('1 de 3','greens en regulación','toma el jugador amateur promedio.'),
 ('3','golpes por ronda','se van solo en 3-putts que no cuentas.'),
 ('41%','up & down','es lo que salva un HCP 15 en sus greens fallados. ¿Y tú?')]
QUOTES=[('El golf no premia al que pega más lejos, sino al que falla menos.',''),
 ('No puedes mejorar lo que no mides.',''),
 ('Cada putt de 1 metro vale un golpe. Trátalo así.',''),
 ('El score se hace en 100 yardas y menos.',''),
 ('Practicar sin objetivo es pasear con palos.',''),
 ('Tu tarjeta dice la verdad que tu memoria edita.','')]
MYTHS=[('Necesitas pegarle más lejos para bajar tu hándicap.','Se ganan más golpes fallando menos y con el juego corto.'),
 ('Las estadísticas son solo para profesionales.','Entre más alto tu hándicap, más golpes fáciles hay que ganar con datos.'),
 ('Jugar todos los días te hace mejor.','Practicar sin objetivo no cambia tu score.'),
 ('El putt es cuestión de suerte.','Es la parte más medible de todo tu juego.'),
 ('Comprar palos nuevos baja tu hándicap.','El hándicap baja con repetición medida, no con recibos.')]
FEATURES=[('shot-analisis.png','Tu coach IA lee tus rondas','Te dice dónde pierdes golpes y qué entrenar.'),
 ('shot-rondas.png','Anota tu ronda en segundos','Fairway, green, up & down y putts, hoyo por hoyo.'),
 ('shot-logros.png','Tu progreso, gamificado','Logros reales por hitos de tu juego, no medallitas vacías.'),
 ('shot-social.png','Tu liga de amigos','Scores en vivo, apuestas claras y cero peleas por la tarjeta.'),
 ('shot-inicio.png','Todo tu golf en una pantalla','Hándicap, tendencia y qué practicar hoy.')]
RETOS=[('RETO: CERO 3-PUTTS','una semana de green disciplinado',['Cuenta tus putts hoyo por hoyo','Primer putt: solo déjala a 1 metro','10 min de putts cortos al día']),
 ('RETO: FAIRWAY FIRST','2 semanas de salidas inteligentes',['Anota cada salida: fairway sí o no','Cambia driver por madera 3 si fallas 3 seguidas','Compara tu % contra tu meta de HCP']),
 ('RETO: ROMPER 90','7 días midiendo cada ronda',['Registra tus próximas 3 rondas completas','Encuentra tu fuga #1 en Análisis IA','Entrena solo eso 20 min al día'])]

# --- THEORY: cola de videos pre-renderizados (ver TEORIA-50.md) ---
# solo SIN publicar (los publicados salen de la cola)
THEORY_COLA=[('theory-putts30-voz.mp4','Un scratch hace 30 putts. ¿Tú cuántos? Esos 6 golpes están en tu putter 🥶'),
 ]  # se agregan conforme se rendericen (tandas semanales)
QUIZES=[('¿Cuál es el par más común en un campo de 18 hoyos?',['70','72','74'],1,'Par 72: cuatro pares 3, cuatro pares 5 y diez pares 4.'),
 ('¿Desde dónde se pierden más golpes?',['El tee','100 yardas y menos','El green'],1,'Más de la mitad de tu score se hace en 100 yardas y menos.'),
 ('¿Cuántos greens en regulación toma un HCP 36?',['1 de 3','1 de 6','1 de 12'],2,'Apenas 1 de cada 12. Ahí está la mina de golpes.'),
 ('¿Qué baja más rápido tu score?',['Driver nuevo','Clases de swing','Medir tu juego'],2,'Sin datos practicas a ciegas. Mide primero.'),
 ('¿Cuántos up & down salva un HCP 15?',['4 de 10','6 de 10','8 de 10'],0,'41%. El juego corto es la frontera del hándicap.'),
 ('¿Qué vale igual que un drive de 250 yardas?',['Un putt de 1 metro','Un chip','Los dos'],2,'Todo golpe vale 1. Tu tarjeta no distingue.'),
 ('¿Cuántos 3-putts hace el amateur por ronda?',['0 a 1','1 a 2','3 o más'],1,'Entre 1 y 2. Dos golpes regalados cada ronda.'),
 ('¿Con qué palo pegas MÁS fairways?',['Driver','Madera 3','Híbrido'],1,'En hoyos cerrados la madera 3 gana score.')]

def nth_del_tipo(fecha,tipo):
    n=0; d=EPOCH
    while d<=fecha:
        if PLAN_SEMANAL[d.weekday()]==tipo and d<fecha: n+=1
        d+=dt.timedelta(days=1)
    return n

HASHTAGS=['#golf #golftips #golfswing #handicap #golfmexico #golfmorelia',
 '#golf #golflife #golfstats #aprendegolf #golfmexico #morelia',
 '#golf #golftok #juegocorto #putting #golfmexico #golfista']
CTA_LINEA='Mídelo con PARFECT: anotas tu ronda y te dice en qué pierdes golpes. Gratis, link en bio.'

def idx(fecha): return (fecha-EPOCH).days
def tipo_del_dia(fecha): return PLAN_SEMANAL[fecha.weekday()]

def pieza_del_dia(fecha):
    i=idx(fecha); t=tipo_del_dia(fecha); w=i//7
    if t=='carrusel':
        c=COLA_CARRUSELES[w%len(COLA_CARRUSELES)]
        return t,c,GANCHO_CARRUSEL[c]
    if t=='theory':
        k=nth_del_tipo(fecha,'theory')%max(len(THEORY_COLA),1)
        f,g=THEORY_COLA[k]; return t,f,g
    if t=='quiz':
        item=QUIZES[nth_del_tipo(fecha,'quiz')%len(QUIZES)]
        return t,item,f'QUIZ ⛳ {item[0]} Responde antes del 3-2-1 👇'
    if t=='entra':
        si=nth_del_tipo(fecha,'entra')%2==0
        return t,si,'¿ENTRA o NO ENTRA? 👀⛳ Di tu apuesta en los comentarios ANTES de que caiga…'
    banco={'meme':MEMES,'stat':STATS,'quote':QUOTES,'myth':MYTHS,'feature':FEATURES,'challenge':RETOS}[t]
    item=banco[w%len(banco)]
    gancho={'meme':f'{item[0]} 😂','stat':f'El dato de hoy: {item[0]} {item[1]} 📊',
        'quote':f'{item[0]} 🧠','myth':f'Mito: “{item[0]}” — la realidad te va a doler 👇',
        'feature':f'{item[1]} 🤖','challenge':f'{item[0]} — ¿te apuntas? 💪'}[t]
    return t,item,gancho

def genera_imagen(t,item,fecha):
    if t=='meme': img=E.meme(item[0],item[1]); slugv=E.slug(item[0])
    elif t=='stat': img=E.stat(*item); slugv=E.slug(item[0]+item[1])
    elif t=='quote': img=E.quote(*item); slugv=E.slug(item[0])
    elif t=='myth': img=E.myth(*item); slugv=E.slug(item[0])
    elif t=='feature': img=E.feature(*item); slugv=E.slug(item[1])
    elif t=='challenge': img=E.challenge(item[0],item[1],item[2]); slugv=E.slug(item[0])
    return img,slugv

def video_de_pieza(folder_rel, outmp4):
    """carpeta de PNGs -> frames -> mp4; v4-* sale en 4K (2160x3840)"""
    uhd=folder_rel.startswith('v4-')
    builder='_build_pro4.py' if uhd else '_build_pro.py'
    r=subprocess.run(['python3',os.path.join(HERE,builder),folder_rel],
                     capture_output=True,text=True,cwd=HERE)
    if r.returncode!=0: print('  ✗ frames:',r.stderr.strip()[:200]); return False
    man=os.path.join(HERE,'_pro_frames',folder_rel+'.manifest.txt')
    enc=os.path.join(HERE,'_encode_4k' if uhd else '_encode_pro')
    if not os.path.exists(enc): print('  ✗ falta _encode_pro'); return False
    r=subprocess.run([enc,man,outmp4],capture_output=True,text=True,cwd=HERE)
    ok=r.returncode==0 and os.path.exists(outmp4)
    if not ok: print('  ✗ encode:',(r.stderr or r.stdout).strip()[:200])
    return ok

def qc(png,mp4,caption):
    res=[]
    if png and os.path.exists(png):
        w,h=Image.open(png).size
        res.append(('imagen cuadrada 1080/2160', w==h and w in (1080,2160)))
    if mp4:
        res.append(('video existe y pesa >0.5MB', os.path.exists(mp4) and os.path.getsize(mp4)>500_000))
    res.append(('caption <=2200 chars', len(caption)<=2200))
    res.append(('tiene hashtags', '#' in caption))
    res.append(('tiene CTA', 'link en bio' in caption.lower()))
    return res

def video_motion(t,item,dest_mp4):
    """video animado nativo por tipo; regresa True si lo logro"""
    import _build_motion as MO
    try:
        if t=='stat': p=MO.video_dato(item[0],item[1],item[2] if len(item)>2 else '')
        elif t=='challenge': p=MO.video_razones(item[0],item[2])
        elif t=='myth': p=MO.video_razones('Mito: '+item[0],['Realidad: '+item[1]])
        elif t=='quote': p=MO.video_razones('Mentalidad de scratch',[item[0]])
        elif t=='meme':
            p=MO.video_meme_putt(item[0],item[1]) if 'putt' in (item[0]+item[1]).lower() else MO.video_razones(item[0],[item[1]])
        elif t=='feature': p=MO.video_app(variant=1+idx(dt.date.today())%2)
        elif t=='quiz': p=MO.video_quiz(item[0],item[1],item[2],item[3])
        elif t=='entra': p=MO.video_entra(item)
        else: return False
        if p: shutil.copy(p,dest_mp4); return True
    except Exception as e:
        print('  motion fallback:',e)
    return False

def preparar(fecha):
    t,item,gancho=pieza_del_dia(fecha)
    i=idx(fecha)
    caption=f'{gancho}\n{CTA_LINEA}\n{HASHTAGS[i%len(HASHTAGS)]}'
    folder=None; pngs=[]
    if t=='carrusel':
        slugv=item; folder=item
    elif t=='theory':
        slugv=item.replace('.mp4','')
    elif t in ('quiz','entra'):
        slugv=E.slug(item[0]) if t=='quiz' else ('entra-si' if item else 'entra-no')
    else:
        img,slugv=genera_imagen(t,item,fecha)
        folder=f'pieza-{fecha.strftime("%Y%m%d")}'
        fdir=os.path.join(HERE,folder); os.makedirs(fdir,exist_ok=True)
        img.save(os.path.join(fdir,'01.png'))
        V.save(V.slide_cta('MIDE TU GOLF','DE VERDAD','shot-inicio.png'),folder,'02.png')
    dest=os.path.join(OUTBOX,f'{fecha.isoformat()}-{t}-{slugv[:30]}')
    os.makedirs(dest,exist_ok=True)
    if folder:
        fdir=os.path.join(HERE,folder)
        pngs=sorted(f for f in os.listdir(fdir) if f.endswith('.png'))
        for f in pngs: Image.open(os.path.join(fdir,f)).save(os.path.join(dest,f))
    # video vertical
    mp4=os.path.join(dest,'video.mp4')
    if t=='theory':
        src=os.path.join(HERE,'motion',item)
        vok=os.path.exists(src) and (shutil.copy(src,mp4) or True)
    elif t=='carrusel':
        vok=video_de_pieza(folder,mp4)
    else:
        vok=video_motion(t,item,mp4)
        if not vok and folder: vok=video_de_pieza(folder,mp4)
    open(os.path.join(dest,'caption.txt'),'w').write(caption)
    rep=qc(os.path.join(dest,pngs[0]) if pngs else None,mp4 if vok else None,caption)
    chk='\n'.join(f'- [{"x" if ok else " "}] {n}' for n,ok in rep)
    open(os.path.join(dest,'CHECKLIST.md'),'w').write(f'''# Publicación {fecha.isoformat()} · {t.upper()}

**Hora sugerida:** {HORA[fecha.weekday()]} (hora Morelia)
**Música sugerida:** TikTok → Sonidos → "Sin límites" → algo upbeat (ej. Bright Aura)

## QC automático
{chk}

## Pasos
1. Arrastra `video.mp4` al uploader de TikTok Studio (yo no puedo meter el archivo).
2. Yo pongo caption + hashtags + música desde Chrome.
3. Publicar (TikTok). En Instagram: sube los PNG como carrusel con el mismo caption.
''')
    estado='✓' if all(ok for _,ok in rep) else '✗ REVISAR'
    print(f'{fecha.isoformat()} · {t:<9} → {os.path.relpath(dest,HERE)}  [{estado}]')
    return dest

def registrar(fecha,vistas,likes,com,comp=0):
    nuevo=not os.path.exists(METR)
    t,_,_=pieza_del_dia(dt.date.fromisoformat(fecha))
    with open(METR,'a',newline='') as f:
        wcsv=csv.writer(f)
        if nuevo: wcsv.writerow(['fecha','tipo','vistas','likes','comentarios','compartidos'])
        wcsv.writerow([fecha,t,vistas,likes,com,comp])
    print(f'registrado: {fecha} ({t}) → {vistas} vistas')

def reporte():
    if not os.path.exists(METR): print('sin métricas aún. usa: registrar <fecha> <vistas> <likes> <com> [comp]'); return
    rows=list(csv.DictReader(open(METR)))
    if not rows: print('metrica.csv vacío'); return
    agg={}
    for r in rows:
        a=agg.setdefault(r['tipo'],[0,0,0])
        a[0]+=int(r['vistas']); a[1]+=int(r['likes'])+int(r['comentarios'])*3+int(r.get('compartidos') or 0)*5; a[2]+=1
    print('=== RENDIMIENTO POR FORMATO ===')
    orden=sorted(agg.items(),key=lambda kv:-kv[1][0]/kv[1][2])
    for t,(v,e,n) in orden:
        print(f'  {t:<10} {v//n:>7} vistas/post · engagement {e//n:>5} · {n} posts')
    best,worst=orden[0][0],orden[-1][0]
    print(f'\n→ ESCALAR: {best} (mete 2 por semana en lugar de 1)')
    if len(orden)>2: print(f'→ REVISAR: {worst} (cambia el gancho 2 semanas; si sigue último, se mata)')
    print('→ Regla: cada domingo corre este reporte y ajusta la semana.')

def main():
    os.makedirs(OUTBOX,exist_ok=True)
    cmd=sys.argv[1] if len(sys.argv)>1 else 'hoy'
    if cmd=='hoy': preparar(dt.date.today())
    elif cmd=='preparar': preparar(dt.date.fromisoformat(sys.argv[2]))
    elif cmd=='semana':
        d=dt.date.today()
        for k in range(7): preparar(d+dt.timedelta(days=k))
    elif cmd=='proximos':
        d=dt.date.today()
        for k in range(14):
            f=d+dt.timedelta(days=k); t,item,g=pieza_del_dia(f)
            print(f'{f.isoformat()} {["lun","mar","mié","jue","vie","sáb","dom"][f.weekday()]} {HORA[f.weekday()]} · {t:<9} · {g[:60]}')
    elif cmd=='registrar': registrar(sys.argv[2],*sys.argv[3:])
    elif cmd=='reporte': reporte()
    else: print(__doc__)

if __name__=='__main__': main()
