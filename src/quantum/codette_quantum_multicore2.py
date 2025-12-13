"""Utility for performing meta analysis on .cocoon files.

This module aggregates quantum and chaos states from saved cocoon files and
visualises the resulting "dream space".  The original script was written in a
monolithic style.  It has been refactored into smaller functions for easier
maintenance and testing.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Iterable, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

LOG = logging.getLogger(__name__)


def _configure_logging(level: str) -> None:
    """Configure global logging."""
    numeric = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        filename="meta_analysis.log",
        level=numeric,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def simple_neural_activator(
    quantum_vec: Iterable[float], chaos_vec: Iterable[float]
) -> int:
    """Return 1 if the combined variance of inputs exceeds a threshold."""
    q_sum = sum(quantum_vec)
    c_var = np.var(list(chaos_vec))
    return int(q_sum + c_var > 1)


def codette_dream_agent(
    quantum_vec: Iterable[float], chaos_vec: Iterable[float]
) -> Tuple[List[float], List[float]]:
    """Generate dream-state vectors based on the provided states."""
    dream_q = [np.sin(q * np.pi) for q in quantum_vec]
    dream_c = [np.cos(c * np.pi) for c in chaos_vec]
    return dream_q, dream_c


def philosophical_perspective(qv: Iterable[float], cv: Iterable[float]) -> str:
    """Provide a whimsical philosophical label for the states."""
    m = max(qv) + max(cv)
    if m > 1.3:
        return "Philosophical Note: This universe is likely awake."
    return "Philosophical Note: Echoes in the void."


def load_cocoon(path: Path) -> dict | None:
    """Synchronously load a single cocoon file with error handling."""
    try:
        with path.open() as f:
            data = json.load(f)
        if not isinstance(data, dict) or "data" not in data:
            raise ValueError("Invalid cocoon schema")
        LOG.debug("Loaded cocoon %s", path)
        return data["data"]
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        LOG.warning("Failed to load %s: %s", path, exc)
        return None


async def load_cocoon_async(path: Path) -> dict | None:
    """Asynchronously load a cocoon using a thread executor."""
    return await asyncio.to_thread(load_cocoon, path)


def analyse_cocoons(folder: Path) -> List[dict]:
    """Analyse cocoon files synchronously."""
    meta_mutations: List[dict] = []

    print("\nMeta Reflection Table:\n")
    header = (
        "Cocoon File | Quantum State | Chaos State | Neural | Dream Q/C | Philosophy"
    )
    print(header)
    print("-" * len(header))

    for path in folder.glob("*.cocoon"):
        try:
            data = load_cocoon(path)
            if data is None:
                continue
            q = data.get("quantum_state", [0, 0])
            c = data.get("chaos_state", [0, 0, 0])
            neural = simple_neural_activator(q, c)
            dream_q, dream_c = codette_dream_agent(q, c)
            phil = philosophical_perspective(q, c)
            entry = {
                "dreamQ": dream_q,
                "dreamC": dream_c,
                "neural": neural,
                "philosophy": phil,
            }
            meta_mutations.append(entry)
            msg = f"{path.name} | {q} | {c} | {neural} | {dream_q}/{dream_c} | {phil}"
            print(msg)
            logging.info(msg)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Warning: {path.name} failed ({exc})")

    return meta_mutations


async def analyse_cocoons_async(folder: Path) -> List[dict]:
    """Asynchronously analyse cocoon files in parallel."""
    meta_mutations: List[dict] = []

    print("\nMeta Reflection Table:\n")
    header = (
        "Cocoon File | Quantum State | Chaos State | Neural | Dream Q/C | Philosophy"
    )
    print(header)
    print("-" * len(header))

    tasks = [load_cocoon_async(p) for p in folder.glob("*.cocoon")]

    for coro in asyncio.as_completed(tasks):
        try:
            data = await coro
            if data is None:
                continue
            q = data.get("quantum_state", [0, 0])
            c = data.get("chaos_state", [0, 0, 0])
            neural = simple_neural_activator(q, c)
            dream_q, dream_c = codette_dream_agent(q, c)
            phil = philosophical_perspective(q, c)
            entry = {
                "dreamQ": dream_q,
                "dreamC": dream_c,
                "neural": neural,
                "philosophy": phil,
            }
            meta_mutations.append(entry)
            msg = f"async | {q} | {c} | {neural} | {dream_q}/{dream_c} | {phil}"
            print(msg)
            logging.info(msg)
        except Exception as exc:  # pylint: disable=broad-except
            logging.warning("async load failed: %s", exc)

    return meta_mutations


def plot_meta_dream(meta_mutations: List[dict]) -> bool:
    """Plot dream scatter. Return True if plotted."""
    if not meta_mutations:
        msg = "No valid cocoons found for meta-analysis."
        print(msg)
        LOG.info(msg)
        return False

    dq0 = [m["dreamQ"][0] for m in meta_mutations]
    dc0 = [m["dreamC"][0] for m in meta_mutations]
    ncls = [m["neural"] for m in meta_mutations]

    plt.figure(figsize=(8, 6))
    sc = plt.scatter(dq0, dc0, c=ncls, cmap="spring", s=100)
    plt.xlabel("Dream Quantum[0]")
    plt.ylabel("Dream Chaos[0]")
    plt.title("Meta-Dream Codette Universes")
    plt.colorbar(sc, label="Neural Activation Class")
    plt.grid(True)
    plt.show()
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse Codette cocoon files")
    parser.add_argument(
        "folder", nargs="?", default=".", help="Folder containing .cocoon files"
    )
    parser.add_argument(
        "--async", dest="use_async", action="store_true", help="Use async loading"
    )
    parser.add_argument(
        "--philosophy-only",
        dest="philo_only",
        action="store_true",
        help="Only output philosophical notes",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ...)",
    )
    args = parser.parse_args()

    _configure_logging(args.log_level)

    if "COCOON_FOLDER" in os.environ and args.folder != ".":
        LOG.info(
            "Using folder %s (COCOON_FOLDER overrides positional %s)",
            os.environ["COCOON_FOLDER"],
            args.folder,
        )
    folder = Path(os.getenv("COCOON_FOLDER", args.folder))

    if args.use_async:
        meta_mutations = asyncio.run(analyse_cocoons_async(folder))
    else:
        meta_mutations = analyse_cocoons(folder)

    if args.philo_only:
        for m in meta_mutations:
            print(m["philosophy"])
        if not meta_mutations:
            raise SystemExit(1)
        return
    if not plot_meta_dream(meta_mutations):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
