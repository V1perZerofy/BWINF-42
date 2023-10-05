import imaplib
import random

layout = []
startX = -1
startY = -1
startZ = -1
dimX = -1
dimY = -1

def is_valid_position(layout, x, y, z):
    return layout[x][y][z] == "."

def inputLayoutFromFile(file):
    f = open(file, "r")
    dimX, dimY = map(int, f.readline().split())
    print(dimX)
    print(dimY)
    layout = [[[0 for _ in range(2)] for _ in range(dimY)] for _ in range(dimX)]
    #outputLayout()
    for i in range(2):
        for j in range(dimY):
            line = list(f.readline())
            for k in range(dimX):
                layout[k][j][i] = line[k]
                if layout[k][j][i] == "A":
                    startX = k
                    startY = j
                    startZ = i
        f.readline()
    #outputLayout()
    print(startX, startY, startZ)

def outputLayout():
    for i in range(2):
        for j in range(dimY):
            for k in range(dimX):
                print(layout[k][j][i])

inputLayoutFromFile("zauberschule0.txt")
outputLayout()