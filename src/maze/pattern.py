from src.patterns.digit_patterns import DIGITS
from src.patterns.char_patterns import CHARS


def make_pattern(pattern_value):
    if pattern_value is None:
        return None

    # convert the input to a string
    s = str(pattern_value).lower()

    # if there is only 1 input
    if len(s) == 1:
        s = "0" + s

    # if it doesnt have 2 chars (more then 2), no pattern
    if len(s) != 2:
        return None

    # first char is left, second char is right
    left = s[0]
    right = s[1]

    # check if the left is in digits or chars or neither
    if left in DIGITS:
        left = DIGITS[left]
    elif left in CHARS:
        left = CHARS[left]
    else:
        return None

    # check if right is in digits or chars or neither
    if right in DIGITS:
        right = DIGITS[right]
    elif right in CHARS:
        right = CHARS[right]
    else:
        return None

    # make the pattern
    # first append the row of left-digit
    # then add a 0, empty
    # then append the row if the right-digit
    pattern = []
    for row in range(len(left)):
        pattern.append(left[row] + [0] + right[row])  # add a gap column

    return pattern


def mark_pattern(grid, pattern) -> None:

    # get the height & width of the grid
    # get the height & width of the pattern
    h = len(grid)
    w = len(grid[0])
    ph = len(pattern)
    pw = len(pattern[0])

    # there needs to be atleast 2 normal-maze-cells
    # around the pattern, or its jut not gonna do
    # the pattern
    if (h + 1) < ph or (w + 1) < pw:
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

                cell.walls = {
                    'N': True,
                    'E': True,
                    'S': True,
                    'W': True
                }

                cell.visited = True
                cell.pattern = True
