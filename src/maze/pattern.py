from src.patterns.digit_patterns import DIGITS
from src.patterns.char_patterns import CHARS
from .generator import Cell


def make_pattern(pattern_value: str) -> list[list[int]] | None:
    """
    Initializes the pattern chars, creates a list of strings
    which we can return to the maze generator
    """
    if pattern_value is None:
        return None

    # convert the input to a string
    s = str(pattern_value).lower()

    # if there is only 1 input, add char. Else return None.
    if len(s) == 1:
        s = "0" + s
    if len(s) != 2:  # add a gap column [0]
        return None

    # first char is left, second char is right
    left_char = s[0]
    right_char = s[1]

    # check if they're in digits, chars or neither
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

    # make a list called pattern
    # first append the row of left-digit
    # then add a 0, empty
    # then append the row if the right-digit
    pattern: list[list[int]] = []

    for row in range(len(left_pattern)):
        pattern.append(left_pattern[row] + [0] + right_pattern[row])

    return pattern


def mark_pattern(grid: list[list[Cell]], pattern: list) -> None:
    # get the height & width of the grid
    # get the height & width of the pattern
    h = len(grid)
    w = len(grid[0])
    ph = len(pattern)
    pw = len(pattern[0])

    # there needs to be atleast 2 normal-maze-cells
    # around the pattern, or its just not gonna do
    # the pattern
    if (h + 1) < ph or (w + 1) < pw:
        input(
            "Warning: Maze too small for '42' pattern (min 9x7)."
            "\nPress Enter to continue..."
            )
        return

    # looks for the coords
    start_x = (w - pw) // 2
    start_y = (h - ph) // 2

    for py in range(ph):
        for px in range(pw):
            if pattern[py][px] == 1:
                grid_x = start_x + px
                grid_y = start_y + py

                cell = grid[grid_y][grid_x]

                if cell.is_start:
                    raise ValueError(
                        "Pattern overlaps with entry at ({grid_x}, {grid_y})"
                        )
                elif cell.is_goal:
                    raise ValueError(
                        "Pattern overlaps with exit at ({grid_x}, {grid_y})"
                        )

                cell.walls = {
                    'N': True,
                    'E': True,
                    'S': True,
                    'W': True
                }

                cell.visited = True
                cell.pattern = True

            # extra flag for cells stuck inside patterns
            if pattern[py][px] == 2:
                grid_x = start_x + px
                grid_y = start_y + py

                cell = grid[grid_y][grid_x]

                if cell.is_start:
                    raise ValueError(
                        f"Pattern overlaps with entry at ({grid_x}, {grid_y})"
                        )
                elif cell.is_goal:
                    raise ValueError(
                        f"Pattern overlaps with exit at ({grid_x}, {grid_y})"
                        )

                cell.visited = True
