import sys
from config_parser import parse_config

# # You will implement a maze generator in Python that takes a configuration file, generates a
# # maze, eventually perfect (with a single path between entrance and exit), and writes it to a
# # file using a hexadecimal wall representation. You will also provide a visual representation
# # of the maze and organize your code so that the generation logic can be reused later.

# Your program must be run with the following command:
# python3 a_maze_ing.py config.txt
# • a_maze_ing.py is your main program file. You must use this name.
# • config.txt is the only argument. It is a plain text file that defines the maze
# generation options. You can use a different filename.
# Your program must handle all errors gracefully: invalid configuration, file not found, bad
# syntax, impossible maze parameters, etc. It must never crash unexpectedly, and must
# always provide a clear error message to the user.

def main():
	print("Amazeing is being initialized...")
	if len(sys.argv) != 2:
		print("Usage: python3 a_maze_ing.py config.txt")
		sys.exit(1)

	print(f"Loading config file: {sys.argv[1]}")

	try:
		config = parse_config(sys.argv[1])
	except ValueError as e:
		print(f"Error: {e}")
		return

	print("Config loaded successfully!")
	print(config)

#config is een dict (soort struct), gaan wij doorsturen naar algo functie


if __name__ == "__main__":
	main()
