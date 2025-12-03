"""Utilities for parsing directional integers and tracking position."""

from __future__ import annotations

from functools import reduce
from pathlib import Path
from typing import Callable, Iterable, Tuple

CYCLE = 100
START_POSITION = 50

State = Tuple[int, int]
StepFn = Callable[[State, int], State]


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


def _step(state: State, delta: int) -> State:
    """Apply a single delta to the running (position, count) pair."""
    position, count = state
    new_position = (position + delta) % CYCLE
    new_count = count + (1 if new_position == 0 else 0)
    return new_position, new_count


def _step_with_delta(state: State, delta: int) -> State:
    """
    Alternative step that also factors in the cycle-scaled delta.

    Besides counting zero crossings, this variant adds ``delta / CYCLE`` (truncated
    toward zero) to the running count so that large moves contribute additional
    cycles.
    """
    position, count = state
    new_position = (position + delta) % CYCLE
    wrap_bonus = 1 if new_position == 0 else 0
    delta_bonus = int(delta / CYCLE)
    return new_position, count + wrap_bonus + delta_bonus


def _reduce_moves(moves: Iterable[int], step: StepFn) -> State:
    """Helper that runs the reducer with the provided step function."""
    return reduce(step, moves, (START_POSITION % CYCLE, 0))


def process_instructions(moves: Iterable[int]) -> Tuple[int, int]:
    """
    Run all moves through the reducer and return the final (position, count).

    count increments each time the wrapped position becomes zero.
    """
    return _reduce_moves(moves, _step)


def process_instructions_with_delta(moves: Iterable[int]) -> Tuple[int, int]:
    """
    Run moves with the alternative step that includes the delta-based bonus.
    """
    return _reduce_moves(moves, _step_with_delta)


def process_file(path: str | Path) -> Tuple[int, int]:
    """Read instructions from a file and return the final (position, count)."""
    raw_lines = Path(path).read_text(encoding="utf-8").splitlines()
    moves = [parse_instruction(line) for line in raw_lines if line.strip()]
    return process_instructions(moves)
