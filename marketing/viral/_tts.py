#!/usr/bin/env python3
# ============================================================
# PARFECT · VOZ de trailer (Gemini TTS) + guiones por video
#   python3 _tts.py linea "texto" salida.wav      # una linea
#   python3 _tts.py video theory-putts30          # cues del guion
# Salida: _voz/<video>/cue-N.wav + cues.json (offsets en seg)
# ============================================================
import os, sys, json, base64, struct, time, urllib.request, urllib.error

HERE=os.path.dirname(os.path.abspath(__file__))
KEY=open(os.path.expanduser('~/.config/parfect/gemini.key')).read().strip()
MODEL=os.environ.get('TTS_MODEL','gemini-3.1-flash-tts-preview')
VOICE=os.environ.get('TTS_VOICE','Charon')   # grave, tipo narrador
ESTILO=('Narra en español mexicano con voz GRAVE y épica, estilo narrador '
        'de tráiler de Netflix, pero con ritmo ÁGIL, sin pausas largas: ')

GUIONES={
 'theory-putts30':[
   (0.3,'Un scratch hace treinta putts por ronda. ¿Tú cuántos?'),
   (4.6,'Hándicap diez, treinta y dos. Hándicap veinte, treinta y cuatro. Amateur promedio: treinta y seis.'),
   (9.9,'Esos seis golpes no están en tu swing. Están en tu putter, y no los estás contando.'),
   (16.2,'Parfect. Tu golf, medido.')],
 'theory-par5':[
   (0.3,'En el par cinco, la meta no es el eagle.'),
   (3.6,'La ruta del héroe: llegar en dos… y terminar en el agua. Doble bogey.'),
   (10.5,'La ruta del que sí baja: tres tiros aburridos… par fácil.'),
   (16.0,'Tres tiros aburridos le ganan a un tiro de héroe.'),
   (21.5,'Parfect. Tu golf, medido.')],
 'theory-bandera':[
   (0.3,'Deja de tirarle a la bandera. Te está costando golpes.'),
   (4.5,'Tu approach no es una línea… es una nube de resultados.'),
   (7.5,'Doce tiros a la bandera: cuatro fallan el green.'),
   (12.5,'Los mismos doce, al centro: once adentro.'),
   (17.5,'La bandera es marketing. El green es score. Parfect.')],
}

def pcm_a_wav(pcm, path, rate=24000):
    with open(path,'wb') as f:
        f.write(b'RIFF'+struct.pack('<I',36+len(pcm))+b'WAVEfmt '+
                struct.pack('<IHHIIHH',16,1,1,rate,rate*2,2,16)+
                b'data'+struct.pack('<I',len(pcm))+pcm)

def tts(texto, path):
    body={'contents':[{'parts':[{'text':ESTILO+'"'+texto+'"'}]}],
          'generationConfig':{'responseModalities':['AUDIO'],
            'speechConfig':{'voiceConfig':{'prebuiltVoiceConfig':{'voiceName':VOICE}}}}}
    req=urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent',
        data=json.dumps(body).encode(),
        headers={'Content-Type':'application/json','x-goog-api-key':KEY})
    for intento in range(5):
        try:
            d=json.load(urllib.request.urlopen(req,timeout=120))
        except urllib.error.HTTPError as e:
            if e.code==429: print('  (limite, espero 25s)'); time.sleep(25); continue
            raise
        try:
            part=d['candidates'][0]['content']['parts'][0]; break
        except (KeyError,IndexError):
            print('  (respuesta sin audio, reintento en 25s)', str(d)[:120]); time.sleep(25)
    else:
        raise RuntimeError('TTS fallo tras 5 intentos')
    data=base64.b64decode(part['inlineData']['data'])
    pcm_a_wav(data,path)
    print(' ->',path,f'({len(data)//48000:.0f}s aprox)' if data else '')
    return path

def video(nombre):
    cues=GUIONES[nombre]
    vd=os.path.join(HERE,'_voz',nombre); os.makedirs(vd,exist_ok=True)
    meta=[]
    for i,(t,txt) in enumerate(cues):
        p=os.path.join(vd,f'cue-{i}.wav')
        if not os.path.exists(p): tts(txt,p); time.sleep(22)
        meta.append({'t':t,'wav':p})
    json.dump(meta,open(os.path.join(vd,'cues.json'),'w'))
    print('cues listos:',vd)

if __name__=='__main__':
    if sys.argv[1]=='linea': tts(sys.argv[2],sys.argv[3])
    elif sys.argv[1]=='video': video(sys.argv[2])
