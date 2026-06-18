# AI Coach (Birdie) — Edge Function

El cerebro real de Birdie. La **llave secreta de Anthropic vive solo aquí**, en el
backend. El navegador (la app y la landing) llama a esta función con la anon key
de Supabase; la función llama a Claude con la llave secreta. Así la llave **nunca**
se filtra en GitHub Pages.

## Desplegar (una sola vez)

Necesitas el [CLI de Supabase](https://supabase.com/docs/guides/cli) y tu llave de
Anthropic (https://console.anthropic.com → API Keys).

Desde la carpeta `parfect/`:

```bash
# 1) enlaza tu proyecto (si no lo has hecho)
supabase link --project-ref xvkbkhyznwoaljjnsxue

# 2) sube la función (sin requerir login del usuario, para que Birdie
#    funcione también en la landing)
supabase functions deploy coach --no-verify-jwt

# 3) guarda la llave secreta de Anthropic en el backend (NUNCA en el navegador)
supabase secrets set ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

Listo. La app detecta sola la función y Birdie se vuelve IA real. Si la función no
está desplegada, Birdie sigue respondiendo con su guion local (no se rompe nada).

## Bajar el costo (opcional)

Por defecto usa **Claude Opus 4.8** (lo más capaz). Para un chatbot de alto volumen
puedes cambiar a **Haiku 4.5** (≈5x más barato) sin tocar código:

```bash
supabase secrets set ANTHROPIC_MODEL=claude-haiku-4-5
```

Modelos válidos: `claude-opus-4-8` (default), `claude-sonnet-4-6`, `claude-haiku-4-5`.

## Probar

```bash
curl -s -X POST \
  "https://xvkbkhyznwoaljjnsxue.supabase.co/functions/v1/coach" \
  -H "Authorization: Bearer <TU_ANON_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"¿Cómo registro una ronda?"}]}'
```

Debe responder `{"text":"..."}`.

## Notas de seguridad

- La **anon key** es pública (está en `js/config.js`) y sirve para invocar la
  función — es lo normal en Supabase, la protege RLS en las tablas.
- La **llave de Anthropic** es secreta y vive solo en `supabase secrets`.
- Endurecimiento futuro (opcional): quitar `--no-verify-jwt` para exigir usuario
  con sesión, y/o añadir un límite de uso por IP/usuario en la función.
