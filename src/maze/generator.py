import random
from .pattern import make_pattern, mark_pattern
from .generator_utils import get_all_neighbors, mark_start_and_exit
from .generator_utils import get_unvisited_neighbors
from .generator_utils import remove_wall_between, wall_exists_between

class Cell:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

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

        self.is_start = False
        self.is_goal = False

        self.pattern = False


def make_grid(width, height) -> list[list[Cell]]:
    """
    Initializes grid for config's values of
    height and width. Returns the grid of cells
    in nested lists.
    """
    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(x, y))
        grid.append(row)

    return grid


def sigma_male_random_maze_generator(grid, bias, seed, pattern) -> None:
    """
    Shi leipe functie
    """
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

        else:
            active.remove(cell)


def wilson_sometimes_hunts(grid, bias, seed, pattern, imprate) -> None:
    """
    Imperfections
    Insane functie waar Sem de docstring voor gaat schrijven
    """

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
                break

            # If no unvisited cell could be connected (all trapped), mark one forcibly
            if not cell_found:
                trapped_cell = unvisited[0]
                trapped_cell.visited = True


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
