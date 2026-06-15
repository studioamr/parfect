/* ============ Shell (header + nav), Dashboard, Perfil ============ */

function navKeyOf(view) {
  if (['ronda', 'nueva', 'detalle'].includes(view)) return 'ronda';
  if (['trainer', 'clubs'].includes(view)) return 'trainer';
  if (['social', 'friend'].includes(view)) return 'social';
  if (view === 'strategy' || view === 'simulator') return 'inicio';
  return 'inicio';
}

function vShell(content) {
  const u = cur();
  const k = navKeyOf(V.view);
  const item = (key, label) =>
    `<button class="nav-item ${k === key ? 'on' : ''}" data-act="nav" data-view="${key}">${ICONS[key]}<span>${label}</span></button>`;
  return `<div class="shell">
    <div class="hdr">
      <span style="width:40px"></span>
      <span class="logo-word">${logoMark(16)} PARFECT</span>
      <button class="avatar-btn" data-act="profile-open" aria-label="Perfil">${esc(initials(u.name))}</button>
    </div>
    <div class="fade-in">${content}</div>
    <nav class="nav">
      ${item('inicio', 'Inicio')}
      ${item('ronda', 'Ronda')}
      <button class="nav-p" data-act="quick-round" aria-label="Iniciar ronda">P</button>
      ${item('trainer', 'Trainer')}
      ${item('social', 'Calendario')}
    </nav>
    ${V.profileOpen ? vProfile() : ''}
  </div>`;
}

function greeting() {
  const h = new Date().getHours();
  if (h < 12) return 'Buenos días';
  if (h < 20) return 'Buenas tardes';
  return 'Buenas noches';
}

/* Mini gráfica de tendencia de score (per-18, mejor=arriba) */
function progressChart(data) {
  const W = 300, H = 110, pad = 22;
  const min = Math.min(...data), max = Math.max(...data), span = Math.max(4, max - min);
  const x = i => data.length > 1 ? pad + i * (W - 2 * pad) / (data.length - 1) : W / 2;
  const y = v => pad + (v - min) / span * (H - 2 * pad);
  const pts = data.map((v, i) => [x(i), y(v)]);
  const line = pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(0)},${p[1].toFixed(0)}`).join(' ');
  const dots = pts.map(p => `<circle cx="${p[0].toFixed(0)}" cy="${p[1].toFixed(0)}" r="3.5" fill="#c9f73e"/>`).join('');
  const sign = v => (v >= 0 ? '+' : '') + v;
  return `<svg width="100%" viewBox="0 0 ${W} ${H}" role="img" aria-label="Tendencia de score">
    <path d="${line}" fill="none" stroke="#c9f73e" stroke-width="2.5" stroke-linejoin="round"/>${dots}
    <text x="${pad}" y="14" fill="#7c8a70" font-family="Inter,system-ui" font-size="10">${sign(data[0])} antes</text>
    <text x="${W - pad}" y="14" fill="#c9f73e" font-family="Inter,system-ui" font-size="11" font-weight="800" text-anchor="end">${sign(data[data.length - 1])} última</text>
  </svg>`;
}
function progressCard(u, rounds) {
  const data = rounds.slice(0, 8).reverse().map(r => { const s = Stats.roundStats(r); return Math.round(s.toPar * 18 / s.holes); });
  let chart, trend = '';
  if (data.length >= 2) {
    chart = progressChart(data);
    const half = Math.ceil(data.length / 2);
    const avgE = data.slice(0, half).reduce((a, b) => a + b, 0) / half;
    const avgL = data.slice(-half).reduce((a, b) => a + b, 0) / half;
    const d = Math.round(avgE - avgL);
    trend = d > 0 ? `📉 Vas mejorando: ~<b class="lime">${d}</b> golpes menos que tus primeras rondas.`
      : d < 0 ? `📈 Has subido ~${-d} golpes — toca apretar la práctica.` : `Estable en tus últimas rondas.`;
  } else {
    chart = `<p class="note">Registra 2+ rondas para ver tu tendencia.</p>`;
  }
  const gap = Math.max(0, Math.round(u.hcp - u.goal));
  return `<div class="card">
    <span class="label">📈 Seguimiento de progreso</span>
    ${chart}
    ${trend ? `<p class="note" style="margin:8px 0 6px">${trend}</p>` : ''}
    <p class="note" style="margin-bottom:0">HCP ${fmtHcp(u.hcp)} · meta ${fmtHcp(u.goal)}${gap > 0 ? ` · te faltan <b class="lime">${gap}</b> para tu meta` : ' · ¡meta alcanzada! 🎯'}</p>
  </div>`;
}

function vDashboard() {
  const u = cur();
  const rounds = myRounds();
  const agg = Stats.aggregate(rounds);
  const head = `<div class="greet">
    <p class="hi">${greeting()}</p>
    <h1>Hola, ${esc(u.name.split(' ')[0])}!</h1>
    <p class="hcp">HCP: ${fmtHcp(u.hcp)} · Meta ${fmtHcp(u.goal)}</p>
  </div>`;

  if (!agg) {
    return head + `<div class="card empty">
      <div class="e-ico">⛳</div>
      <h3>Tu perfil de jugador empieza aquí</h3>
      <p>Registra tu primera ronda — o carga datos de ejemplo para ver PARFECT en acción.</p>
      <button class="btn primary" data-act="quick-round">${logoMark(15)} Registrar mi primera ronda</button>
      <button class="btn ghost" data-act="seed-demo">Cargar datos de ejemplo</button>
    </div>`;
  }

  const radar = Stats.radarOf(agg);
  return head + `
    <div class="card">
      <span class="label">Perfil de habilidades</span>
      <div class="radar-wrap">${radarSVG(radar.labels, radar.values)}</div>
    </div>
    <div class="grid2">
      ${statCard(agg.fwPct.toFixed(0) + '%', 'Fairways', agg.fwPct)}
      ${statCard(agg.girPct.toFixed(0) + '%', 'GIR', agg.girPct)}
      ${statCard(agg.scrPct.toFixed(0) + '%', 'Up/Down', agg.scrPct)}
      ${statCard(agg.putts18.toFixed(0), 'Putts / Ronda', Stats.clamp((38 - agg.putts18) / 11 * 100, 0, 100))}
    </div>`;
}

/* ============ Perfil (sheet) ============ */
function vProfile() {
  const u = cur();
  return `<div class="overlay" data-act="profile-close">
    <div class="sheet" data-act="noop">
      <div class="grab"></div>
      <h2>Tu perfil</h2>
      <div class="field"><label>Nombre</label><input id="p-name" value="${esc(u.name)}"></div>
      <div class="field-row">
        <div class="field"><label>Hándicap</label><input id="p-hcp" type="number" step="1" value="${esc(u.hcp)}"></div>
        <div class="field"><label>Meta</label><input id="p-goal" type="number" step="1" value="${esc(u.goal)}"></div>
      </div>
      <div class="field"><label>Campo de casa</label>
        <div class="chips">${COURSE_ORDER.map(id => `<button class="chip sm ${(u.homeCourse || 'campestre') === id ? 'on' : ''}" data-act="prof-campo" data-c="${id}">${esc(COURSES[id].name.split(' · ')[0].replace('Club ', '').replace(' Morelia', ''))}</button>`).join('')}</div>
      </div>
      <button class="btn primary" data-act="profile-save">Guardar cambios</button>
      <button class="btn" data-act="go-clubs">🎒 Mis bastones y distancias</button>
      <div style="margin-top:18px">${vLogros()}</div>
      <button class="btn ghost" data-act="seed-demo" style="margin-top:14px">Cargar datos de ejemplo</button>
      <button class="btn danger" data-act="wipe-mine">${V.wipeArm ? '¿Seguro? Toca otra vez para borrar tus rondas' : 'Borrar mis rondas y prácticas'}</button>
      <button class="btn" data-act="logout">Cerrar sesión</button>
      <p class="note">Cuenta local: ${esc(u.email)} · Tus datos viven solo en este dispositivo.</p>
    </div>
  </div>`;
}
