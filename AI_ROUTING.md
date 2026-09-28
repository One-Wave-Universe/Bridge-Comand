# AI Routing — Start Here

AI agents working in this repository must use the One-Wave Device Lattice rather than stopping at an unavailable local listener.

Read, in order:
1. `AI_BRIDGE_START_HERE.md`
2. `DEVICE_LATTICE.md`
3. `GITHUB_DEVICE_CONTROL_PLANE.md`
4. `METADATA_AND_HANDOFF_CONTRACT.md`
5. `PHONE_BRIDGE_PROFILE.md` when phone-originated
6. `PHONE_GITHUB_JETSON.md` for immediate phone→machine work
7. `chatgpt-plugin/one-wave-hive-pipe/skills/bridge-control/SKILL.md`

## AI route behavior

For every cross-device task:
- determine source node and target node;
- create/preserve one stable request ID;
- preserve canon, provenance, assumption/transformation IDs and limits;
- use a healthy direct route when available;
- otherwise use GitHub as the durable control plane;
- otherwise queue/store-and-forward under the same request ID;
- record failures as receipts;
- after three equivalent failures switch route/angle;
- do not ask the human to babysit a listener when another authorized route exists;
- do not claim execution until the final target returns a matching receipt.

Phone, laptop and Jetson are peers in the routing lattice. Laptop and Jetson may be execution workers. Phone is primarily a control/client endpoint but may originate files/sensor captures with provenance.

Never expose tokens, weaken authentication, or turn “open lattice” into unauthenticated shell access.
