"""Entry point to run the parser over the bundled input.

This script reads instructions from ``input.txt`` in the repository root
and prints the resulting position and wrap count produced by ``parser``.
"""

from __future__ import annotations

from pathlib import Path

from parser import process_file

INPUT_PATH = Path(__file__).with_name("input.txt")


def main() -> None:
    position, count = process_file(INPUT_PATH)
    print(f"Final position: {position}")
    print(f"Zero-crossings count: {count}")


if __name__ == "__main__":
    main()
