from src.rendering.mlx_renderer import cell_to_tile_index
from src.maze.generator import Cell
from typing import TextIO


def mark_goal(grid: list[list[Cell]]) -> Cell:
    """
    finds the 'goal' cell in grid, returns cell.
    """
    for row in grid:
        for cell in row:
            if cell.is_goal:
                goal = cell
    return goal


def print_maze_hex(grid: list[list[Cell]], f: TextIO) -> None:
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


def print_doors(config: dict, f: TextIO) -> None:
    """
    Finds entrance and exit and prints coordinates
    """
    entry_x, entry_y = config['ENTRY']
    exit_x, exit_y = config['EXIT']
    f.write(f"\n{entry_x},{entry_y}\n{exit_x},{exit_y}")


def print_path(grid: list[list[Cell]], f: TextIO) -> None:
    """
    Tracks from goal (current) to start what direction
    the path has made.
    """
    current = mark_goal(grid)
    directions: list[str] = []

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


def print_output_main(grid: list[list[Cell]], config: dict) -> None:
    """
    Opens or creates output_maze.txt,
    calls the print path function.
    """
    # print(f"Printing output to {config['OUTPUT_FILE']}")
    f = open(f"{config['OUTPUT_FILE']}", "w")
    print_maze_hex(grid, f)
    print_doors(config, f)
    print_path(grid, f)
