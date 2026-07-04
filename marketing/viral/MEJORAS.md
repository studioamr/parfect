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

| 18 | updown | Probé fondo claro estilo landing ("DAY") → André: "horrible, regresa como estábamos" | **REVERTIDO a dark premium**. Regla: el mundo landing (cielo/campo claro) vive SOLO en el avatar del perfil; los videos son dark negro-verde + glow SIEMPRE. Se queda: gancho #11 bunker (la arena lee muy bien en dark) |

| 19 | updown v2 | André: cerrar CADA video mostrando la función REAL de la app acorde al tema | **app_outro()**: teléfono con captura VIVA de la app (marketing/shots), paneo lento, tap ripple lima, botón CTA pulsante + url; mapa tema→captura en TEORIA-50.md |

| 20 | debajo | André: el clip de la app duró muy poco | **app_outro v2**: ~11s (antes 6), pan COMPLETO de la pantalla y 2 capturas con deslizamiento entre ellas |

| 21 | 20min | André: que el demo SIMULE el uso (entrenamiento) | **app_outro v3 SIMULACIÓN**: capturas nuevas del flujo real de Entreno (analisis→tab Entreno→"30 min"→AI Coach) grabadas de la app viva (_shots2.swift); el tap lima DISPARA el cambio de pantalla con crossfade smoothstep |

| 22 | fairway | faltaba conclusión (descarga/waitlist) y los títulos aún con micro-lag | **poptext v3**: sin re-escalado de fuente (fade+rise subpíxel) = títulos mantequilla; **app_outro cierra SIEMPRE con tarjeta final**: DESCARGA + wordmark + botón lima + "únete a la waitlist en la landing" + url |

| 23 | uso01 | André pidió serie de TODOS los casos de uso | **Serie "ASÍ SE USA PARFECT"** (SERIE-USO.md, 12 eps): el video ES la app con PASOS numerados (chips lima) + taps causales + conclusión; capturas nuevas del flujo Nueva Ronda (12/13/14) |

| 24 | tanda día 1 | el MEME cayó en "Contenido en revisión" + Solo yo automático (patrón POV/texto) | vigilar el formato meme: si 2 seguidos caen en revisión, sustituirlo por 2º dato/quiz en la mezcla diaria; revisar mañana si TikTok lo liberó y regresarlo a "Todo el mundo" |

| 25 | uso03 | André: los videos artesanales (EP13-21/USO) gustan más que los de tanda auto | **Mezcla 2.0**: THEORYs de tanda = ARTESANALES (gancho único); +1 USO diario; lo auto solo quiz/dato/VF; el 2º dato sale de la mezcla |

| 25 | lag | André: la tanda auto se sintió simple; quiere MÁS diseño y elementos de golf (mostró el grid) | **Regla de mezcla 2.0**: los slots THEORY de cada tanda = ARTESANALES (diagramas ricos: dianas, greens, trayectorias, gancho único); teoria_auto solo de respaldo; +1 USO diario |

## Reglas vigentes (acumuladas)
1. Frame 1 = portada diseñada. Nunca abrir de negro.
2. Todo texto vive ≥ `dur_lectura`; labels entran a mitad de fase.
3. Un solo mensaje en pantalla por momento; ftxt garantiza el relevo suave.
4. Gancho de apertura NUEVO cada video (9 en catálogo, seguir inventando).
5. Música: Keinemusik ↔ Black Coffee alternando, track NO repetido.
6. Caption verificado en pantalla antes de Publicar.
7. Branding de la app en cada frame: wordmark + chip EP lima + @parfectapp.
8. NUNCA usar ✓/✗ tipográficos (tofu en Arial Black): color + texto, o dibujarlos.
9. TODO video cierra con app_outro() y la captura que corresponde al tema.
10. Después de publicar: anotar aquí la observación del día.
