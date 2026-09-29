const $ = id => document.getElementById(id);
async function load() {
  const cfg = await browser.storage.local.get({
    defaultProvider: "gemini",
    providers: { gemini: { enabled: true, model: "gemini-3.8-flash", apiKey: "" } }
  });
  $("defaultProvider").value = cfg.defaultProvider;
  $("geminiEnabled").checked = !!cfg.providers.gemini.enabled;
  $("geminiModel").value = cfg.providers.gemini.model || "gemini-3.8-flash";
  $("geminiKey").value = cfg.providers.gemini.apiKey || "";
  $("status").textContent = cfg.providers.gemini.apiKey ? "Gemini key configured." : "Gemini key not configured.";
}
async function save() {
  const old = await browser.storage.local.get({providers:{}});
  const providers = {...old.providers, gemini:{
    enabled:$("geminiEnabled").checked,
    model:$("geminiModel").value.trim() || "gemini-3.8-flash",
    apiKey:$("geminiKey").value.trim()
  }};
  await browser.storage.local.set({defaultProvider:$("defaultProvider").value,providers});
  $("status").textContent="Saved locally in this Firefox profile.";
}
async function test() {
  await save();
  $("status").textContent="Testing...";
  const id="hub-test-"+Date.now();
  const receipt=await browser.runtime.sendMessage({
    type:"ONE_WAVE_AI_REQUEST",requestId:id,source:"popup",provider:"gemini",
    reference:"https://github.com/One-Wave-Universe/Bridge-Comand",
    message:"Reply in one short sentence confirming the One-Wave AI Hub transport test."
  });
  $("status").textContent=receipt.ok ? "PASS\n"+receipt.response : "HOLD\n"+receipt.error;
}
$("save").addEventListener("click",save);
$("test").addEventListener("click",test);
load();
