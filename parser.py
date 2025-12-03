"""Utilities for parsing directional integers and tracking position."""

from __future__ import annotations

from functools import reduce
from pathlib import Path
from typing import Iterable, Tuple

CYCLE = 100
START_POSITION = 50


def parse_instruction(raw: str) -> int:
    """
    Convert a raw instruction like 'L68' or 'R10' into a signed integer.

    The first character determines the sign. 'L' is negative, 'R' is positive.
    """
    token = raw.strip()
    if not token:
        raise ValueError("Empty instruction")

    direction = token[0].upper()
    if direction not in {"L", "R"}:
        raise ValueError(f"Invalid instruction prefix: {token}")

    try:
        magnitude = int(token[1:])
    except ValueError as exc:
        raise ValueError(f"Invalid numeric value in instruction: {token}") from exc

    return -magnitude if direction == "L" else magnitude


def _step(state: Tuple[int, int], delta: int) -> Tuple[int, int]:
    """Apply a single delta to the running (position, count) pair."""
    position, count = state
    new_position = (position + delta) % CYCLE
    new_count = count + (1 if new_position == 0 else 0)
    return new_position, new_count


def process_instructions(moves: Iterable[int]) -> Tuple[int, int]:
    """
    Run all moves through the reducer and return the final (position, count).

    count increments each time the wrapped position becomes zero.
    """
    return reduce(_step, moves, (START_POSITION % CYCLE, 0))


def process_file(path: str | Path) -> Tuple[int, int]:
    """Read instructions from a file and return the final (position, count)."""
    raw_lines = Path(path).read_text(encoding="utf-8").splitlines()
    moves = [parse_instruction(line) for line in raw_lines if line.strip()]
    return process_instructions(moves)
