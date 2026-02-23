*This project has been created as part of the 42 curriculum by jsmidt, sbonevel.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator and visualizer written in Python. It generates mazes from a configuration file, writes them to an output file using a hexadecimal wall encoding, and displays them either in the terminal via ASCII rendering or graphically via the MiniLibX (MLX) library.

The generator supports both perfect mazes (exactly one path between any two cells) and imperfect mazes with multiple paths. Every generated maze contains a hidden "42" pattern formed by fully closed cells, and includes a computed shortest path from entry to exit.

The maze generation logic is packaged as a standalone reusable Python library (`mazegen`) that can be installed via pip.

---

## Instructions

### Requirements

- Python 3.10 or later
- MiniLibX (included, for graphical display)

### Installation

```bash
make install
```

### Running the program

```bash
python3 a_maze_ing.py config.txt
```

Or via the Makefile:

```bash
make run
```

### Debug mode

```bash
make debug
```

### Lint

```bash
make lint
```

### Clean

```bash
make clean
```

---

## Configuration File Format

The configuration file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are treated as comments and ignored.

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Generate a perfect maze | `PERFECT=True` |
| `SEED` | Random seed for reproducibility | `SEED=42` |
| `BIAS` | Algorithm bias (0.0–1.0) | `BIAS=0.5` |
| `IMPRATE` | Imperfection rate (0–100) | `IMPRATE=65` |
| `PATTERN` | Pattern to embed in maze | `PATTERN=42` |
| `RENDER` | Display mode (`2D` or `MLX`) | `RENDER=2D` |

A default `config.txt` is provided at the root of the repository.

---

## Maze Generation Algorithms

### Growing Tree (covers DFS and Prim's)

The `sigma_male_random_maze_generator` function implements the **Growing Tree** algorithm, controlled by a `bias` parameter:

- `bias = 1.0` → always picks the most recently added cell → behaves as **Recursive Backtracker (DFS)**, producing long winding corridors
- `bias = 0.0` → always picks a random cell → behaves as **Prim's algorithm**, producing mazes with many short dead ends
- `0.0 < bias < 1.0` → hybrid behaviour between the two

This means a single function covers two classic algorithms depending on configuration.

### Wilson's + Hunt-and-Kill

The `wilson_sometimes_hunts` function combines **Wilson's algorithm** (loop-erased random walks) with a **Hunt-and-Kill** fallback. The `bias` parameter controls how often each branch is used. An `imprate` (imperfection rate) parameter randomly removes extra walls to create imperfect mazes with multiple paths.

### Why these algorithms?

Wilson's algorithm guarantees a uniform spanning tree, meaning every possible perfect maze is equally likely to be generated. The Growing Tree algorithm was chosen for its flexibility — one implementation covers the full spectrum from DFS to Prim's by adjusting a single parameter. The Hunt-and-Kill fallback ensures progress when Wilson's random walks get stuck in sparse unvisited regions.

---

## Visual Representation

Two display modes are available:

**Terminal ASCII** — renders the maze directly in the terminal using box-drawing characters. Entry, exit, and the solution path are clearly marked.

**MiniLibX (MLX)** — graphical window rendering. Set `RENDER=MLX` in your config file to use this mode.

### User interactions

| Key / Action | Effect |
|---|---|
| `R` | Re-generate a new maze |
| `P` | Show / hide the shortest path |
| `C` | Cycle wall colours |
| `ESC` or close window | Exit |

---

## Reusable Module

The maze generation logic is packaged as a standalone pip-installable library.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from maze import MazeGenerator

config = {
    'WIDTH': 20,
    'HEIGHT': 15,
    'ENTRY': (0, 0),
    'EXIT': (19, 14),
    'PERFECT': True,
    'SEED': 42,
    'BIAS': 0.7,
}

mg = MazeGenerator(config)
grid = mg.generate()
```

### Accessing the maze structure

`mg.generate()` returns a 2D list of `Cell` objects (`grid[y][x]`).

Each `Cell` exposes:

```python
cell.x, cell.y          # coordinates
cell.walls              # dict: {'N': bool, 'E': bool, 'S': bool, 'W': bool}
cell.is_start           # True if this is the entry cell
cell.is_goal            # True if this is the exit cell
cell.in_path            # True if this cell is part of the shortest path
```

### Custom parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `WIDTH` | int | required | Maze width |
| `HEIGHT` | int | required | Maze height |
| `ENTRY` | tuple | required | Entry `(x, y)` |
| `EXIT` | tuple | required | Exit `(x, y)` |
| `PERFECT` | bool | required | Perfect maze or not |
| `SEED` | int/None | `None` | Random seed |
| `BIAS` | float | `0.5` | Growing Tree bias |
| `IMPRATE` | int | `65` | Imperfection rate (imperfect mazes only) |

### Building the package from source

```bash
python -m venv build_env
source build_env/bin/activate
pip install build
python -m build
```

This produces `dist/mazegen-1.0.0-py3-none-any.whl` and `dist/mazegen-1.0.0.tar.gz`.

---

## Team & Project Management

### Roles

**jsmidt** — configuration file parsing, MLX graphical output, Makefile, general file system structure, lint compliance.

**sbonevel** — all maze generation algorithms (Growing Tree / DFS / Prim's, Wilson's + Hunt-and-Kill), terminal ASCII output, maze solver.

### Planning

We started by agreeing on the `Cell` data structure and the config format so both of us could work in parallel from day one. The initial plan was to finish generation first, then display, then packaging — this held up reasonably well. The main deviation was that the circular import between `generator.py` and `pattern.py` cost us time mid-project, which we resolved by moving `Cell` into its own `cell.py` module.

### What worked well

Splitting generation and display cleanly between team members meant we rarely blocked each other. Using a bias parameter to cover both DFS and Prim's in one function kept the codebase lean.

### What could be improved

We underestimated the time needed for flake8/mypy compliance, especially with type hints across the whole codebase. Starting lint early would have saved time at the end.

### Tools used

- Python 3.13
- MiniLibX for graphical rendering
- `build` for packaging
- `mypy` and `flake8` for static analysis and style
- Git for version control

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Buckblog: Maze algorithms by Jamis Buck](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [Wilson's algorithm explained](https://en.wikipedia.org/wiki/Loop-erased_random_walk)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [MiniLibX documentation](https://harm-smits.github.io/42docs/libs/minilibx)
- [mypy documentation](https://mypy.readthedocs.io/)

### AI usage

AI (Claude) was used for the following tasks:
- Explaining the differences between maze generation algorithms and helping choose between them
- Debugging the circular import issue between `generator.py` and `pattern.py`
- Guiding the Python packaging process (`pyproject.toml` setup, `python -m build`, `.whl` structure)
- Reviewing type hint syntax for `mypy` compliance
- Drafting this README

All AI-generated content was reviewed, tested, and validated by both team members before inclusion in the project.