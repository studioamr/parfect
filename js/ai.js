/* ============ AI Coach (Birdie) · cliente ============
   Llama a la Edge Function "coach" de Supabase (la llave de Anthropic vive en
   el backend, NUNCA aquí). Si no hay nube configurada o la función no está
   desplegada, AI.on() es false / chat() devuelve {ok:false} y la app usa el
   guion local de Birdie como respaldo (nunca se rompe). */
const AI = (() => {
  const cfg = (typeof window !== 'undefined' && window.PARFECT_CONFIG) || {};
  const BASE = cfg.SUPABASE_URL ? String(cfg.SUPABASE_URL).replace(/\/$/, '') : '';
  const KEY = cfg.SUPABASE_ANON_KEY || '';
  const URL = BASE ? BASE + '/functions/v1/coach' : '';
  let avail = true;            // se apaga si la función no existe (404/501)

  const on = () => !!(URL && KEY && avail);

  /* resumen compacto de stats del jugador actual (solo si hay rondas) */
  function statsBlurb() {
    try {
      if (typeof Stats === 'undefined' || typeof myRounds !== 'function') return '';
      const u = (typeof cur === 'function') ? cur() : null;
      const agg = Stats.aggregate(myRounds());
      if (!agg) return '';
      const r = n => Math.round(n);
      const sp = n => (n >= 0 ? '+' : '') + r(n);
      const lines = [
        `Hándicap: ${u && u.hcp != null ? u.hcp : '—'} · meta: ${u && u.goal != null ? u.goal : '—'}`,
        `Rondas registradas: ${agg.rounds}`,
        `Score promedio (18): ${r(agg.avgScore18)} (${sp(agg.avgToPar)} al par)`,
        `Fairways: ${r(agg.fwPct)}% · Greens en regulación: ${r(agg.girPct)}% · Up&down: ${r(agg.scrPct)}%`,
        `Putts/18: ${agg.putts18.toFixed(1)} · 3-putts: ${r(agg.threePct)}% · Penales/18: ${agg.penals18.toFixed(1)}`,
      ];
      if (typeof Trainer !== 'undefined' && Trainer.analyze) {
        const d = Trainer.analyze(agg, u || {});
        if (d && d.focus && d.focus[0]) lines.push(`Mayor fuga de golpes ahora: ${d.focus[0].titulo}`);
      }
      return lines.join('\n');
    } catch (e) { return ''; }
  }

  /* msgs: arreglo del chat [{from:'me'|'bot', text, typing?}]; opts.stats opcional */
  async function chat(msgs, opts) {
    opts = opts || {};
    if (!on()) return { ok: false };
    let m = (msgs || [])
      .filter(x => x && x.text && !x.typing)
      .map(x => ({ role: x.from === 'me' ? 'user' : 'assistant', content: String(x.text) }));
    while (m.length && m[0].role !== 'user') m.shift();   // debe empezar en user
    if (!m.length) return { ok: false };
    const body = { messages: m };
    const stats = opts.stats != null ? opts.stats : statsBlurb();
    if (stats) body.stats = stats;
    try {
      const res = await fetch(URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + KEY, 'apikey': KEY },
        body: JSON.stringify(body),
      });
      if (res.status === 404 || res.status === 501) { avail = false; return { ok: false }; }
      if (!res.ok) return { ok: false, status: res.status };
      const j = await res.json();
      if (j && typeof j.text === 'string' && j.text.trim()) return { ok: true, text: j.text.trim() };
      return { ok: false };
    } catch (e) { return { ok: false }; }
  }

  return { on, chat, statsBlurb };
})();
