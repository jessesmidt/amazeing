import os
import time
import random
from typing import Any
from src.maze.generator import Cell


##########################################
# Pattern Characters
##########################################

PATTERN_WALL = "▒▒"
PATTERN_EMPTY = "░░"

<<<<<<< HEAD
START_BLOCK = "\033[42m  \033[0m"
GOAL_BLOCK = "\033[41m  \033[0m"
=======
>>>>>>> f70abb5 (pattern fixes)

##########################################
# Colour System
##########################################

class Style:
    """
    Predefined shades for background, wall, and path.
    Each color has three levels: darkest (bg), medium (wall), lightest (path)
    """

    COLOR_SHADES = {
        "black":    (16, 236, 239),
        "red":      (88, 160, 210),
        "green":    (22, 34, 46),
        "yellow":   (184, 190, 226),
        "blue":     (17, 27, 33),
        "magenta":  (89, 127, 165),
        "cyan":     (38, 45, 51),
        "white":    (250, 255, 231),
    }

    def __init__(self, bg_color: str, wall_color: str, path_color: str):
        self.bg = self.make_block(bg_color, "bg")
        self.wall = self.make_block(wall_color, "wall")
        self.path = self.make_block(path_color, "path")

        self.start = "\033[48;5;46m  \033[0m"
        self.goal = "\033[48;5;196m  \033[0m"

    def make_block(self, color_name: str, level: str) -> str:
        color_name = color_name.lower()
        if color_name not in self.COLOR_SHADES:
            raise ValueError(f"Unsupported color: {color_name}")

        index = {"bg": 0, "wall": 1, "path": 2}[level]
        code = self.COLOR_SHADES[color_name][index]
        return f"\033[48;5;{code}m  \033[0m"


##########################################
# Terminal Display
##########################################

class TerminalDisplay:
    def __init__(
        self,
        grid: list[list[Cell]],
        config: dict[str, Any],
        style: Style | None = None,
    ) -> None:
        self.grid = grid
        self.config = config
        self.show_solution = False
        self.error_message: str | None = None

        self.style = style or Style("black", "blue", "red")

        self.solution_cells = [
            cell
            for row in self.grid
            for cell in row
            if cell.in_path
        ]

        # Reset visual state for animation/toggling
        for cell in self.solution_cells:
            cell.in_path = False

    ##########################################
    # Rendering Loop
    ##########################################

    def render(self) -> None:
        while True:
            os.system("clear")
            self.draw_maze()

            if self.error_message:
                print(f"\n {self.error_message}")

            choice = self.ascii_menu()

            if not self.handle_choice(choice):
                break

    ##########################################
    # Character Helpers
    ##########################################

    def _wall_char(self, cell: Cell) -> str:
        return PATTERN_WALL if cell.pattern else self.style.wall

    def _open_char(self, cell: Cell, in_path: bool = False) -> str:
        if in_path and self.show_solution:
            return self.style.path
        return PATTERN_EMPTY if cell.pattern else self.style.bg

    ##########################################
    # Maze Drawing
    ##########################################

    def draw_maze(self) -> None:
        h = len(self.grid)
        w = len(self.grid[0])

        for y in range(h):

            # TOP (north walls)
            for x in range(w):
                cell = self.grid[y][x]
                north_open = (
                    y > 0 and cell.in_path and self.grid[y - 1][x].in_path
                )

                print(self._wall_char(cell), end="")
                if cell.walls["N"]:
                    print(self._wall_char(cell), end="")
                else:
                    print(self._open_char(cell, north_open), end="")
                print(self._wall_char(cell), end="")
            print()

            # MIDDLE (west + interior + east)
            for x in range(w):
                cell = self.grid[y][x]

                west_open = (
                    x > 0 and cell.in_path and self.grid[y][x - 1].in_path
                )
                east_open = (
                    x < w - 1 and cell.in_path and self.grid[y][x + 1].in_path
                )

                if cell.walls["W"]:
                    print(self._wall_char(cell), end="")
                else:
                    print(self._open_char(cell, west_open), end="")

                if cell.is_start:
                    print(self.style.start, end="")
                elif cell.is_goal:
                    print(self.style.goal, end="")
                else:
                    print(self._open_char(cell, cell.in_path), end="")

                if cell.walls["E"]:
                    print(self._wall_char(cell), end="")
                else:
                    print(self._open_char(cell, east_open), end="")
            print()

            # BOTTOM (south walls)
            for x in range(w):
                cell = self.grid[y][x]
                south_open = (
                    y < h - 1 and cell.in_path and self.grid[y + 1][x].in_path
                )

                print(self._wall_char(cell), end="")
                if cell.walls["S"]:
                    print(self._wall_char(cell), end="")
                else:
                    print(self._open_char(cell, south_open), end="")
                print(self._wall_char(cell), end="")
            print()

    ##########################################
    # Menu
    ##########################################

    def ascii_menu(self) -> int:
        print(
            "\n=== A-Maze-Ing ==="
            "\n1. Re-generate a new maze"
            "\n2. Show/Hide path from entry to exit"
            "\n3. Pick custom color"
            "\n4. Quit"
        )
        try:
            return int(input("Choice? (1-4): "))
        except ValueError:
            return -1

    ##########################################
    # Menu Handler
    ##########################################

    def handle_choice(self, choice: int) -> bool:
        if choice == 1:
            self.regenerate_maze()

        elif choice == 2:
            if self.show_solution:
                self.hide_solution()
            else:
                self.animate_solution_random(delay=0.05)

        elif choice == 3:
            self.pick_colors()

        elif choice == 4:
            return False

        else:
            print("Invalid choice!")
            time.sleep(1)

        return True

    ##########################################
    # Actions
    ##########################################

    def regenerate_maze(self) -> None:
        from src.maze.generator import generate_maze
        from src.maze.maze_solver import solve_maze
        from src.maze.print_output import print_output_main

        self.grid = generate_maze(self.config)
        solve_maze(self.grid)

        # Store solution once
        self.solution_cells = [
            cell for row in self.grid for cell in row if cell.in_path
        ]

        # Reset visual state
        for cell in self.solution_cells:
            cell.in_path = False

        self.show_solution = False
        print_output_main(self.grid, self.config)

    ##########################################
    # Solution Logic
    ##########################################

    def hide_solution(self) -> None:
        for cell in self.solution_cells:
            cell.in_path = False

        self.show_solution = False
        os.system("clear")
        self.draw_maze()

    def animate_solution_random(self, delay: float = 0.05) -> None:
        if not self.solution_cells:
            self.error_message = "No solution path found!"
            return

        # Ensure hidden first
        for cell in self.solution_cells:
            cell.in_path = False

        self.show_solution = True

        shuffled = self.solution_cells.copy()
        random.shuffle(shuffled)

        for cell in shuffled:
            cell.in_path = True
            os.system("clear")
            self.draw_maze()
            time.sleep(delay)

        # Make sure fully visible
        for cell in self.solution_cells:
            cell.in_path = True

    ##########################################
    # Color Picker
    ##########################################

    def pick_colors(self) -> None:
        print("Available colors:")
        print(", ".join(Style.COLOR_SHADES.keys()))
        print()

        try:
            bg = input("Background color: ").strip().lower()
            wall = input("Wall color: ").strip().lower()
            path = input("Path color: ").strip().lower()

            for color in (bg, wall, path):
                if color not in Style.COLOR_SHADES:
                    raise ValueError(f"Unsupported color: {color}")

            self.style = Style(bg, wall, path)
            self.error_message = None

        except ValueError as e:
            self.error_message = str(e)
            time.sleep(1)
