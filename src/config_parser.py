import os
from typing import Dict, Tuple
from pathlib import Path

def parse_config(filename: str) -> dict:
    """
    Parse maze config file.
    Returns dict with keys:
    WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT
    Optional: SEED, BIAS, PATTERN, RENDER
    Raises ValueError if invalid format or missing required keys
    """
    config = {}
    required_keys = {'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'}
    optional_keys = {'SEED', 'BIAS', 'PATTERN', 'RENDER'}

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Configuration file '{filename}' not found.")

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            parts = line.split('=')
            if len(parts) != 2:
                raise ValueError(f"Invalid line format: '{line}'. Expected KEY=VALUE")

            key = parts[0].strip()
            value = parts[1].strip()

            config[key] = value

    missing_keys = required_keys - config.keys()
    if missing_keys:
        raise ValueError(f"Missing required keys: {missing_keys}")

    try:
        # Required conversions
        config['WIDTH'] = int(config['WIDTH'])
        config['HEIGHT'] = int(config['HEIGHT'])

        if config['WIDTH'] <= 0 or config['HEIGHT'] <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive integers")

        entry_parts = config['ENTRY'].split(',')
        if len(entry_parts) != 2:
            raise ValueError(f"ENTRY must be in format 'x,y', got: {config['ENTRY']}")
        entry = (int(entry_parts[0]), int(entry_parts[1]))
        config['ENTRY'] = entry

        exit_parts = config['EXIT'].split(',')
        if len(exit_parts) != 2:
            raise ValueError(f"EXIT must be in format 'x,y', got: {config['EXIT']}")
        exit_pos = (int(exit_parts[0]), int(exit_parts[1]))
        config['EXIT'] = exit_pos

        if not (0 <= entry[0] < config['WIDTH'] and 0 <= entry[1] < config['HEIGHT']):
            raise ValueError(f"ENTRY {entry} is outside maze bounds")

        if not (0 <= exit_pos[0] < config['WIDTH'] and 0 <= exit_pos[1] < config['HEIGHT']):
            raise ValueError(f"EXIT {exit_pos} is outside maze bounds")

        if entry == exit_pos:
            raise ValueError("ENTRY and EXIT must be different positions")

        config['PERFECT'] = config['PERFECT'].lower() in ('true', '1', 'yes')

        # Optional conversions
        if 'SEED' in config:
            config['SEED'] = int(config['SEED'])

        if 'BIAS' in config:
            config['BIAS'] = float(config['BIAS'])
            if not (0.0 <= config['BIAS'] <= 1.0):
                raise ValueError("BIAS must be between 0 and 1")

        if 'PATTERN' in config:
            pattern = str(config['PATTERN'])

            if len(pattern) != 2:
                raise ValueError("PATTERN must be exactly 2 characters long")

            if not pattern.isalnum():
                raise ValueError("PATTERN must be alphanumeric (letters and numbers only)")
            config['PATTERN'] = pattern

        if 'RENDER' in config:
            render = str(config['RENDER'])

            if render != "MLX" and render != "ASCII":
                raise ValueError("RENDER must be either MLX or ASCII")

            config['RENDER'] = str(config['RENDER'])

    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid value in config: {e}")

    return config