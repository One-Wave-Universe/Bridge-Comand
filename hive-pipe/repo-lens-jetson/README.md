# Repo Lens Jetson route

This transport lives in Bridge-Comand. Builds owns the loop runner; One-Wave-Science owns interpretation and evidence contracts. The service reads public science metadata and sends visible prompts to the previously responding free DeepSeek Firefox relay. It exposes no shell or repository-write operation.

GitHub Actions authenticates with a short-lived, signed OIDC identity. The gateway verifies GitHub's RSA signature, audience, owner, repository, exact feature branch, exact workflow path, push event and expiry. There is no persistent gateway key to copy into GitHub or publish. The server listens only on Jetson loopback behind a separate Cloudflare tunnel.

`/metadata` permits read-only CERN Open Data, HEPData, GWOSC/LIGO/Virgo/KAGRA, MAST, HEASARC and Gaia metadata URLs. Every AI uses this same route after repository reference. It preserves unchanged source JSON, endpoint, retrieval time, byte count, headers and SHA-256. It does not silently truncate, manufacture units or turn metadata into detector measurements. This access covers the registered pipeline families, not a claim to have downloaded every archive record. Provider pagination remains explicit.

`/chat` uses the free web relay at the existing private-network address. Only actual visible responses count. Vendor model identity may be unexposed and remains labeled accordingly. Existing relay, gateway, checkout and laptop files are preserved. The named runtime cache holds these few transport files, never a repository clone.

New user units: repo-lens-jetson.service and repo-lens-tunnel.service. Cloudflare quick-tunnel hostname can change after tunnel restart; update Builds/repo-lens/jetson-endpoint.json and the app configuration if it changes. A stale route yields HOLD rather than a simulated answer.

The `/chat` actor field selects DEEPSEEK, GPT, CLAUDE or GROK. GPT uses the official pinned Codex 0.160.0 client and its ChatGPT sign-in on this Jetson, with a read-only, ephemeral invocation. Its matching transport test completed on 2026-10-03 with thread `01a101a5-0b62-7321-9a51-f6de5c947108`. DeepSeek's matching free-web test returned `webrelay-6d4021d7db8c4f88812605d2fe675cb8`. Those tests prove model transport, not app loop activation or scientific interpretation.

Claude's official pinned 2.1.288 client is installed but was not signed in at inspection. Its adapter remains UNVERIFIED until authentication and a matching visible response. Grok's official Responses API adapter requires a locally supplied XAI_API_KEY; no authenticated route was found and no response has been fabricated. Missing authentication fails only that actor. Actor locks are separate; no actor holds the metadata route or another provider's lock.

Clients must use the Repo Lens MCP bootstrap automatically, reference current Git instructions, and execute authorized terminal work through their connected Remote Desktop Commander or Hive Pipe tools. Do not require the user to relay commands or output. Account authorization is the remaining human step where a provider requires it; credentials stay off Git and out of receipts.
