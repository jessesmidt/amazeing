# Maze Data Structure Proposal

## Option 1: 2D List of Integers
- Each cell = integer (0-15) representing walls in binary
- Pros: Simple, matches output format
- Cons: Harder to work with during generation

## Option 2: 2D List of Dictionaries
- Each cell = {'N': True, 'E': False, 'S': True, 'W': True}
- Pros: Very readable, easy to modify
- Cons: Need conversion for output

## My recommendation: 
- Mijn voorkeur gaat uit naar 2D list of integers, lijkt mij makkelijker te programmeren. Misschien omdat ik de tweede optie niet zo goed begrijp, beste samen even bespreken.