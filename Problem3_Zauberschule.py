import imaplib
import random

layout = []

def is_valid_position(layout, x, y, z):
    return layout[x][y][z] == "."

def inputLayoutFromFile(file):
    f = open(file, "r")
    dimX, dimY = map(int, f.readline().split())
    print(dimX)
    print(dimY)
    layout = [[[0 for _ in range(2)] for _ in range(dimY)] for _ in range(dimX)]
    print(layout)
    for i in range(2):
        for j in range(dimY):
            line = list(f.readline())
            for k in range(dimX):
                layout[k][j][i] = line[k]
        f.readline()
    print(layout)


#test = [[0 for _ in range(2)] for _ in range(3)]
#[1][0] = 1
#print(test)
inputLayoutFromFile("zauberschule0.txt")