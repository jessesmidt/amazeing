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


def print_maze_hex(grid, f) -> None:
    """
    Outputs the  per cell in hexadecimal value.
    """
    h = len(grid)
    w = len(grid[0])
    for y in range(h):
        for x in range(w):
            cell = grid[y][x]
            f.write(f"{cell_to_tile_index(cell):x}")
        f.write("\n")


def print_doors(config, f) -> None:
    """
    Finds entrance and exit and prints coordinates
    """
    entry_x, entry_y = config['ENTRY']
    exit_x, exit_y = config['EXIT']
    f.write(f"\n{entry_x},{entry_y}\n{exit_x},{exit_y}")

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
    f.write(f"\n{''.join(directions)}")


def print_output_main(grid, config) -> None:
    """
    Opens or creates output_maze.txt,
    calls the print path function.
    """
    print("Printing output_maze.txt")
    f = open('output_maze.txt', 'w')
    print_maze_hex(grid, f)
    print_doors(config, f)
    print_path(grid, f)
