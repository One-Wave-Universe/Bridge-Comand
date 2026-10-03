# DeepSeek Firefox input repair — prepared, not deployed

The observed relay at `192.168.55.100:3000` returned an upstream WebDriver
read timeout on localhost port 48359 after 120 seconds, including for a small
multiline marker. JSON-escaping the marker also timed out. This proves a browser
transport failure; it does not prove which WebDriver command is blocked.

`firefox_relay.py` preserves the inspected Jetson relay source, except that it
replaces character-by-character prompt typing with one native textarea value
update, dispatches input/change events and verifies exact readback before Enter.
It also removes the fallback that returned partial text after a response timeout.
This is a prepared input repair, not a claim that the currently stuck browser is
recovered. A stable text interval remains the inherited completion heuristic;
it is not an authenticated provider completion signal.

The original inspected source SHA-256 is
`dbf6a962d24b506aefe66c8ed0ad4c226e51f793cf01da51deb29d28fbc62365`.
The user-modified Science checkout file was not changed.

Three offline regression tests pass: complete large multiline/Unicode input is
inserted without character typing, a readback mismatch never submits, and a
changing partial answer at timeout raises rather than returning success.
These tests use a fake driver and do not prove the live site's event handling.

## Required live activation

Restore the Dell Desktop Commander connection. The computer is reachable for
relay HTTP requests but both Commander registrations are offline; SSH port 22,
Hive port 8765 and the observed WebDriver port are unavailable remotely.
No provider password, API key or copy/paste terminal operation is required from
the user for this repair.

The agent must then inspect the actual Dell service and source, preserve its
current profile and any user edits, compare with the inspected source, and apply
only the input/timeout delta. Restart only that relay's managed browser/service
to clear the stuck driver. Do not kill unrelated Firefox sessions or overwrite
the user's checkout. If source differs, start a fresh Reference cycle.

Prove exact marker responses for short, multiline and realistic 6000-character
pieces before launching another full-repository request. Finally verify that all
Builds segments and final synthesis succeed in the actual app runner, with full
coverage and CERN/GWOSC provenance. A health response or a short marker alone
does not establish full-loop verification.
