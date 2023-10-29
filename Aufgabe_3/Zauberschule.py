#BWINF Runde_1 Aufgabe_3
import numpy as np


def inputLayoutFromFile(file):
    f = open(file, "r")
    dimY, dimX = map(int, f.readline().strip().split())
    layer = 2
    layout = np.array([[['' for _ in range(layer)] for _ in range(dimY)] for _ in range(dimX)])

    for i in range(2):
        for j in range(dimY):
            line = list(f.readline().strip())
            for k in range(dimX):
                layout[k, j, i] = line[k]
                if(layout[k, j, i] == 'A'):
                    startX, startY, startLayer = k, j, i
        f.readline()
    
    return layout, dimX, dimY, startX, startY, startLayer

def isValidPosition(layout, dimX, dimY, x, y, layer):
    if(0 <= x < dimX and 0 <= y < dimY and 0 <= layer < 2):
        return layout[x][y][layer] != "#"
    return False

def findShortestPathWithDijkstra(layout, dimX, dimY, startX, startY, startLayer):
    shortestDistance = -1
    x, y, layer = startX, startY, startLayer
    movement = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    data = {}
    data[startX, startY, startLayer] = [0, None, True]
    sPF = False

    while sPF == False:
        data[x, y, layer][2] = True
        shortestDistance = data[x, y, layer][0]
        if layout[x][y][layer] == "B":
            sPF = True
            return data, shortestDistance, x, y, layer
        for dX, dY, dLayer in movement:
            if isValidPosition(layout, dimX, dimY, x + dX, y + dY, layer + dLayer):
                thisDistance = data[(x, y, layer)][0]
                thatDistance = data.get((x + dX, y + dY, layer + dLayer), [-1])[0]
                if dLayer == 0 and (thatDistance == -1  or thatDistance > thisDistance + 1):
                    data[x + dX, y + dY, layer + dLayer] = [thisDistance + 1, (x, y, layer), False]
                if dLayer != 0 and (thatDistance == -1 or thatDistance > thisDistance + 3):
                    data[x + dX, y + dY, layer + dLayer] = [thisDistance + 3, (x, y, layer), False]
        shortestDistance = float('inf')
        newNode = []
        for values in data.items():
            if values[1][0] < shortestDistance and values[1][2] == False:
                shortestDistance = values[1][0]
                newNode = values[0]
        x, y, layer = newNode[0], newNode[1], newNode[2]
  
def outputPath(layout, data, goalX, goalY, goalLayer):
    followX, followY, followLayer = (goalX, goalY, goalLayer)
    thisX, thisY, thisLayer = data[goalX, goalY, goalLayer][1]
    movementSigns = {(1, 0, 0): ">", (-1, 0, 0): "<", (0, 1, 0): "v", (0, -1, 0): "^", (0, 0, 1): "!", (0, 0, -1): "!"}

    while(True):
        print(layout[thisX, thisY, thisLayer])
        currentSign = movementSigns[followX - thisX, followY - thisY, followLayer - thisLayer]
        layout[thisX, thisY, thisLayer] = currentSign
        if(data.get(data[thisX, thisY, thisLayer][1]) != None):
            followX, followY, followLayer = thisX, thisY, thisLayer
            thisX, thisY, thisLayer = data[thisX, thisY, thisLayer][1]
        else: break
    for i in range(2):
        for j in range(dimY):
            print(''.join(layout[:, j, i]))

if __name__ == '__main__':
    layout, dimX, dimY, startX, startY, startLayer = inputLayoutFromFile("Aufgabe_3/input/zauberschule5.txt")
    print(dimX, dimY)
    data, distance, goalX, goalY, goalLayer = findShortestPathWithDijkstra(layout, dimX, dimY, startX, startY, startLayer)
    outputPath(layout, data, goalX, goalY, goalLayer)
    print(distance)
    print(goalX, goalY, goalLayer)