from src.rendering.mlx_renderer import cell_to_tile_index

f = open('output_maze.txt', 'w')

def print_output(grid) -> None:
    h = len(grid)
    w = len(grid[0])
    for y in range(h):
        for x in range(w):
            cell = grid[y][x]
            f.write(f"{cell_to_tile_index(cell):x}")
        f.write("\n")