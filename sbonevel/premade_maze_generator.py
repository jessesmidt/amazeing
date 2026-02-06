

start = (1,1)
goal = (8,5)

width = 8
height = 8

N = 1
W = 2
S = 4
E = 8

grid = [
    [11, 0, 0, 0, 0, 0, 0, 0],
    [10, 0, 0, 15, 0, 3, 0, 0],
    [10, 0, 5, 0, 0, 15, 0, 0],
    [10, 0, 0, 0, 0, 0, 0, 0],
    [12, 5, 5, 5, 5, 0, 5, 3],
    [0, 0, 5, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 4, 4, 0, 0, 14],
]



MAX_CELL = N + W + S + E  # 15

# def make_full_wall_grid(width, height):
#     return [[MAX_CELL for _ in range(width)] for _ in range(height)]


# def make_grid(width, height):
#     grid = []

#     for y in range(height):
#         row = []
#         for x in range(width):
#             row.append(0)
#         grid.append(row)

#     return grid

# def add_outer_walls(grid):
#     h = len(grid)
#     w = len(grid[0])

#     for y in range(h):
#         for x in range(w):

#             if y == 0:
#                 grid[y][x] |= N

#             if y == h - 1:
#                 grid[y][x] |= S

#             if x == 0:
#                 grid[y][x] |= W

#             if x == w - 1:
#                 grid[y][x] |= E


def print_maze(grid):
    h = len(grid)
    w = len(grid[0])

    # Print the top border
    top = "┌" + "───┬" * (w - 1) + "───┐"
    print(top)

    for y in range(h):
        # Print vertical walls line
        line = ""
        for x in range(w):
            if grid[y][x] & W:
                line += "│"
            else:
                line += " "

            line += "   "

        # always end the line with right border
        line += "│"
        print(line)

        # Print horizontal wall line (between rows)
        if y < h - 1:
            line = ""
            for x in range(w):
                if grid[y][x] & S:
                    line += "───"
                else:
                    line += "   "

                if x < w - 1:
                    # intersections
                    line += "┼"
                else:
                    line += "┤"
            print("├" + line[:-1])  # add left border

    # Print bottom border
    bottom = "└" + "───┴" * (w - 1) + "───┘"
    print(bottom)







# grid = make_grid(width, height)
# grid = make_full_wall_grid(width, height)
# add_outer_walls(grid)
print_maze(grid)



