# Phone → GitHub → Jetson

This is the preferred phone control route.

## Path

`PHONE → GITHUB → GITHUB ACTIONS → AUTHENTICATED HIVE PIPE GATEWAY → JETSON → ACTION LOG/RECEIPT → PHONE`

GitHub is the durable public control plane. The phone does not need LAN access, SSH, localhost access, an inbound port, or a persistent background process.

## Phone operation

From GitHub mobile/web:
1. Open Bridge-Comand.
2. Open **Actions → Jetson Command Lane**.
3. Choose **Run workflow**.
4. Supply a bounded `argv_json` or simple `command`, plus intention/consequence.
5. Run it.
6. Read the resulting Action log/receipt from the phone.

The workflow runs on a GitHub-hosted runner and calls the authenticated Hive Pipe gateway. The gateway token remains a GitHub secret and is never entered on the phone.

## Proof

A green GitHub-hosted workflow alone proves only the GitHub portion unless its command step contains a Jetson result.

End-to-end PASS requires the Action log to show the Jetson terminal result, including exit code and expected output.

## Safe phone smoke test

Use a harmless command such as:

`argv_json: ["uname","-a"]`

Intention: `Verify phone→GitHub→Jetson command route.`

Consequence: `Read system identity only; make no machine changes.`

## Offline behavior

If the Jetson gateway is unreachable, the Action fails visibly and preserves the failure log. The phone remains able to inspect/retry through GitHub. Do not reinterpret a failed Action as successful execution.

For durable deferred work, use the phone store-and-forward contract; for immediate machine execution, use Jetson Command Lane.
