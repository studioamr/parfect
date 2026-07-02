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
