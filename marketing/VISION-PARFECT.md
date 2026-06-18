# PARFECT — Recapitulación, visión y ruta a una valuación de millones

> Documento estratégico. Estado del producto a junio 2026.

---

## 1. Qué es PARFECT hoy (recapitulación)

PARFECT es una **app de golf (PWA instalable) en español** que combina tres cosas que normalmente viven en apps separadas:
**analítica de tu juego + un coach con IA que te dice qué entrenar + una capa social/competitiva** (ligas, torneos, tee times). Funciona 100% local (tus datos en tu dispositivo) y ya tiene **backend en Supabase** para multijugador real.

~10,450 líneas de código, sin framework pesado, cargando rápido. Pilares construidos:

**Tracker (tu tarjeta)**
- Registro de rondas 9/18 hoyos sobre campos reales (Campestre Morelia, Tres Marías, Altozano) hoyo por hoyo: fairways, greens, up & down, putts, penales.
- Scorecard pro (OUT/IN/total), resumen de ronda con escena por hora del día.

**Motor de métricas (Stats)**
- Estadísticas nivel pro: %fairways, GIR, scrambling, putts/ronda, 3-putts, reparto de score (eagle→doble), normalización a 18 hoyos, radar de 6 ejes, tendencia.

**Análisis IA (coach)**
- Diagnóstico que cruza tus rondas y te dice **exactamente dónde pierdes golpes**, en orden de prioridad, contra metas por hándicap.

**Entrenamiento**
- **AI Coach**: arma tu sesión según el tiempo que tengas y tus puntos débiles (con resumen del diagnóstico antes).
- **Entrenamiento libre**: cronómetro por bastón o por ejercicio de una **biblioteca de 50 drills**.
- Historial de entrenamientos y registro persistente.

**Academia**
- 18 niveles tipo trivia (estilo Duolingo) para aprender golf, con desbloqueo progresivo.

**Gamificación**
- Rangos por hándicap, trofeos míticos por metas (% pares, birdies, scrambling…), logros.

**Social / comunidad**
- Feed de amigos con tarjetas de ronda, **Liga de amigos** (ranking), **Torneo en juego**, **próximos eventos / tee times**, party con apuesta opcional por modalidad.
- Portal discreto de **coaches y clubes**.

**Marca y activos reales**
- Landing premium (cielo dinámico, escena de campo animada), reseñas, premios, **carrusel de patrocinadores reales** (Mercedes-Benz, Titleist, Aeroméxico, TaylorMade, Chandon, Electrolit, Federación Mexicana de Golf…).
- **Fotos reales** de un torneo real (UNIMO / Universidad Montrer) y narrativa **"del torneo local a una beca afuera"** (ángulo juvenil).
- Asistente **Birdie** (chatbot de ayuda) en app y landing.

**Infraestructura**
- Supabase (auth, feed, eventos, coach) con migraciones SQL + RLS; modo local de respaldo.
- PWA instalable, i18n es/en, temas claro/oscuro, selector de entorno del campo.
- **Suite de pruebas** (26/26 verde) sobre la lógica central.

**Traducción para un inversionista:** ya existe un producto funcional, con backend, con relaciones reales de clubes y marcas, y un nicho claro (golf hispano + cantera juvenil). No es una idea: es tracción incipiente.

---

## 2. Visión extensa

### El problema
El golfista promedio **practica sin saber qué entrenar** y mide su mejora solo con el score final. Las herramientas serias (Arccos, Shot Scope) son caras, en inglés, dependen de sensores/hardware y se sienten de laboratorio. Las sociales (18Birdies, TheGrint) no enseñan a mejorar. **Nadie une "entiende tu juego + dime qué hacer + compite con tus amigos" en español y sin fricción.**

### Por qué ahora
- El golf vive un boom post-pandemia (jugadores nuevos, más jóvenes, más mujeres).
- LatAm y el mercado **hispano de EE. UU.** están desatendidos en software de golf.
- La IA hace por fin viable un "coach" creíble y barato a escala.

### Mercado (honesto)
- **Global:** decenas de millones de golfistas activos; el software de golf de consumo es un mercado de cientos de millones de USD y creciendo.
- **México:** chico pero **premium** (~200 campos, audiencia de alto poder adquisitivo, marcas dispuestas a patrocinar — ya lo demostraste).
- **La cuña real:** México → LatAm → hispano-US. Empiezas donde tienes ventaja injusta (Morelia, clubes, torneos) y te expandes.
- **Capa juvenil/becas:** un ángulo emocional y de retención brutal (padres, academias, federación, universidades).

### Posicionamiento
> **"El Strava + Whoop del golf, en español, con coach IA."**
Medición + comunidad (Strava) + diagnóstico accionable y hábito (Whoop), enfocado primero al mundo hispano y a la cantera juvenil.

### Foso competitivo (lo que te hace difícil de copiar)
1. **Datos propietarios** de juego por golfista (mientras más rondas, mejor el coach → se vuelve insustituible).
2. **Network effects locales**: ligas, torneos y tee times atan a comunidades enteras de un club.
3. **Relaciones B2B ya iniciadas**: clubes, marcas, una universidad con torneo propio.
4. **Capa juvenil/becas**: nadie más la tiene y crea lealtad multi-año.
5. **IA coach** entrenada con la taxonomía de drills y métricas propias.

### Modelo de negocio (múltiples motores)
1. **Freemium → PARFECT Pro** (suscripción): coach IA ilimitado, analítica avanzada, planes, sin límites. ~US$5–9/mes.
2. **B2B Clubes (SaaS)**: panel para clubes/academias — torneos, ligas, leaderboard en vivo, base de socios. Contrato recurrente anual (el ingreso que más sube la valuación).
3. **Marcas / patrocinios**: torneos y retos patrocinados (ya tienes Mercedes, Chandon, etc.).
4. **Marketplace de coaches**: clases, comisión por reserva.
5. **Datos agregados / insights** (a futuro, con privacidad): tendencias de juego para marcas y campos.
6. **Hardware/afiliación** (más adelante): bolas, wedges, e-commerce afiliado.

---

## 3. Hacia dónde tiene que ir (ruta a "millones de USD" de valuación)

### Cómo se valúan estas apps (realista)
- Una valuación de **millones de dólares** se logra por **una de dos vías**: (a) **tracción medible** (usuarios activos + retención + primeros ingresos) que justifique una ronda **pre-seed/seed**, o (b) **ARR** (ingreso recurrente anual) con múltiplos típicos de **5–10× ARR** para software de consumo, más si el crecimiento es alto.
- En la práctica para ti: con un buen producto (ya lo tienes) + **señales de retención y primeros clientes B2B**, una ronda pre-seed/seed puede valuar el proyecto en el rango de **US$2–8M**. Llegar a **decenas de millones** exige ARR real y crecimiento.

### Las métricas que un inversionista te va a pedir
- **Retención** D1 / D7 / D30 (lo #1). Una app de hábito necesita D30 sano.
- **WAU/MAU** y rondas registradas por usuario/mes.
- **Conversión a Pro** y **ARPU**; **churn**.
- **B2B**: nº de clubes, contrato anual promedio, retención logo.
- **CAC vs LTV** y crecimiento orgánico (viralidad de torneos/ligas).

### Fases con objetivos

**Fase 0 — Validación (ahora → 3 meses)**
- Meta: **50 → 1,000 usuarios reales en Morelia**, midiendo retención de verdad.
- Cierra el loop: registrar ronda → ver diagnóstico → entrenar → mejorar score (el "momento ajá").
- Instrumenta analítica de producto (eventos, embudos). Hoy vuelas a ciegas.
- Corre 2–3 **ligas/torneos reales** en clubes (ya tienes la relación). Cada torneo = adquisición masiva + retención.
- Entregable inversor: gráfica de retención + testimonios + 1 club piloto.

**Fase 1 — Tracción / Seed (3 → 12 meses)**
- **5k–20k usuarios**, primeros ingresos: **Pro** lanzado + **3–5 clubes B2B** pagando.
- IA **real** (LLM con la API de Claude) para el coach y Birdie — un diferenciador demostrable.
- Pagos (Stripe), hándicap/ranking confiable, anti-trampa en scores.
- Apps en las tiendas (wrapper de la PWA) para distribución y credibilidad.
- Valuación objetivo: **~US$3–8M** pre con buen crecimiento + equipo.

**Fase 2 — Escala / Series A (12 → 30 meses)**
- **100k+ usuarios**, **ARR US$1–3M** (Pro + B2B + marcas), expansión a LatAm y hispano-US.
- Integraciones: hándicap oficial, wearables, GPS/mapa de campos.
- Programa juvenil/becas institucionalizado (federaciones, universidades).
- Valuación objetivo: **US$20–50M**.

**Fase 3 — Liderazgo regional (30+ meses)**
- Estándar del golf hispano; datos + marketplace + posibles dispositivos.
- **ARR US$10M+** → valuación **US$100M+**.

### Palancas que más suben la valuación (en orden)
1. **Retención** demostrada (todo lo demás depende de esto).
2. **Ingreso recurrente B2B** (clubes) — contratos anuales = múltiplo alto.
3. **Network effects** (ligas/torneos que crecen solos).
4. **IA real** + datos propietarios (narrativa defensible).
5. **Equipo** (un fundador que ejecuta rápido — ya lo demuestras — + un técnico/comercial).

### Qué construir técnicamente para soportarlo
- Backend robusto (Supabase ya); **auth, sync offline, anti-cheat de scores**.
- **Coach IA real** (API de Claude) sobre tus métricas y biblioteca de drills.
- **Panel B2B para clubes** (torneos, socios, leaderboard en vivo, cobros).
- **Pagos** (Stripe / suscripciones), **hándicap** confiable, **GPS de campos**.
- Integraciones: wearables, hándicap oficial, e-mail/push, analítica de producto.

### Riesgos y mitigación
- **Mercado mexicano chico** → la tesis es LatAm + hispano-US desde el inicio; México es la pista de despegue.
- **Retención del golfista casual** → hábito vía ligas/torneos y recordatorios, no solo stats.
- **Dependes de hardware (Arccos/Shot Scope) compiten)** → tú ganas en captura manual rápida + IA + comunidad + idioma + precio.
- **Monetización** → B2B clubes da ingreso temprano y estable mientras crece el consumer.

### Próximos 90 días (acciones concretas)
1. **Instrumentar analítica** de producto (sin esto no hay historia de inversión).
2. Lanzar **2 ligas/torneos** en clubes de Morelia y medir retención.
3. Activar **PARFECT Pro** (aunque sea precio simbólico) para probar disposición a pagar.
4. Firmar **1 club piloto B2B**.
5. Conectar el **coach IA real** (API de Claude) — es tu demo estrella.
6. Armar un **deck** de 10 láminas con la gráfica de retención + activos (clubes, marcas, torneo UNIMO, fotos reales).

---

### Una línea para el pitch
> *"PARFECT convierte cada ronda en un plan de mejora con IA y enlaza a los golfistas con su club y su comunidad — empezando por el mercado hispano que nadie atiende y la cantera juvenil que crea lealtad de por vida."*
