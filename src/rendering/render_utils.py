from src.maze.generator import Cell


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
