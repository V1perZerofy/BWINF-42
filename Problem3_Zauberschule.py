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
    layout = [[[0 for _ in range(dimX)] for _ in range(dimY)] for _ in range(2)]
    #print(layout)
    for i in range(1):
        for j in range(dimY - 1):
            line = list(f.readline())
            for k in range(dimX - 1):
                layout[k][j][i] = line[k]
                print(layout)
        f.readline()
    print(layout)



inputLayoutFromFile("zauberschule0.txt")