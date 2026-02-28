from mlx import Mlx
from typing import Any
from src.maze.generator import Cell


class MLXDisplay:
    """
    Graphical maze display using the MiniLibX library.

    Renders the maze grid as tiles, overlays the solution path,
    and provides a button bar for user interaction.

    Attributes:
        TILE_SIZE: Pixel dimensions of each maze tile.
        BUTTON_BAR_HEIGHT: Pixel height of the button bar at the top.
    """
    TILE_SIZE = 32
    BUTTON_BAR_HEIGHT = 50

    def __init__(
        self, grid: list[list[Cell]], width: int, height: int, config: dict
            ):
        """
        Initialize the MLX window and load all tile assets.

        Args:
            grid: 2D list of Cell objects representing the maze.
            width: Number of cells horizontally.
            height: Number of cells vertically.
            config: Parsed configuration stored as a dict.
        """
        self.grid = grid
        self.width = width
        self.height = height
        self.config = config
        self.show_solution = False
        self.running = True

        win_width = max(width * self.TILE_SIZE, 320)
        win_height = height * self.TILE_SIZE + self.BUTTON_BAR_HEIGHT

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            win_width,
            win_height,
            f"A-Maze-ing, {self.height}x{self.width}"
        )

        # self.mlx.mlx_sync(self.mlx.SYNC_IMAGE_WRITABLE,
        # #self.mlx.SYNC_WIN_FLUSH, self.win_ptr)
        self.tiles = self.load_tiles()
        # Hook for window close (X button) - event 17
        self.mlx.mlx_hook(self.win_ptr, 17, 0, self.close_window, None)
        # Hook for key press
        self.mlx.mlx_key_hook(self.win_ptr, self.key_handler, None)
        # Hook for mouse click
        self.mlx.mlx_mouse_hook(self.win_ptr, self.mouse_handler, None)

    def key_handler(self, keycode: int, param: None) -> int:
        """
        Handle key press events.

        Closes the window when the ESC key is pressed (keycode 65307).

        Args:
            keycode: The code of the pressed key.
            param: Unused parameter required by the MLX hook signature.

        Returns:
            0 on completion.
        """
        if keycode == 65307:
            self.close_window(None)
        return 0

    def mouse_handler(
            self, button: int, x: int, y: int, param: None
                ) -> int:
        """
        Handle mouse button click events.

        Forwards left click (button 1) to handle_click for button detection.

        Args:
            button: The mouse button that was pressed.
            x: Horizontal cursor position at time of click.
            y: Vertical cursor position at time of click.
            param: Unused parameter required by the MLX hook signature.

        Returns:
            0 on completion.
        """
        if button == 1:
            self.handle_click(x, y)
        return 0

    def close_window(self, param: None) -> None:
        """
        Stop the display loop by setting running to False.

        Args:
            param: Unused parameter required by the MLX hook signature.
        """
        self.running = False

    def load_tiles(self) -> dict[str | int, Any]:
        """
        Load all tile and UI asset images from the assets directory.

        Loads the 16 wall-configuration tiles (tile_0.png to tile_f.png),
        path/start/goal markers, and button bar images.

        Returns:
            Dict mapping tile identifiers (int for wall tiles,
            str for markers and buttons) to MLX image pointers.
        """
        tiles: dict[str | int, Any] = {}
        for i in range(16):
            filename = f"assets/tile_{i:x}.png"
            img_ptr, w, h = (
                self.mlx.mlx_png_file_to_image(self.mlx_ptr, filename)
            )
            tiles[i] = img_ptr

        # Load path/start/goal markers
        tiles['path'], _, _ = (
            self.mlx.mlx_png_file_to_image(
                self.mlx_ptr, "assets/path_marker.png"
                )
        )
        tiles['start'], _, _ = (
            self.mlx.mlx_png_file_to_image(
                self.mlx_ptr, "assets/start_marker.png"
                )
        )
        tiles['goal'], _, _ = (
            self.mlx.mlx_png_file_to_image(
                self.mlx_ptr, "assets/goal_marker.png"
                )
        )

        # Load UI buttons
        tiles['btn_bar'], _, _ = (
            self.mlx.mlx_png_file_to_image(
                self.mlx_ptr, "assets/btn_bar.png"
                )
        )
        tiles['btn_generate'], _, _ = (
            self.mlx.mlx_png_file_to_image(
                self.mlx_ptr, "assets/btn_generate.png"
                )
        )
        tiles['btn_solve'], _, _ = (
            self.mlx.mlx_png_file_to_image(
                self.mlx_ptr, "assets/btn_solve.png"
                )
        )
        tiles['btn_hide'], _, _ = (
            self.mlx.mlx_png_file_to_image(
                self.mlx_ptr, "assets/btn_hide.png"
                )
        )
        return tiles

    def render(self) -> None:
        """
        Render the full display in the correct draw order.

        Draws the maze tiles, optionally overlays the solution path,
        renders the entry and exit markers, then draws the button bar.
        Flushes the window after all drawing is complete.
        """
        self.render_maze()
        if self.show_solution:
            self.render_path()
        self.render_doors()
        self.draw_buttons()

        self.mlx.mlx_sync(self.mlx_ptr, self.mlx.SYNC_WIN_FLUSH, self.win_ptr)

    def render_maze(self) -> None:
        """
        Draw each maze cell as a tile based on its wall configuration.

        Iterates over the grid and places the corresponding wall tile
        for each cell, offset by the button bar height.
        """
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                tile_index = cell_to_tile_index(cell)

                px = x * self.TILE_SIZE
                py = y * self.TILE_SIZE + self.BUTTON_BAR_HEIGHT

                self.mlx.mlx_put_image_to_window(
                    self.mlx_ptr, self.win_ptr,
                    self.tiles[tile_index], px, py
                    )

    def render_path(self) -> None:
        """
        Overlay path, start, and goal markers on the maze.

        Only draws if show_solution is True. Draws a path marker on
        every cell flagged as in_path, and start/goal markers on their
        respective cells.
        """
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                px = x * self.TILE_SIZE
                py = y * self.TILE_SIZE + self.BUTTON_BAR_HEIGHT

                if cell.in_path:
                    self.mlx.mlx_put_image_to_window(
                        self.mlx_ptr, self.win_ptr,
                        self.tiles['path'], px, py
                    )

                if cell.is_start:
                    self.mlx.mlx_put_image_to_window(
                        self.mlx_ptr, self.win_ptr,
                        self.tiles['start'], px, py
                    )

                if cell.is_goal:
                    self.mlx.mlx_put_image_to_window(
                        self.mlx_ptr, self.win_ptr,
                        self.tiles['goal'], px, py
                    )

    def render_doors(self) -> None:
        pass
        """
        Draw the entry and exit markers onto the maze.

        Iterates the full grid to find and render start and goal cells.
        """
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                px = x * self.TILE_SIZE
                py = y * self.TILE_SIZE + self.BUTTON_BAR_HEIGHT

                if cell.is_start:
                    self.mlx.mlx_put_image_to_window(
                        self.mlx_ptr, self.win_ptr,
                        self.tiles['start'], px, py
                    )

                if cell.is_goal:
                    self.mlx.mlx_put_image_to_window(
                        self.mlx_ptr, self.win_ptr,
                        self.tiles['goal'], px, py
                    )

    def draw_buttons(self) -> None:
        """
        Draw the button bar and its buttons onto the window.

        Renders the background bar, the generate button, and the
        solve/hide toggle button depending on the current show_solution state.
        """
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr,
            self.tiles['btn_bar'], 0, 0
        )

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr,
            self.tiles['btn_generate'], 10, 10
        )

        solve_img = (
            self.tiles['btn_hide'] if self.show_solution
            else self.tiles['btn_solve']
        )
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr,
            solve_img, 170, 10
        )

    def handle_click(self, x: int, y: int) -> None:
        """
        Handle mouse clicks within the button bar.

        Ignores clicks below the button bar. Checks click coordinates
        against the generate and solve/hide button regions and triggers
        the corresponding action.

        Args:
            x: Horizontal position of the click.
            y: Vertical position of the click.
        """
        if y > self.BUTTON_BAR_HEIGHT:
            return

        btn_y = 10
        btn_height = 30

        if 10 <= x <= 150 and btn_y <= y <= btn_y + btn_height:
            self.regenerate_maze(self.config)

        elif 170 <= x <= 310 and btn_y <= y <= btn_y + btn_height:
            self.toggle_solution()

    def regenerate_maze(self, config: dict) -> None:
        """
        Generate a new maze, solve it, write the output file, and redraw.

        Resets show_solution to False and clears the window before rendering.

        Args:
            config: Parsed configuration stored as a dict.
        """
        from src.maze.generator import generate_maze
        from src.maze.print_output import print_output_main
        from src.maze.maze_solver import solve_maze
        self.grid = generate_maze(config)
        solve_maze(self.grid)
        print_output_main(self.grid, config)
        self.show_solution = False
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_sync(self.mlx_ptr, self.mlx.SYNC_WIN_FLUSH, self.win_ptr)
        self.render()

    def toggle_solution(self) -> None:
        """
        Toggle the solution path visibility and redraw the display.

        Flips show_solution, clears the window, and re-renders so the
        change is reflected immediately.
        """
        self.show_solution = not self.show_solution
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_sync(self.mlx_ptr, self.mlx.SYNC_WIN_FLUSH, self.win_ptr)
        self.render()


def cell_to_tile_index(cell: Cell) -> int:
    """
    Convert a Cell's wall configuration to a tile index (0-15).

    Args:
        cell: Cell object with walls dict

    Returns:
        int: Index from 0-15 representing which tile PNG to use
    """
    value = 0
    if cell.walls['N']:
        value |= 1
    if cell.walls['E']:
        value |= 2
    if cell.walls['S']:
        value |= 4
    if cell.walls['W']:
        value |= 8
    return value


def print_maze_mlx(grid: list[list[Cell]], config: dict) -> None:
    """
    Write the maze output file and launch the MLX graphical display.

    Initializes the MLXDisplay, renders the initial frame, and starts
    the MLX event loop. A loop hook checks display.running each tick
    and exits the loop cleanly when the window is closed.

    Args:
        grid: 2D list of Cell objects representing the maze.
        config: Parsed configuration stored as a dict.
    """
    from src.maze.print_output import print_output_main
    print_output_main(grid, config)
    display = MLXDisplay(grid, config['WIDTH'], config['HEIGHT'], config)
    display.render()

    def check_running(param: None) -> int:
        if not display.running:
            display.mlx.mlx_loop_exit(display.mlx_ptr)
        return 0

    display.mlx.mlx_loop_hook(display.mlx_ptr, check_running, None)
    display.mlx.mlx_loop(display.mlx_ptr)
