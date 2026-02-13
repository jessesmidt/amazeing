
"""

	Heuristic Search Psuedo-code


function A_STAR(start, goal, maze):
- location of start
- location of goal
- and the maze generated ofcourse



    open_set = priority queue
    open_set.push(start, priority = h(start))

	

    came_from = empty map

    g_score[start] = 0

    while open_set is not empty:

        current = open_set.pop_lowest_priority()

        if current == goal:
            return RECONSTRUCT_PATH(came_from, current)

        for each neighbor of current:
            if neighbor is a wall:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score
               OR tentative_g < g_score[neighbor]:

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + h(neighbor)

                open_set.push(neighbor, priority = f_score)

    return FAILURE

	
HEURISTIC SEARCH

f(n) = g(n) + h(n)

f(n) = best case total distance if i pick this node

g(n) = cost from start to current node
        - so amount of steps taken so far yk
		
h(n) = esitmated distance to finish
        - something like manhatten works well for this or something


	
"""

width = 8
height = 8


##########
#   #    #    
# # # ## #
# #    # #
# #### # #
#        #
##########




# define the function print_maze
# parameters (maze, entry exit)
# 	-> 	when calling funciton we require these 3
# 	- 	maze (assortment of 1's and 0's in a grid)
# 	- 	entry (x & y cords of the entry/start)
# 	-	exit (x & y cords of the exit/finish)
# 
# for loop condition
# 	-	for y (row indexing)
# 	-	, row (tell y is the row indexing)
#	-	indexes inside maze (checks if indexes exist)
# 
# for x, cell in enumerate(row)
# 	-	x is just the indexing for each collum (cell)
# 	-	inumerate(row), get the row indexing, also just y
# if start coords == current coords
# 	-	this becomes S (start)
# else if goal coords == current coords
# 	-	this becomes G (goal)
# else 
# 	do a # if cell == 1
# 	else do ' ' 
# then print the line we just made yk
# and do y++


# def print_maze(maze, start, goal):
# 	for y, row in enumerate(maze):
# 		line = ""
# 		for x, cell in enumerate(row):
# 			if start == (x,y):
# 				line += 'S'
# 			elif goal == (x,y):
# 				line += 'G'
# 			else:
# 				line += '#' if cell == 1 else ' '
# 		print(line)

# print_maze(maze, start, goal)


import heapq







start = (1,1)
goal = (8,5)


# This makes the class 'Cell'
# It storest this info
# coords (x, y)
# if it has a wall in a direction(true)
# or not (false || air)#
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.walls = {
            'N': True,
            'S': True,
            'E': True,
            'W': True
        }

        self.g = float('inf')
        self.mhd = 0
        self.f = float('inf')
        
        self.parent = None
        self.in_path = False

        self.is_start = False
        self.is_goal = False


# define manhattan function
# manhattan function returns the distance
# from current to goal (absolute distance)
# (current_x - goal_x) + (current_y - goal_y)#
def manhattan(cell, goal):
	return abs(cell[0] - goal[0]) + abs(cell[1] -  goal[1])



def get_neighbors(cell, maze):
    neighbors = []

    x, y = cell.x, cell.y

    if not cell.walls['N']:
        neighbors.append(maze[y - 1][x])
    if not cell.walls['S']:
        neighbors.append(maze[y + 1][x])
    if not cell.walls['W']:
        neighbors.append(maze[y][x - 1])
    if not cell.walls['E']:
        neighbors.append(maze[y][x + 1])

    return neighbors

def reconstruct_path(goal):
     current = goal
     while current.parent:
          current.in_path = True
          current = current.parent


# define the function solve_maze
# needs this info:
#   start = starting cell (with the cords etc)
#   goal = the goal cell (with the cords etc)
#   maze = 2d maze structure yk
# 
# Make 2 sets
#   open_set = all cells we might still visit
#   closed_set = all cells we already checked type xi
# 
# Initialize Start Cell
#   g = distance from start to current
#   mhd = manhattan distance to goal
#   f = mhd + g
# 
# Add the start to the open set yk
# 
# while open_set
#   keep looking untill there aint nothing to explore yk
# 
# currrent = min..etc.
#   look through open_set
#   idk wtf is happening here ngl
# 
# if current == goal
#   cheack if the goal is reached type xi
#   cuz then we gotta go back and reconstruct
#   the path using the parent-chain-shit
# 
# open_set.remove(current) & closed_set.add(current)
#   remove it from the ones we havent explored yet
#   add it to the ones that we have already explored type xi#
def solve_maze(start, goal, maze):
    open_set = []
    closed_set = set()

    start.g = 0
    start.mhd = manhattan(start, goal)
    start.f = start.g + start.mhd
        
    open_set.append(start)

    while open_set:
            #look for the cell with the lowest f
        current = min(open_set, key=lambda c: c.f)
        
        if current == goal:
            return reconstruct_path(goal)

        open_set.remove(current)
        closed_set.add(current)
        
        for neighbor in get_neighbors(current, maze):
            if neighbor in closed_set:
                continue

            tentative_g = current.g + 1
            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tentative_g >= neighbor.g:
                continue

            neighbor.parent = current
            neighbor.g = tentative_g
            neighbor.mhd = manhattan(neighbor, goal)
            neighbor.f = neighbor.g + neighbor.mhd

