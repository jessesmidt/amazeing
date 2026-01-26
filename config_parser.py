# IV.3
# Configuration file format
# The configuration file must contain one ‘KEY=VALUE‘ pair per line.
# Lines starting with # are comments and must be ignored.
# The following keys are mandatory:
# Key
# Description
# Example
# WIDTH
# Maze width (number of cells) WIDTH=20
# HEIGHT
# Maze height
# HEIGHT=15
# ENTRY
# Entry coordinates (x,y)
# ENTRY=0,0
# EXIT
# Exit coordinates (x,y)
# EXIT=19,14
# OUTPUT_FILE Output filename
# OUTPUT_FILE=maze.txt
# PERFECT
# Is the maze perfect?
# PERFECT=True

import sys
from typing import Dict, Tuple
from pathlib import Path

def parse_config(filename: str) -> dict:
	"""
	Parse maze config file.
	Returns dict with keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT
	Raises ValueError if invalid format or missing required keys
	"""
	config = {} #dict return type, makkelijk uit te pakken.
	required_keys = {'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'}

	with open(filename, 'r') as file:
		for line in file:
			line = line.strip()

			if not line:
				continue
			
			if line.startswith('#'):
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

	# converting types. Using try / error to raise errors.
	try:
		config['WIDTH'] = int(config['WIDTH'])
		config['HEIGHT'] = int(config['HEIGHT'])

		entry_parts = config['ENTRY'].split(',')
		if len(entry_parts) != 2:
			raise ValueError(f"ENTRY must be in format 'x,y', got: {config['ENTRY']}")
		config['ENTRY'] = (int(entry_parts[0]), int(entry_parts[1]))

		exit_parts = config['EXIT'].split(',')
		if len(exit_parts) != 2:
			raise ValueError(f"EXIT must be in format 'x,y' got: {config['EXIT']}")
		config['EXIT'] = (int(exit_parts[0]), int(exit_parts[1]))

		config['PERFECT'] = config['PERFECT'].lower() in ('true', '1', 'yes')

	# Input validation

		if config['WIDTH'] <= 0 or config['HEIGHT'] <= 0:
			raise ValueError("WIDTH and HEIGHT must be positive integers")
		
		entry_x = int(entry_parts[0])
		entry_y = int(entry_parts[1])
		if not (0 <= entry_x < config['WIDTH'] and 0 <= entry_y < config['HEIGHT']):
			raise ValueError(f"ENTRY {config['ENTRY']} is outside maze bounds")

		exit_x = int(exit_parts[0])
		exit_y = int(exit_parts[1])
		if not (0 <= exit_x < config['WIDTH'] and 0 <= exit_y < config['HEIGHT']):
			raise ValueError(f"EXIT {config['EXIT']} is outside maze bounds")

		if config['ENTRY'] == config['EXIT']:
			raise ValueError("ENTRY and EXIT must be different positions")

	except (ValueError, IndexError) as e:
		raise ValueError(f"Invalid value in config: {e}")

	return config
