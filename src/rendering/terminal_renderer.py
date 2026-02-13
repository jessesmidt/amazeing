##########################################
#       Printer / Visuals
##########################################

# maze asci visuals
WALL = "██"
EMPTY = "  "

PATTERN_WALL = "▒▒"
PATTERN_EMPTY = "░░"

START_BLOCK = "\033[42m  \033[0m"
GOAL_BLOCK = "\033[41m  \033[0m"

def print_maze_ascii(grid):
    h = len(grid)
    w = len(grid[0])

    for y in range(h):

        # ── TOP (north walls)
        for x in range(w):
            cell = grid[y][x]

            wall_char = PATTERN_WALL if cell.pattern else WALL
            empty_char = PATTERN_EMPTY if cell.pattern else EMPTY

            print(wall_char, end="")

            if cell.walls['N']:
                print(wall_char, end="")
            else:
                print(empty_char, end="")

            print(wall_char, end="")
        print()

        # ── MIDDLE (west + interior + east)
        for x in range(w):
            cell = grid[y][x]

            wall_char = PATTERN_WALL if cell.pattern else WALL
            empty_char = PATTERN_EMPTY if cell.pattern else EMPTY

            if cell.walls['W']:
                print(wall_char, end="")
            else:
                print(empty_char, end="")

            if cell.is_start:
                content = START_BLOCK
            elif cell.is_goal:
                content = GOAL_BLOCK
            else:
                content = empty_char

            print(content, end="")

            if cell.walls['E']:
                print(wall_char, end="")
            else:
                print(empty_char, end="")
        print()

        # ── BOTTOM (south walls)
        for x in range(w):
            cell = grid[y][x]

            wall_char = PATTERN_WALL if cell.pattern else WALL
            empty_char = PATTERN_EMPTY if cell.pattern else EMPTY

            print(wall_char, end="")

            if cell.walls['S']:
                print(wall_char, end="")
            else:
                print(empty_char, end="")

            print(wall_char, end="")
        print()

