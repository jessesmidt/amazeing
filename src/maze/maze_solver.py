from generator import Cell
from typing import Any


"""
HEURISTIC SEARCH

f(n) = g(n) + h(n)

f(n) = best case total distance if i pick this node

g(n) = cost from start to current node
        - so amount of steps taken so far yk

h(n) = esitmated distance to finish
        - something like manhatten works well for this or something
"""

# print_maze
# parameters (maze, entry exit)
# 	-> 	when calling funciton we require these 3
# 	- 	maze (assortment of 1's and 0's in a grid)
# 	- 	entry (x & y cords of the entry/start)
# 	-	exit (x & y cords of the exit/finish)

# for loop condition
# -	for y (row indexing)
# -	, row (tell y is the row indexing)
# -	indexes inside maze (checks if indexes exist)

# for x, cell in enumerate(row)
# 	-	x is just the indexing for each collum (cell)
# 	-	inumerate(row), get the row indexing, also just y
# if start coords == current coords
# 	-	this becomes S (start)
# else if goal coords == current coords
# 	-	this becomes G (goal)
# else
# 	do a # if cell == 1
# 	else do ' '
# then print the line we just made yk
# and do y++


def manhattan(a: Cell, b: Cell) -> Any:
    """
    manhattan function returns the distance in int
    from current to goal (absolute distance)
    (current_x - goal_x) + (current_y - goal_y)
    """
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_neighbors(cell: Cell, maze: list[list[Cell]]) -> list[Cell]:
    """
    Finds all neighbouring Cells to 'cell' inside grid
    (or maze) and returns them in a list.
    """
    neighbors = []
    x, y = cell.x, cell.y

    if not cell.walls['N']:
        neighbors.append(maze[y - 1][x])
    if not cell.walls['S']:
        neighbors.append(maze[y + 1][x])
    if not cell.walls['W']:
        neighbors.append(maze[y][x - 1])
    if not cell.walls['E']:
        neighbors.append(maze[y][x + 1])

    return neighbors


def reconstruct_path(goal: Cell) -> None:
    """
    Goes over the path, starting at goal.
    Finding parent until they reach start.
    Start has no parent so current will be set
    to None.
    """
    current = goal
    while current:
        current.in_path = True
        current = current.parent

# define the function solve_maze
# needs this info:
#   start = starting cell (with the cords etc)
#   goal = the goal cell (with the cords etc)
#   maze = 2d maze structure yk

# Make 2 sets
#   open_set = all cells we might still visit
#   closed_set = all cells we already checked type xi

# Initialize Start Cell
#   g = distance from start to current
#   mhd = manhattan distance to goal
#   f = mhd + g

# Add the start to the open set yk
# while open_set
#   keep looking untill there aint nothing to explore yk

# currrent = min..etc.
#   look through open_set
#   idk wtf is happening here ngl

# if current == goal
#   check if the goal is reached type xi
#   cuz then we gotta go back and reconstruct
#   the path using the parent-chain-shit

# open_set.remove(current) & closed_set.add(current)
#   remove it from the ones we havent explored yet
#   add it to the ones that we have already explored type xi#


def solve_maze(grid: list[list[Cell]]) -> None:
    """
    Uses A* pathfinding to solve the maze.

    Finds the shortest possible path from the start to
    the goal cell by using Manhattan distance heuristic.

    Modifies the cells by setting their parent and path.

    Args:
        grid: A 2D list of Cell objects representing the maze structure.
    """
    start = None
    goal = None

    for row in grid:
        for cell in row:
            if cell.is_start:
                start = cell
            if cell.is_goal:
                goal = cell

    # Reset any previous path
    for row in grid:
        for cell in row:
            cell.in_path = False
            cell.g = float('inf')
            cell.f = float('inf')
            cell.parent = None

    open_set = []
    closed_set = set()

    if start is None:
        return None
    start.g = 0
    start.mhd = manhattan(start, goal)
    start.f = start.g + start.mhd

    open_set.append(start)

    while open_set:
        # look for the cell with the lowest f
        current = min(open_set, key=lambda c: c.f)

        if current == goal:
            reconstruct_path(goal)
            return

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue

            tentative_g = current.g + 1
            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tentative_g >= neighbor.g:
                continue

            neighbor.parent = current
            neighbor.g = tentative_g
            neighbor.mhd = manhattan(neighbor, goal)
            neighbor.f = neighbor.g + neighbor.mhd
