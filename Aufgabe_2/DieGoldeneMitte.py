#BWINF Runde_1 Aufgabe_2
import numpy as np
import math


def inputCubeFromFile(file):
    f = open(file, "r")
    dimX, dimY, dimZ = map(int, f.readline().strip().split())
    cube = np.array([[['' for _ in range(dimZ)] for _ in range(dimY)] for _ in range(dimX)])
    cube[math.floor(dimX / 2), math.floor(dimY / 2), math.floor(dimZ / 2)] = "G"
    numberOfPieces = int(f.readline().strip())
    pieces = []
    for _ in range(numberOfPieces):
        pieces.append(f.readline().strip().split())
    return cube, dimX, dimY, dimZ, pieces, numberOfPieces

def printCube(cube):
    for i in range(3):
        for j in range(dimY):
            print(cube[:, j, i])
        print("")

if __name__ == '__main__':
    cube, dimX, dimY, dimZ, pieces, numberOfPieces = inputCubeFromFile("Aufgabe_2/input/raetsel1.txt")
    print(dimX, dimY, dimZ)
    printCube(cube)
    print(numberOfPieces)
    print(pieces)