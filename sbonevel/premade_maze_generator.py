
import random


start = (1,1)
goal = (8,5)

width = 10
height = 10

N = 1
W = 2
S = 4
E = 8

# grid = [
#     [11, 0, 0, 0, 0, 0, 0, 0],
#     [10, 0, 0, 15, 0, 3, 0, 0],
#     [10, 0, 5, 0, 0, 15, 0, 0],
#     [10, 0, 0, 0, 0, 0, 0, 0],
#     [6, 5, 5, 5, 5, 0, 5, 9],
#     [0, 0, 5, 0, 0, 0, 0, 2],
#     [0, 0, 0, 0, 0, 0, 0, 2],
#     [0, 0, 0, 4, 4, 0, 0, 14],
# ]



MAX_CELL = N + W + S + E  # 15

# def make_full_wall_grid(width, height):
#     return [[MAX_CELL for _ in range(width)] for _ in range(height)]


def make_grid(width, height):
    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(0)
        grid.append(row)

    return grid

def add_outer_walls(grid):
    h = len(grid)
    w = len(grid[0])

    for y in range(h):
        for x in range(w):

            if y == 0:
                grid[y][x] |= N

            if y == h - 1:
                grid[y][x] |= S

            if x == 0:
                grid[y][x] |= W

            if x == w - 1:
                grid[y][x] |= E

def shit_filler(grid):
    h = len(grid)
    w = len(grid[0])

    for y in range(h):
        for x in range(w):
            if grid[y][x] == 0:
                grid[y][x] = random.randint(0,14)


def slightly_less_shit_filler(grid):
    h = len(grid)
    w = len(grid[0])
    dirs = [N, W, S, E]

    for y in range(h):
        for x in range(w):
            if grid[y][x] == 0:
                random.shuffle(dirs)
                cell = 0

                for d in dirs[:random.randint(0, 1)]:
                    cell |= d

                grid[y][x] = cell

###########################################3
# Slightly better one yk
#############################


RANDOMNESS = 20

def random_coord(grid):
    h = len(grid)
    w = len(grid[0])

    y = random.randrange(h)
    x = random.randrange(w)

    return y, x

def add_random_walls(min, max):
    dirs = [N, W, S, E]
    random.shuffle(dirs)

    cell = 0
    for d in dirs[:random.randint(min, max)]:
        cell |= d

    return cell

def fix_neigbours(grid, y, x):
    h = len(grid)
    w = len(grid[0])

    before = grid[y][x]

    if x > 0 and (grid[y][x-1] & E):
        grid[y][x] |= W
    if x < w-1 and (grid[y][x+1] & W):
        grid[y][x] |= E
    if y > 0 and (grid[y-1][x] & S):
        grid[y][x] |= N
    if y < h-1 and (grid[y+1][x] & N):
        grid[y][x] |= S


    # return False only if it changed
    return grid[y][x] == before


def rules(grid, y, x):
    walls = bin(grid[y][x]).count("1")

    if walls == 4:
        return True

    before = grid[y][x]

    if walls == 0:
        grid[y][x] = add_random_walls(0,2)

    return grid[y][x] == before



def fix_edge_cases(grid, y, x):
    h = len(grid)
    w = len(grid[0])

    before = grid[y][x]

    # count walls
    walls = bin(grid[y][x]).count("1")

    # only act when the cell has 3 walls (1 opening)
    if walls != 3:
        return grid[y][x] == before

    # TOP edge
    if y == 0 and not x == w - 1 and not (grid[y][x] & N):
        # opening is north, drill inward
        grid[y][x] |= S

    # BOTTOM edge
    if y == h - 1 and not x == w - 1 and not (grid[y][x] & S):
        grid[y][x] |= N

    # LEFT edge
    if x == 0 and not (grid[y][x] & W):
        grid[y][x] |= E

    # RIGHT edge
    if x == w - 1 and not (grid[y][x] & E):
        grid[y][x] |= W

    return grid[y][x] == before





def slightly_better_filler(grid):
    h = len(grid)
    w = len(grid[0])

    used = set()
    placed = 0

    while placed < RANDOMNESS:
        y, x = random_coord(grid)

        # avoid already filled cells
        if grid[y][x] != 0:
            continue

        # avoid placing next to existing seeds
        too_close = False
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if (y + dy, x + dx) in used:
                    too_close = True
                    break
            if too_close:
                break

        if too_close:
            continue

        # valid seed!
        grid[y][x] = add_random_walls(0, 3)
        used.add((y, x))
        placed += 1
    

    done = False

    while not done:
        changed_any = False

        for y in range(h):
            for x in range(w):

                if not fix_neigbours(grid, y, x):
                    changed_any = True

                if not rules(grid, y, x):
                    changed_any = True
                
                if not fix_edge_cases(grid, y, x):
                    changed_any = True

        if not changed_any:
            done = True


########################################################


                
                







WALL = "█"
EMPTY = " "

def print_maze(grid):
    h = len(grid)
    w = len(grid[0])
    for y in range(h):
        for x in range(w):
            print(WALL, end="")
            print(WALL, end="")
            if grid[y][x] & N:
                print(WALL, end="")
                print(WALL, end="")
            else:
                print(EMPTY, end="")
                print(EMPTY, end="")
            print(WALL, end="")
            print(WALL, end="")
        print('\n', end="")
        for x in range(w):
            if grid[y][x] & W:
                print(WALL, end="")
                print(WALL, end="")
            else:
                print(EMPTY, end="")
                print(EMPTY, end="")
            print(EMPTY, end="")
            print(EMPTY, end="")
            if grid[y][x] & E:
                print(WALL, end="")
                print(WALL, end="")
            else:
                print(EMPTY, end="")
                print(EMPTY, end="")
        print('\n', end="")
        for x in range(w):
            print(WALL, end="")
            print(WALL, end="")
            if grid[y][x] & S:
                print(WALL, end="")
                print(WALL, end="")
            else:
                print(EMPTY, end="")
                print(EMPTY, end="")
            print(WALL, end="")
            print(WALL, end="")
        print('\n', end="")









grid = make_grid(width, height)

# grid = make_full_wall_grid(width, height)

# shit_filler(grid)
# slightly_less_shit_filler(grid)

# slightly_better_filler(grid)


add_outer_walls(grid)

print_maze(grid)




