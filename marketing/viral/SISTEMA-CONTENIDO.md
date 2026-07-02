# Sistema de contenido PARFECT — pide y confirma

> **v3 (2026-07-01):** todo el diseño migró al estilo profesional
> "EDITORIAL DE DATOS" (navy+lima / papel editorial) y ahora existe el
> **departamento automático** (`_dept.py` + rutina diaria 9:47 am).
> Manual completo: `OPERACION.md`.

Tú NO tienes que escribir copy ni diseñar. Me pides un formato con un tema, yo lo
genero al instante con la marca, te lo enseño, y tú solo dices "va" o "cámbiale X".

Todo sale a `contenido/` (carruseles) y `contenido-extra/` (piezas sueltas), en
formato listo para subir. Recuerda: TikTok web solo acepta **video** → los carruseles
los convierto a MP4 + música (ya probado). Las piezas sueltas son para **Instagram/
stories** (foto) o también las vuelvo video si quieres.

---

## Los 7 formatos (pilares de contenido)

| Formato | Para qué sirve | Cómo me lo pides |
|---|---|---|
| **Carrusel** | Educativo, guarda-comparte (el que más crece) | "hazme un carrusel de [tema], 6 puntos" |
| **Meme** | Relatable, el que más comentarios/compartidos genera | "hazme un meme de [situación]" |
| **Stat / dato** | Gancho rápido, autoridad de datos | "hazme un stat: [número] [de qué]" |
| **Quote / mentalidad** | Inspiración, marca, guarda-comparte | "hazme un quote: [frase]" |
| **Mito vs realidad** | Educa rompiendo creencias, alto engagement | "hazme un mito: [mito] / [verdad]" |
| **Reto / challenge** | Comunidad, comentarios, retención | "hazme un reto: [nombre] con [pasos]" |
| **Feature de la app** | Conversión (muestra la app + link) | "hazme un feature de [pantalla]" |

## Calendario semanal sugerido (regla del pro: 1 post/día, no 10)
- **Lun** Carrusel (educativo fuerte para arrancar semana)
- **Mar** Meme (engagement)
- **Mié** Stat del día
- **Jue** Mito vs realidad
- **Vie** Feature de la app (empuja el link antes del finde)
- **Sáb** Quote / mentalidad
- **Dom** Reto de la semana

→ Con esto cubres los 7 días con variedad; el algoritmo premia constancia + formatos distintos, NO volumen alto de lo mismo.

## Ya listo en tu perfil (paquete de arranque)
- 3 quotes · 3 stats · 3 memes · 2 mitos · 1 reto · 2 features  →  `contenido-extra/`
- 14 carruseles (100 imágenes)  →  `contenido/`

## Cómo lo genero (interno, por si lo quieres correr tú)
```bash
cd ~/claude/parfect/marketing/viral
python3 _content_engine.py starter                       # paquete variado
python3 _content_engine.py meme "setup" "remate"         # un meme
python3 _content_engine.py stat "62%" "de GIR" "sub"     # un dato
python3 _content_engine.py quote "frase" "autor?"        # una quote
python3 _content_engine.py myth "mito" "verdad"          # mito/realidad
python3 _content_engine.py feature shot-rondas.png "Titulo" "beneficio"
python3 _content_engine.py challenge "RETO X" "meta" "paso1" "paso2"
python3 _build_viral.py                                   # los 14 carruseles
```

## El flujo contigo (pide → confirma)
1. Me dices: *"hazme 3 memes y 2 stats para esta semana"*.
2. Genero y te muestro las imágenes.
3. Tú: *"va"* (o *"cámbiale el texto de la 2"*).
4. Cuando toque subir: abro TikTok en Chrome, subo el video, le pongo música de la
   biblioteca de TikTok + caption, y **tú das el clic de Publicar** (ese paso es tuyo
   por seguridad — es lo que además te protege de que TikTok te marque como bot).
