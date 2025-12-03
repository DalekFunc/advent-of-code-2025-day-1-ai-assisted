from parser import (
    CYCLE,
    START_POSITION,
    parse_instruction,
    process_file,
    process_instructions,
)


def test_process_file_counts_resets(tmp_path):
    input_text = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""
    input_path = tmp_path / "input.txt"
    input_path.write_text(input_text, encoding="utf-8")

    position, count = process_file(input_path)

    assert position == 32
    assert count == 3


def test_parse_and_reduce_directly():
    moves = [parse_instruction(token) for token in ["L1", "R2", "L2", "R1"]]
    position, count = process_instructions(moves)
    assert position == (START_POSITION - 1 + 2 - 2 + 1) % CYCLE
    assert count == 0
