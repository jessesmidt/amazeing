import random
# maze input stats
start = (1,1)
goal = (8,5)

width = 10
height = 10


# cardinal wall stats
N = 1
S = 2
E = 4
W = 8

MAX_CELL = N + W + S + E


# maze asci visuals
WALL = "█"
EMPTY = " "

# maze controls
BIAS = 1      # 0 = roomy, 1 = long corridors
SEED = None       # set to none for full-random

# maze helper lists
DIRS = {
    'N': (0, -1),
    'S': (0,  1),
    'E': (1,  0),
    'W': (-1, 0)
}

OPPOSITE = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}


class Cell:
    def __init__(self, x, y):
        # this cell has these x & y coords
        self.x = x
        self.y = y

        # cardinal walls, True = Wall
        self.walls = {
            'N': True,
            'E': True,
            'S': True,
            'W': True
        }

        # have we visited this cell during generation
        self.visited = False

        # important for heuristic search algo
        self.g = float('inf')
        self.mhd = 0
        self.f = float('inf')
        
        # helps to recreate the best path
        self.parent = None
        self.in_path = False

        # is it the start or the goal
        self.is_start = False
        self.is_goal = False

        # is it part of the 42 symbol in the middle
        self.fortytwo = False

def make_grid(width, height):
    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(x, y))
        grid.append(row)

    return grid

##########################################
#       Help The Maze
##########################################

def remove_wall_between(a, b):
    dx = b.x - a.x
    dy = b.y - a.y

    # determine direction from a to b
    if dx == 1 and dy == 0:
        direction = 'E'
    elif dx == -1 and dy == 0:
        direction = 'W'
    elif dx == 0 and dy == 1:
        direction = 'S'
    elif dx == 0 and dy == -1:
        direction = 'N'
    else:
        raise ValueError("Cells are not adjacent")

    # remove walls on both sides using OPPOSITE
    a.walls[direction] = False
    b.walls[OPPOSITE[direction]] = False


def get_unvisited_neighbors(grid, cell):
    neighbors = []
    h = len(grid)
    w = len(grid[0])
    x = cell.x
    y = cell.y

    # check we arent at the top edge
    # check if the cell above (y-1) is not visited
    if y > 0 and not grid[y-1][x].visited:
        neighbors.append(grid[y-1][x])

    # check we arent at the bottom edge
    # check if the cell below (y+1) is not visited
    if y < h-1 and not grid[y+1][x].visited:
        neighbors.append(grid[y+1][x])

    # check we arent at the left edge
    # check if the cell left (x-1) is not visited
    if x > 0 and not grid[y][x-1].visited:
        neighbors.append(grid[y][x-1])

    # check we arent at the right edge
    # check if the cell right (x+1) is not visited
    if x < w-1 and not grid[y][x+1].visited:
        neighbors.append(grid[y][x+1])

    return neighbors

def random_start(grid):
    return grid[random.randrange(len(grid))][random.randrange(len(grid[0]))]

##########################################
#       Maze Generation
##########################################

def sigma_male_random_maze_generator(grid, bias=BIAS, seed=SEED):

    # if the seed has not been made yet,
    if seed is not None:
        random.seed(seed)

    # find a random cell to start at yk
    start = grid[random.randrange(len(grid))][random.randrange(len(grid[0]))]
    start.visited = True
    
    # list of cells we are currently growing from
    # first one would be start ofc
    active = [start]

    while active:

        # decide which cell to go from next
        # if // go from the last cell, DFS, long corridors
        # else // go from random cell we can grow from, Prim, roomy
        if random.random() < bias:
            cell = active[-1]
        else:
            cell = random.choice(active)

        # we get the unvisited neighbours of the cell we are at
        # neighbours is a list of cells with .visited = False
        neighbors = get_unvisited_neighbors(grid, cell)

        # if the cell has any neighbors that havent been visited yet
        # pick a random neighboring cell
        # remove the all in between them
        # that neighbor is now visited
        # we add it to the active list
        if neighbors:
            next = random.choice(neighbors)
            remove_wall_between(cell, next)
            next.visited = True
            active.append(next)

        # if the cell has no unvisited neighbors
        # we dont wanna grow from this cell anymore
        else:
            active.remove(cell)

##########################################
#       Printer / Visuals
##########################################

def print_maze(grid):
    h = len(grid)
    w = len(grid[0])

    for y in range(h):

        # ── TOP (north walls)
        for x in range(w):
            cell = grid[y][x]
            print(WALL * 2, end="")
            if cell.walls['N']:
                print(WALL * 2, end="")
            else:
                print(EMPTY * 2, end="")
            print(WALL * 2, end="")
        print()

        # ── MIDDLE (west + interior + east)
        for x in range(w):
            cell = grid[y][x]
            if cell.walls['W']:
                print(WALL * 2, end="")
            else:
                print(EMPTY * 2, end="")

            print(EMPTY * 2, end="")

            if cell.walls['E']:
                print(WALL * 2, end="")
            else:
                print(EMPTY * 2, end="")
        print()

        # ── BOTTOM (south walls)
        for x in range(w):
            cell = grid[y][x]
            print(WALL * 2, end="")
            if cell.walls['S']:
                print(WALL * 2, end="")
            else:
                print(EMPTY * 2, end="")
            print(WALL * 2, end="")
        print()





##########################################
#       Run that shit
##########################################

grid = make_grid(width, height)

sigma_male_random_maze_generator(grid)

print_maze(grid)

