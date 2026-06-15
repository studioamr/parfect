# PROMPT DE DISEÑO — PARFECT estilo igloo.inc

> Pégame este prompt cuando quieras que rediseñe PARFECT con el lenguaje visual de
> [igloo.inc](https://www.igloo.inc/). Está pensado para seguirse tal cual.

---

## Rol
Actúa como un diseñador UI/UX de clase mundial (nivel Awwwards "Site of the Day").
Vas a rediseñar **PARFECT**, una app de golf cuyo corazón es: **registrar rondas,
guardar tarjetas, entrenar y ver tu progreso**. El objetivo es que se sienta como un
producto premium internacional ("unicornio"), inmersivo y memorable, con el lenguaje
de igloo.inc adaptado al golf — sin perder funcionalidad ni rendimiento en celular.

## La esencia de igloo.inc (referencia a destilar)
- **Void negro mate** con profundidad infinita; sensación de "entrar" a un espacio.
- **Objeto 3D central** (en igloo: un témpano/cristal de hielo iridiscente) que **rota
  y se transforma con el scroll**, como protagonista de la marca.
- **Metáfora "iceberg"**: una marca esconde varias capas por debajo; **revelas más al
  descender**. El scroll cuenta una historia (scrollytelling).
- **Scroll suave** (tipo Lenis) + **animaciones encadenadas a waypoints** (tipo GSAP):
  cada sección "se ensambla" al entrar a viewport.
- **Tipografía grotesca de alto contraste**, mayúsculas finas, tracking amplio,
  jerarquía dramática (titulares enormes vs. cuerpo discreto).
- **Gradientes árticos** fríos pero legibles; **halos tipo aurora** en hover;
  microinteracciones "glassy" (vidrio).
- **Footer interactivo de partículas** que se reorganizan en figuras al hacer hover.
- **Performance impecable**: lazy loading, `prefers-reduced-motion`, LCP ~1s.

## Adaptación a PARFECT (golf)
- **Metáfora**: cambia el iceberg por **"tu juego en capas / el campo bajo la
  superficie"**. Al descender revelas capas: la punta = tu **hándicap**; debajo tus
  **números**; debajo tus **rondas recientes**; debajo tu **entrenamiento**.
- **Objeto 3D central** (elige uno y hazlo memorable):
  - una **bola de golf de cristal/iridiscente** que rota lento; o
  - un **green topográfico** (curvas de nivel) que se inclina con el scroll; o
  - la **bandera/hoyo** como tótem.
- Mantén identidad de golf, pero tratada **premium**: el verde calle / lima como
  *brillo*, no como neón plano.

## Dirección de arte
- **Fondo**: void casi negro verdoso (ej. `#050807`) con vignette radial sutil.
- **Acentos**: lima refinada (`#c9f73e`) para el brillo + un **frío menta/cian**
  (ej. `#7fe9c6`) para halos aurora y profundidad "helada".
- **Vidrio** (glassmorphism sutil) en cards flotantes; **bordes hairline**; sombras
  profundas y suaves; grano muy sutil opcional (sin recargar).
- Sin emojis: toda iconografía en SVG.

## Tipografía
- **Display**: grotesca de alto contraste o condensada para titulares gigantes (la
  marca, el hándicap). Mayúsculas, tracking amplio, peso fuerte.
- **Cuerpo/datos**: grotesca neutra legible (Inter u similar).
- **Números** (hándicap, scores, putts): protagonistas, tamaño dramático, tabulares.

## Movimiento (lo que define el estilo — cuídalo)
- **Scroll suave** (easing ligero en JS, o Lenis vía CDN si se permite).
- **Reveal por sección** con IntersectionObserver: fade + translate + des-blur,
  **encadenado** (stagger).
- **Parallax por capas** (ya existe `data-speed` en la landing).
- **Objeto central reactivo al scroll** (rota / escala / cambia viewBox).
- **Halos aurora** en hover (radial gradient que sigue el cursor).
- **`prefers-reduced-motion`**: todo estático y perfectamente legible.
- **Mobile primero**: pausar animaciones fuera de viewport (ya existe
  `pauseOffscreenSvgs`), cero jank, scroll fluido.

## Estructura propuesta (Inicio como "descenso")
1. **Hero**: marca + objeto 3D central + el **hándicap gigante** emergiendo.
2. **Capa 1 — Tus números**: rondas, putts, GIR que se ensamblan al entrar.
3. **Capa 2 — Rondas recientes**: tarjetas de vidrio tocables (abren el detalle).
4. **Capa 3 — Entrenamiento**: la siguiente sesión / drills clave.
5. **Footer**: partículas que forman una bandera/hoyo al hover + CTA.

## Componentes
- **Cards de vidrio** con hairline + glow sutil al hover.
- **Botones** pill con aurora hover y estados claros (hover/active/focus).
- **Data-viz premium**: anillos, sparklines finas, números display — **NO gifs
  cartoon**.
- **Scorecard elegante** (color-coded: birdie / par / bogey) sobre el void.

## Restricciones técnicas (PARFECT)
- **Vanilla HTML/CSS/JS** (sin framework). Lo "3D" se **simula** con SVG/Canvas +
  gradientes + capas + parallax (no WebGL pesado). Partículas en Canvas: mantener
  ligero.
- **Mobile-first**, GitHub Pages, cache-busting (`?v=N` en index.html + `parfect-vN`
  en sw.js), deploy = commit + push, verificar con curl hasta ver la versión nueva.
- **Mantener**: 3 campos reales (Campestre / Tres Marías / Altozano con sus
  pares/yardas), datos locales (localStorage), **i18n ES/EN**, **tema claro/oscuro**,
  sin emojis.
- **Accesibilidad**: contraste AA, `prefers-reduced-motion`, focus visible, safe-area
  iOS (notch + home indicator).
- **Performance**: LCP rápido, animaciones pausadas fuera de pantalla, nada que
  bloquee el scroll.

## Proceso
1. **Guardar el modelo actual antes de cambiar** (tag git, p. ej. ya existe
   `mvp-2026-base`).
2. Rediseñar primero **landing + Inicio** con este lenguaje; **enseñar una imagen
   (mockup)** antes de construir.
3. Tras aprobación, extender a **Perfil, Trainer y Tarjeta**.

## Tono de copy
Profesional de golf, premium, conciso, ligeramente aspiracional. Bilingüe ES/EN.

---

### Referencias
- Sitio: https://www.igloo.inc/
- Awwwards SOTD: https://www.awwwards.com/sites/igloo-inc
- Case study: https://www.awwwards.com/igloo-inc-case-study.html
- Desglose técnico (WebGL/cristales): https://www.webgpu.com/showcase/igloo-inc-procedural-crystals/
