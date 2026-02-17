import random

from src.patterns.digit_patterns import DIGITS
from src.patterns.char_patterns import CHARS

# cardinal wall stats
N = 1
S = 2
E = 4
W = 8

OPPOSITE = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}

# the cell type shit
class Cell:
    def __init__(self, x, y) -> None:
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
        # g = cost, mhd = estimated cost using city block
        # f combined g + mhd score. decides what cell is next
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
def make_grid(width, height) -> list[list[Cell]]:
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
    if (h + 1) <  ph or (w + 1) < pw:
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

def mark_start_and_exit(grid, start, goal) -> None:
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

def remove_wall_between(a, b) -> None:
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


def get_unvisited_neighbors(grid, cell) -> list:
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

def get_all_neighbors(grid, cell):
    neighbors = []
    h = len(grid)
    w = len(grid[0])
    x = cell.x
    y = cell.y

    # Up
    if y > 0:
        neighbor = grid[y-1][x]
        if not neighbor.pattern:
            neighbors.append(neighbor)

    # Down
    if y < h-1:
        neighbor = grid[y+1][x]
        if not neighbor.pattern:
            neighbors.append(neighbor)

    # Left
    if x > 0:
        neighbor = grid[y][x-1]
        if not neighbor.pattern:
            neighbors.append(neighbor)

    # Right
    if x < w-1:
        neighbor = grid[y][x+1]
        if not neighbor.pattern:
            neighbors.append(neighbor)

    return neighbors


def wall_exists_between(a, b):
    dx = b.x - a.x
    dy = b.y - a.y

    if dx == 1:
        return a.walls['E']
    if dx == -1:
        return a.walls['W']
    if dy == 1:
        return a.walls['S']
    if dy == -1:
        return a.walls['N']

    return False


def random_start(grid):
    return grid[random.randrange(len(grid))][random.randrange(len(grid[0]))]

##########################################
#       Maze Generation
##########################################

def sigma_male_random_maze_generator(grid, bias, seed, pattern) -> None:

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
#       Imperfections
##########################################

def wilson_sometimes_hunts(grid, bias, seed, pattern, imprate):

    if seed is not None:
        random.seed(seed)

    mark_pattern(grid, pattern)

    # --- Initialize tree with one visited cell ---
    while True:
        start = grid[random.randrange(len(grid))][random.randrange(len(grid[0]))]
        if not start.pattern:
            break

    start.visited = True

    while True:

        unvisited = [
            cell
            for row in grid
            for cell in row
            if not cell.visited and not cell.pattern
        ]

        if not unvisited:
            break

        # =========================
        # WILSON BRANCH
        # =========================
        if random.random() < bias:

            cell = random.choice(unvisited)
            path = [cell]

            while not cell.visited:

                neighbors = get_all_neighbors(grid, cell)

                if not neighbors:
                # Dead end — stop this walk
                    break
                
                next_cell = random.choice(neighbors)



                if next_cell in path:
                    loop_index = path.index(next_cell)
                    path = path[:loop_index + 1]
                else:
                    path.append(next_cell)

                cell = next_cell

            # Carve the loop-erased path
            for i in range(len(path) - 1):

                current = path[i]
                next_cell = path[i + 1]

                remove_wall_between(current, next_cell)

                current.visited = True
                next_cell.visited = True

                # ---- IMPERFECTION ----
                if random.randint(1, 100) <= imprate:

                    extra_neighbors = [
                        n for n in get_all_neighbors(grid, current)
                        if n.visited and n != next_cell
                    ]

                    if extra_neighbors:
                        extra = random.choice(extra_neighbors)

                        if wall_exists_between(current, extra):
                            remove_wall_between(current, extra)

        # =========================
        # HUNT BRANCH
        # =========================
        else:

                        
            random.shuffle(unvisited)

            cell_found = False

            for cell in unvisited:
                visited_neighbors = [
                    n for n in get_all_neighbors(grid, cell)
                    if n.visited
                ]

                if not visited_neighbors:
                    # Cannot connect this cell — try next one
                    continue

                # pick a random visited neighbor to connect
                next_cell = random.choice(visited_neighbors)
                remove_wall_between(cell, next_cell)
                cell.visited = True

                # ---- IMPERFECTION ----
                if random.randint(1, 100) <= imprate:
                    extra_neighbors = [
                        n for n in get_all_neighbors(grid, cell)
                        if n.visited and n != next_cell
                    ]
                    if extra_neighbors:
                        extra = random.choice(extra_neighbors)
                        if wall_exists_between(cell, extra):
                            remove_wall_between(cell, extra)

                cell_found = True
                break  # exit the for-loop because we successfully added a cell

            # If no unvisited cell could be connected (all trapped), mark one forcibly
            if not cell_found:
                trapped_cell = unvisited[0]
                trapped_cell.visited = True




    




##########################################
#       Run that shit
##########################################


def generate_maze(config: dict) -> list[list[int]]:
    """
    Generate a maze base on configuration dictionary.

    Args:
        config: Dict with mandatory keys WIDTH, HEIGHT, ENTRY,
            EXIT, PERFECT
        optional: SEED, BIAS, PATTERN, RENDER
    
        Returns: 2D list of Cell objects representing the maze
    """
    width = config['WIDTH']
    height = config['HEIGHT']
    start = config['ENTRY']
    goal = config['EXIT']
    perfect = config['PERFECT']
    imprate = int(config['IMPRATE'])
    seed = config.get('SEED', None)
    bias = config.get('BIAS', 0.5)
    pattern = config.get('PATTERN', '42')

    grid = make_grid(width, height)

    if width >= 9 and height >= 7:
        pattern_grid = make_pattern(pattern)
        if pattern_grid:
            mark_pattern(grid, pattern_grid)
        else:
            print(f"Warning: Could not create pattern '{pattern}'")
    else:
        print(
            f"Warning: Could not create pattern '{pattern}', "
            "width and height not sufficient, minimum = 9x7"
            )

    mark_start_and_exit(grid, start, goal)

    if perfect:
        sigma_male_random_maze_generator(grid, bias=bias, seed=seed, pattern=pattern)

    if not perfect:
        wilson_sometimes_hunts(grid, bias=bias, seed=seed, pattern=pattern, imprate = imprate)



    return grid




