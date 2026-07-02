# BITÁCORA DE MEJORA CONTINUA — línea THEORY (video a video)

Protocolo: después de CADA video se anota qué se observó y qué se cambia
para el siguiente. Nada se repite igual si algo se puede leer/ver mejor.

| # | Video | Observación | Mejora aplicada |
|---|---|---|---|
| 1-5 | bandera→putts30 | abrían con fondo vacío; texto estático | regla frame-1 portada; poptext |
| 6 | 3putts | textos no daban tiempo de leerse | `dur_lectura` (2.6s + 0.38s/palabra) en TODO |
| 7 | wedges | labels llegaban al final de la fase | labels a mitad de fase (t>0.5) |
| 8 | drive | textos se encimaban entre transiciones | `ftxt` con fade-in/out + stroke oscuro |
| 9 | 100y | gancho repetido aburre | rotación de ganchos (5 distintos) |
| 10 | ladocorto | — | gancho #5 split-wipe estrenado |
| 13 | putt1m | — | gancho #6 péndulo; gauges comparativos |
| 14 | bogey | caption no entró al subir (foco) | verificar caption con screenshot ANTES de publicar |
| 15 | practica | — | gancho #8 garabato; narrativa antes/después |
| 16 | tarjeta | fades lineales se sentían duros | **ftxt v2: smoothstep + deslizamiento 18px** (entra subiendo, sale flotando); poptext con alpha suave y overshoot 1.12 |

| 17 | brecha | el deslizamiento de ftxt se veía con lag (PIL mueve por píxeles ENTEROS a 30fps) | **ftxt v3 subpíxel**: el offset fraccional se reparte en 2 draws ponderados por alpha + recorrido corto (8px); fondo con gradiente+viñeta precalculados; **chrome v2 con branding de la app**: chip lima "THEORY · EP nn" + @parfectapp |

## Reglas vigentes (acumuladas)
1. Frame 1 = portada diseñada. Nunca abrir de negro.
2. Todo texto vive ≥ `dur_lectura`; labels entran a mitad de fase.
3. Un solo mensaje en pantalla por momento; ftxt garantiza el relevo suave.
4. Gancho de apertura NUEVO cada video (9 en catálogo, seguir inventando).
5. Música: Keinemusik ↔ Black Coffee alternando, track NO repetido.
6. Caption verificado en pantalla antes de Publicar.
7. Branding de la app en cada frame: wordmark + chip EP lima + @parfectapp.
8. Después de publicar: anotar aquí la observación del día.
