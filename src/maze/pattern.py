from src.patterns.digit_patterns import DIGITS
from src.patterns.char_patterns import CHARS
from .generator import Cell
import sys
import time


def make_pattern(pattern_value: str) -> list[list[int]] | None:
    """
    Build a 2D pattern grid from a one- or two-character string.

    Looks up each character in the DIGITS or CHARS maps and combines
    them side by side with an empty column in between. If only one
    character is given, '0' is prepended automatically.

    Args:
        pattern_value: A one- or two-character string (e.g. "42", "ab", "4").

    Returns:
        A 2D list of integers representing the combined pattern,
        or None if the input is invalid or contains unrecognised characters.
    """
    s = str(pattern_value).lower()
    if len(s) == 1:
        s = "0" + s
    if len(s) != 2:
        return None

    left_char = s[0]
    right_char = s[1]

    if left_char in DIGITS:
        left_pattern = DIGITS[left_char]
    elif left_char in CHARS:
        left_pattern = CHARS[left_char]
    else:
        return None

    if right_char in DIGITS:
        right_pattern = DIGITS[right_char]
    elif right_char in CHARS:
        right_pattern = CHARS[right_char]
    else:
        return None

    pattern: list[list[int]] = []
    for row in range(len(left_pattern)):
        pattern.append(left_pattern[row] + [0] + right_pattern[row])

    return pattern


def mark_pattern(grid: list[list[Cell]], pattern: list[list[int]]) -> None:
    """
    Mark cells in the grid as part of a visual pattern (e.g. "42").

    Centers the pattern on the grid and marks matching cells accordingly.
    Cells marked with 1 in the pattern are fully walled and excluded from
    maze generation. Cells marked with 2 are only marked as visited,
    acting as interior filler cells inside the pattern.

    Args:
        grid: 2D list of Cell objects representing the maze.
        pattern: 2D list of integers where 1 marks a pattern wall cell,
                 2 marks an interior filler cell, and 0 is ignored.

    Raises:
        ValueError: If the pattern overlaps with the entry or exit cell.
    """
    h = len(grid)
    w = len(grid[0])
    ph = len(pattern)
    pw = len(pattern[0])

    if (h + 1) < ph or (w + 1) < pw:
        print("Warning: Maze too small for '42' pattern", file=sys.stderr)
        time.sleep(3)
        return

    start_x = (w - pw) // 2
    start_y = (h - ph) // 2

    for py in range(ph):
        for px in range(pw):
            value = pattern[py][px]
            if value not in (1, 2):
                continue

            grid_x = start_x + px
            grid_y = start_y + py
            cell = grid[grid_y][grid_x]

            if cell.is_start:
                raise ValueError(
                    f"Pattern overlaps with entry at ({grid_x}, {grid_y})"
                )
            if cell.is_goal:
                raise ValueError(
                    f"Pattern overlaps with exit at ({grid_x}, {grid_y})"
                )

            cell.visited = True

            if value == 1:
                cell.walls = {'N': True, 'E': True, 'S': True, 'W': True}
                cell.pattern = True
