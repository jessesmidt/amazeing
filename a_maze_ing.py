import sys
from src.config_parser import parse_config
from src.maze.generator import generate_maze
from src.maze.print_output import print_output_main
from src.maze.maze_solver import solve_maze
from src.rendering.terminal_renderer import TerminalDisplay
from src.rendering.mlx_renderer import print_maze_mlx
from src.maze.maze_solver import solve_maze

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    # print(f"Loading config file: {sys.argv[1]}")

    try:
        config = parse_config(sys.argv[1])
    except ValueError as e:
        print(f"Error: {e}")
        return
    # print(f"Config loaded successfully!\n{config}")

    try:
        grid = generate_maze(config)
    except ValueError as e:
        print(f"Error: {e}")
        return

    solve_maze(grid)

    if config['RENDER'] == 'MLX':
        print_maze_mlx(grid, config)
    else:
        display = TerminalDisplay(grid, config)
        display.render()
        print_output_main(grid, config)


if __name__ == "__main__":
	main()
