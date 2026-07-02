# Calendario de publicación — ahora es AUTOMÁTICO

El calendario ya no se mantiene a mano: lo genera el departamento
(`_dept.py`) con rotación infinita de formatos y horas optimizadas por día.

```bash
cd ~/claude/parfect/marketing/viral
python3 _dept.py proximos    # ver los próximos 14 días (fecha, hora, gancho)
python3 _dept.py hoy         # preparar la publicación de hoy
```

Además hay una **rutina diaria programada** (9:47 am) que prepara el post
del día sola y te avisa qué arrastrar a TikTok. Los domingos corre el
reporte de métricas y propone el experimento de la semana.

Plan semanal fijo (rota el contenido, no el ritmo):

| Día | Formato | Hora |
|---|---|---|
| Lun | Carrusel educativo | 19:30 |
| Mar | Meme | 13:00 |
| Mié | Stat del día | 19:30 |
| Jue | Mito vs realidad | 13:00 |
| Vie | Feature de la app | 17:00 |
| Sáb | Quote | 11:00 |
| Dom | Reto de la semana | 18:00 |

Detalle completo del sistema: `OPERACION.md`.
