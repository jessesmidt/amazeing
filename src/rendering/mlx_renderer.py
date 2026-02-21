from mlx import Mlx
from typing import Any
from src.maze.generator import Cell


class MLXDisplay():
    TILE_SIZE = 32
    BUTTON_BAR_HEIGHT = 50

    def __init__(
        self, grid: list[list[Cell]], width: int, height: int, config: dict
            ):
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
        """Handle ESC key"""
        if keycode == 65307:
            self.close_window(None)
        return 0

    def mouse_handler(
            self, button: int, x: int, y: int, param: None
                ) -> int:
        """Handle mouse button clicks"""
        if button == 1:
            self.handle_click(x, y)
        return 0

    def close_window(self, param: None) -> None:
        """Properly close the window and exit"""
        self.running = False

    def load_tiles(self) -> dict[str | int, Any]:
        """
        Load all tile png's, returns list of pointers to images
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
        """Render the display"""
        self.render_maze()
        if self.show_solution:
            self.render_path()
        self.render_doors()
        self.draw_buttons()

        self.mlx.mlx_sync(self.mlx_ptr, self.mlx.SYNC_WIN_FLUSH, self.win_ptr)

    def render_maze(self) -> None:
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
        """render solution path using overlay images"""
        if not self.show_solution:
            return

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                px = x * self.TILE_SIZE
                py = y * self.TILE_SIZE + self.BUTTON_BAR_HEIGHT

                # Draw path marker on path cells
                if cell.in_path:
                    self.mlx.mlx_put_image_to_window(
                        self.mlx_ptr, self.win_ptr,
                        self.tiles['path'], px, py
                    )

                # Draw start marker (green circle)
                if cell.is_start:
                    self.mlx.mlx_put_image_to_window(
                        self.mlx_ptr, self.win_ptr,
                        self.tiles['start'], px, py
                    )

                # Draw goal marker (blue circle)
                if cell.is_goal:
                    self.mlx.mlx_put_image_to_window(
                        self.mlx_ptr, self.win_ptr,
                        self.tiles['goal'], px, py
                    )

    def render_doors(self) -> None:
        """Draw entrance and exit doors using images"""
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
        """Draw button bar using images"""
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
        """Handle mouse clicks on buttons"""
        # Check if click is in button bar area
        if y > self.BUTTON_BAR_HEIGHT:
            return

        btn_y = 10
        btn_height = 30

        if 10 <= x <= 150 and btn_y <= y <= btn_y + btn_height:
            print("Generate button clicked!")
            self.regenerate_maze(self.config)

        elif 170 <= x <= 310 and btn_y <= y <= btn_y + btn_height:
            print("Solve button clicked!")
            self.toggle_solution()

    def regenerate_maze(self, config: dict) -> None:
        """Regenerate the maze and redraw"""
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
        """Toggle showing/hiding the solution path"""
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
    from src.maze.print_output import print_output_main
    print_output_main(grid, config)
    display = MLXDisplay(grid, config['WIDTH'], config['HEIGHT'], config)
    display.render()

    def check_running(param: None) -> int:
        if not display.running:
            display.mlx.mlx_loop_exit(display.mlx_ptr)
            print("Esc key pressed - closing MLX")
        return 0

    display.mlx.mlx_loop_hook(display.mlx_ptr, check_running, None)
    display.mlx.mlx_loop(display.mlx_ptr)
