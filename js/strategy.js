/* ============ Estrategia de campo (beta) — Club de Golf Campestre Morelia ============
   Datos del mapa oficial del club (par/yardas reales, 9 hoyos · par 72).
   Cada hoyo se recrea como dibujo propio fiel al trazo real (dogleg, agua, green).
   La zona de aterrizaje se calcula con la dispersión real del jugador. */

const CAMP_COURSE = { name: 'Club Campestre Morelia', sub: '9 hoyos · Par 72 · plano' };

/* yds = mesa azul (campeonato). dog: left|right|straight. hazard: water/bunker + lado */
const CAMP_HOLES = [
  { n: 1, par: 5, yds: 503, dog: 'straight', hazard: 'bunker-right', desc: 'Par 5 largo y plano, calle amplia.' },
  { n: 2, par: 5, yds: 550, dog: 'right', hazard: 'bunker-left', desc: 'El par 5 más largo; coloca dos golpes.' },
  { n: 3, par: 3, yds: 174, dog: 'straight', hazard: 'water-right', desc: 'Par 3 corto con laguna a la derecha del green.' },
  { n: 4, par: 4, yds: 405, dog: 'left', hazard: 'bunker-right', desc: 'Dogleg suave a la izquierda.' },
  { n: 5, par: 3, yds: 201, dog: 'straight', hazard: 'bunker-left', desc: 'El par 3 más largo; toma palo de más.' },
  { n: 6, par: 4, yds: 432, dog: 'right', hazard: 'bunker-left', desc: 'Par 4 largo; coloca el drive a la derecha.' },
  { n: 7, par: 5, yds: 529, dog: 'left', hazard: 'water-right', desc: 'Par 5 alcanzable en dos si pegas recto.' },
  { n: 8, par: 3, yds: 176, dog: 'straight', hazard: 'water-left', desc: 'Par 3 sobre el agua a la izquierda.' },
  { n: 9, par: 4, yds: 407, dog: 'right', hazard: 'bunker-right', desc: 'Par 4 de cierre hacia la casa club.' },
];

function clubForDistance(user, yds) {
  const clubs = (user && user.clubs) || {};
  const bag = CLUBS.map(c => ({ name: c.name, carry: clubs[c.id] != null ? clubs[c.id] : CLUB_DEFAULT[c.id] }))
    .filter(c => c.carry);
  if (!bag.length) return null;
  bag.sort((a, b) => Math.abs(a.carry - yds) - Math.abs(b.carry - yds));
  return bag[0];
}

function strategyRecommend(hole, user, agg) {
  const fw = agg ? agg.fwPct : 50;
  const width = Math.round(Math.max(20, Math.min(60, 60 - (fw - 35) * 0.9)));
  const m = (agg && agg.missTee) || { izq: 0, der: 0 };
  const bias = m.der > m.izq * 1.2 ? 'der' : m.izq > m.der * 1.2 ? 'izq' : 'centro';
  const hz = hole.hazard || '';

  if (hole.par === 3) {
    const club = clubForDistance(user, hole.yds);
    let aim = 'Centro del green';
    if (hz.includes('right')) aim = 'Centro-izquierda';
    if (hz.includes('left')) aim = 'Centro-derecha';
    const reason = hz.includes('water')
      ? `Par 3 de ${hole.yds} yds. Apunta al centro: el agua castiga el lado ${hz.includes('right') ? 'derecho' : 'izquierdo'}.`
      : `Par 3 de ${hole.yds} yds. Apunta al centro del green y juega a dos putts.`;
    return { par3: true, club: club ? club.name : 'Hierro', leave: hole.yds, aim, reason, width, bias };
  }

  const carry = (user.clubs && user.clubs.dr) || CLUB_DEFAULT.dr;
  const dl = hole.dog;
  let club, landing, aim, reason;
  const tight = width >= 46 && ((dl === 'left' && bias === 'der') || (dl === 'right' && bias === 'izq'));
  if (tight) {
    club = 'Madera 3'; landing = carry - 35;
    aim = dl === 'left' ? 'Lado interior izquierdo' : 'Lado interior derecho';
    reason = `Tu dispersión (~${width} yds) no perdona en este dogleg. Coloca la salida con madera al lado interior.`;
  } else {
    club = 'Driver'; landing = carry;
    aim = bias === 'der' ? 'Centro-izquierda' : bias === 'izq' ? 'Centro-derecha' : 'Centro de la calle';
    reason = hole.yds >= 480
      ? `Par ${hole.par} de ${hole.yds} yds. Saca distancia con el driver; te quedará un segundo golpe largo.`
      : `Tu dispersión cabe en la calle. Driver y tendrás un approach corto.`;
  }
  const leave = Math.max(hole.yds - landing, 0);
  const approach = clubForDistance(user, leave);
  return { par3: false, club, landing, leave, aim, reason, width, bias, approach: approach ? approach.name : null };
}

function bez(t, p0, c, p2) {
  const u = 1 - t;
  return u * u * p0 + 2 * u * t * c + t * t * p2;
}

function holeStrategySVG(hole, rec) {
  const W = 360, H = 470;
  const par3 = hole.par === 3;
  const gx = hole.dog === 'left' ? 124 : hole.dog === 'right' ? 236 : 180;
  const gy = 104;
  const Cx = par3 ? 180 : (hole.dog === 'left' ? 232 : hole.dog === 'right' ? 128 : 180);
  const Cy = 262;
  const tee = [180, 446];
  const fairD = `M180,446 Q ${Cx},${Cy} ${gx},${gy}`;
  const fairW = par3 ? 40 : 74;

  const t = par3 ? 1 : Math.max(0.15, Math.min(0.82, rec.landing / hole.yds));
  const lx = par3 ? gx : bez(t, 180, Cx, gx);
  const ly = par3 ? gy : bez(t, 446, Cy, gy);
  const lrx = Math.max(24, Math.min(56, rec.width));
  const lry = lrx * 0.58;

  const hz = hole.hazard || '';
  let hazSVG = '';
  if (hz) {
    const side = hz.includes('left') ? -1 : 1;
    const hzx = gx + side * 54, hzy = gy + 30;
    const water = hz.includes('water');
    hazSVG = `<ellipse cx="${hzx}" cy="${hzy}" rx="${water ? 30 : 24}" ry="${water ? 19 : 14}" fill="${water ? '#2f7fa6' : '#ddcb8c'}"/>
      ${water ? `<ellipse cx="${hzx - 5}" cy="${hzy - 4}" rx="${17}" ry="9" fill="#3f96bd" opacity="0.7"/>` : ''}
      <rect x="${hzx - 32}" y="${hzy - 44}" width="64" height="19" rx="9.5" fill="${water ? '#16323f' : '#3a2a16'}" stroke="${water ? '#3f96bd' : '#e0a25a'}"/>
      <text x="${hzx}" y="${hzy - 30}" fill="${water ? '#7fc3df' : '#e0a25a'}" font-family="Inter,system-ui,sans-serif" font-size="10" font-weight="800" text-anchor="middle">${water ? 'Agua' : 'Bunker'}</text>`;
  }

  const recRoute = par3 ? `M180,446 L${gx},${gy}` : `M180,446 L${lx.toFixed(0)},${ly.toFixed(0)} L${gx},${gy}`;
  const aggRoute = par3 ? '' : `M180,446 L${(hole.dog === 'left' ? gx + 18 : hole.dog === 'right' ? gx - 18 : 180)},250 L${gx},${gy}`;

  return `<svg width="100%" viewBox="0 0 ${W} ${H}" role="img" aria-label="Estrategia hoyo ${hole.n}">
    <rect x="0" y="0" width="${W}" height="${H}" rx="18" fill="#0a0f08" stroke="#1d2914"/>
    <path d="${fairD}" fill="none" stroke="#2f6b39" stroke-width="${fairW}" stroke-linecap="round"/>
    <path d="${fairD}" fill="none" stroke="#3a8043" stroke-width="${fairW - 26}" stroke-linecap="round" opacity="0.5"/>
    <ellipse cx="${gx}" cy="${gy}" rx="44" ry="31" fill="#57b15c" stroke="#2f6b39" stroke-width="2"/>
    <circle cx="${gx + 6}" cy="${gy + 2}" r="3.2" fill="#0a0f08"/>
    <line x1="${gx + 6}" y1="${gy + 2}" x2="${gx + 6}" y2="${gy - 38}" stroke="#eef3e6" stroke-width="2"/>
    <path d="M${gx + 6},${gy - 38} L${gx + 22},${gy - 33} L${gx + 6},${gy - 28} Z" fill="#c9f73e"/>
    ${hazSVG}
    <ellipse cx="${lx.toFixed(0)}" cy="${ly.toFixed(0)}" rx="${(lrx + 14).toFixed(0)}" ry="${(lry + 9).toFixed(0)}" fill="#c9f73e" opacity="0.08"/>
    ${aggRoute ? `<path d="${aggRoute}" fill="none" stroke="#e0a25a" stroke-width="2" stroke-dasharray="2 7" opacity="0.7"/>` : ''}
    <path d="${recRoute}" fill="none" stroke="#c9f73e" stroke-width="3" stroke-dasharray="3 6"/>
    <ellipse cx="${lx.toFixed(0)}" cy="${ly.toFixed(0)}" rx="${lrx.toFixed(0)}" ry="${lry.toFixed(0)}" fill="#c9f73e" opacity="0.16" stroke="#c9f73e" stroke-width="1.5" stroke-dasharray="4 4">
      <animate attributeName="opacity" values="0.10;0.24;0.10" dur="2.4s" repeatCount="indefinite"/>
    </ellipse>
    <circle r="5.5" fill="#ffffff">
      <animateMotion dur="3.2s" repeatCount="indefinite" path="${recRoute}"/>
      <animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.06;0.5;0.85;1" dur="3.2s" repeatCount="indefinite"/>
    </circle>
    <rect x="169" y="440" width="22" height="8" rx="2" fill="#9ab07f"/>
    <text x="180" y="463" fill="#9ab07f" font-family="Inter,system-ui,sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">TEE</text>
    ${!par3 ? `<rect x="${(lx - 50).toFixed(0)}" y="${(ly - lry - 25).toFixed(0)}" width="100" height="21" rx="10.5" fill="#c9f73e"/>
      <text x="${lx.toFixed(0)}" y="${(ly - lry - 10).toFixed(0)}" fill="#0a0f08" font-family="Inter,system-ui,sans-serif" font-size="11" font-weight="800" text-anchor="middle">Tu zona ideal</text>` : ''}
  </svg>`;
}

function vStrategy() {
  const u = cur();
  const agg = Stats.aggregate(myRounds());
  const idx = V.holeIdx || 0;
  const hole = CAMP_HOLES[idx];
  const rec = strategyRecommend(hole, u, agg);
  const chips = CAMP_HOLES.map((h, i) => `<button class="hole-chip ${i === idx ? 'on' : ''}" data-act="sel-hole" data-i="${i}">${h.n}</button>`).join('');
  return `<button class="auth-back" data-act="nav" data-view="inicio">← Inicio</button>
    <div class="greet" style="padding-top:6px">
      <p class="hi">${esc(CAMP_COURSE.name)}</p>
      <h1 style="font-size:24px">Hoyo ${hole.n} · Par ${hole.par}</h1>
      <p class="hcp">${hole.yds} yds (azules) · ${esc(CAMP_COURSE.sub)}</p>
    </div>
    <div class="hole-strip">${chips}</div>
    <div class="card" style="padding:12px">${holeStrategySVG(hole, rec)}</div>
    <p class="small muted" style="margin-top:-4px">${esc(hole.desc)}</p>
    <div class="card">
      <span class="prio">Recomendado</span>
      <h3 style="margin-top:12px;font-size:19px;font-weight:900">${esc(rec.club)} · ${esc(rec.aim.toLowerCase())}</h3>
      <p style="font-size:14px;margin-top:8px">${esc(rec.reason)}</p>
      <div class="grid2" style="margin-top:12px">
        <div><div class="stat-num" style="font-size:22px">${rec.par3 ? hole.yds : rec.leave}</div><div class="stat-cap">${rec.par3 ? 'yds al green' : 'yds a green (2°)'}</div></div>
        <div><div class="stat-num" style="font-size:22px">~${rec.width}</div><div class="stat-cap">tu dispersión (yds)</div></div>
      </div>
      ${!rec.par3 && rec.approach ? `<p class="tip">Para el approach, tu ${esc(rec.approach)} cubre esa distancia.</p>` : ''}
    </div>
    <div class="card">
      <span class="label">Cómo se lee</span>
      <p class="tip">Línea <b class="lime">verde</b>: ruta recomendada para tu juego.${rec.par3 ? '' : ' Línea <b style="color:var(--danger)">ámbar</b>: agresiva (más riesgo).'}</p>
      <p class="tip">El óvalo verde es dónde caen tus tiros según tu % de calles — por eso evita los obstáculos.</p>
    </div>
    <p class="note" style="margin-bottom:24px">Recreación basada en el mapa oficial del club (par y yardas reales). Es una representación fiel del trazo, no un levantamiento topográfico. La estrategia se calcula con tu dispersión real.</p>`;
}
