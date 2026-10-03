#!/usr/bin/env python3
"""Brain Buddy hard reference gate.

A worker process is never launched unless a validated reference packet contains
both conversation and repository reference. The worker receives the packet on
stdin; it never receives an ungated bare question.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any

REQUIRED_CONV = ("current_turns", "prior_turns", "human_corrections", "provenance")
REQUIRED_REPO = ("owning_repo", "canonical_start", "branch", "revision", "relevant_references")


class GateBlocked(RuntimeError):
    pass


def nonempty(v: Any) -> bool:
    if v is None: return False
    if isinstance(v, str): return bool(v.strip())
    if isinstance(v, (list, dict)): return bool(v)
    return True


def validate(packet: dict[str, Any]) -> None:
    errors: list[str] = []
    if packet.get("brain_buddy") is not True: errors.append("brain_buddy must be true")
    for k in ("request_id", "question"):
        if not nonempty(packet.get(k)): errors.append(f"missing {k}")
    conv = packet.get("conversation")
    repo = packet.get("repository")
    if not isinstance(conv, dict): errors.append("missing conversation reference")
    else:
        for k in REQUIRED_CONV:
            if not nonempty(conv.get(k)): errors.append(f"conversation.{k} missing")
    if not isinstance(repo, dict): errors.append("missing repository reference")
    else:
        for k in REQUIRED_REPO:
            if not nonempty(repo.get(k)): errors.append(f"repository.{k} missing")
    if errors: raise GateBlocked("; ".join(errors))


def canonical(packet: dict[str, Any]) -> bytes:
    return json.dumps(packet, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def main() -> int:
    ap = argparse.ArgumentParser(description="Brain Buddy reference gate")
    ap.add_argument("--packet", required=True, type=Path)
    ap.add_argument("--worker", nargs=argparse.REMAINDER,
                    help="worker command; validated packet is supplied on stdin")
    ap.add_argument("--validate-only", action="store_true")
    args = ap.parse_args()

    try:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        validate(packet)
    except (OSError, json.JSONDecodeError, GateBlocked) as exc:
        print(json.dumps({"gate":"BLOCKED","error":str(exc)}))
        return 2

    digest = hashlib.sha256(canonical(packet)).hexdigest()
    gate = {"gate":"OPEN","request_id":packet["request_id"],"reference_sha256":digest}

    if args.validate_only:
        print(json.dumps(gate))
        return 0
    if not args.worker:
        print(json.dumps({"gate":"BLOCKED","error":"no worker supplied"}))
        return 2

    # Critical boundary: only this path launches a worker, and only after validate().
    payload = {
        "brain_buddy_reference_gate": gate,
        "reference_packet": packet,
        "instruction": "Use only the supplied reference packet for project state. Return the same request_id and identify unresolved conflicts rather than guessing."
    }
    proc = subprocess.run(args.worker, input=json.dumps(payload), text=True)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
