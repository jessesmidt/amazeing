from .generator import Cell
from typing import Any


OPPOSITE = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}


def mark_start_and_exit(
        grid: list[list[Cell]], start: Cell, goal: Cell
        ) -> None:
    """
    Connects the config file's start and goal cell
    and marks them.
    """
    sx, sy = start
    gx, gy = goal

    start_cell = grid[sy][sx]
    goal_cell = grid[gy][gx]

    start_cell.is_start = True
    goal_cell.is_goal = True


def remove_wall_between(a: Cell, b: Cell) -> None:
    """
    Removes the wall between two given cells.
    Finds out direction, removes a's wall
    and uses opposite to remove for b.
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
