# One-Wave AI Hub — Firefox

Provider-neutral browser bridge. The popup is configuration only; the background
router handles provider calls while Firefox is running.

## v0.1 provider
- Gemini REST `generateContent`
- default model: `gemini-3.8-flash`
- API key sent only as the `x-goog-api-key` request header
- strict request ID validation
- local verified receipt

## Secret boundary
Provider keys live in Firefox extension `storage.local`. They are never written
to GitHub receipts and are never injected into webpage DOM. This is local
extension storage, not an Android Keystore; use a dedicated/restricted provider
key and revoke it if the Firefox profile/device is compromised.

## Request contract
Send a runtime message:
```json
{
  "type": "ONE_WAVE_AI_REQUEST",
  "requestId": "unique-id",
  "source": "chatgpt",
  "provider": "gemini",
  "reference": "https://github.com/One-Wave-Universe/Bridge-Comand",
  "message": "question"
}
```

The router returns a `one-wave-browser-ai-relay/v1` RESPONSE or HOLD envelope.

## Next adapters
OpenAI, Anthropic/Claude, xAI/Grok, DeepSeek and other providers belong behind
the same adapter boundary. Each new provider must add only its required host
permission and adapter; the request/receipt contract stays unchanged.

## Firefox note
Manifest V3 background scripts are event-driven/non-persistent. Durable state is
kept in `storage.local`, so the popup can be closed without losing provider
configuration.
