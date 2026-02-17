from src.rendering.mlx_renderer import cell_to_tile_index
from src.maze.generator import Cell

def mark_goal(grid) -> Cell:
    """
    finds the 'goal' cell in grid, returns cell.
    """
    for row in grid:
        for cell in row:
            if cell.is_goal:
                goal = cell
    return goal


def print_output(grid) -> None:
    """
    Opens or creates output_maze.txt
    Outputs the  per cell in hexadecimal value.
    calls the print path function.
    """
    f = open('output_maze.txt', 'w')
    h = len(grid)
    w = len(grid[0])
    for y in range(h):
        for x in range(w):
            cell = grid[y][x]
            f.write(f"{cell_to_tile_index(cell):x}")
        f.write("\n")

    print_path(grid, f)


def print_path(grid, f) -> None:
    """
    Tracks from goal (current) to start what direction
    the path has made. 
    """
    current = mark_goal(grid)
    directions = []

    while current.parent:
        parent = current.parent

        if current.x == parent.x + 1:
            directions.append('E')
        if current.x == parent.x - 1:
            directions.append('W')
        if current.y == parent.y + 1:
            directions.append('S')
        if current.y == parent.y - 1:
            directions.append('N')

        current = parent
    directions.reverse()
    f.write(f"{''.join(directions)}")
