import imaplib
import random

layout = []
dimX, dimY, startX, startY, startZ = -1, -1, -1, -1, -1

def is_valid_position(layout, x, y, z):
    return layout[x][y][z] == "."

def inputLayoutFromFile(file):
    global layout, dimX, dimY
    f = open(file, "r")
    dimX, dimY = map(int, f.readline().split())
    layout = [[[0 for _ in range(2)] for _ in range(dimY)] for _ in range(dimX)]
    for i in range(2):
        for j in range(dimY):
            line = list(f.readline())
            for k in range(dimX):
                layout[k][j][i] = line[k]
        f.readline()

def outputLayout():
    global layout, dimX, dimY
    for i in range(2):
        for j in range(dimY):
            current = ''
            for k in range(dimX):
                current = current + str(layout[k][j][i])
            print(current)

if __name__ == '__main__':
    inputLayoutFromFile("zauberschule0.txt")
    outputLayout()
    #print(layout[1][1][0])

