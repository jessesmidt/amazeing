from mlx import Mlx
import sys

class MLXDisplay():
    TILE_SIZE = 32
    BUTTON_BAR_HEIGHT = 50

    def __init__(self, grid, width, height, config):
        self.grid = grid
        self.width = width
        self.height = height
        self.config = config
        self.show_solution = False

        win_width = width * self.TILE_SIZE
        win_height = height * self.TILE_SIZE + self.BUTTON_BAR_HEIGHT

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            win_width,
            win_height,
            f"A-Maze-ing, {self.height}x{self.width}"
        )

        # self.mlx.mlx_sync(self.mlx.SYNC_IMAGE_WRITABLE, self.mlx.SYNC_WIN_FLUSH, self.win_ptr)
        self.tiles = self.load_tiles()

        # Hook for window close (X button) - event 17
        self.mlx.mlx_hook(self.win_ptr, 17, 0, self.close_window, None)
        # Hook for key press
        self.mlx.mlx_key_hook(self.win_ptr, self.key_handler, None)
        # Hook for mouse click
        self.mlx.mlx_mouse_hook(self.win_ptr, self.mouse_handler, None)

    def key_handler(self, keycode, param):
        """Handle ESC key"""
        if keycode == 65307:
            self.close_window(None)
        return 0
    
    def mouse_handler(self, button, x, y, param):
        """Handle mouse button clicks"""
        if button == 1:
            self.handle_click(x, y)
        return 0

    def close_window(self, param):
        """Properly close the window and exit"""
        # Destroy window
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        # Exit cleanly
        sys.exit(0)

    def load_tiles(self):
        """Load all tile png's"""
        tiles = {}
        for i in range(16):
            filename = f"assets/tile_{i:x}.png"
            img_ptr, w, h = self.mlx.mlx_png_file_to_image(self.mlx_ptr, filename)
            tiles[i] = img_ptr
        
        # Load path/start/goal markers
        tiles['path'], _, _ = self.mlx.mlx_png_file_to_image(self.mlx_ptr, "assets/path_marker.png")
        tiles['start'], _, _ = self.mlx.mlx_png_file_to_image(self.mlx_ptr, "assets/start_marker.png")
        tiles['goal'], _, _ = self.mlx.mlx_png_file_to_image(self.mlx_ptr, "assets/goal_marker.png")
        
        # Load UI buttons
        tiles['btn_bar'], _, _ = self.mlx.mlx_png_file_to_image(self.mlx_ptr, "assets/btn_bar.png")
        tiles['btn_generate'], _, _ = self.mlx.mlx_png_file_to_image(self.mlx_ptr, "assets/btn_generate.png")
        tiles['btn_solve'], _, _ = self.mlx.mlx_png_file_to_image(self.mlx_ptr, "assets/btn_solve.png")
        tiles['btn_hide'], _, _ = self.mlx.mlx_png_file_to_image(self.mlx_ptr, "assets/btn_hide.png")
        
        return tiles
    
    def render(self):
        """Render the display"""
        self.render_maze()
        if self.show_solution:
            self.render_path()

        self.draw_buttons()

        self.mlx.mlx_sync(self.mlx_ptr, self.mlx.SYNC_WIN_FLUSH, self.win_ptr)

    def render_maze(self):
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

    def render_path(self):
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

    def draw_buttons(self):
        """Draw button bar using images"""
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr,
            self.tiles['btn_bar'], 0, 0
        )
    
        # Draw generate button at (10, 10)
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr,
            self.tiles['btn_generate'], 10, 10
        )
        
        # Draw solve/hide button at (170, 10)
        solve_img = self.tiles['btn_hide'] if self.show_solution else self.tiles['btn_solve']
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr,
            solve_img, 170, 10
        )

    def handle_click(self, x, y):
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


    def regenerate_maze(self, config):
        """Regenerate the maze and redraw"""
        from src.maze.generator import generate_maze
        self.grid = generate_maze(config)
        self.show_solution = False
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_sync(self.mlx_ptr, self.mlx.SYNC_WIN_FLUSH, self.win_ptr)
        self.render()

    def toggle_solution(self):
        """Toggle showing/hiding the solution path"""
        if not self.show_solution:
            from src.maze.maze_solver import solve_maze
            solve_maze(self.grid)

            path_count = sum(1 for row in self.grid for cell in row if cell.in_path)
            print(f"Path cells found: {path_count}")

            if path_count == 0:
                print("WARNING: No path found! solve_maze might not be setting cell.in_path")

        self.show_solution = not self.show_solution
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_sync(self.mlx_ptr, self.mlx.SYNC_WIN_FLUSH, self.win_ptr)
        self.render()

def cell_to_tile_index(cell) -> int:
    """
    Convert a Cell's wall configuration to a tile index (0-15).

    Args:
        cell: Cell object with walls dict

    Returns:
        int: Index from 0-15 representing which tile PNG to use
    """
    value = 0
    if cell.walls['N']:
        value |= 1  # N = 1
    if cell.walls['S']:
        value |= 2  # S = 2
    if cell.walls['E']:
        value |= 4  # E = 4
    if cell.walls['W']:
        value |= 8  # W = 8
    return value


def print_maze_mlx(grid, config):
    display = MLXDisplay(grid, config['WIDTH'], config['HEIGHT'], config)
    display.render()
    display.mlx.mlx_loop(display.mlx_ptr)
