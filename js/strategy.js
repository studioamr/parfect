/* ============ Estrategia por hoyo — multi-campo ============
   Esquema GENÉRICO (entendible, no a escala) con zonas de riesgo y la ruta recomendada,
   + preview tiro por tiro. La recomendación usa tu bolsa (carry) y tu efectividad por palo,
   que sale de tu Tracker (si no hay, de lo que cargaste en Mis palos, o un default). */

const CAMP_HOLES = [
  { n: 1, par: 5, yds: 503, dog: 'straight', desc: 'Par 5 largo y plano; calle amplia.',
    risks: [{ at: 'drive', side: 'right', kind: 'bunker' }],
    tips: ['Coloca el drive al centro-izquierda; los bunkers de calle están a la derecha.', 'Si no llegas en dos, deja un wedge cómodo de tercer golpe.'] },
  { n: 2, par: 5, yds: 550, dog: 'right', desc: 'El par 5 más largo; un arroyo cruza antes del green.',
    risks: [{ at: 'green', side: 'left', kind: 'bunker' }],
    tips: ['Prioriza calle, no distancia: es el hoyo más largo.', 'El arroyo cruza antes del green — si no llegas en dos, deja el tercer golpe corto del agua.'] },
  { n: 3, par: 3, yds: 174, dog: 'straight', desc: 'Par 3 corto con laguna a la izquierda del green.',
    risks: [{ at: 'green', side: 'left', kind: 'water' }],
    tips: ['Apunta al centro-derecha; la laguna castiga la izquierda.', 'Fallar a la derecha (al bunker) se salva mejor que mojar la bola.'] },
  { n: 4, par: 4, yds: 405, dog: 'left', desc: 'Dogleg suave a la izquierda.',
    risks: [{ at: 'green', side: 'right', kind: 'bunker' }], tips: ['Coloca el drive al centro; deja approach de hierro medio.'] },
  { n: 5, par: 3, yds: 201, dog: 'straight', desc: 'El par 3 más largo; toma palo de más.',
    risks: [{ at: 'green', side: 'left', kind: 'bunker' }], tips: ['Es largo: toma un palo más y juega al centro del green.'] },
  { n: 6, par: 4, yds: 432, dog: 'right', desc: 'Par 4 largo; coloca el drive.',
    risks: [{ at: 'green', side: 'left', kind: 'bunker' }], tips: ['Par 4 exigente: prioriza estar en calle para atacar el green.'] },
  { n: 7, par: 5, yds: 529, dog: 'left', desc: 'Par 5 alcanzable en dos si pegas recto.',
    risks: [{ at: 'green', side: 'right', kind: 'water' }], tips: ['Si pegas recto, es alcanzable en dos; ojo con el agua a la derecha.'] },
  { n: 8, par: 3, yds: 176, dog: 'straight', desc: 'Par 3 sobre el agua a la izquierda.',
    risks: [{ at: 'green', side: 'left', kind: 'water' }], tips: ['Apunta al centro-derecha; el agua castiga el lado izquierdo.'] },
  { n: 9, par: 4, yds: 407, dog: 'right', desc: 'Par 4 de cierre hacia la casa club.',
    risks: [{ at: 'green', side: 'right', kind: 'bunker' }], tips: ['Hoyo de cierre: deja la bola en calle y ataca el green al centro.'] },
];

/* Genera hoyos genéricos a partir de pares/yardas (Tres Marías, Altozano) */
function buildHoles(pars, yards) {
  return pars.map((par, i) => {
    const n = i + 1;
    const dog = par === 3 ? 'straight' : (n % 2 === 0 ? 'right' : 'left');
    const risks = par === 3
      ? [{ at: 'green', side: n % 2 ? 'left' : 'right', kind: n % 4 === 0 ? 'water' : 'bunker' }]
      : [{ at: 'green', side: n % 2 ? 'right' : 'left', kind: 'bunker' }];
    return { n, par, yds: yards[i], dog, risks, desc: `Par ${par} de ${yards[i]} yds.` };
  });
}
const TM_PARS = [4, 4, 3, 4, 5, 3, 4, 5, 4, 4, 4, 4, 3, 3, 4, 5, 4, 5];
const TM_YDS = [433, 466, 207, 434, 555, 187, 389, 530, 404, 520, 380, 374, 214, 216, 509, 541, 350, 545];
const ALT_PARS = [4, 5, 4, 4, 3, 5, 3, 4, 4, 4, 4, 3, 4, 3, 4, 5, 4, 5];
const ALT_YDS = ALT_PARS.map(p => p === 3 ? 195 : p === 4 ? 420 : 565);

const COURSES = {
  campestre: { id: 'campestre', name: 'Club Campestre Morelia', sub: '9 hoyos · Par 72', holes: CAMP_HOLES },
  tresmarias: { id: 'tresmarias', name: 'Tres Marías · El Reto', sub: '18 hoyos · Par 72', approx: true, holes: buildHoles(TM_PARS, TM_YDS) },
  altozano: { id: 'altozano', name: 'Altozano Morelia', sub: '18 hoyos · Par 72', approx: true, holes: buildHoles(ALT_PARS, ALT_YDS) },
};
const COURSE_ORDER = ['campestre', 'tresmarias', 'altozano'];

/* ---- bolsa + efectividad (efectividad sale del Tracker) ---- */
function trackerEff(clubName) {
  const ps = (typeof myPractices === 'function' ? myPractices() : []).filter(p => p.drill === clubName);
  if (!ps.length) return null;
  const last = ps.slice(-3);
  const att = last.reduce((a, p) => a + p.attempts, 0), hit = last.reduce((a, p) => a + p.hits, 0);
  return att ? Math.round((hit / att) * 100) : null;
}
function bagInfo(user) {
  const clubs = (user && user.clubs) || {};
  const personalized = Object.keys(clubs).some(k => clubs[k] != null);
  return CLUBS.map(c => {
    let carry;
    if (personalized) { const cc = clubC(clubs, c.id); if (cc == null) return null; carry = cc; }
    else { if (!DEFAULT_BAG.includes(c.id)) return null; carry = CLUB_DEFAULT[c.id]; }
    const eff = trackerEff(c.name) != null ? trackerEff(c.name) : (clubE(clubs, c.id) != null ? clubE(clubs, c.id) : CLUB_EFF_DEFAULT);
    return { id: c.id, name: c.name, group: c.group, carry, eff, effSrc: trackerEff(c.name) != null ? 'tracker' : (clubE(clubs, c.id) != null ? 'perfil' : 'default') };
  }).filter(Boolean);
}
function clubForDistance(user, yds, opts) {
  let bag = bagInfo(user);
  if (opts && opts.noDriver) bag = bag.filter(c => c.id !== 'dr');
  if (!bag.length) return null;
  bag.sort((a, b) => (Math.abs(a.carry - yds) - Math.abs(b.carry - yds)) || (b.eff - a.eff));
  return bag[0];
}
function dispersionYds(eff) { return Math.round(Math.max(12, Math.min(50, 70 - eff * 0.55))); }

function teeShot(hole, user) {
  const bag = bagInfo(user);
  if (!bag.length) return null;
  const longs = bag.filter(c => ['dr', 'w3', 'w5', 'w7', 'h4', 'h5', 'h6', 'i3', 'i4'].includes(c.id) && c.carry >= hole.yds * 0.4).sort((a, b) => b.carry - a.carry);
  let pick = bag.find(c => c.id === 'dr') || longs[0] || bag.sort((a, b) => b.carry - a.carry)[0];
  const driveRisk = (hole.risks || []).find(r => r.at === 'drive');
  if (driveRisk && pick && pick.eff < 65) {
    const safer = longs.filter(c => c.eff >= pick.eff + 8 && c.carry >= hole.yds * 0.45).sort((a, b) => b.carry - a.carry)[0];
    if (safer) pick = safer;
  }
  return pick;
}
function teeAim(hole, bias) {
  const dr = (hole.risks || []).find(r => r.at === 'drive');
  if (dr) return dr.side === 'right' ? 'Centro-izquierda, lejos del peligro' : 'Centro-derecha, lejos del peligro';
  return bias === 'der' ? 'Centro-izquierda' : bias === 'izq' ? 'Centro-derecha' : 'Centro de la calle';
}
function greenAim(hole) {
  const g = (hole.risks || []).find(r => r.at === 'green');
  if (g) return g.side === 'left' ? 'Centro-derecha del green' : 'Centro-izquierda del green';
  return 'Centro del green';
}

function planHole(hole, user, agg) {
  const m = (agg && agg.missTee) || { izq: 0, der: 0 };
  const bias = m.der > m.izq * 1.2 ? 'der' : m.izq > m.der * 1.2 ? 'izq' : 'centro';
  const mk = (label, c, dist, target, def) => ({ label, name: c ? c.name : def, carry: c ? c.carry : null, eff: c ? c.eff : CLUB_EFF_DEFAULT, effSrc: c ? c.effSrc : 'default', dist: Math.round(dist), disp: dispersionYds(c ? c.eff : CLUB_EFF_DEFAULT), target });
  const shots = [];

  if (hole.par === 3) { shots.push(mk('Tiro al green', clubForDistance(user, hole.yds), hole.yds, greenAim(hole), 'Hierro')); return { shots, bias }; }

  const tee = teeShot(hole, user);
  const teeCarry = tee ? tee.carry : 250;
  shots.push(mk('Salida', tee, teeCarry, teeAim(hole, bias), 'Driver'));
  const remaining = Math.max(hole.yds - teeCarry, 0);

  if (hole.par === 4) {
    shots.push(mk('Approach', clubForDistance(user, remaining, { noDriver: true }), remaining, greenAim(hole), 'Hierro'));
  } else {
    const best = bagInfo(user).filter(c => c.id !== 'dr').sort((a, b) => b.carry - a.carry)[0];
    const reachable = best && remaining <= best.carry + 5 && remaining > 50;
    if (reachable) {
      shots.push(mk('Segundo · al green', clubForDistance(user, remaining, { noDriver: true }), remaining, greenAim(hole), 'Madera'));
    } else {
      const adv = Math.max(remaining - 105, 60);
      const c = clubForDistance(user, adv, { noDriver: true });
      const advDist = c ? Math.min(c.carry, remaining - 40) : adv;
      shots.push(mk('Segundo · colocar', c, advDist, 'Centro de la calle', 'Hierro'));
      const leave = Math.max(hole.yds - teeCarry - advDist, 30);
      shots.push(mk('Approach', clubForDistance(user, leave, { noDriver: true }), leave, greenAim(hole), 'Wedge'));
    }
  }
  return { shots, bias };
}

function bez(t, a, c, b) { const u = 1 - t; return u * u * a + 2 * u * t * c + t * t * b; }

function holeSchematic(hole, plan) {
  const W = 340, H = 458, par3 = hole.par === 3;
  const green = hole.dog === 'left' ? [120, 106] : hole.dog === 'right' ? [222, 106] : [170, 100];
  const ctrl = par3 ? [170, 270] : (hole.dog === 'left' ? [224, 262] : hole.dog === 'right' ? [118, 262] : [170, 262]);
  const tee = [170, 442], gx = green[0], gy = green[1];
  const fair = `M${tee[0]},${tee[1]} Q ${ctrl[0]},${ctrl[1]} ${gx},${gy}`;
  let cum = 0; const pts = [];
  plan.shots.forEach(s => { cum += s.dist; const f = Math.min(cum / hole.yds, 1); pts.push({ s, p: [bez(f, tee[0], ctrl[0], gx), bez(f, tee[1], ctrl[1], gy)] }); });
  pts[pts.length - 1].p = [gx, gy];
  const route = `M${tee[0]},${tee[1]} ` + pts.map(q => `L${q.p[0].toFixed(0)},${q.p[1].toFixed(0)}`).join(' ');
  let risks = '', labels = '';
  (hole.risks || []).forEach(r => {
    let rx, ry;
    if (r.at === 'drive') { const lp = pts[0].p; rx = lp[0] + (r.side === 'left' ? -42 : 42); ry = lp[1]; }
    else { rx = gx + (r.side === 'left' ? -48 : 48); ry = gy + 18; }
    const water = r.kind === 'water';
    risks += `<ellipse cx="${rx.toFixed(0)}" cy="${ry.toFixed(0)}" rx="${water ? 27 : 21}" ry="${water ? 17 : 12}" fill="${water ? '#2f7fa6' : '#ddcb8c'}"/>`;
    labels += `<rect x="${(rx - 25).toFixed(0)}" y="${(ry - (water ? 17 : 12) - 19).toFixed(0)}" width="50" height="16" rx="8" fill="${water ? '#16323f' : '#3a2a16'}" stroke="${water ? '#3f96bd' : '#e0a25a'}"/><text x="${rx.toFixed(0)}" y="${(ry - (water ? 17 : 12) - 7).toFixed(0)}" fill="${water ? '#7fc3df' : '#e0a25a'}" font-family="Inter,system-ui,sans-serif" font-size="9" font-weight="800" text-anchor="middle">${water ? 'Agua' : 'Bunker'}</text>`;
  });
  let lands = '';
  pts.forEach((q, i) => {
    if (i === pts.length - 1) return;
    const rx = Math.max(14, Math.min(32, q.s.disp * 0.7)), ry = rx * 0.7;
    lands += `<ellipse cx="${q.p[0].toFixed(0)}" cy="${q.p[1].toFixed(0)}" rx="${rx.toFixed(0)}" ry="${ry.toFixed(0)}" fill="#c9f73e" opacity="0.15" stroke="#c9f73e" stroke-width="1.4" stroke-dasharray="4 4"><animate attributeName="opacity" values="0.09;0.22;0.09" dur="2.4s" repeatCount="indefinite"/></ellipse>
      <text x="${q.p[0].toFixed(0)}" y="${(q.p[1] + 3).toFixed(0)}" fill="#c9f73e" font-family="Inter,system-ui,sans-serif" font-size="11" font-weight="900" text-anchor="middle">${i + 1}</text>`;
  });
  return `<svg width="100%" viewBox="0 0 ${W} ${H}" role="img" aria-label="Esquema hoyo ${hole.n}">
    <rect x="0" y="0" width="${W}" height="${H}" rx="16" fill="#0a0f08" stroke="#1d2914"/>
    <path d="${fair}" fill="none" stroke="#2f6b39" stroke-width="${par3 ? 42 : 64}" stroke-linecap="round"/>
    <path d="${fair}" fill="none" stroke="#3a8043" stroke-width="${par3 ? 22 : 34}" stroke-linecap="round" opacity="0.5"/>
    <ellipse cx="${gx}" cy="${gy}" rx="38" ry="27" fill="#57b15c" stroke="#2f6b39" stroke-width="2"/>
    <circle cx="${gx + 5}" cy="${gy + 1}" r="3" fill="#0a0f08"/>
    <line x1="${gx + 5}" y1="${gy + 1}" x2="${gx + 5}" y2="${gy - 34}" stroke="#eef3e6" stroke-width="2"/>
    <path d="M${gx + 5},${gy - 34} L${gx + 19},${gy - 30} L${gx + 5},${gy - 26} Z" fill="#c9f73e"/>
    ${risks}${lands}
    <path d="${route}" fill="none" stroke="#c9f73e" stroke-width="2.5" stroke-dasharray="3 6"/>
    <circle r="5" fill="#fff"><animateMotion dur="3.6s" repeatCount="indefinite" path="${route}"/><animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.05;0.5;0.85;1" dur="3.6s" repeatCount="indefinite"/></circle>
    ${labels}
    <rect x="161" y="440" width="18" height="7" rx="2" fill="#9ab07f"/><text x="170" y="${H - 5}" fill="#9ab07f" font-family="Inter,system-ui,sans-serif" font-size="10" font-weight="700" text-anchor="middle">TEE</text>
  </svg>`;
}

function vStrategy() {
  const u = cur();
  const agg = Stats.aggregate(myRounds());
  const course = COURSES[V.courseId] || COURSES.campestre;
  if (V.holeIdx >= course.holes.length) V.holeIdx = 0;
  const idx = V.holeIdx || 0;
  const hole = course.holes[idx];
  const plan = planHole(hole, u, agg);
  const courseChips = COURSE_ORDER.map(id => `<button class="chip sm ${id === course.id ? 'on' : ''}" data-act="sel-course" data-c="${id}">${esc(COURSES[id].name.split(' · ')[0].replace('Club ', '').replace(' Morelia', ''))}</button>`).join('');
  const chips = course.holes.map((h, i) => `<button class="hole-chip ${i === idx ? 'on' : ''}" data-act="sel-hole" data-i="${i}">${h.n}</button>`).join('');
  const r0 = (hole.risks || [])[0];
  const avoid = r0 ? `${r0.kind === 'water' ? 'Agua' : 'Bunker'} a la ${r0.side === 'left' ? 'izquierda' : 'derecha'}${r0.at === 'green' ? ' del green' : ' de la zona de caída'} — si dudas, falla al lado contrario.` : null;
  const effTag = s => s.effSrc === 'tracker' ? ' (de tu Tracker)' : s.effSrc === 'perfil' ? '' : ' (estimada)';

  const shotCards = plan.shots.map((s, i) => `<div class="card">
      <div style="display:flex;justify-content:space-between;align-items:baseline">
        <span class="prio ${i > 0 ? 'p2' : ''}">${i + 1} · ${esc(s.label)}</span>
        <span class="lime" style="font-size:17px;font-weight:900">${s.dist} yds</span>
      </div>
      <h3 style="margin-top:10px;font-size:19px;font-weight:900">${esc(s.name)}${s.carry ? ` <span class="muted" style="font-size:13px;font-weight:600">· vuela ~${s.carry} yds</span>` : ''}</h3>
      <p class="hcp" style="font-size:13px;margin-top:1px">Apunta: ${esc(s.target.toLowerCase())}</p>
      <div class="bar" style="margin-top:9px"><i style="width:${s.eff}%"></i></div>
      <p class="note" style="margin-top:4px">Efectividad ${s.eff}%${effTag(s)} · dispersión ~${s.disp} yds</p>
    </div>`).join('');

  return `<div class="sec-h"><h2>Estrategia</h2><span class="small muted">por hoyo, según tu juego</span></div>
    <div class="chips" style="margin-top:8px">${courseChips}</div>
    <div class="greet" style="padding-top:10px">
      <p class="hi">${esc(course.name)}${course.approx ? ' · yardas aprox.' : ''}</p>
      <h1 style="font-size:23px">Hoyo ${hole.n} · Par ${hole.par} · ${hole.yds} yds</h1>
    </div>
    <div class="hole-strip">${chips}</div>
    <div class="card" style="padding:12px">${holeSchematic(hole, plan)}</div>
    <p class="small muted" style="margin-top:-4px">Esquema genérico (no a escala). Los números marcan tus tiros y las zonas de aterrizaje según tu efectividad.</p>
    ${avoid ? `<div class="card"><span class="label">⚠️ Dónde no fallar</span><p style="font-size:14px;margin-top:6px">${esc(avoid)}</p></div>` : ''}
    <div class="sec-h"><h2 style="font-size:16px">Tu plan, tiro por tiro</h2></div>
    ${shotCards}
    <div class="card"><span class="label">Notas del hoyo</span>${(hole.tips || [hole.desc]).map(t => `<p class="tip">${esc(t)}</p>`).join('')}</div>
    <p class="note" style="margin-bottom:24px">Recomendación con tu bolsa y tu efectividad por palo (sale de tu Tracker; edita carries en Perfil → Mis palos). ${course.approx ? 'Yardas por hoyo aproximadas.' : 'Par y yardas reales.'}</p>`;
}
