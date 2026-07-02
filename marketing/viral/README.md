# Carruseles virales — TikTok / Instagram / Reels

Generados con `_build_viral.py` (mismo motor de marca que `../posts/`).
Estilo carrusel tipo "10 verdades / 5 formas de..." — el mismo formato que usan
cuentas de golf con millones de views (Scratch AI, Ryan Bartkiewicz, etc.),
pero con la marca y copy REALES de PARFECT.

**Nota de honestidad:** el CTA final manda al link (no hay badge falso de
App Store/Google Play — la app no está publicada en tiendas todavía).

## Carrusel 1 · `carrusel1-verdades/` (10 slides)
"8 verdades del golf que nadie te dice" — gancho educativo, cierra con Análisis IA.

**Caption sugerido:**
> 8 verdades del golf que nadie te dice 🏌️⛳ (la 5 me dolió)
> Las mido con PARFECT — anotas tu ronda y te dice en qué pierdes golpes de verdad.
> Link en bio, gratis.
> #golf #golfswing #golftips #hándicap #golfmexico #golfmorelia

## Carrusel 2 · `carrusel2-bajar-hcp/` (7 slides)
"5 formas de bajar tu hándicap más rápido" — consejos accionables, cierra con Rondas.

**Caption sugerido:**
> 5 formas de bajar tu hándicap más rápido (sin pegarle más lejos) 👇
> PARFECT te dice exactamente qué practicar según tus rondas reales.
> Gratis, link en bio.
> #golf #golftips #golflife #bajatuhandicap #golfmexico

## Carrusel 3 · `carrusel3-dato/` (2 slides)
Gancho de un solo dato — formato rápido para Reels/Stories.

**Caption sugerido:**
> El dato que más golpes te cuesta y ni te habías dado cuenta 👀
> Mide tu juego real con PARFECT. Link en bio.
> #golf #golfstats #golftips

## Carruseles 4–14 (81 slides más, 100 en total)
Estilo "EDITORIAL DE DATOS v3" (navy profundo + tipografía gigante + un acento
lima + retícula fina + trayectoria de bola + screenshots reales; serie PAPEL
editorial para quotes/memes/retos). Ver OPERACION.md:

| # | Carpeta | Tema |
|---|---|---|
| 4 | `carrusel4-mitos/` | 7 mitos del golf que te están deteniendo |
| 5 | `carrusel5-senales/` | 6 señales de que pierdes golpes sin darte cuenta |
| 6 | `carrusel6-tabla-hcp/` | Cómo juega cada hándicap (36 → 0) |
| 7 | `carrusel7-habitos/` | 5 hábitos de golfistas de un dígito |
| 8 | `carrusel8-errores-green/` | 7 errores que te cuestan golpes en el green |
| 9 | `carrusel9-preguntas/` | 5 preguntas después de cada ronda |
| 10 | `carrusel10-cambia/` | 6 cosas que cambian cuando mides tu golf |
| 11 | `carrusel11-amigos/` | 5 razones para llevar la cuenta con una app |
| 12 | `carrusel12-practica/` | 5 formas de aprovechar tu tiempo de práctica |
| 13 | `carrusel13-curiosos/` | 6 datos de golf que te van a sorprender |
| 14 | `carrusel14-no-bajas-90/` | 3 razones por las que no bajas de 90 |

Caption genérico que sirve para cualquiera de estos (ajusta el gancho de la 1a línea al título):
> [Título del carrusel] 🏌️⛳
> Los mido con PARFECT — anotas tu ronda y te dice en qué pierdes golpes de verdad.
> Gratis, link en bio.
> #golf #golftips #golfswing #hándicap #golfmexico #golfmorelia

Sugerencia de cadencia: publica 1 carrusel cada 2-3 días → **100 imágenes te dan ~5 semanas** de contenido diario/interdiario sin repetir.

## Cómo publicarlas (esto sí lo tienes que hacer tú)
No hay forma de subir esto a TikTok en automático desde aquí — TikTok requiere
tu sesión/cuenta y no hay integración para eso. Dos caminos:

1. **Manual (gratis):** abre TikTok/Instagram → crea post → sube las imágenes
   en orden (01, 02, 03…) como carrusel → pega el caption de arriba.
2. **Programado:** usa Buffer, Later o Metricool (tienen integración oficial
   con TikTok) — subes las carpetas una vez y programas 2-3 semanas de una sentada.

## Editar / regenerar
```bash
cd ~/claude/parfect/marketing/viral
python3 _build_viral.py
```
Cambia el copy en las listas `C1_TRUTHS` / `C2_TIPS` dentro de `_build_viral.py`.
