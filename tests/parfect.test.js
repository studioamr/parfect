/* ============ PARFECT · pruebas de lógica (corren en el navegador) ============
   Cubren el motor de métricas (Stats), el coach IA (Trainer), almacenamiento
   (Store/Demo), la Academia y la biblioteca de drills. No tocan el DOM ni la red.
   Abre tests/index.html (o sirve la carpeta) para verlas; el resumen también va a la consola. */
(function () {
  const T = { pass: 0, fail: 0, results: [] };
  const test = (n, fn) => { try { fn(); T.pass++; T.results.push({ n, ok: true }); } catch (e) { T.fail++; T.results.push({ n, ok: false, e: String((e && e.message) || e) }); } };
  const assert = (c, m) => { if (!c) throw new Error(m || 'assert falló'); };
  const eq = (a, b, m) => { if (a !== b) throw new Error((m || 'eq') + ': esperaba ' + b + ' y obtuve ' + a); };
  const approx = (a, b, t, m) => { if (Math.abs(a - b) > (t || 0.001)) throw new Error((m || 'approx') + ': esperaba ~' + b + ' y obtuve ' + a); };
  const range = (a, lo, hi, m) => { if (!(a >= lo && a <= hi)) throw new Error((m || 'range') + ': ' + a + ' fuera de [' + lo + ',' + hi + ']'); };

  // ronda fija de N hoyos; sc(par) define el score por hoyo
  const fixture = (n = 18, sc = p => p) => ({
    id: 't', userId: 'u', date: '2026-01-01',
    holes: Stats.PAR_SEQ.slice(0, n).map(par => ({ par, score: sc(par), tee: par === 3 ? null : 'fw', app: 'gir', putts: 2, dist: '8-20' })),
  });

  /* ---------- Stats.roundStats ---------- */
  test('roundStats: ronda de pares (par/score/toPar/fw/gir/putts)', () => {
    const s = Stats.roundStats(fixture());
    eq(s.holes, 18, 'holes'); eq(s.par, 72, 'par'); eq(s.score, 72, 'score'); eq(s.toPar, 0, 'toPar');
    eq(s.gir, 18, 'gir'); eq(s.putts, 36, 'putts'); eq(s.fwTot, 14, 'fwTot'); eq(s.fw, 14, 'fw');
  });
  test('roundStats: ronda de 9 hoyos', () => { eq(Stats.roundStats(fixture(9)).holes, 9); });
  test('roundStats: sin hoyos no truena', () => { const s = Stats.roundStats({ holes: [] }); eq(s.holes, 0); eq(s.par, 0); eq(s.score, 0); });
  test('roundStats: bogeys → toPar positivo', () => { eq(Stats.roundStats(fixture(18, p => p + 1)).toPar, 18); });

  /* ---------- Stats.aggregate ---------- */
  test('aggregate: null/[] → null', () => { assert(Stats.aggregate(null) === null, 'null'); assert(Stats.aggregate([]) === null, 'vacío'); });
  test('aggregate: una ronda', () => {
    const a = Stats.aggregate([fixture()]);
    eq(a.rounds, 1, 'rounds'); eq(a.holesPlayed, 18, 'holesPlayed');
    approx(a.fwPct, 100, 0.1, 'fwPct'); approx(a.girPct, 100, 0.1, 'girPct'); approx(a.putts18, 36, 0.1, 'putts18');
    eq(a.series.length, 1, 'series');
  });
  test('aggregate: 9 hoyos se normaliza a 18', () => {
    const par9 = Stats.PAR_SEQ.slice(0, 9).reduce((x, y) => x + y, 0);
    approx(Stats.aggregate([fixture(9)]).avgScore18, par9 * 2, 0.5, 'avgScore18');
  });
  test('aggregate: scoreDist suma = holesPlayed', () => {
    const a = Stats.aggregate([fixture(), fixture(18, p => p + 1)]);
    const d = a.scoreDist;
    eq(d.eagle + d.birdie + d.par + d.bogey + d.dbl, d.total, 'suma');
    eq(d.total, 36, 'total'); eq(d.par, 18, 'par'); eq(d.bogey, 18, 'bogey');
  });
  test('aggregate: porcentajes en 0–100', () => {
    const a = Stats.aggregate([fixture()]);
    range(a.fwPct, 0, 100, 'fwPct'); range(a.girPct, 0, 100, 'girPct'); range(a.scrPct, 0, 100, 'scrPct'); range(a.threePct, 0, 100, 'threePct');
  });

  /* ---------- Stats.radarOf ---------- */
  test('radarOf: 6 valores en 0–100', () => { const r = Stats.radarOf(Stats.aggregate([fixture()])); eq(r.values.length, 6); r.values.forEach(v => range(v, 0, 100)); });
  test('radarOf: sin agg → default de 6', () => { eq(Stats.radarOf(null).values.length, 6); });

  /* ---------- Trainer.analyze ---------- */
  test('Trainer.analyze: sin agg → readiness none', () => { const d = Trainer.analyze(null, {}); eq(d.readiness, 'none'); eq(d.focus.length, 0); });
  test('Trainer.analyze: agg válido → focus bien formado', () => {
    const a = Stats.aggregate([fixture(18, p => p + 1)]);
    const d = Trainer.analyze(a, { hcp: 15, goal: 10 });
    assert(Array.isArray(d.focus), 'focus es array');
    d.focus.forEach(f => { assert(f.key, 'key'); assert(f.titulo, 'titulo'); assert(Array.isArray(f.drills) && f.drills.length > 0, 'drills'); });
  });
  test('Trainer.analyze: focus ordenado por impacto (lost desc)', () => {
    const f = Trainer.analyze(Stats.aggregate([fixture(18, p => p + 2)]), { hcp: 18, goal: 10 }).focus;
    for (let i = 1; i < f.length; i++) assert(f[i - 1].lost >= f[i].lost, 'orden en índice ' + i);
  });

  /* ---------- Store + Demo ---------- */
  test('Store.uid: único y no vacío', () => { const a = Store.uid(), b = Store.uid(); assert(a && a.length > 3, 'longitud'); assert(a !== b, 'únicos'); });
  test('Store.save/load: round-trip (sin pisar tus datos)', () => {
    const snap = localStorage.getItem('parfect_v1');
    try {
      Store.save({ users: [{ id: 'x' }], session: 'x', rounds: [], practices: [], marker: 42 });
      const back = Store.load();
      eq(back.marker, 42, 'marker'); eq(back.session, 'x', 'session'); assert(Array.isArray(back.rounds), 'rounds array');
    } finally { snap === null ? localStorage.removeItem('parfect_v1') : localStorage.setItem('parfect_v1', snap); }
  });
  test('Store.load: forma por defecto', () => {
    const snap = localStorage.getItem('parfect_v1');
    try { localStorage.removeItem('parfect_v1'); const s = Store.load(); ['users', 'rounds', 'practices', 'parties'].forEach(k => assert(Array.isArray(s[k]), k + ' array')); }
    finally { snap === null ? localStorage.removeItem('parfect_v1') : localStorage.setItem('parfect_v1', snap); }
  });
  test('Demo.rounds: n rondas de 18 hoyos válidas', () => {
    const rs = Demo.rounds('u9', 5);
    eq(rs.length, 5, 'n');
    rs.forEach(r => { eq(r.holes.length, 18, 'holes'); eq(r.userId, 'u9', 'userId'); r.holes.forEach(h => { assert(h.par > 0, 'par'); assert(h.score > 0, 'score'); }); });
    assert(Stats.aggregate(rs) !== null, 'agregable');
  });
  test('Demo.practices: válidas (hits ≤ attempts)', () => {
    const ps = Demo.practices('u9');
    assert(ps.length > 0, 'no vacía');
    ps.forEach(p => { eq(p.userId, 'u9', 'userId'); assert(p.area, 'area'); assert(p.attempts > 0, 'attempts'); assert(p.hits <= p.attempts, 'hits<=attempts'); });
  });

  /* ---------- Academia ---------- */
  test('Academia: 18 niveles', () => { eq(ACADEMY_N, 18); });
  test('Academia: levelQs(i) = 10 preguntas bien formadas', () => {
    const qs = levelQs(0); eq(qs.length, 10, 'count');
    qs.forEach(q => { assert(q.q, 'q'); eq(q.opts.length, 4, 'opts'); range(q.a, 0, 3, 'a'); });
  });
  test('Academia: levelQs es determinista por nivel', () => { eq(JSON.stringify(levelQs(3)), JSON.stringify(levelQs(3))); });
  test('Academia: desbloqueo por nivel', () => {
    assert(quizUnlocked(null, 0), 'nivel 0 abierto');
    assert(!quizUnlocked(null, 1), 'nivel 1 bloqueado');
    assert(quizUnlocked({ acQuiz: { 0: 7 } }, 1), 'nivel 1 con 7/10');
    assert(!quizUnlocked({ acQuiz: { 0: 6 } }, 1), 'nivel 1 con 6/10 sigue bloqueado');
  });
  test('Academia: quizProgress cuenta aprobados (≥7)', () => { const p = quizProgress({ acQuiz: { 0: 8, 1: 7, 2: 3 } }); eq(p.done, 2, 'done'); eq(p.total, 18, 'total'); });

  /* ---------- Biblioteca de drills ---------- */
  test('DRILL_LIBRARY: no vacía y con categoría válida', () => {
    assert(DRILL_LIBRARY.length > 0, 'no vacía');
    const cats = DRILL_CATS.map(c => c.id);
    DRILL_LIBRARY.forEach(d => { assert(d.name, 'name'); assert(cats.includes(d.cat), 'cat válida: ' + d.cat); });
  });

  /* ---------- Integración ---------- */
  test('Integración: Demo → aggregate → analyze sin errores', () => {
    const a = Stats.aggregate(Demo.rounds('uX', 8));
    assert(a, 'agg'); const d = Trainer.analyze(a, { hcp: 14, goal: 9 }); assert(Array.isArray(d.focus), 'focus');
  });

  window.__TESTS = T;
  const out = document.getElementById('out');
  if (out) {
    out.innerHTML = `<h2 class="${T.fail === 0 ? 'ok' : 'bad'}">${T.fail === 0 ? '✅ Todas pasaron' : '❌ ' + T.fail + ' fallaron'} · ${T.pass}/${T.pass + T.fail}</h2>`
      + T.results.map(r => `<div class="row ${r.ok ? 'ok' : 'bad'}">${r.ok ? '✓' : '✗'} ${r.n}${r.ok ? '' : ' — ' + r.e}</div>`).join('');
  }
  console.log('[PARFECT TESTS] ' + T.pass + ' pass / ' + T.fail + ' fail', T.fail ? T.results.filter(r => !r.ok) : '');
})();
