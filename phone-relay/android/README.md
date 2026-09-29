# One-Wave Relay Android app

Minimal phone worker for the existing One-Wave relay contract.

## What it does

1. Stores one stable request ID and GitHub reference.
2. Builds the canonical request envelope.
3. Uses Android ACTION_SEND to hand the request to Gemini.
4. Receives text shared back into One-Wave Relay.
5. Rejects a response unless it contains the exact request ID.
6. Creates a SHA-256 receipt and shares it back to ChatGPT or another target.

No Jetson, SSH, inbound listener, or GitHub Actions are in the live AI message path.

## Build

Open `phone-relay/android` in Android Studio and build/install the `app` debug variant.

CLI on a machine with Android SDK/Gradle:

```bash
cd phone-relay/android
gradle :app:assembleDebug
```

Acceptance remains a real Gemini reply with the matching request ID, followed by a verified receipt.
