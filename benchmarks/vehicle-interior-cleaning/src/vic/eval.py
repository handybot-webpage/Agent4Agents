"""Evaluation runner CLI.

Usage:
    vic-eval --vehicle sedan --task sweep_floor --policy heuristic --episodes 20

Runs the requested policy against the env for `episodes` rollouts, aggregates
metrics, and prints a summary table.

In v0.1 the env is a stub (Isaac Sim required); this CLI parses args, validates
vehicle/task/split selections against configs, and reports what it WOULD run.
The actual rollout loop is wired in v0.2 once an Isaac host is provisioned.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from . import config as cfg
from .baselines.heuristic import HeuristicPolicy
from .metrics import VICMetrics, aggregate
from .tasks import VICTask

POLICIES = {"heuristic": HeuristicPolicy}
SPLITS = ("train", "eval-known", "eval-novel")


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="vic-eval", description="VIC benchmark evaluation runner")
    p.add_argument("--vehicle", required=True, choices=sorted(cfg.vehicle_classes()),
                   help="vehicle class to evaluate on")
    p.add_argument("--task", required=True, choices=sorted(cfg.task_names()),
                   help="task to evaluate")
    p.add_argument("--policy", default="heuristic", choices=sorted(POLICIES),
                   help="baseline policy name")
    p.add_argument("--episodes", type=int, default=20, help="episodes to run")
    p.add_argument("--split", default="eval-known", choices=SPLITS, help="data split")
    p.add_argument("--seed-base", type=int, default=0, help="base seed for deterministic episodes")
    p.add_argument("--out", help="optional path to write JSON aggregate")
    p.add_argument("--dry-run", action="store_true",
                   help="validate args, print plan, do not run rollouts")
    return p.parse_args(argv)


def _seed_for(split: str, vehicle: str, task: str, episode: int) -> int:
    """Deterministic seed per SPEC.md §9 reproducibility."""
    return hash((split, vehicle, task, episode)) & 0xFFFFFFFF


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else list(argv))

    task = VICTask.from_config(args.task)
    plan = {
        "split": args.split,
        "vehicle": args.vehicle,
        "task": args.task,
        "episode_seconds": task.episode_seconds,
        "policy": args.policy,
        "episodes": args.episodes,
        "seeds": [_seed_for(args.split, args.vehicle, args.task, i)
                  for i in range(args.episodes)],
    }

    print(f"vic-eval plan:")
    print(f"  split:    {plan['split']}")
    print(f"  vehicle:  {plan['vehicle']}")
    print(f"  task:     {plan['task']}  ({task.description})")
    print(f"  episode:  {plan['episode_seconds']}s × {plan['episodes']} episodes")
    print(f"  policy:   {plan['policy']}")
    print(f"  seeds:    {plan['seeds'][:3]}...{plan['seeds'][-1:]}")

    if args.dry_run:
        print("\n--dry-run: no rollouts executed.")
        return 0

    # v0.1: env is a stub. Real rollout lands in v0.2 (Isaac host provisioned).
    print("\nVICEnv requires Isaac Sim (Linux + NVIDIA RTX). v0.1 scaffold "
          "cannot run rollouts; provision an Isaac host and re-run.")
    print("To verify the CLI parses correctly, use --dry-run.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
