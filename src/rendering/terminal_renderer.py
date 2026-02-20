import os
import time
from src.maze.generator import Cell

WALL = "██" 
EMPTY = "  "

PATTERN_WALL = "▒▒"
PATTERN_EMPTY = "░░"

START_BLOCK = "\033[42m  \033[0m"
GOAL_BLOCK = "\033[41m  \033[0m"
PATH_BLOCK = "\033[44m  \033[0m"

class TerminalDisplay:
    def __init__(self, grid: list[list[Cell]], config: dict[str, any]) -> None:
        """
        Initialize the terminal display with maze and config.
        """
        self.grid = grid
        self.config = config
        self.show_solution = False
        self.color_index = 0
        self.error_message = None

    def render(self) -> None:
        """
        Rendering loop
        """
        while True:
            os.system('clear')
            self.draw_maze()
            
            if self.error_message:
                print(f"\n {self.error_message}")
            choice = self.ascii_menu()

            if not self.handle_choice(choice):
                break

    def draw_maze(self) -> None:
        """
        
        """
        h = len(self.grid)
        w = len(self.grid[0])

        for y in range(h):

            # ── TOP (north walls)
            for x in range(w):
                cell = self.grid[y][x]

                # NW corner
                if cell.pattern:
                    print(PATTERN_WALL, end="")
                else:
                    print(WALL, end="")

                # north corridor
                if cell.walls["N"]:
                    if cell.pattern:
                        print(PATTERN_WALL, end="")
                    else:
                        print(WALL, end="")
                else:
                    # no wall: check if both cells are in the path
                    if y > 0 and cell.in_path and self.grid[y-1][x].in_path and self.show_solution:
                        print(PATH_BLOCK, end="")
                    else:
                        if cell.pattern:
                            print(PATTERN_EMPTY, end="")
                        else:
                            print(EMPTY, end="")

                # NE corner
                if cell.pattern:
                    print(PATTERN_WALL, end="")
                else:
                    print(WALL, end="")

            print()

            # ── MIDDLE (west + interior + east)
            for x in range(w):
                cell = self.grid[y][x]

                # west corridor
                if cell.walls["W"]:
                    if cell.pattern:
                        print(PATTERN_WALL, end="")
                    else:
                        print(WALL, end="")
                else:
                    if x > 0 and cell.in_path and self.grid[y][x-1].in_path and self.show_solution:
                        print(PATH_BLOCK, end="")
                    else:
                        if cell.pattern:
                            print(PATTERN_EMPTY, end="")
                        else:
                            print(EMPTY, end="")

                # center content
                if cell.is_start:
                    print(START_BLOCK, end="")
                elif cell.is_goal:
                    print(GOAL_BLOCK, end="")
                elif cell.in_path and self.show_solution:
                    print(PATH_BLOCK, end="")
                else:
                    if cell.pattern:
                        print(PATTERN_EMPTY, end="")
                    else:
                        print(EMPTY, end="")

                # east corridor
                if cell.walls["E"]:
                    if cell.pattern:
                        print(PATTERN_WALL, end="")
                    else:
                        print(WALL, end="")
                else:
                    if x < w - 1 and cell.in_path and self.grid[y][x+1].in_path and self.show_solution:
                        print(PATH_BLOCK, end="")
                    else:
                        if cell.pattern:
                            print(PATTERN_EMPTY, end="")
                        else:
                            print(EMPTY, end="")

            print()

            # ── BOTTOM (south walls)
            for x in range(w):
                cell = self.grid[y][x]

                # SW corner
                if cell.pattern:
                    print(PATTERN_WALL, end="")
                else:
                    print(WALL, end="")

                # south corridor
                if cell.walls["S"]:
                    if cell.pattern:
                        print(PATTERN_WALL, end="")
                    else:
                        print(WALL, end="")
                else:
                    if y < h - 1 and cell.in_path and self.grid[y+1][x].in_path and self.show_solution:
                        print(PATH_BLOCK, end="")
                    else:
                        if cell.pattern:
                            print(PATTERN_EMPTY, end="")
                        else:
                            print(EMPTY, end="")

                # SE corner
                if cell.pattern:
                    print(PATTERN_WALL, end="")
                else:
                    print(WALL, end="")
            print()

    def ascii_menu(self) -> int:
        """
        Prints menu below the maze, can regenerate maze, change colors and show / hide path.
        """
        print(
            "\n=== A-Maze-Ing ==="
            "\n1. Re-generate a new maze"
            "\n2. Show/Hide path from entry to exit"
            "\n3. Rotate maze colors"
            "\n4. Quit"
            )
        try:
            return int(input("Choice? (1-4): "))
        except ValueError:
            return -1
        
    def handle_choice(self, choice: int) -> bool:
        from src.maze.print_output import print_output_main
        if choice == 1:
            self.regenerate_maze()
        elif choice == 2:
            self.toggle_solution()
        elif choice == 3:
            print("change maze colors")
        elif choice == 4:
            print("")
            return False
        else:
            print("Invalid choice!")
            time.sleep(1)
        return True

    def regenerate_maze(self):
            """Regenerate the maze and redraw"""
            from src.maze.generator import generate_maze
            from src.maze.print_output import print_output_main
            from src.maze.maze_solver import solve_maze
            self.grid = generate_maze(self.config)
            solve_maze(self.grid)
            print_output_main(self.grid, self.config)
            self.show_solution = False

    def toggle_solution(self) -> None:
        """Toggle path"""
        self.show_solution = not self.show_solution

    def rotate_colors(self) -> None:
        """Choose color scheme"""
        pass
