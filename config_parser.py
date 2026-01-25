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
	require_keys = {'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'}

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

	return config
	
	# TODO: 
    # 6. Convert types (int(), tuple(), bool())

# def main():
# 	parse_config("config.txt")


# if __name__ == "__main__":
# 	main()