import random

from digit_patterns import DIGITS
from char_patterns import CHARS

# maze input stats
start = (1,1)
goal = (14,13)

width = 15
height = 15


# cardinal wall stats
N = 1
S = 2
E = 4
W = 8

MAX_CELL = N + E + S + W


# maze asci visuals
WALL = "██"
EMPTY = "  "

PATTERN_WALL = "▒▒"
PATTERN_EMPTY = "░░"

START_BLOCK = "\033[42m  \033[0m"
GOAL_BLOCK = "\033[41m  \033[0m"




# maze controls
BIAS = 0.5      # 0 = roomy, 1 = long corridors
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

# pick any number or letter combination to place in the middle of the maze
PATTERN = "69"

# the cell type shit
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

        # is it part of the pattern in the middle
        self.pattern = False




# makes the grid type shit
def make_grid(width, height):
    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(x, y))
        grid.append(row)

    return grid

##########################################
#       42 Reasons to stay
##########################################

def make_pattern(pattern_value):
    # if there aint no pattern, there aint no pattern
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

    # make the patern
    # first append the row of left-digit
    # then add a 0, empty
    # then append the row if the right-digit
    pattern = []
    for row in range(len(left)):
        pattern.append(left[row] + [0] + right[row])  # add a gap column

    return pattern

def mark_pattern(grid, pattern):

    # get the height & width of the grid
    # get the height & width of the pattern
    h = len(grid)
    w = len(grid[0])
    ph = len(pattern)
    pw = len(pattern[0])

    # there needs to be atleast 2 normal-maze-cells
    # around the pattern, or its jut not gonna do
    # the pattern
    if (h + 2) <  ph or (w + 2) < pw:
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

    
    
##########################################
#       The way in & out
##########################################

def mark_start_and_exit(grid, start, goal):
    h = len(grid)
    w = len(grid[0])

    sx, sy = start
    gx, gy = goal

    start_cell = grid[sy][sx]
    goal_cell = grid[gy][gx]
    
    start_cell.is_start = True
    goal_cell.is_goal = True

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

    # Up
    if y > 0:
        neighbor = grid[y-1][x]
        if not neighbor.visited and not neighbor.pattern:
            neighbors.append(neighbor)

    # Down
    if y < h-1:
        neighbor = grid[y+1][x]
        if not neighbor.visited and not neighbor.pattern:
            neighbors.append(neighbor)

    # Left
    if x > 0:
        neighbor = grid[y][x-1]
        if not neighbor.visited and not neighbor.pattern:
            neighbors.append(neighbor)

    # Right
    if x < w-1:
        neighbor = grid[y][x+1]
        if not neighbor.visited and not neighbor.pattern:
            neighbors.append(neighbor)

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

    # mark all the cells with a pattern
    mark_pattern(grid, pattern)

    # find a random cell to start at yk that isnt in the patern
    while True:
        start = grid[random.randrange(len(grid))][random.randrange(len(grid[0]))]
        if not start.pattern:
            break
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






##########################################
#       Run that shit
##########################################

grid = make_grid(width, height)
pattern = make_pattern(PATTERN)
mark_start_and_exit(grid, start, goal)

sigma_male_random_maze_generator(grid)


print_maze(grid)

