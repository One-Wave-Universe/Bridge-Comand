# Council Chamber: Choice, Re-reference, Reset, and Interrupt Model

Status: architecture rule; implementation pending verification.

## Primitive
A loop does not seek a globally correct choice. It resolves a choice from its own current differential state.

VIEW -> WEIGH -> CHOOSE -> ACT/HOLD -> CONSEQUENCE -> NEW VIEW

Reference supplies views; it does not own the choice.

## Choice modes
A loop may choose to WATCH, MOVE, WORK, TALK, THINK-HARD, HOLD, RE-REFERENCE, or RESET.

THINK-HARD closes the active inner loop to ordinary external input. Incoming work is buffered until the boundary opens. This is a state boundary, not a wall against critical interrupts.

## Internal dialogue
Internal dialogue is another nested loop. It performs differential weighing, assumption checking, memory/reference comparison, and choice. It is not an automatic "ask another worker" step.

## Asynchronous Council
Council members do not synchronize on a round or wait for consensus.

If Gemini resolves while DeepSeek is still thinking, Gemini and ChatGPT may branch into a dialogue. DeepSeek continues independently. If DeepSeek later resolves while the recipient is inside another closed loop, its result waits at that boundary. When admitted, it is a new VIEW, not a retroactive vote.

No provider owns the clock. Pending work must not be fabricated.

## Weight of time
Unresolved state has history. Weight may change while a thought remains unresolved and while other branches develop around it. Do not reduce this to an application timeout.

## Interrupt channel
Closed loops admit exceptional interrupts for:
- reference drift;
- destructive rewrite/delete or threat to a known-good state;
- a contradiction that invalidates an active premise;
- safety/resource/credential/data danger;
- detected behavior-loop failure, including repeated explanation without execution when executable work exists.

An interrupt does not dictate the choice. It forces a VIEW boundary.

## Re-reference
A loop may choose RE-REFERENCE when its active state has drifted, assumptions are stale, or it is losing the baseline. Re-reference returns to Baseline Zero / owning repo / canon and reconstructs the current state before continuing.

## Reset
RESET is a valid choice when the loop itself has become unproductive. Reset means:
1. checkpoint useful unresolved state;
2. discard transient conversational/action state that is causing the loop;
3. re-enter from the last known reference/hard stop;
4. VIEW current evidence again;
5. make a new choice.

Reset is not destructive rollback of canonical work and must not erase receipts or known-good state.

## Action-drift watchdog
The system must distinguish explaining from doing. When the current goal is executable and the loop repeatedly produces narration without taking an available action, raise ACTION_DRIFT. ACTION_DRIFT opens the boundary and offers RE-REFERENCE or RESET as choices.

## Repository protection
Known-good states are hard stops. New work branches from them. Destructive rewrite is an interrupt-class event. Never silently replace canonical state merely to resolve a conflict.

## Recursive scale
These rules recur at internal-dialogue, individual, branch/squadron, Council, and community scale. Higher scale does not erase local choice.
