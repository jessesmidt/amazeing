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
PATH_BLOCK = "\033[44m  \033[0m"



def print_maze_ascii(grid):
    h = len(grid)
    w = len(grid[0])

    for y in range(h):

        # ── TOP (north walls)
        for x in range(w):
            cell = grid[y][x]

            # NW corner
            if cell.pattern:
                print(PATTERN_WALL, end="")
            else:
                print(WALL, end="")

            # north corridor
            if cell.walls["N"]:
                if cell.pattern:
                    print(PATTERN_WALL, end="")
                else:
                    print(WALL, end="")
            else:
                # no wall: check if both cells are in the path
                if y > 0 and cell.in_path and grid[y-1][x].in_path:
                    print(PATH_BLOCK, end="")
                else:
                    if cell.pattern:
                        print(PATTERN_EMPTY, end="")
                    else:
                        print(EMPTY, end="")

            # NE corner
            if cell.pattern:
                print(PATTERN_WALL, end="")
            else:
                print(WALL, end="")

        print()

        # ── MIDDLE (west + interior + east)
        for x in range(w):
            cell = grid[y][x]

            # west corridor
            if cell.walls["W"]:
                if cell.pattern:
                    print(PATTERN_WALL, end="")
                else:
                    print(WALL, end="")
            else:
                if x > 0 and cell.in_path and grid[y][x-1].in_path:
                    print(PATH_BLOCK, end="")
                else:
                    if cell.pattern:
                        print(PATTERN_EMPTY, end="")
                    else:
                        print(EMPTY, end="")

            # center content
            if cell.is_start:
                print(START_BLOCK, end="")
            elif cell.is_goal:
                print(GOAL_BLOCK, end="")
            elif cell.in_path:
                print(PATH_BLOCK, end="")
            else:
                if cell.pattern:
                    print(PATTERN_EMPTY, end="")
                else:
                    print(EMPTY, end="")

            # east corridor
            if cell.walls["E"]:
                if cell.pattern:
                    print(PATTERN_WALL, end="")
                else:
                    print(WALL, end="")
            else:
                if x < w - 1 and cell.in_path and grid[y][x+1].in_path:
                    print(PATH_BLOCK, end="")
                else:
                    if cell.pattern:
                        print(PATTERN_EMPTY, end="")
                    else:
                        print(EMPTY, end="")

        print()

        # ── BOTTOM (south walls)
        for x in range(w):
            cell = grid[y][x]

            # SW corner
            if cell.pattern:
                print(PATTERN_WALL, end="")
            else:
                print(WALL, end="")

            # south corridor
            if cell.walls["S"]:
                if cell.pattern:
                    print(PATTERN_WALL, end="")
                else:
                    print(WALL, end="")
            else:
                if y < h - 1 and cell.in_path and grid[y+1][x].in_path:
                    print(PATH_BLOCK, end="")
                else:
                    if cell.pattern:
                        print(PATTERN_EMPTY, end="")
                    else:
                        print(EMPTY, end="")

            # SE corner
            if cell.pattern:
                print(PATTERN_WALL, end="")
            else:
                print(WALL, end="")

        print()


