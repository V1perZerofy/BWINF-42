import imaplib
import random
import numpy as np


def isValidPosition(layout, dimX, dimY, x, y, layer):
    return layout[x][y][layer] == "." and 0 <= x < dimX and 0 <= y < dimY and 0 <= layer <= 2


def inputLayoutFromFile(file):
    f = open(file, "r")
    dimX, dimY = map(int, f.readline().split(' '))
    layer = 2
    layout = np.array([[['' for _ in range(layer)] for _ in range(dimY)] for _ in range(dimX)])

    for i in range(2):
        for j in range(dimY):
            line = list(f.readline())
            for k in range(dimX):
                layout[k, j, i] = line[k]
                if(layout[k, j, i] == 'A'):
                    startX, startY, startLayer = k, j, i
        f.readline()
    
    return layout, dimX, dimY, startX, startY, startLayer


def findShortestPathWithDijkstra(layout, dimX, dimY, startX, startY, startLayer):
    x, y, layer = startX, startY, startLayer
    movement = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    lib = {}
    lib[startX, startY, startLayer] = 0, None

    for dX, dY, dLayer in movement:
        if isValidPosition(layout, dimX, dimY, x + dX, y + dY, layer + dLayer):
            print("Valid")
        else:
            print("Invalid")



def outputLayout(layout, dimY):
    for i in range(dimY):
        print(''.join(layout[:, i, 0]))
    for j in range(dimY):
        print(''.join(layout[:, j, 1]))


if __name__ == '__main__':
    layout, dimX, dimY, startX, startY, startLayer = inputLayoutFromFile("zauberschule0.txt")
    print(dimX, dimY)
    outputLayout(layout, dimY)
    findShortestPathWithDijkstra(layout, dimX, dimY, startX, startY, startLayer)


    #if layout[x, y, layer] == 'B':
    #    return x, y, layer, lib