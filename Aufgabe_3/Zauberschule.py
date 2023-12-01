#BWINF Runde_1 Aufgabe_3
import numpy as np
import time as t



#inputs route from a valid file
def inputLayoutFromFile(file):

    #the file is opened and the dimensions of each layer contained in the first line are saved
    f = open(file, "r", encoding = 'utf-8')
    dimensions = f.readline().strip().split()

    #the start coordinates and a goal check are initialized for later error check
    startX, startY, startZ = -1, -1, -1
    goalFound = False

    #if the first line did not contain two integers an error message is returned
    if bool(dimensions) is False: return "first line has to contain the y and x dimension"
    if dimensions[0].isdigit() is False: return "first line has to contain the y and x dimension"
    dimY, dimX = map(int, dimensions)

    #a 3d numpy array is initialized using the saved dimensions
    layout = np.array([[['' for _ in range(2)] for _ in range(dimY)] for _ in range(dimX)])

    #iteration through the layers
    for i in range(2):

        #the input rows are placed into the array at the correct position
        for j in range(dimY):
            line = list(f.readline().strip())
            layout[:, j, i] = line

            #if a line has the wrong number of characters an error message is returned
            if len(line) != dimX: return "the rows have to have the correct number of characters"

            #the current line is scanned for the starting and end point
            for k in range(dimX):
                if(layout[k, j, i] == 'A'):
                    startX, startY, startZ = k, j, i
                if(layout[k, j, i] == 'B'):
                    goalFound = True

                #if an invalid character is contained in the input an error message is returned
                if (layout[k, j, i] == 'A' or 'B' or '#' or '.') == False: return "layout has wrong syntax"

        #the empty line between the layers is skipped
        f.readline()

    #if the start coordinates or the goal were not found an error message is returned
    if startX == -1 or goalFound == False: print("no start coordinates or goal where found")

    #the filled 3d array is returned
    return layout, dimX, dimY, startX, startY, startZ



#returns wether a position is in bounds of the layout and on a path or not
def isValidPosition(layout, dimX, dimY, x, y, z):

    #checks if the position is in bounds
    if(0 <= x < dimX and 0 <= y < dimY and 0 <= z < 2):

        #returns if a wall is in the position
        return layout[x][y][z] != "#"

    #if the position is out of bounds False is returned
    return False



#returns the collected path information, the shortest distance from the start to the goal and the coordinates of the goal
def findShortestPathWithDijkstra(layout, dimX, dimY, startX, startY, startZ):

    #coordinates to save current position and direction tuple are initialized
    x, y, z = startX, startY, startZ
    movement = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    #library that saves distance to start, predecessor and visit status for coordinates is initialized and data of starting point is entered
    data = {}
    data[startX, startY, startZ] = [0, None, True]

    #iterates through different positions till the goal is found or all positions where checked
    while True:

        #current position is marked in library
        data[x, y, z][2] = True

        #if the current position is the goal, the collected path information, the shortest distance from the start to the goal and the coordinates of the goal is returned
        if layout[x][y][z] == "B":
            return data, shortestDistance, x, y, z

        #iteration through all six directions from current position
        for dX, dY, dZ in movement:

            #if the new positon is valid, the distance to the current position and the distance to the new position, if there is one, is extracted from the library and saved
            #if there is no entry for the new position in the library yet, the distance is saved as infinite
            if isValidPosition(layout, dimX, dimY, x + dX, y + dY, z + dZ):
                distanceToCurrentPosition = data[(x, y, z)][0]
                distanceToNewPosition = data.get((x + dX, y + dY, z + dZ), [float('inf')])[0]

                #if the new position is on the same layer as the current, it is checked if the distance to the current position + 1 is smaller than currently saved distance
                #if the new position is on a different layer as the current, it is checked if the distance to the current position + 3 is smaller than currently saved distance
                #if that is the case the library entry to the new position is overwritten with the new distance, the current position as the predecessor and the previous visit status
                #if there was no previous entry, a new one is created with the calculated distance, the current position as the predecessor and the visit status as False
                if dZ == 0 and (distanceToNewPosition > distanceToCurrentPosition + 1):
                    data[x + dX, y + dY, z + dZ] = [distanceToCurrentPosition + 1, (x, y, z), data.get((x + dX, y + dY, z + dZ), [None, None, False])[2]]
                if dZ != 0 and (distanceToNewPosition > distanceToCurrentPosition + 3):
                    data[x + dX, y + dY, z + dZ] = [distanceToCurrentPosition + 3, (x, y, z), data.get((x + dX, y + dY, z + dZ), [None, None, False])[2]]

        #to find a new position a tuple saving the new position and an integer saving the current shortst distance are initialized
        shortestDistance = float('inf')
        newNode = ()

        #iteration through the whole library
        for values in data.items():

            #if the distance of the current element is smaller than the currently saved distance and the element was not visited yet,
            #the new shortest distance and the coordinates of the element are saved
            distanceOfCurrentElement, visitStatus, coordinatesOfCurrentElement = values[1][0], values[1][2], values[0]
            if distanceOfCurrentElement < shortestDistance and visitStatus == False:
                shortestDistance = distanceOfCurrentElement
                newNode = coordinatesOfCurrentElement
        
        #if all positions where visited an error message is returned
        if newNode == (): return "no valid path from start to goal"

        #the new position is set for the next iteration
        x, y, z = newNode



#returns the layout with the marked path that was created using the collected path information
def outputPath(layout, data, goalX, goalY, goalZ):

    #the current position is initialized as the goal and the next position as its predecessor
    currentX, currentY, currentZ = goalX, goalY, goalZ
    predecessorX, predecessorY, predecessorZ = data[goalX, goalY, goalZ][1]

    #the specific directions are associated with the different direction characters in a library
    movementSigns = {(1, 0, 0): ">", (-1, 0, 0): "<", (0, 1, 0): "v", (0, -1, 0): "^", (0, 0, 1): "!", (0, 0, -1): "!"}

    #backtracks through the saved path till the start is reached
    while(True):

        #the sign that shows the movement from the predecessor of the current position to the current position is extracted from the library
        currentSign = movementSigns[currentX - predecessorX, currentY - predecessorY, currentZ - predecessorZ]

        #the extracted sign is assigned to the current position in the layout
        layout[predecessorX, predecessorY, predecessorZ] = currentSign

        #if a predecessor of the current position exists / if the start is not reached yet, the current and the predecessor position is overwritten
        if(data.get(data[predecessorX, predecessorY, predecessorZ][1]) != None):
            currentX, currentY, currentZ = predecessorX, predecessorY, predecessorZ
            predecessorX, predecessorY, predecessorZ = data[predecessorX, predecessorY, predecessorZ][1]

        #if the start is reached, a break occurs
        else: break

    #iteration through the layers
    for i in range(2):

        #the individual rows are read from the layout, converted to a string and printed to the console
        for j in range(dimY):
            print(''.join(layout[:, j, i]))

        #an empty line is printed to the console to easily differentiate between layers
        print("")



#main
if __name__ == '__main__':

    #the time calculation starts and the input layout is read
    start = t.perf_counter()
    layout = inputLayoutFromFile("Aufgabe_3/input/zauberschule5.txt")

    #the error message is printed to the console if an error occured
    if isinstance(layout, str):
        print("Error")
        print(layout)

    #execution of code if no error occured
    else:

        #the dimensions and start coordinates are printed to the console
        layout, dimX, dimY, startX, startY, startZ = layout
        print(dimX, dimY)
        print(startX, startY, startZ)

        #the shortest path to the goal is calculated
        data = findShortestPathWithDijkstra(layout, dimX, dimY, startX, startY, startZ)

        #the error message is printed to the console if an error occured
        if isinstance(data, str):
            print("Error")
            print(data)

        #execution of code if no error occured
        else:

            #the shortest path is printed to the console
            data, distance, goalX, goalY, goalZ = data
            outputPath(layout, data, goalX, goalY, goalZ)

            #the goal coordinates and the distance from start to goal as well as the taken time are printed to the console
            print(goalX, goalY, goalZ)
            print(distance)
            end = t.perf_counter()
            print(end - start)
