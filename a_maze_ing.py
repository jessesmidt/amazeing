# You will implement a maze generator in Python that takes a configuration file, generates a
# maze, eventually perfect (with a single path between entrance and exit), and writes it to a
# file using a hexadecimal wall representation. You will also provide a visual representation
# of the maze and organize your code so that the generation logic can be reused later.

Your program must be run with the following command:
python3 a_maze_ing.py config.txt
• a_maze_ing.py is your main program file. You must use this name.
• config.txt is the only argument. It is a plain text file that defines the maze
generation options. You can use a different filename.
Your program must handle all errors gracefully: invalid configuration, file not found, bad
syntax, impossible maze parameters, etc. It must never crash unexpectedly, and must
always provide a clear error message to the user.
IV.3
Configuration file format
The configuration file must contain one ‘KEY=VALUE‘ pair per line.
Lines starting with # are comments and must be ignored.
The following keys are mandatory:
Key
Description
Example
WIDTH
Maze width (number of cells) WIDTH=20
HEIGHT
Maze height
HEIGHT=15
ENTRY
Entry coordinates (x,y)
ENTRY=0,0
EXIT
Exit coordinates (x,y)
EXIT=19,14
OUTPUT_FILE Output filename
OUTPUT_FILE=maze.txt
PERFECT
Is the maze perfect?
PERFECT=True