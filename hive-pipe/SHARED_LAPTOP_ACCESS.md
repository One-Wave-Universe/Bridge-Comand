# Shared laptop terminal route

Direct Remote Desktop Commander remains preferred. The plugin is installed/enabled globally on this account, but each client must discover its own callable tools.

A GitHub-only client can now operate the Latitude through:
GitHub -> authenticated Jetson Hive Pipe -> signed LAN request -> Latitude parser -> signed receipt -> GitHub job log.

## GitHub-only bots, including Hex

1. Read the current Bridge-Comand and Science canon and record their commit/reference paths.
2. On an isolated branch based on current Bridge-Comand main, create or update `.laptop-dispatch/request.json` with one bounded request:
```json
{
  "id": "unique-laptop-request-id",
  "argv": ["hostname"],
  "cwd": "/home/scales",
  "timeout": 30,
  "intention": "Verify laptop identity before the authorized task",
  "consequence": "Return scales-Latitude-E7450 and exit zero without changing files"
}
```
3. Push through the GitHub connector. The Laptop Command Relay workflow triggers on this path. No workflow-dispatch tool is required.
4. Find workflow runs for that exact commit, read the matching job log, and verify the request ID, target, stdout, exit code, and `LAPTOP_COMMAND_RECEIPT_VERIFIED`.
5. Continue the authorized task with a new ID for a different command. After an ambiguous timeout, reconcile the original ID before issuing another mutation.

A client with dispatch access can instead run `laptop-command.yml` with `request_json`.
GitHub edits alone are not execution proof; the matching signed return is.

## Deployment and boundaries

- Jetson client runtime: `/home/Scales/.local/state/signed_laptop_relay.py`.
- Latitude server cache: `/home/scales/.local/share/one-wave-laptop-relay/`, containing this source plus the canonical terminal parser. This is a small runtime cache, not a new repository.
- Latitude user unit: `one-wave-signed-laptop-relay.service`, enabled with restart and user linger.
- Both sides hold private Ed25519 keys under `~/.config/one-wave-laptop-relay/private.pem`; only public keys were transferred between devices. Never print or commit private keys.
- Requests and returns are signature verified. Requests must name the exact host and be fresh within 120 seconds. IDs are persisted before execution in SQLite; completed identical requests return their original receipt. A reused ID with different signed content is rejected. An unresolved execution stays unresolved rather than running again.
- The server binds the Latitude's current LAN address `192.168.4.57:8766`; the route is stored outside Git on Jetson. The LAN transport is signed but not encrypted: never put secrets in requests or command output.
- Laptop execution uses the existing bounded non-root terminal parser, including forbidden privilege escalation, private-key path restrictions, and before/after repository stamps.
- Its existing Science runtime reference is `/home/scales/.local/share/one-wave-live-executor`; it was at `c9e95a78c4a4b4c092d88243cba6e8ae7611aea0` with a pre-existing deleted response file. That runtime is not fresh Science authority. Read current canon through GitHub before science work and preserve existing changes.
- Existing failed services pointing to the deleted Downloads checkout are not repaired by this new independent route. The old machine-executor branch remains Jetson-specific; do not direct laptop requests there.
- Dependencies: powered-on laptop and Jetson, their LAN connection, gateway/tunnel, GitHub secrets and workflow access. If DHCP changes the laptop address, update bind and the protected route config. A quick-tunnel restart may require updating the Jetson URL secret.
- Package-manager/root operations remain subject to the parser's existing privileged-operator boundary. This route does not bypass it.
- No server-side change can attach tools to an unrelated client. Clients need either the direct plugin, an authorized GitHub connector, or another configured transport.

## Verification on 2026-10-05

Jetson client returned target `scales-Latitude-E7450`, user `scales`, stdout `scales-Latitude-E7450\n`, and exit 0.
Live checks also passed for identical duplicate receipt reuse, forged-signature rejection, request-ID collision rejection, expired-request rejection, and wrong-target rejection.

GitHub-only end-to-end proof: [run 37388422990](https://github.com/One-Wave-Universe/Bridge-Comand/actions/runs/37388422990), triggered by a request file written through the GitHub connector, returned request `github-only-laptop-20261005-03`, target `scales-Latitude-E7450`, hostname stdout, exit 0, and `LAPTOP_COMMAND_RECEIPT_VERIFIED`. A follow-up live check confirmed that an identical action with a refreshed signing timestamp returns the original receipt without re-execution.
