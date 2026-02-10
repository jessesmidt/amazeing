import random

start = (1,1)
goal = (8,5)

width = 10
height = 10

N = 1
W = 2
S = 4
E = 8

MAX_CELL = N + W + S + E

WALL = "█"
EMPTY = " "

RANDOMNESS = 20

###########################################

def make_grid(width, height):
    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(0)
        grid.append(row)

    return grid

###########################################

def betterer_maze_generator(grid):
    h = len(grid)
    w = len(grid[0])

    used = set()
    placed = 0

    while placed < RANDOMNESS:
        y, x = random_coord(grid)


        if grid[y][x] != 0:
            continue


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

        # valid seed found
        grid[y][x] = add_random_walls(0, 3)
        used.add((y, x))
        placed += 1
    

    done = False

    while not done:
        changed_any = False

        for y in range(h):
            for x in range(w):
                if not zero_insurance(grid, y, x):
                    changed_any = True
                    

                if not fix_neigbours(grid, y, x):
                    changed_any = True

                if not add_outer_walls(grid, y, x):
                    changed_any = True

        if not changed_any:
            done = True


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

def neighbor_has_three_walls(grid, y, x):
    h = len(grid)
    w = len(grid[0])

    for dy, dx in ((0,1), (0,-1), (1,0), (-1,0)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w:
            if bin(grid[ny][nx]).count("1") == 3:
                return True
    return False

def add_outer_walls(grid, y , x):
    h = len(grid)
    w = len(grid[0])

    before = grid[y][x]

    if y == 0:
        grid[y][x] |= N
    if y == h - 1:
        grid[y][x] |= S
    if x == 0:
        grid[y][x] |= W
    if x == w - 1:
        grid[y][x] |= E

    return grid[y][x] == before

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

def zero_insurance(grid, y, x):

    before = grid[y][x]
    if grid[y][x] == 0 and not neighbor_has_three_walls(grid, y, x):
         grid[y][x] = add_random_walls(1, 1)
    return grid[y][x] == before

def fifteen_insurance(grid, y, x):
    
    before = grid[y][x]
    if grid[y][x] == 0 and not neighbor_has_three_walls(grid, y, x):
         grid[y][x] = add_random_walls(1, 1)
    return grid[y][x] == before








###########################################
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

betterer_maze_generator(grid)

print_maze(grid)