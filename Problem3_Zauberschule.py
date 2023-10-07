import imaplib
import random
import numpy as np

def is_valid_position(layout, x, y, layer):
    return layout[layer][x][y] == "."

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
                    startX, startY, startZ = k, j, i
        f.readline()
    return layout, dimX, dimY, startX, startY, startZ

def findShortestPath(layout, dimX, dimY):
    print(0 == 0)

def outputLayout(layout, dimY):
    for i in range(dimY):
        print(''.join(layout[:, i, 0]))
    for j in range(dimY):
        print(''.join(layout[:, j, 1]))

if __name__ == '__main__':
    layout, dimX, dimY, startX, startY, startZ = inputLayoutFromFile("zauberschule0.txt")
    print(dimX, dimY)
    outputLayout(layout, dimY)
    findShortestPath(layout, dimX, dimY)


