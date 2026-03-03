import sys
from src.config_parser import parse_config
from src.maze.generator import generate_maze
from src.maze.print_output import print_output_main
from src.maze.maze_solver import solve_maze


def main() -> None:
    """
    Checks for amount of arguments, parses config,
    creates and solves a grid. Then picks render option.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
    except ValueError as e:
        print(f"Error: {e}")
        return
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    try:
        grid = generate_maze(config)
    except ValueError as e:
        print(f"Error: {e}")
        return

    config['RENDER'] = config.get('RENDER', 'ASCII')

    try:
        solve_maze(grid)
    except ValueError as e:
        print(f"Error: {e}")
        return

    if config['RENDER'] == 'MLX':
        try:
            from src.rendering.mlx_renderer import print_maze_mlx
            print_maze_mlx(grid, config)
        except ModuleNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            from src.rendering.terminal_renderer import TerminalDisplay
            print_output_main(grid, config)
            display = TerminalDisplay(grid, config)
            display.render()
        except ValueError as e:
            print(f"Error: {e}")
            return


if __name__ == "__main__":
    main()
