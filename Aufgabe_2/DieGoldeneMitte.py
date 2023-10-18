#BWINF Runde_1 Aufgabe_2
import numpy as np
import math
finished = False


def inputCubeFromFile(file):
    f = open(file, "r")
    dimX, dimY, dimZ = map(int, f.readline().strip().split())
    cube = np.array([[["" for _ in range(dimZ)] for _ in range(dimY)] for _ in range(dimX)])
    cube[math.floor(dimX / 2), math.floor(dimY / 2), math.floor(dimZ / 2)] = "G"
    numberOfPieces = int(f.readline().strip())
    pieces = []
    for _ in range(numberOfPieces):
        pieces.append(f.readline().strip().split())
    return cube, pieces, dimX, dimY, dimZ, numberOfPieces

def isValidPosition(cube, dimX, dimY, dimZ, x, y, z):
    if(0 <= x < dimX and 0 <= y < dimY and 0 <= z < dimZ):
        return cube[x][y][z] == ""
    return False

def inputPiece(cube, pieces, dimX, dimY, dimZ, pieceNumber):
    printCube(cube)
    global finished
    directions = [(pieces[pieceNumber][0], pieces[pieceNumber][1], pieces[pieceNumber][2]), (pieces[pieceNumber][0], pieces[pieceNumber][2], pieces[pieceNumber][1]), 
                (pieces[pieceNumber][1], pieces[pieceNumber][0], pieces[pieceNumber][2]), (pieces[pieceNumber][1], pieces[pieceNumber][2], pieces[pieceNumber][0]), 
                (pieces[pieceNumber][2], pieces[pieceNumber][0], pieces[pieceNumber][1]), (pieces[pieceNumber][2], pieces[pieceNumber][1], pieces[pieceNumber][0])]
    print(directions)
    for k in range(dimZ):
        for j in range(dimY):
            for i in range(dimX):
                #for direction in directions:
                if(isValidPosition(cube, dimX, dimY, dimZ, i, j, k)):
                    cube[i][j][k] = pieceNumber
                    if(pieceNumber == 7):
                        return cube, pieceNumber
                    inputPiece(cube, pieces, dimX, dimY, dimZ, pieceNumber + 1)
                    if(pieceNumber == 7):
                        return cube, pieceNumber

    return cube, pieceNumber


def printCube(cube):
    for i in range(3):
        for j in range(dimY):
            print(cube[:, j, i])
        print("")

if __name__ == '__main__':
    cube, pieces, dimX, dimY, dimZ, numberOfPieces = inputCubeFromFile("Aufgabe_2/input/raetsel1.txt")
    print(dimX, dimY, dimZ)
    printCube(cube)
    print(numberOfPieces)
    print(pieces)
    cube, pieceNumber = inputPiece(cube, pieces, dimX, dimY, dimZ, 0)
    printCube(cube)