# PARFECT → App Store · guía de subida

**Estado: el proyecto iOS está COMPLETO y listo para firmar.** Lo que falta requiere tu Apple ID y tu tarjeta — nadie más puede hacerlo por ti (ni debe).

Qué hay aquí:
- `ios/` — proyecto Xcode nativo (Capacitor 8, sin CocoaPods, Swift Package Manager)
- `www/` — copia empaquetada de la app (regenerable con `./build-www.sh`)
- `appstore/` — 5 screenshots 1290×2796 listos para la ficha (iPhone 6.7")
- Ícono 1024 y splash de marca ya integrados en el proyecto
- Info.plist listo: solo retrato, permisos de fotos/cámara redactados, exención de cifrado declarada

---

## Los 3 pasos que SOLO tú puedes hacer

### 1. Prepara la Mac (una vez, ~1 hora en descargas)
- **Actualiza macOS** (Ajustes → General → Actualización de software). Estás en 14.4 y el Xcode que Apple exige para subir apps hoy pide algo más nuevo.
- **Instala Xcode** desde la Mac App Store (gratis, ~12 GB). Ábrelo una vez y acepta la licencia.

### 2. Cuenta de Apple Developer (una vez, $99 USD/año)
- Entra a https://developer.apple.com/programs/enroll/ con tu Apple ID.
- Inscríbete como individuo (o como empresa si ya tienes razón social — tarda más pero sale "PARFECT" como vendedor en vez de tu nombre).
- La verificación puede tardar de horas a un par de días.

### 3. Firma, archiva y sube (15 minutos cuando 1 y 2 estén listos)
1. Abre `native/ios/App/App.xcodeproj` en Xcode.
2. Selecciona el target **App** → pestaña **Signing & Capabilities** → marca "Automatically manage signing" → elige tu **Team**.
3. (Opcional pero recomendado) Conecta tu iPhone con cable y dale ▶ para probarla en tu teléfono real — esto funciona incluso antes de pagar la cuenta.
4. Arriba, selecciona destino **Any iOS Device (arm64)** → menú **Product → Archive**.
5. Al terminar: **Distribute App → App Store Connect → Upload** (todo en automático).
6. Entra a https://appstoreconnect.apple.com → Mis apps → ➕ Nueva app → pega la ficha de abajo → sube los screenshots de `native/appstore/` → selecciona el build que subiste → **Enviar a revisión**. La revisión tarda 1–3 días.

---

## La ficha (copiar y pegar en App Store Connect)

| Campo | Valor |
|---|---|
| Nombre | `PARFECT · Golf con datos` |
| Subtítulo | `Tu golf, medido.` |
| Bundle ID | `mx.parfect.app` (ya configurado en el proyecto) |
| Categoría | Deportes |
| Precio | Gratis |
| URL de soporte | `https://studioamr.github.io/parfect/` |
| URL de política de privacidad | `https://studioamr.github.io/parfect/legal.html` |
| Versión | 1.0.0 |

**Descripción:**

```
El golfista promedio juega la misma ronda por años porque no se mide. PARFECT convierte cada ronda y cada práctica en datos — y te dice exactamente qué entrenar para bajar tu hándicap.

⛳ SCORECARD INTELIGENTE
Captura tu ronda en 4 toques por hoyo: calle, green, putts y listo. Funciona sin señal — en el campo no hay internet y no importa.

📊 ANÁLISIS DE TU JUEGO
Fairways, greens en regulación, putts, up & down, birdies y dobles. PARFECT encuentra dónde estás dejando golpes y te lo dice en español claro.

🎯 ENTRENA LO QUE FALLAS
Plan de práctica basado en TUS números, con sesiones guiadas, tracker de ejercicios y coach con IA que te lee en tiempo real.

👥 JUEGA CON TUS CUATES
Rondas en grupo con marcador en vivo, tarjeta compartible, feed de amigos y trofeos por cada logro real.

🏌️ TU CLUB
Torneos con leaderboard en vivo, roster y academia juvenil con progreso medible y reporte a padres.

Hecho en México, en español de verdad, con los campos mexicanos precargados. Tu cuenta se guarda en la nube y tus datos son tuyos.
```

**Keywords (máx. 100 caracteres):**
```
golf,handicap,score,tarjeta,estadisticas,putt,green,campo,torneo,birdie,swing,practica
```

**Clasificación de edad:** en el cuestionario, todo "No", EXCEPTO si pregunta por concursos/competencias: las "apuestas" del modo party son un marcador social entre amigos — PARFECT no procesa ni custodia dinero. Decláralo como competencias entre usuarios; la app queda 4+ o 12+.

**App Privacy (cuestionario de privacidad):**
- Datos vinculados al usuario: Email, Nombre (para la cuenta) y Datos de uso (analítica propia, sin terceros).
- No hay tracking entre apps ni anuncios. No se vende ningún dato.

**Notas para el revisor de Apple (campo "Notes"):**
```
PARFECT is a Spanish-first golf stats app for the Mexican market. No login is
required to explore: on the home screen tap "Ver con datos de ejemplo" to browse
the full app with sample data, or create a free account with any email.
The app works fully offline (golf courses have no signal); the cloud account
syncs when online. The social "party" mode includes a friendly-bet SCOREBOARD
only — the app never processes or holds money.
```

---

## Cuando cambies la web app

El wrapper empaqueta una copia de la web. Para que la versión de App Store traiga lo último:

```sh
cd native
./build-www.sh          # copia index/js/css/assets frescos a www/
npx cap sync ios        # los mete al proyecto Xcode
# luego en Xcode: subir el número de versión → Product → Archive → Upload
```

---

## Honestidad sobre el riesgo de revisión

Apple a veces rechaza apps envueltas con la guideline **4.2 (funcionalidad mínima)**. PARFECT tiene buen caso: es local-first (funciona 100% sin internet, no es "un sitio en un webview"), con captura, análisis y entrenamiento reales. Si aun así llega un rechazo 4.2, el plan B ya está definido: v1.1 con push notifications nativas, share sheet y haptics (Capacitor los da casi gratis) y se reenvía. No es el fin de nada — es un ida y vuelta normal con Apple.
