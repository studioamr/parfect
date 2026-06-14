/* ============ Vistas públicas: Landing + Auth ============ */

function vLanding() {
  return `<div class="shell no-nav fade-in">
    <div class="land-top">
      <span class="logo-word" style="font-weight:900;font-style:italic;letter-spacing:.18em;color:var(--lime);display:flex;align-items:center;gap:7px;font-size:15px">${logoMark(17)} PARFECT</span>
      <div class="links">
        <button class="btn sm ghost" data-act="go" data-view="login">Iniciar sesión</button>
        <button class="btn sm primary" data-act="go" data-view="signup">Empezar gratis</button>
      </div>
    </div>

    <div class="land-hero">
      <span class="badge">⛳ Golf · Stats · IA</span>
      <h1 class="land-h1">Deja de practicar.<br/><span class="lime">Empieza a mejorar.</span></h1>
      <p class="land-sub">PARFECT anota tu juego hoyo por hoyo, te dice en qué estás fallando y qué practicar para bajar tu hándicap. Y cuando juegas con amigos, lleva las apuestas por ti.</p>
      <button class="btn primary" data-act="go" data-view="signup">Crear cuenta gratis</button>
      <button class="btn ghost" data-act="go" data-view="login">Ya tengo cuenta</button>
      <div class="mini-stats">
        <div class="mini-stat"><b>4 toques</b><span>por hoyo</span></div>
        <div class="mini-stat"><b>Apuestas</b><span>con amigos</span></div>
        <div class="mini-stat"><b>IA</b><span>tu coach</span></div>
      </div>
    </div>

    <div class="land-sec">
      <h2 class="land-h2">Todo lo que necesitas<br/>para jugar mejor</h2>
      <p class="land-lead">Cinco herramientas que convierten tus números en mejoras de verdad.</p>

      <div class="card feat">
        <div class="f-ico">${ICONS.feat_round}</div>
        <h3>Anota tus rondas</h3>
        <p>Captura cada hoyo en 4 toques: salida, approach, juego corto y putts. En segundos.</p>
      </div>
      <div class="card feat">
        <div class="f-ico">${ICONS.feat_stats}</div>
        <h3>Tus números</h3>
        <p>Calles, greens, salvadas y putts, claros y a la mano. Sabes exactamente cómo juegas.</p>
      </div>
      <div class="card feat">
        <div class="f-ico">${ICONS.feat_ai}</div>
        <h3>Parfect Trainer</h3>
        <p>La IA revisa tus rondas, te dice por qué pierdes golpes y te arma ejercicios para tu caso.</p>
      </div>
      <div class="card feat">
        <div class="f-ico">${ICONS.feat_track}</div>
        <h3>Parfect Tracker</h3>
        <p>Anota cada práctica con tus aciertos y comprueba si de verdad estás mejorando.</p>
      </div>
      <div class="card feat">
        <div class="f-ico">${ICONS.social}</div>
        <h3>Parfect Party 🎉</h3>
        <p>Juega y apuesta con amigos: Skins, La corta, La larga y más. Cada quien anota desde su celular y la app saca las cuentas sola. Ideal para tu torneo.</p>
      </div>
    </div>

    <div class="land-sec">
      <h2 class="land-h2">Cómo funciona</h2>
      <p class="land-lead">Tres pasos, sin complicarte.</p>
      <div class="step">
        <span class="s-num">01</span>
        <div><h3>Anota tu ronda</h3><p>Captura cada hoyo en 30 segundos desde tu celular.</p></div>
      </div>
      <div class="step">
        <span class="s-num">02</span>
        <div><h3>Mira dónde fallas</h3><p>La app encuentra dónde se te van los golpes de más.</p></div>
      </div>
      <div class="step">
        <span class="s-num">03</span>
        <div><h3>Practica lo correcto</h3><p>Practica solo lo que te hace falta. Sin perder el tiempo.</p></div>
      </div>
    </div>

    <div class="land-cta">
      <span class="label">¿Listo para jugar tu mejor golf?</span>
      <h2 class="land-h2" style="margin-top:10px">Tu hándicap<br/><span class="lime">te está esperando.</span></h2>
      <p class="land-lead">Crea tu cuenta gratis y empieza hoy.</p>
      <button class="btn primary" data-act="go" data-view="signup">Empezar ahora</button>
    </div>

    <div class="land-foot">
      <span class="logo-word">${logoMark(15)} PARFECT</span>
      Tu app para mejorar en el golf y jugar con amigos.<br/>
      Tus datos se guardan en tu dispositivo.
    </div>
  </div>`;
}

/* ============ Auth ============ */

function vAuth(mode) {
  const vals = V.authVals || {};
  const err = V.err ? `<p class="form-err">${esc(V.err)}</p>` : '';
  if (mode === 'login') {
    return `<div class="shell no-nav fade-in">
      <button class="auth-back" data-act="go" data-view="landing">← Volver</button>
      <h1 class="auth-h">Hola de nuevo 👋</h1>
      <p class="auth-sub">Inicia sesión para seguir construyendo tu perfil de jugador.</p>
      <div class="field"><label>Email</label><input id="f-email" type="email" autocomplete="email" placeholder="tu@email.com" value="${esc(vals.email || '')}"></div>
      <div class="field"><label>Contraseña</label><input id="f-pass" type="password" autocomplete="current-password" placeholder="••••••••"></div>
      ${err}
      <button class="btn primary" data-act="login">Iniciar sesión</button>
      <p class="auth-alt">¿Aún no tienes cuenta? <button data-act="go" data-view="signup">Crear cuenta gratis</button></p>
    </div>`;
  }
  return `<div class="shell no-nav fade-in">
    <button class="auth-back" data-act="go" data-view="landing">← Volver</button>
    <h1 class="auth-h">Crea tu cuenta</h1>
    <p class="auth-sub">60 segundos y empiezas a registrar. Tus datos se guardan en este dispositivo.</p>
    <div class="field"><label>Nombre</label><input id="f-name" type="text" autocomplete="name" placeholder="¿Cómo te llamamos?" value="${esc(vals.name || '')}"></div>
    <div class="field"><label>Email</label><input id="f-email" type="email" autocomplete="email" placeholder="tu@email.com" value="${esc(vals.email || '')}"></div>
    <div class="field"><label>Contraseña</label><input id="f-pass" type="password" autocomplete="new-password" placeholder="Mínimo 4 caracteres"></div>
    <div class="field-row">
      <div class="field"><label>Hándicap actual</label><input id="f-hcp" type="number" inputmode="decimal" step="1" placeholder="ej. 18" value="${esc(vals.hcp ?? '')}"></div>
      <div class="field"><label>Meta</label><input id="f-goal" type="number" inputmode="decimal" step="1" placeholder="ej. 12" value="${esc(vals.goal ?? '')}"></div>
    </div>
    <label class="check"><input id="f-demo" type="checkbox" ${vals.demo ? 'checked' : ''}> Cargar datos de ejemplo para explorar la app</label>
    ${err}
    <button class="btn primary" data-act="signup">Crear cuenta gratis</button>
    <p class="auth-alt">¿Ya tienes cuenta? <button data-act="go" data-view="login">Iniciar sesión</button></p>
  </div>`;
}
