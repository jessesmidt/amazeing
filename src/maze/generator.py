import random


class Cell:
    """
    Represents a single cell in the maze grid.

    Attributes:
        x: Column index of the cell.
        y: Row index of the cell.
        walls: Dict indicating which walls (N/E/S/W) are closed.
        visited: Whether this cell has been visited during maze generation.
        g: Actual cost from start cell (used in pathfinding).
        mhd: Manhattan distance heuristic to goal (used in pathfinding).
        f: Combined score g + mhd, determines next cell in pathfinding.
        parent: Previous cell on the shortest path,
                used for path reconstruction.
        in_path: Whether this cell is part of the solution path.
        is_start: Whether this cell is the maze entrance.
        is_goal: Whether this cell is the maze exit.
        pattern: Whether this cell is part of a reserved pattern (e.g. "42").
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize a Cell at position (x, y) with all walls closed.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.
        """
        self.x = x
        self.y = y

        self.walls: dict[str, bool] = {
            'N': True,
            'E': True,
            'S': True,
            'W': True
        }

        self.visited: bool = False

        self.g: float = float('inf')
        self.mhd: float = 0.0
        self.f: float = float('inf')

        self.parent: Cell | None = None
        self.in_path: bool = False

        self.is_start: bool = False
        self.is_goal: bool = False

        self.pattern: bool = False


def growing_sigma_tree(
        grid: list[list[Cell]], bias: float, seed: int | None
        ) -> None:
    """
    Generate a perfect maze using the Growing Tree algorithm.

    Maintains a list of active cells. Each iteration, a cell is selected
    from the active list based on the bias value: higher bias favors the
    most recently added cell (resembling recursive backtracking), while
    lower bias selects randomly (resembling Prim's algorithm).

    A wall is carved to a random unvisited neighbor, which is then added
    to the active list. If a cell has no unvisited neighbors, it is removed
    from the active list. The algorithm ends when the active list is empty.

    Args:
        grid: 2D list of Cell objects representing the maze.
        bias: Probability (0.0 to 1.0) of selecting the most recent active
              cell. At 1.0, behaves like recursive backtracking. At 0.0,
              behaves like Prim's algorithm.
        seed: Optional random seed for reproducibility.
    """
    from .generator_utils import (
        get_unvisited_neighbors,
        remove_wall_between,
    )

    if seed is not None:
        random.seed(seed)

    while True:
        start = grid[
            random.randrange(len(grid))][random.randrange(len(grid[0]))]
        if not start.pattern:
            break

    start.visited = True
    active = [start]

    while active:
        cell = active[-1] if random.random() < bias else random.choice(active)
        neighbors = get_unvisited_neighbors(grid, cell)

        if neighbors:
            next_cell = random.choice(neighbors)
            remove_wall_between(cell, next_cell)
            next_cell.visited = True
            active.append(next_cell)
        else:
            active.remove(cell)


def wilson_sometimes_hunts(
        grid: list[list[Cell]], bias: float, seed: int | None, imprate: int
        ) -> None:
    """
    Generate a maze using a hybrid Wilson's algorithm and
    Hunt-and-Kill approach.

    Each iteration, a random value determines which algorithm
    handles the next unvisited cell.
    Wilson's algorithm (random walk with loop erasure) is used
    when the random value falls below the bias threshold,
    otherwise Hunt-and-Kill scans for an unvisited cell
    adjacent to the existing maze.

    Imperfections can be introduced by randomly removing extra walls during
    path carving, creating loops and making the maze imperfect.

    Args:
        grid:   2D list of Cell objects representing the maze.
        bias:   Probability (0.0 to 1.0) of using Wilson's
                algorithm per iteration.
        seed:   Optional random seed for reproducibility.
        imprate:Percentage chance (0-100) of removing an extra wall per step,
                creating imperfections in the maze.
    """
    if seed is not None:
        random.seed(seed)

    while True:
        start = grid[
            random.randrange(len(grid))][random.randrange(len(grid[0]))]
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

        if random.random() < bias:
            _wilson_step(grid, unvisited, imprate)
        else:
            _hunt_step(grid, unvisited, imprate)


def _wilson_step(
        grid: list[list[Cell]], unvisited: list[Cell], imprate: int
        ) -> None:
    """
    Perform one Wilson's algorithm step: random walk with loop erasure.

    Starts a random walk from an unvisited cell. If the walk revisits a cell
    already in the current path, the loop is erased. The walk ends when it
    reaches a visited cell, at which point all cells along the path are carved.

    Args:
        grid: 2D list of Cell objects representing the maze.
        unvisited: List of all currently unvisited, non-pattern cells.
        imprate: Percentage chance (0-100) of removing an extra wall per step.
    """
    from .generator_utils import (
        get_all_neighbors,
        remove_wall_between,
    )

    cell = random.choice(unvisited)
    path = [cell]

    while not cell.visited:
        neighbors = get_all_neighbors(grid, cell)
        if not neighbors:
            break

        next_cell = random.choice(neighbors)

        if next_cell in path:
            path = path[:path.index(next_cell) + 1]
        else:
            path.append(next_cell)

        cell = next_cell

    for i in range(len(path) - 1):
        current = path[i]
        next_cell = path[i + 1]

        remove_wall_between(current, next_cell)
        current.visited = True
        next_cell.visited = True

        _maybe_add_imperfection(grid, current, next_cell, imprate)


def _hunt_step(
        grid: list[list[Cell]], unvisited: list[Cell], imprate: int
        ) -> None:
    """
    Perform one Hunt-and-Kill step: scan for an
    unvisited cell with a visited neighbor.

    Shuffles unvisited cells and scans for the first
    one adjacent to the existing maze.
    Carves a passage to that neighbor and marks the cell as visited.
    If no valid cell is found, the first unvisited cell is
    forcibly marked visited to prevent the algorithm from getting stuck.

    Args:
        grid: 2D list of Cell objects representing the maze.
        unvisited: List of all currently unvisited, non-pattern cells.
        imprate: Percentage chance (0-100) of removing an extra wall per step.
    """
    from .generator_utils import get_all_neighbors, remove_wall_between

    random.shuffle(unvisited)

    for cell in unvisited:
        visited_neighbors = [
            n for n in get_all_neighbors(grid, cell) if n.visited
            ]

        if not visited_neighbors:
            continue

        next_cell = random.choice(visited_neighbors)
        remove_wall_between(cell, next_cell)
        cell.visited = True

        _maybe_add_imperfection(grid, cell, next_cell, imprate)
        return

    unvisited[0].visited = True


def _maybe_add_imperfection(
        grid: list[list[Cell]], cell: Cell, exclude: Cell, imprate: int
        ) -> None:
    """
    Randomly remove an extra wall to introduce an imperfection.

    Args:
        grid: 2D list of Cell objects representing the maze.
        cell: The cell to potentially carve an extra passage from.
        exclude: A neighbor to exclude from consideration (already connected).
        imprate: Percentage chance (0-100) of removing an extra wall.
    """
    from .generator_utils import (
        get_all_neighbors, remove_wall_between, wall_exists_between
        )

    if random.randint(1, 100) > imprate:
        return

    extra_neighbors = [
        n for n in get_all_neighbors(grid, cell)
        if n.visited and n != exclude
    ]

    if extra_neighbors:
        extra = random.choice(extra_neighbors)
        if wall_exists_between(cell, extra):
            remove_wall_between(cell, extra)


class MazeGenerator:
    def __init__(self, config: dict) -> None:
        """
        Initializes grid and required config inputs.
        Uses get() to set values to optional keys.
        Calls make_pattern to mark pattern on 2d grid.
        """
        from .pattern import make_pattern
        self.width = config['WIDTH']
        self.height = config['HEIGHT']
        self.start = config['ENTRY']
        self.goal = config['EXIT']
        self.perfect = config['PERFECT']

        self.seed = config.get('SEED')
        self.bias = config.get('BIAS', 0.5)
        self.pattern_value = config.get('PATTERN', '42')
        self.render = config.get('RENDER', '2D')
        self.imprate = config.get('IMPRATE', 65)

        if self.seed is not None:
            random.seed(self.seed)

        self.grid = self.make_grid()
        self.pattern = make_pattern(self.pattern_value)

    def make_grid(self) -> list[list[Cell]]:
        """
        Initializes grid for config's values of
        height and width. Returns the grid of cells
        in nested lists.
        """
        grid = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(x, y))
            grid.append(row)

        return grid

    def generate(self) -> list[list[Cell]]:
        """

        """
        from .generator_utils import mark_start_and_exit
        from .pattern import mark_pattern
        mark_start_and_exit(self.grid, self.start, self.goal)

        if self.pattern:
            mark_pattern(self.grid, self.pattern)

        if self.perfect:
            growing_sigma_tree(
                self.grid,
                bias=self.bias,
                seed=self.seed,
            )
        else:
            wilson_sometimes_hunts(
                self.grid,
                bias=self.bias,
                seed=self.seed,
                imprate=self.imprate
            )

        return self.grid


def generate_maze(config: dict) -> list[list[Cell]]:
    generator = MazeGenerator(config)
    return generator.generate()
