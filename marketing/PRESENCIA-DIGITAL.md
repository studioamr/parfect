# PARFECT · Puesta en línea 0–100

Datos de tu proyecto (ya en el código):
- **Supabase URL:** `https://xvkbkhyznwoaljjnsxue.supabase.co`
- **Callback de Google (para Supabase):** `https://xvkbkhyznwoaljjnsxue.supabase.co/auth/v1/callback`
- **URL actual de la app:** `https://studioamr.github.io/parfect/`
- **URL raíz limpia (opcional, si renombras el repo a `studioamr.github.io`):** `https://studioamr.github.io`

El código de "Continuar con Google" y email ya está desplegado. Faltan estos pasos en tus cuentas.

---

## A) Login con Google

### 1. Google Cloud Console — https://console.cloud.google.com
1. Crea un proyecto: **PARFECT**.
2. **APIs y servicios → Pantalla de consentimiento de OAuth** → tipo **External** →
   - Nombre de la app: **PARFECT**
   - Correo de soporte y de contacto: tu Gmail
   - Guarda. (Puedes dejarlo en "Testing" con tu correo agregado como usuario de prueba, o **Publicar** para que entre cualquiera.)
3. **APIs y servicios → Credenciales → Crear credenciales → ID de cliente de OAuth** → tipo **Aplicación web**:
   - **Orígenes de JavaScript autorizados:**
     - `https://studioamr.github.io`
   - **URI de redireccionamiento autorizados:**
     - `https://xvkbkhyznwoaljjnsxue.supabase.co/auth/v1/callback`
   - Crear → **copia el Client ID y el Client Secret**.

### 2. Supabase — https://app.supabase.com (tu proyecto)
1. **Authentication → Providers → Google** → **Enable** → pega **Client ID** y **Client Secret** → **Save**.
2. **Authentication → URL Configuration**:
   - **Site URL:** `https://studioamr.github.io/parfect/`
   - **Redirect URLs** (con `/**` al final):
     - `https://studioamr.github.io/parfect/**`

Listo: el botón "Continuar con Google" ya inicia sesión.

---

## B) Login con email/contraseña
- **Authentication → Providers → Email** debe estar **enabled** (viene activado).
- Para que entren al instante en demos: **Authentication → Providers → Email → desactiva "Confirm email"**.
  (Para producción seria, déjalo activado; ya manejamos el aviso de "confirma tu correo".)
- Usa el mismo **Site URL / Redirect URLs** del paso A2.

---

## C) URL del sitio
✅ Ya renombraste el usuario a **parfectapp**. Tu sitio vive en **https://studioamr.github.io/parfect/** (el deck en `/parfect/deck/`). El remoto de git ya apunta ahí.

¿Quieres la URL raíz sin `/parfect/` (**https://studioamr.github.io**)?
1. Repo → **Settings → General → Repository name** → renómbralo a **studioamr.github.io** → **Rename**.
2. Avísame y actualizo el remoto + los dominios en Google/Supabase a la URL raíz.

---

## D) Coach IA real (Birdie con IA)
Desde la carpeta `parfect/` con el CLI de Supabase:
```bash
supabase functions deploy coach --no-verify-jwt
supabase secrets set ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
```
(Guía completa en `supabase/functions/coach/README.md`.)

---

## E) Fotos/videos a la nube (Supabase Storage)
✅ **Ya está.** El bucket público **`round-media`** existe (lo creó la migración 03) y tanto las fotos de ronda como el feed apuntan a él. Al guardar una ronda con foto, la app la sube a `round-media/<tu-id>/<ronda>.jpg` y guarda la URL pública. (No necesitas crear el bucket `media`; eso era un nombre viejo, ya corregido en el código.)

---

## Checklist (estado verificado · jun 2026)
- [x] Supabase: tablas core (`profiles`, `rounds`, `practices`) — rondas sincronizan ✅
- [x] Supabase: tablas sociales (`posts`, `likes`, `comments`, `events`…) — feed listo ✅
- [x] Supabase: Email habilitado + autoconfirmación → login por correo funciona ✅
- [x] Storage: bucket público `round-media` (fotos/videos) ✅
- [ ] **Supabase: Google provider con Client ID/Secret** ← pendiente
- [ ] **Google Cloud: OAuth client** (origen `https://studioamr.github.io` + redirect `https://xvkbkhyznwoaljjnsxue.supabase.co/auth/v1/callback`) ← pendiente
- [ ] Supabase: Site URL + Redirect URLs (para el regreso de Google)
- [ ] **Desplegar Edge Function `coach` + secreto `ANTHROPIC_API_KEY`** (Birdie con IA real) ← pendiente
- [ ] Correr la migración `supabase/migrations/05_clubs.sql` (clubes en la nube) ← pendiente
- [x] Usuario renombrado a **parfectapp** → sitio en `https://studioamr.github.io/parfect/` ✅ (repo sigue "parfect"; renómbralo a `studioamr.github.io` si quieres URL raíz)
- [ ] (Después) Pasarela de pago para planes de club (Stripe/Mercado Pago)
