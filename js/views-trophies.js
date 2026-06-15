/* ============ Vista Trofeos: metas + logros ============ */

function vTrophies() {
  const u = cur();
  const list = Trophies.evaluate();
  const unlocked = list.filter(a => a.done).length;
  const goals = Trophies.goals();
  const fmtG = (v, suffix) => (v == null ? '—' : (suffix === '%' ? Math.round(v) + '%' : (Number.isInteger(v) ? v : v.toFixed(1))));

  const goalRows = goals.map(g => {
    const pct = Math.round((g.prog || 0) * 100);
    return `<div class="goal">
      <div class="goal-top">
        <span>${esc(g.label)}</span>
        <span class="${g.met ? 'lime' : 'muted'}">${fmtG(g.cur, g.suffix)} <span class="muted">/ meta ${fmtG(g.target, g.suffix)}</span></span>
      </div>
      <div class="bar"><i style="width:${pct}%"></i></div>
    </div>`;
  }).join('');

  const cards = list.map(a => `<div class="trophy ${a.done ? 'on' : ''}">
    <div class="t-ic">${golfIcon(a.ic, a.done ? 'gi-spin' : '')}</div>
    <div class="t-body">
      <b>${esc(a.t)}</b>
      <span>${esc(a.d)}</span>
      ${!a.done && a.prog > 0 && a.prog < 1 ? `<div class="bar mini"><i style="width:${Math.round(a.prog * 100)}%"></i></div>` : ''}
      ${a.sub ? `<span class="t-sub">${esc(a.sub)}</span>` : ''}
    </div>
    <div class="t-state">${a.done ? '✓' : ''}</div>
  </div>`).join('');

  return `<div class="sec-h"><h2>Trofeos</h2><span class="small muted">${unlocked}/${list.length} logros</span></div>

    <div class="card">
      <span class="label">Tus metas</span>
      <p class="note" style="margin-top:0;margin-bottom:10px">Tu progreso hacia un hándicap de ${fmtHcp(u.goal)}.</p>
      ${goalRows}
    </div>

    <div class="sec-h"><h2 style="font-size:18px">Logros</h2></div>
    <div class="trophy-grid">${cards}</div>
    ${unlocked === 0 ? `<p class="note">Registra rondas y prácticas para empezar a desbloquear logros.</p>` : ''}
  `;
}

/* Solo logros (sin metas) — su propia sección */
function vLogros() {
  const list = Trophies.evaluate();
  const unlocked = list.filter(a => a.done).length;
  const cards = list.map(a => `<div class="trophy ${a.done ? 'on' : ''}">
    <div class="t-ic">${golfIcon(a.ic, a.done ? 'gi-spin' : '')}</div>
    <div class="t-body">
      <b>${esc(a.t)}</b>
      <span>${esc(a.d)}</span>
      ${!a.done && a.prog > 0 && a.prog < 1 ? `<div class="bar mini"><i style="width:${Math.round(a.prog * 100)}%"></i></div>` : ''}
      ${a.sub ? `<span class="t-sub">${esc(a.sub)}</span>` : ''}
    </div>
    <div class="t-state">${a.done ? '✓' : ''}</div>
  </div>`).join('');
  return `<div class="sec-h"><h2>Logros</h2><span class="small muted">${unlocked}/${list.length} desbloqueados</span></div>
    <div class="trophy-grid">${cards}</div>
    ${unlocked === 0 ? `<p class="note">Registra rondas y prácticas para empezar a desbloquear logros.</p>` : ''}`;
}

/* Números clave para llegar a tu meta (según tu HCP objetivo) */
function vKeyTargets(u) {
  const agg = Stats.aggregate(myRounds());
  const goal = u.goal != null ? u.goal : Math.max(0, (u.hcp != null ? u.hcp : 12) - 5);
  const b = Stats.benchFor(goal);
  const cur = agg ? { fw: Math.round(agg.fwPct), gir: Math.round(agg.girPct), ud: Math.round(agg.scrPct), putts: Math.round(agg.putts18) } : null;
  const row = (label, c, t, sfx) => `<div class="pl-rr stat">
      <div class="pl-rr-id"><b>${label}</b>${cur ? `<span>ahora ${c}${sfx}</span>` : ''}</div>
      <span class="pl-rr-score">${t}${sfx}</span>
    </div>`;
  return `<div class="sec-h" style="margin-top:6px"><h2 style="font-size:16px">${golfIcon('green')} Números clave · meta HCP ${fmtHcp(goal)}</h2></div>
    <p class="note" style="margin:0 0 4px">Lo que juega un HCP ${fmtHcp(goal)}. El badge lima es tu objetivo.</p>
    <div class="pl-rr-list">
    ${row('Fairways', cur ? cur.fw : '', Math.round(b.fwPct), '%')}
    ${row('Greens (GIR)', cur ? cur.gir : '', Math.round(b.girPct), '%')}
    ${row('Up & down', cur ? cur.ud : '', Math.round(b.scrPct), '%')}
    ${row('Putts / ronda', cur ? cur.putts : '', Math.round(b.putts18), '')}
    </div>`;
}

/* Tabla de referencia: qué stats tiene cada nivel de hándicap */
function vHcpReference(u) {
  const levels = [0, 5, 10, 15, 20, 25];
  const near = levels.reduce((a, b) => (Math.abs(b - u.hcp) < Math.abs(a - u.hcp) ? b : a), levels[0]);
  const nearGoal = levels.reduce((a, b) => (Math.abs(b - u.goal) < Math.abs(a - u.goal) ? b : a), levels[0]);
  const rows = levels.map(h => {
    const b = Stats.benchFor(h);
    const tags = [];
    if (h === near) tags.push('tú');
    if (h === nearGoal) tags.push('meta');
    const cls = h === nearGoal ? 'hcp-goal' : (h === near ? 'hcp-me' : '');
    return `<tr class="${cls}">
      <td class="hcp-h">${h}${tags.length ? ` <span class="hcp-tag">${tags.join('·')}</span>` : ''}</td>
      <td>${Math.round(b.fwPct)}%</td>
      <td>${Math.round(b.girPct)}%</td>
      <td>${Math.round(b.scrPct)}%</td>
      <td>${Math.round(b.putts18)}</td>
    </tr>`;
  }).join('');
  return `<div class="card">
    <span class="label">Referencia por hándicap</span>
    <p class="note" style="margin-top:0;margin-bottom:8px">Cómo juega cada nivel. Úsalo de mapa para saber qué buscar.</p>
    <div class="sc-scroll"><table class="sc-table ref-table">
      <thead><tr><th class="sc-name">HCP</th><th>Calles</th><th>GIR</th><th>U/D</th><th>Putts</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}
