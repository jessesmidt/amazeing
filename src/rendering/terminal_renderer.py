import os
import time
from typing import Any
from src.maze.generator import Cell


WALL = "██"
EMPTY = "  "

PATTERN_WALL = "▒▒"
PATTERN_EMPTY = "░░"

START_BLOCK = "\033[42m  \033[0m"
GOAL_BLOCK = "\033[41m  \033[0m"
PATH_BLOCK = "\033[44m  \033[0m"


class TerminalDisplay:
    def __init__(
            self, grid: list[list[Cell]], config: dict[str, Any]
            ) -> None:
        """
        Initialize the terminal display.

        Args:
            grid: 2D list of Cell objects representing the maze.
            config: Parsed configuration stored as a dict.
        """
        self.grid = grid
        self.config = config
        self.show_solution = False
        self.color_index = 0
        self.error_message: str | None = None

    def render(self) -> None:
        """
        Main rendering loop for the terminal display.

        Clears the screen, draws the maze, and shows the menu on each
        iteration. Exits when handle_choice returns False.
        """
        while True:
            os.system('clear')
            self.draw_maze()

            if self.error_message:
                print(f"\n {self.error_message}")
            choice = self.ascii_menu()

            if not self.handle_choice(choice):
                break

    def _wall_char(self, cell: Cell) -> str:
        """
        Return the correct wall character for a cell.

        Args:
            cell: The cell to get the wall character for.

        Returns:
            PATTERN_WALL if the cell is part of a pattern, otherwise WALL.
        """
        return PATTERN_WALL if cell.pattern else WALL

    def _open_char(self, cell: Cell, in_path: bool = False) -> str:
        """
        Return the correct open/corridor character for a cell.

        Args:
            cell: The cell to get the character for.
            in_path: Whether this position is part of the solution path.

        Returns:
            PATH_BLOCK if in_path and solution is visible,
            PATTERN_EMPTY if the cell is a pattern cell, otherwise EMPTY.
        """
        if in_path and self.show_solution:
            return PATH_BLOCK
        return PATTERN_EMPTY if cell.pattern else EMPTY

    def draw_maze(self) -> None:
        """
        Render the maze to the terminal using block characters.

        Each cell is drawn as a 3x3 block covering the top (north wall),
        middle (west wall, interior, east wall), and bottom (south wall).
        Pattern cells, start/goal markers, and the solution path are all
        rendered with distinct characters or colors.
        """
        h = len(self.grid)
        w = len(self.grid[0])

        for y in range(h):
            for x in range(w):
                cell = self.grid[y][x]
                north_open = (
                    y > 0 and cell.in_path and self.grid[y-1][x].in_path)
                print(self._wall_char(cell), end="")
                if cell.walls["N"]:
                    print(self._wall_char(cell), end="")
                else:
                    print(self._open_char(cell, north_open), end="")
                print(self._wall_char(cell), end="")
            print()

            for x in range(w):
                cell = self.grid[y][x]
                west_open = (
                    x > 0 and cell.in_path and self.grid[y][x-1].in_path)
                east_open = (
                    x < w - 1 and cell.in_path and self.grid[y][x+1].in_path)

                if cell.walls["W"]:
                    print(self._wall_char(cell), end="")
                else:
                    print(self._open_char(cell, west_open), end="")

                if cell.is_start:
                    print(START_BLOCK, end="")
                elif cell.is_goal:
                    print(GOAL_BLOCK, end="")
                else:
                    print(self._open_char(cell, cell.in_path), end="")

                if cell.walls["E"]:
                    print(self._wall_char(cell), end="")
                else:
                    print(self._open_char(cell, east_open), end="")
            print()

            for x in range(w):
                cell = self.grid[y][x]
                south_open = (
                    y < h - 1 and cell.in_path and self.grid[y+1][x].in_path)
                print(self._wall_char(cell), end="")
                if cell.walls["S"]:
                    print(self._wall_char(cell), end="")
                else:
                    print(self._open_char(cell, south_open), end="")
                print(self._wall_char(cell), end="")
            print()

    def ascii_menu(self) -> int:
        """
        Display the interactive menu and return the user's choice.

        Returns:
            The selected option as an integer, or -1 if input was invalid.
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
        """
        Execute the action corresponding to the user's menu choice.

        Args:
            choice: The menu option selected by the user.

        Returns:
            False if the user chose to quit, True otherwise.
        """
        if choice == 1:
            self.regenerate_maze()
        elif choice == 2:
            self.toggle_solution()
        elif choice == 3:
            print("Sem doe je ding")
        elif choice == 4:
            return False
        else:
            print("Invalid choice!")
            time.sleep(1)
        return True

    def regenerate_maze(self) -> None:
        """
        Generate a new maze, solve it, write the output file, and update
        the grid. Resets show_solution to False.
        """
        from src.maze.generator import generate_maze
        from src.maze.print_output import print_output_main
        from src.maze.maze_solver import solve_maze
        self.grid = generate_maze(self.config)
        solve_maze(self.grid)
        print_output_main(self.grid, self.config)
        self.show_solution = False

    def toggle_solution(self) -> None:
        """
        Toggle visibility of the solution path.
        """
        self.show_solution = not self.show_solution

    def rotate_colors(self) -> None:
        """
        Cycle through available wall color schemes.
        """
        pass
