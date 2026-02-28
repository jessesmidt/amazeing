from .generator import Cell
from typing import Any


OPPOSITE = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}


def mark_start_and_exit(
        grid: list[list[Cell]], start: tuple[int, int], goal: tuple[int, int]
        ) -> None:
    """
    Mark the start and goal cells in the grid.

    Args:
        grid: 2D list of Cell objects representing the maze.
        start: (x, y) coordinates of the entry cell.
        goal: (x, y) coordinates of the exit cell.
    """
    sx, sy = start
    gx, gy = goal

    grid[sy][sx].is_start = True
    grid[gy][gx].is_goal = True


def remove_wall_between(a: Cell, b: Cell) -> None:
    """
    Remove the shared wall between two adjacent cells.

    Determines the direction from a to b, then opens the wall
    on both sides using the opposite direction mapping.

    Args:
        a: The source cell.
        b: The destination cell, must be directly adjacent to a.

    Raises:
        ValueError: If a and b are not adjacent (not exactly one step apart).
    """
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


def get_unvisited_neighbors(grid: list[list[Cell]], cell: Cell) -> list:
    """
    Finds neighbours in 4 directions, checks for
    their .visited status. If not visited or part of pattern,
    appends to list. A list of all usable neighbours
    is returned.

    args:
        grid: 2D list of Cell objects representing the maze.
        cell: the target Cell which neighbours we're finding.

    returns:
        neighbors: a list of Cells which sorround the target Cell
    """
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


def get_all_neighbors(grid: list[list[Cell]], cell: Cell) -> list[Cell]:
    """
    Finds neighbours in 4 directions, except for cells
    that are part of a pattern, appends to list.
    A list of all available neighbours is returned.
    """
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


def wall_exists_between(a: Cell, b: Cell) -> Any:
    """
    Checks between cell a and b for wall.
    Returns true if 2 cells have a wall, else
    return false.
    """
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
