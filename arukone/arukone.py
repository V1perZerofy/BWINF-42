import random #for generating random numbers
from collections import deque
import math
import json #for saving the puzzle and solution to a .json file
from drawArukone import main as draw_puzzle

excluded = []
paths = []

def is_valid_position(puzzle, x, y):
    #check if the cell is within the grid and is empty and is not part of an existing path
    return puzzle[x][y] == 0 and (x, y) not in excluded

def generator(n, numCount): #generate a puzzle
    puzzle = [[0 for _ in range(n)] for _ in range(n)] #create an empty grid
    for num in range(1, numCount + 1): #for each number
        placed = False #boolean to indicate if the number has been placed
        for _ in range(n*n):  #attempts scaled to the size of the puzzle
            x1, y1 = random.randint(0, n-1), random.randint(0, n-1) #get random coordinates for the first number
            x2, y2 = random.randint(0, n-1), random.randint(0, n-1) #get random coordinates for the second number
            if (x1, y1) != (x2, y2) and is_valid_position(puzzle, x1, y1) and is_valid_position(puzzle, x2, y2) and doesPathExist(puzzle, (x1, y1), (x2, y2), excluded): #if the coordinates are not the same and are valid and a path exists between them (using A*)
                puzzle[x1][y1] = num #place the number at the first coordinates
                puzzle[x2][y2] = num #place the number at the second coordinates
                placed = True #indicate that the number has been placed
                break #break out of the loop
        if not placed: #if the number was not placed
            return None  #return None to indicate that the number pair could not be placed (this will cause the puzzle to be regenerated)
    return puzzle, paths #return the puzzle and the paths	


#save functions
#save puzzle to file txt
def saveAsTxt(puzzle, n, numCount):
    f = open("arukone/exports/puzzle.txt", "w")
    f.write(str(n) + "\n")
    f.write(str(numCount) + "\n")
    for row in puzzle:
        f.write(' '.join(map(str, row)) + "\n")
    f.close()

#save puzzle and solution to .json file for drawing
def saveAsJson(puzzle, n, numCount):
    data = {
        "puzzle": puzzle,
        "solution": paths
    }

    with open("arukone/exports/puzzle.json", "w") as f:
        json.dump(data, f)

#print functions
def print_puzzle(puzzle, n, numCount):
    print(n)
    print(numCount)
    for row in puzzle:
        print(' '.join(map(str, row)))

def print_excluded(excluded):
    print(excluded)

#A* Algorithm Implementation to check if a path exists between two points
def heuristic(a, b):
    #Manhattan distance on a square grid
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def doesPathExist(puzzle, start, end, excluded):
    n = len(puzzle) #size of the puzzle
    open_set = set([start]) #set of nodes to be evaluated
    came_from = {} #map of navigated nodes
    g_score = {start: 0} #cost from start along best known path
    f_score = {start: heuristic(start, end)} #estimated total cost from start to goal through y

    while open_set: #while there are still nodes to be evaluated
        current = min(open_set, key=lambda x: f_score[x]) #node in open_set having the lowest f_score[] value

        if current == end: #if the current node is the end node
            path = reconstruct_path(came_from, current) #reconstruct the path
            excluded.extend(path) #add the path to the excluded list
            paths.append(path) #add the path to the paths list
            return True #return true to indicate that a path exists

        open_set.remove(current) #remove the current node from the open_set
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]: #for each neighbor of the current node
            neighbor = (current[0] + dx, current[1] + dy) #get the neighbor's coordinates
            if 0 <= neighbor[0] < n and 0 <= neighbor[1] < n and neighbor not in excluded: #if the neighbor is within the grid and is not part of an existing path
                tentative_g_score = g_score[current] + 1 #calculate the tentative g_score
                if tentative_g_score < g_score.get(neighbor, float("inf")): #if the tentative g_score is less than the neighbor's g_score
                    came_from[neighbor] = current #set the neighbor's came_from to the current node
                    g_score[neighbor] = tentative_g_score #set the neighbor's g_score to the tentative g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end) #set the neighbor's f_score to the tentative g_score + the heuristic
                    if neighbor not in open_set: #if the neighbor is not in the open_set
                        open_set.add(neighbor) #add the neighbor to the open_set

    return False #return false because no path was found

def reconstruct_path(came_from, current): #reconstruct the path
    total_path = [current] #start with the current node
    while current in came_from: #while the current node is in the came_from map
        current = came_from[current] #set the current node to the node that came before it
        total_path.append(current) #add the current node to the total path
    return total_path[::-1] #return the total path in reverse order (start to end)

def main(n): 
    numCount = random.randint(n//2, n)
    puzzle, path = generator(n, numCount)
    if puzzle is None:
        print('Failed to generate a puzzle')
    else:
        print_puzzle(puzzle, n, numCount)
        saveAsTxt(puzzle, n, numCount)
        saveAsJson(puzzle, n, numCount)

if __name__ == '__main__':
    main(20)
    draw_puzzle()
