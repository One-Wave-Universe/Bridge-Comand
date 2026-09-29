const PROVIDERS = {
  gemini: {
    defaultModel: "gemini-3.8-flash",
    async call({ apiKey, model, requestId, reference, message }) {
      const prompt = [
        "REQUEST_ID: " + requestId,
        "REFERENCE: " + (reference || ""),
        "",
        "Return the REQUEST_ID exactly at the start of your response.",
        "REQUEST:",
        message
      ].join("\n");
      const response = await fetch(
        "https://generativelanguage.googleapis.com/v1beta/models/" +
          encodeURIComponent(model || this.defaultModel) + ":generateContent",
        {
          method: "POST",
          credentials: "omit",
          cache: "no-cache",
          headers: {
            "Content-Type": "application/json",
            "x-goog-api-key": apiKey
          },
          body: JSON.stringify({
            contents: [{ role: "user", parts: [{ text: prompt }] }]
          })
        }
      );
      const raw = await response.text();
      if (!response.ok) throw new Error("Gemini HTTP " + response.status + ": " + raw);
      const data = JSON.parse(raw);
      const text = (data.candidates?.[0]?.content?.parts || [])
        .map(p => p.text || "").join("").trim();
      if (!text.startsWith("REQUEST_ID: " + requestId)) {
        throw new Error("Gemini response/request ID mismatch");
      }
      return text;
    }
  }
};

async function config() {
  return browser.storage.local.get({
    defaultProvider: "gemini",
    providers: {
      gemini: { enabled: true, model: PROVIDERS.gemini.defaultModel, apiKey: "" }
    }
  });
}

async function route(req) {
  if (!req || req.type !== "ONE_WAVE_AI_REQUEST") throw new Error("Bad request envelope");
  if (!/^[A-Za-z0-9._-]{1,120}$/.test(req.requestId || "")) throw new Error("Invalid request ID");
  if (!req.message || typeof req.message !== "string") throw new Error("Message required");
  const cfg = await config();
  const providerName = req.provider || cfg.defaultProvider;
  const adapter = PROVIDERS[providerName];
  const p = cfg.providers?.[providerName];
  if (!adapter || !p?.enabled) throw new Error("Provider unavailable: " + providerName);
  if (!p.apiKey) throw new Error(providerName.toUpperCase() + " API key is not configured");
  const startedAt = new Date().toISOString();
  const response = await adapter.call({
    apiKey: p.apiKey,
    model: p.model,
    requestId: req.requestId,
    reference: req.reference || "",
    message: req.message
  });
  const receipt = {
    schema: "one-wave-browser-ai-relay/v1",
    state: "RESPONSE",
    id: req.requestId,
    source: providerName,
    target: req.source || "chatgpt",
    reference: req.reference || "",
    response,
    ok: true,
    started_at: startedAt,
    completed_at: new Date().toISOString()
  };
  await browser.storage.local.set({ lastReceipt: receipt });
  return receipt;
}

browser.runtime.onMessage.addListener((message) => {
  if (message?.type === "ONE_WAVE_AI_REQUEST") {
    return route(message).catch(error => ({
      schema: "one-wave-browser-ai-relay/v1",
      state: "HOLD",
      id: message?.requestId || "",
      ok: false,
      error: error.message
    }));
  }
  if (message?.type === "ONE_WAVE_STATUS") {
    return config().then(c => ({
      ok: true,
      defaultProvider: c.defaultProvider,
      providers: Object.fromEntries(
        Object.entries(c.providers || {}).map(([k,v]) => [k, {enabled: !!v.enabled, configured: !!v.apiKey, model: v.model || ""}])
      )
    }));
  }
});
