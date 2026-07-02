# PARFECT · Departamento de Marketing Automático

**Misión:** máxima exposición de PARFECT con 1 post diario de calidad
profesional, medido y ajustado cada semana. Tú solo arrastras un archivo
y das un clic; todo lo demás es automático.

---

## El concepto visual (v3 · "Editorial de Datos")

Analytics deportivo premium (referencia Whoop/Strava/Scratch):
- **Serie NAVY** — fondo azul-noche profundo, tipografía gigante, UN acento
  lima, retícula fina con esquinas lima, número gigante delineado, barra de
  progreso del carrusel, trayectoria de bola punteada, screenshots reales de
  la app con borde lima. Para: carruseles, stats, mitos, features.
- **Serie PAPEL** — editorial claro, serifa Georgia itálica, subrayado lima
  estilo marcador. Para: quotes, memes, retos.

Nada de personajes caricatura, nada de ruido. Si un diseño nuevo no se ve
como portada de revista deportiva, no sale.

## La máquina (`_dept.py`)

| Comando | Qué hace |
|---|---|
| `python3 _dept.py hoy` | Prepara la publicación de hoy completa |
| `python3 _dept.py semana` | Prepara los próximos 7 días |
| `python3 _dept.py proximos` | Muestra el plan de 14 días (fecha, hora, gancho) |
| `python3 _dept.py registrar <fecha> <vistas> <likes> <com> [comp]` | Guarda métricas |
| `python3 _dept.py reporte` | Qué formato escalar y cuál matar |

Cada publicación sale a `outbox/<fecha>-<tipo>-<slug>/` con:
`video.mp4` (vertical 1080×1920, transiciones + Ken Burns) · PNGs (para
Instagram) · `caption.txt` (gancho + CTA + hashtags rotados) · `CHECKLIST.md`
(hora sugerida, música sugerida, QC automático).

## Calendario editorial (rota solo, hora optimizada por día)

| Día | Formato | Hora (Morelia) | Por qué |
|---|---|---|---|
| Lun | Carrusel educativo | 19:30 | Arranque fuerte, prime time |
| Mar | Meme | 13:00 | Humor a la hora de comida |
| Mié | Stat del día | 19:30 | Autoridad de datos |
| Jue | Mito vs realidad | 13:00 | Debate → comentarios |
| Vie | Feature de la app | 17:00 | Empuja el link antes del finde |
| Sáb | Quote | 11:00 | Golfistas en el campo por la mañana |
| Dom | Reto de la semana | 18:00 | Comunidad, compromiso semanal |

## Ciclo de calidad e innovación (semanal, domingo)

1. `registrar` las métricas de los 7 posts (TikTok Studio → Analytics).
2. `reporte` → dice qué formato ESCALAR (2×/semana) y cuál REVISAR/matar.
3. Regla de innovación: **cada semana entra 1 experimento nuevo**
   (gancho distinto, serie visual nueva, tema nuevo) y se compara contra
   el promedio. Si gana, entra a la rotación; si pierde, fuera.
4. Los bancos de contenido viven arriba de `_dept.py` (MEMES, STATS,
   QUOTES, MYTHS, FEATURES, RETOS) — pídeme "agrega 10 memes nuevos"
   y los sumo al banco: la rotación los toma sola.

## Reglas fijas del departamento

- 1 post/día. Constancia > volumen. Nunca 10 posts de golpe.
- Música SIEMPRE de la biblioteca "Sin límites" de TikTok (sin copyright).
- Copy honesto: nada de badges falsos de App Store ni cifras inventadas.
- El clic final de Publicar y el login son de André (regla de seguridad).
- Cross-post: el mismo outbox sirve para TikTok (video) e Instagram (PNGs).

## División del trabajo

| Quién | Hace |
|---|---|
| **La máquina** (`_dept.py` + rutina diaria) | genera, diseña, escribe caption, QC, calendario, métricas |
| **Claude** (yo, en la rutina diaria) | corro la máquina, superviso calidad, pongo caption+música en TikTok, propongo experimentos |
| **André** | arrastra `video.mp4` al uploader, clic en Publicar, pasa las métricas del domingo |
