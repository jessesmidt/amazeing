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

        self.tiles = self.load_tiles()

        self.buttons = {
            'generate': (10, 10, 150, 40),
            'solve': (170, 10, 310, 40)
        }

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
            img_ptr, w, h = self.mlx.mlx_png_file_to_image(
                self.mlx_ptr,
                filename
            )
            tiles[i] = img_ptr

        path_marker, _, _ = self.mlx.mlx_png_file_to_image(
            self.mlx_ptr,
            "assets/path_marker.png"
        )
        tiles['path'] = path_marker
        
        start_marker, _, _ = self.mlx.mlx_png_file_to_image(
            self.mlx_ptr,
            "assets/start_marker.png"
        )
        tiles['start'] = start_marker
        
        goal_marker, _, _ = self.mlx.mlx_png_file_to_image(
            self.mlx_ptr,
            "assets/goal_marker.png"
        )
        tiles['goal'] = goal_marker

        return tiles
    
    def render(self):
        """Render the display"""
        self.render_maze()
        if self.show_solution:
            self.render_path()

        self.draw_buttons()

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
        """Generate and solve buttons"""
        btn_height = 30
        btn_y = 10

        gen_x1, gen_y1 = 10, btn_y
        gen_x2, gen_y2 = 150, btn_y + btn_height

        solve_x1, solve_y1 = 170, btn_y
        solve_x2, solve_y2 = 310, btn_y + btn_height

        for y in range(gen_y1, gen_y2):
            for x in range(gen_x1, gen_x2):
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr, self.win_ptr, x, y,
                    0x4CAF50
                )

        for y in range(solve_y1, solve_y2):
            for x in range(solve_x1, solve_x2):
                color = 0x2196F3 if not self.show_solution else 0xFF5722
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr, self.win_ptr, x, y, color
                )

        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win_ptr, 
            gen_x1 + 20, gen_y1 + 10, 
            0xFFFFFF, "Generate Maze"
        )

        solve_text = "Hide Path" if self.show_solution else "Solve Maze"
        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win_ptr,
            solve_x1 + 25, solve_y1 + 10,
            0xFFFFFF, solve_text
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