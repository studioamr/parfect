#!/usr/bin/env python3
# ============================================================
# PARFECT · RUTA A — pipeline Veo (cortos estilo Pixar "BETO")
# Genera los clips del GUION-PIXAR.md con la API de Gemini/Veo.
#   python3 _veo_pipeline.py test        # escena 1 de prueba
#   python3 _veo_pipeline.py escena 3    # una escena
#   python3 _veo_pipeline.py todas       # las 7
# Salida: clips-pixar/NN.mp4  (+ NN.json de metadata)
# Llave: ~/.config/parfect/gemini.key
# ============================================================
import os, sys, json, time, urllib.request, urllib.error

HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'clips-pixar'); os.makedirs(OUT,exist_ok=True)
KEY=open(os.path.expanduser('~/.config/parfect/gemini.key')).read().strip()
MODEL=os.environ.get('VEO_MODEL','veo-3.1-fast-generate-preview')
BASE='https://generativelanguage.googleapis.com/v1beta'

PERSONAJE=("A 35-year-old Mexican man named Beto, short dark hair, light stubble, "
    "athletic build, white golf polo and gray pants, expressive face, "
    "Pixar-style 3D animation, cinematic lighting, shallow depth of field.")

ESCENAS=[
 ("Beto sits alone in a golf cart at sunset, light rain, looking at a crumpled scorecard, sighs deeply, melancholic close-up, slow push-in.",
  "105 GOLPES. OTRA VEZ."),
 ("Club terrace: three friends laugh and raise beer glasses at a table; Beto in the background forces a smile, slow motion, warm evening light.",
  "SUS AMIGOS YA NI APOSTABAN CON ÉL."),
 ("Warm kitchen at night: his mother smiles from the dining table and asks him something; Beto pouring coffee freezes his smile, subtle awkward moment.",
  "¿CÓMO VA EL GOLF, MIJO?"),
 ("Beto lying in bed at night staring at the ceiling, blue phone light on his face, restless, intimate close shot.",
  "PRACTICABA MÁS QUE TODOS… Y NADA."),
 ("Close-up of Beto's hand holding a smartphone in the dark, screen glowing green, his tired face slowly turning intrigued, reflection of the screen in his eyes.",
  "HASTA QUE MIDIÓ SU JUEGO."),
 ("Beto on a putting green at golden sunrise, practicing short putts with determination, several balls lined up, energetic montage feel, dynamic camera.",
  "SU FUGA NO ERA EL SWING. ERA EL PUTT."),
 ("A golf ball drops into the hole, Beto raises his arms in triumph, his three friends run in and hug him, flag waving, joyful celebration, golden hour.",
  "89. PRIMERA VEZ ABAJO DE 90."),
]

def _post(url,body):
    req=urllib.request.Request(url,data=json.dumps(body).encode(),
        headers={'Content-Type':'application/json','x-goog-api-key':KEY})
    return json.load(urllib.request.urlopen(req,timeout=120))

def _get(url):
    req=urllib.request.Request(url,headers={'x-goog-api-key':KEY})
    return json.load(urllib.request.urlopen(req,timeout=120))

def generar(i, aspect='9:16'):
    prompt=f"{PERSONAJE} {ESCENAS[i][0]} Vertical 9:16 composition, no text, no captions, no subtitles."
    body={'instances':[{'prompt':prompt}],
          'parameters':{'aspectRatio':aspect}}
    try:
        op=_post(f'{BASE}/models/{MODEL}:predictLongRunning',body)
    except urllib.error.HTTPError as e:
        err=e.read().decode()[:400]
        if aspect=='9:16' and ('aspect' in err.lower() or 'INVALID' in err):
            print('  9:16 no soportado, reintento 16:9 (recorto al ensamblar)')
            return generar(i,aspect='16:9')
        print('  HTTP',e.code,err); return None
    name=op.get('name')
    print(f'  escena {i+1}: operacion {name.split("/")[-1][:12]}… ',end='',flush=True)
    for _ in range(120):
        time.sleep(10)
        st=_get(f'{BASE}/{name}')
        if st.get('done'):
            if 'error' in st: print('ERROR:',str(st['error'])[:300]); return None
            resp=st.get('response',{})
            vids=(resp.get('generateVideoResponse',{}).get('generatedSamples')
                  or resp.get('generatedVideos') or resp.get('videos') or [])
            if not vids:
                print('sin video en respuesta:',json.dumps(resp)[:300]); return None
            v=vids[0].get('video',vids[0])
            uri=v.get('uri') or v.get('videoUri')
            dest=os.path.join(OUT,f'{i+1:02d}.mp4')
            if uri:
                req=urllib.request.Request(uri,headers={'x-goog-api-key':KEY})
                open(dest,'wb').write(urllib.request.urlopen(req,timeout=300).read())
            elif v.get('bytesBase64Encoded'):
                import base64; open(dest,'wb').write(base64.b64decode(v['bytesBase64Encoded']))
            else:
                print('formato desconocido:',json.dumps(v)[:200]); return None
            json.dump({'sub':ESCENAS[i][1]},open(os.path.join(OUT,f'{i+1:02d}.json'),'w'))
            print(f'OK -> {dest} ({os.path.getsize(dest)//1_000_000}MB)')
            return dest
        print('.',end='',flush=True)
    print('timeout'); return None

if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'test'
    if cmd=='test': generar(0)
    elif cmd=='escena': generar(int(sys.argv[2])-1)
    elif cmd=='todas':
        for i in range(len(ESCENAS)):
            if not os.path.exists(os.path.join(OUT,f'{i+1:02d}.mp4')): generar(i)
    else: print(__doc__)
