/* ============ Sync multi-dispositivo para parties (MQTT sobre WSS) ============
   Sin backend propio: usa un broker público con el código de la party como canal.
   Cada cambio publica el estado completo (retained) con rev/ts: last-writer-wins. */

const DEVICE_ID = (() => {
  let id = localStorage.getItem('parfect_device');
  if (!id) { id = Math.random().toString(36).slice(2, 12); localStorage.setItem('parfect_device', id); }
  return id;
})();

const Sync = (() => {
  const BROKER = 'wss://broker.emqx.io:8084/mqtt';
  const topicFor = code => 'parfect/v1/party/' + code;
  let client = null;
  let status = 'off'; // off | connecting | on
  const watching = new Set();
  const pending = {}; // code → {fn, timer} esperando estado para unirse

  const available = () => typeof mqtt !== 'undefined';

  function connect() {
    if (!available() || client) return;
    status = 'connecting';
    client = mqtt.connect(BROKER, {
      reconnectPeriod: 4000,
      connectTimeout: 10000,
      clientId: 'parfect_' + DEVICE_ID + '_' + Math.random().toString(16).slice(2, 6),
    });
    client.on('connect', () => {
      status = 'on';
      for (const c of watching) client.subscribe(topicFor(c));
      safeRender();
    });
    client.on('offline', () => { status = 'connecting'; safeRender(); });
    client.on('error', () => {});
    client.on('message', (t, msg) => {
      let data;
      try { data = JSON.parse(msg.toString()); } catch { return; }
      const code = t.split('/').pop();
      if (pending[code]) {
        const { fn, timer } = pending[code];
        delete pending[code];
        clearTimeout(timer);
        fn(data);
        return;
      }
      apply(data);
    });
  }

  function safeRender() { try { render(); } catch (e) {} }

  /** Integra estado remoto si es más nuevo que el local */
  function apply(remote) {
    if (!remote || !remote.code || remote.origin === DEVICE_ID) return;
    const local = S.parties.find(p => p.code === remote.code);
    if (local) {
      if ((remote.rev || 0) < (local.rev || 0)) return;
      if ((remote.rev || 0) === (local.rev || 0) && (remote.ts || 0) <= (local.ts || 0)) return;
      Object.assign(local, remote);
    } else {
      S.parties.push(remote);
    }
    Store.save(S);
    safeRender();
  }

  function watch(code) {
    if (!available() || !code) return;
    watching.add(code);
    connect();
    if (client && client.connected) client.subscribe(topicFor(code));
  }

  function publish(party) {
    if (!available() || !party) return;
    watch(party.code);
    const payload = JSON.stringify({ ...party, origin: DEVICE_ID });
    if (client) client.publish(topicFor(party.code), payload, { retain: true, qos: 0 });
  }

  /** Busca una party remota por código (espera el mensaje retained del canal) */
  function joinRemote(code, fn, timeoutMs = 8000) {
    if (!available()) { fn(null); return; }
    const timer = setTimeout(() => {
      if (pending[code]) { delete pending[code]; fn(null); }
    }, timeoutMs);
    pending[code] = { fn, timer };
    watch(code);
  }

  return { available, connect, watch, publish, joinRemote, apply, status: () => status };
})();
