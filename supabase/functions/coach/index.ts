// ============================================================
// PARFECT · AI Coach (Birdie) — Supabase Edge Function
// La LLAVE de Anthropic vive SOLO aquí (secreto del backend); el navegador
// nunca la ve. El cliente (la app / la landing) llama a esta función con la
// anon key de Supabase; la función llama a Claude con la llave secreta.
//
// Desplegar (una sola vez, desde la carpeta del proyecto):
//   supabase functions deploy coach --no-verify-jwt
//   supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
//   (opcional) supabase secrets set ANTHROPIC_MODEL=claude-haiku-4-5
// ============================================================
import Anthropic from "npm:@anthropic-ai/sdk@^0.70";

const KEY = Deno.env.get("ANTHROPIC_API_KEY");
// Por defecto Opus 4.8. Para bajar costo del chatbot puedes poner
// ANTHROPIC_MODEL=claude-haiku-4-5 (≈5x más barato) sin tocar el código.
const MODEL = Deno.env.get("ANTHROPIC_MODEL") || "claude-opus-4-8";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });

const SYSTEM = `Eres Birdie, el asistente y AI Coach de golf de PARFECT (app de análisis de golf en español, México).

Tu personalidad: cercano, motivador y directo, como un buen entrenador. Hablas español de México, claro y sin tecnicismos innecesarios. Usas máximo un emoji por respuesta (a veces ninguno).

Tus dos trabajos:
1) AYUDA con la app PARFECT: registrar rondas (botón verde "P" abajo al centro), Análisis IA, Trainer (AI Coach o Entrenamiento libre), Academia (niveles tipo trivia), Social (jugar con amigos por código y leaderboard en vivo), perfil y hándicap automático.
2) COACHING de golf real: si te dan los datos del jugador, úsalos para dar consejos concretos y priorizados (dónde pierde más golpes y qué practicar primero). Nunca inventes números que no estén en los datos; si no hay datos, da consejo general y sugiere registrar algunas rondas para personalizar.

Reglas:
- Respuestas BREVES: 2 a 5 frases. Ve al grano, accionable.
- No des consejo médico ni financiero. No prometas resultados garantizados.
- Si preguntan algo fuera del golf o de la app, reconduce con amabilidad.`;

type InMsg = { role?: string; content?: unknown };

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);
  if (!KEY) return json({ error: "missing_api_key" }, 500);

  let payload: { messages?: InMsg[]; stats?: unknown };
  try { payload = await req.json(); } catch { return json({ error: "bad_json" }, 400); }

  const inMsgs = Array.isArray(payload?.messages) ? payload.messages : [];
  const messages = inMsgs
    .filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .slice(-16)
    .map((m) => ({ role: m.role as "user" | "assistant", content: (m.content as string).slice(0, 2000) }));
  // El primer turno debe ser del usuario
  while (messages.length && messages[0].role !== "user") messages.shift();
  if (!messages.length) return json({ error: "no_messages" }, 400);

  const stats = typeof payload?.stats === "string" ? (payload.stats as string).slice(0, 1800) : "";
  const system = stats
    ? `${SYSTEM}\n\nDATOS DEL JUGADOR (úsalos para personalizar; no inventes números que no estén aquí):\n${stats}`
    : SYSTEM;

  try {
    const client = new Anthropic({ apiKey: KEY });
    const resp = await client.messages.create({
      model: MODEL,
      max_tokens: 1024,
      system,
      messages,
    });
    if (resp.stop_reason === "refusal") {
      return json({ text: "Mejor pregúntame de tu golf o de cómo sacarle jugo a PARFECT 🙂" });
    }
    const text = resp.content
      .filter((b) => b.type === "text")
      .map((b) => (b as { text: string }).text)
      .join("")
      .trim();
    return json({ text: text || "…" });
  } catch (e) {
    return json({ error: "upstream", detail: String((e as Error)?.message || e) }, 502);
  }
});
