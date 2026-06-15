/* ============ Shell (header + nav), Dashboard, Perfil ============ */

function navKeyOf(view) {
  if (['ronda', 'nueva', 'detalle'].includes(view)) return 'ronda';
  if (['trainer', 'clubs'].includes(view)) return 'trainer';
  if (['perfil', 'clubs', 'friend'].includes(view)) return 'perfil';
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
      ${item('perfil', 'Perfil')}
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

/* Próximos eventos (para Inicio) */
function upcomingCard(u) {
  const tl = todayLocal();
  const up = (u.events || []).filter(e => e.date >= tl && e.type !== 'descanso').sort((a, b) => a.date.localeCompare(b.date)).slice(0, 4);
  if (!up.length) return '';
  const rows = up.map(e => `<button class="cal-ev ${e.type}" data-act="cal-goto" data-date="${e.date}" style="width:100%;text-align:left;cursor:pointer">
      <div class="r-main"><b>${esc(e.title || EV_LABEL[e.type])}</b><span>${EV_ICON[e.type]} ${calDateLabel(e.date)}${e.area ? ' · ' + esc(e.area) : ''}</span></div><span class="muted">›</span>
    </button>`).join('');
  return `<div class="card"><span class="label">📅 Próximos eventos</span>${rows}</div>`;
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
    </div>
    <div class="card">
      <span class="label">Tarjetas pasadas</span>
      ${rounds.slice(0, 5).map(r => { const s = Stats.roundStats(r); return `<button class="hist-row" data-act="round-detail" data-id="${r.id}">
        <div class="r-main"><b>${esc(r.course)}${r.partyId ? ' 🎉' : ''}</b><span>${fmtDate(r.date)} · ${s.holes} hoyos · ${s.putts} putts</span></div>
        <div class="r-side"><b>${s.score}</b><span>${fmtToPar(s.toPar)}</span></div>
      </button>`; }).join('')}
      <button class="btn sm ghost" data-act="nav" data-view="ronda" style="margin-top:12px">Ver todas las tarjetas →</button>
    </div>`;
}

/* ---- reparto de score: birdies / pares / bogeys… ---- */
function vScoreDist(agg) {
  const d = agg.scoreDist;
  if (!d || !d.total) return '';
  const tot = d.total;
  const cats = [
    { label: 'Birdie o mejor', n: d.eagle + d.birdie, col: 'var(--lime)' },
    { label: 'Par', n: d.par, col: '#57b15c' },
    { label: 'Bogey', n: d.bogey, col: '#ff9f43' },
    { label: 'Doble o peor', n: d.dbl, col: 'var(--danger)' },
  ];
  const pct = n => Math.round((n / tot) * 100);
  const seg = cats.filter(c => c.n > 0).map(c => `<span style="width:${(c.n / tot) * 100}%;background:${c.col}"></span>`).join('');
  const rows = cats.map(c => `<div class="sd-row">
    <span class="sd-dot" style="background:${c.col}"></span>
    <span class="sd-lab">${c.label}</span>
    <span class="sd-pct">${pct(c.n)}%</span>
    <span class="sd-n">${c.n}</span>
  </div>`).join('');
  return `<div class="card">
    <span class="label">Mi juego · ${agg.holesPlayed} hoyos${d.eagle ? ` · ${d.eagle} águila${d.eagle > 1 ? 's' : ''} 🦅` : ''}</span>
    <div class="sd-bar">${seg}</div>
    <div class="sd-list">${rows}</div>
  </div>`;
}

/* ---- carry de cada bastón de mi bolsa (editable aquí mismo) ---- */
function vBagEditor(u) {
  const clubs = u.clubs || {};
  const groupName = { largo: 'Maderas e híbridos', hierros: 'Hierros', wedges: 'Wedges' };
  const groupIc = { largo: 'club', hierros: 'tee', wedges: 'green' };
  const sections = ['largo', 'hierros', 'wedges'].map(g => {
    const tiles = CLUBS.filter(c => c.group === g).map(c => {
      const cc = clubC(clubs, c.id);
      return `<div class="carry-tile">
        <input class="carry-in" id="club-c-${c.id}" type="number" inputmode="numeric" placeholder="${CLUB_DEFAULT[c.id]}" value="${cc != null ? cc : ''}">
        <span>${esc(c.name)}</span>
      </div>`;
    }).join('');
    return `<p class="sd-sub">${golfIcon(groupIc[g])} ${groupName[g]}</p><div class="carry-grid">${tiles}</div>`;
  }).join('');
  return `<div class="card">
    <span class="label">${golfIcon('club')} Mi bolsa · carry por bastón</span>
    <p class="note" style="margin-top:0;margin-bottom:6px">Ajusta el carry de cada bastón (en yardas). Deja en blanco los que no uses.</p>
    ${sections}
    <button class="btn primary" data-act="save-clubs" style="margin-top:14px">Guardar carries</button>
  </div>`;
}

/* cabecera grande del perfil: nombre + hándicap + campo de casa */
function vPerfilHero(u) {
  const ini = String(u.name || '?').trim().split(/\s+/).map(w => w[0]).slice(0, 2).join('').toUpperCase();
  const home = (u.homeCourse && COURSES[u.homeCourse]) ? COURSES[u.homeCourse] : COURSES.campestre;
  const homeName = home.name.split(' · ')[0];
  const nRounds = myRounds().length;
  return `<div class="card phero">
    <div class="phero-row">
      <div class="phero-av">${esc(ini)}</div>
      <div class="phero-id">
        <h1 class="phero-name">${esc(u.name)}</h1>
        <p class="phero-course">${golfIcon('flag')} ${esc(homeName)}</p>
      </div>
    </div>
    <div class="phero-stats">
      <div><b>${fmtHcp(u.hcp)}</b><span>Hándicap</span></div>
      <div><b>${fmtHcp(u.goal)}</b><span>Meta</span></div>
      <div><b>${nRounds}</b><span>Rondas</span></div>
    </div>
  </div>`;
}

/* ============ Perfil (página) ============ */
function vPerfil() {
  const u = cur();
  const agg = Stats.aggregate(myRounds());
  return `<div class="sec-h"><h2>Tu perfil</h2></div>
    ${vPerfilHero(u)}
    ${agg ? vScoreDist(agg) : ''}
    ${vBagEditor(u)}
    <div class="card">
      <span class="label">Editar perfil</span>
      <div class="field"><label>Nombre</label><input id="p-name" value="${esc(u.name)}"></div>
      <div class="field-row">
        <div class="field"><label>Hándicap</label><input id="p-hcp" type="number" step="1" value="${esc(u.hcp)}"></div>
        <div class="field"><label>Meta</label><input id="p-goal" type="number" step="1" value="${esc(u.goal)}"></div>
      </div>
      <div class="field"><label>Campo de casa</label>
        <div class="chips">${COURSE_ORDER.map(id => `<button class="chip sm ${(u.homeCourse || 'campestre') === id ? 'on' : ''}" data-act="prof-campo" data-c="${id}">${esc(COURSES[id].name.split(' · ')[0].replace('Club ', '').replace(' Morelia', ''))}</button>`).join('')}</div>
      </div>
      <button class="btn primary" data-act="profile-save">Guardar cambios</button>
    </div>
    ${vLogros()}
    <div class="sec-h" style="margin-top:18px"><h2 style="font-size:16px">${golfIcon('flag')} Patrocinadores y ofertas</h2></div>
    <div class="card">
      <p class="note" style="margin-top:0;margin-bottom:8px">Ofertas de aliados (próximamente). Espacio para patrocinadores.</p>
      <div class="club-grid">
        <div class="club-tile"><b>Tu club</b><span class="ct-goal">Reserva tu tee time</span></div>
        <div class="club-tile"><b>Equipo</b><span class="ct-goal">Palos, bolas y más</span></div>
        <div class="club-tile"><b>Clases</b><span class="ct-goal">Encuentra un PRO</span></div>
        <div class="club-tile"><b>Anúnciate</b><span class="ct-goal">Tu marca aquí</span></div>
      </div>
    </div>
    <div class="sec-h" style="margin-top:18px"><h2 style="font-size:16px">Configuración</h2></div>
    <div class="card">
      <button class="btn ghost" data-act="seed-demo">Cargar datos de ejemplo</button>
      <button class="btn danger" data-act="wipe-mine">${V.wipeArm ? '¿Seguro? Toca otra vez para borrar tus rondas' : 'Borrar mis rondas y prácticas'}</button>
      <button class="btn" data-act="logout">Cerrar sesión</button>
      <p class="note">Cuenta local: ${esc(u.email)} · Tus datos viven solo en este dispositivo.</p>
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
