#BWINF Runde_1 Aufgabe_2
import numpy as np
import math

finished = False


def inputCubeFromFile(file):
    f = open(file, "r")
    dimX, dimY, dimZ = map(int, f.readline().strip().split())
    cube = np.array([[['' for _ in range(dimZ)] for _ in range(dimY)] for _ in range(dimX)])
    cube[math.floor(dimX / 2), math.floor(dimY / 2), math.floor(dimZ / 2)] = "G"
    numberOfPieces = int(f.readline().strip())
    pieces = []
    for _ in range(numberOfPieces):
        pieces.append(list(map(int, f.readline().strip().split())))
    for i in range(len(pieces)):
         pieces[i].append(chr(65 + i))
    pieces = sorted(pieces, key = lambda x: x[0] * x[1] * x[2], reverse = True)
    return cube, pieces, dimX, dimY, dimZ, numberOfPieces

def isValidPosition(cube, dimX, dimY, dimZ, x, y, z):
    if(0 <= x < dimX and 0 <= y < dimY and 0 <= z < dimZ):
        return cube[x][y][z] == ""
    return False

def inputPiece(cube, pieces, dimX, dimY, dimZ, pieceNumber):
    global finished
    if(pieceNumber == len(pieces)):
        finished = True
        return cube, pieceNumber
    rotations = [(pieces[pieceNumber][0], pieces[pieceNumber][1], pieces[pieceNumber][2]), (pieces[pieceNumber][1], pieces[pieceNumber][2], pieces[pieceNumber][0]), 
                (pieces[pieceNumber][2], pieces[pieceNumber][0], pieces[pieceNumber][1]), (pieces[pieceNumber][0], pieces[pieceNumber][2], pieces[pieceNumber][1]), 
                (pieces[pieceNumber][1], pieces[pieceNumber][0], pieces[pieceNumber][2]), (pieces[pieceNumber][2], pieces[pieceNumber][1], pieces[pieceNumber][0])]
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    dimConstant = None
    if(pieces[pieceNumber][0] == pieces[pieceNumber][1] or pieces[pieceNumber][0] == pieces[pieceNumber][2] or pieces[pieceNumber][1] == pieces[pieceNumber][2]): dimConstant = 3
    if(pieces[pieceNumber][0] == pieces[pieceNumber][1] == pieces[pieceNumber][2]): dimConstant = 1
    topList = []

    for k in range(dimZ):
        for j in range(dimY):
            for i in range(dimX):
                if(isValidPosition(cube, dimX, dimY, dimZ, i, j, k)):
                    for rotation in rotations[:dimConstant]:
                        active = True
                        neighbours = 0
                        for l in range(rotation[0]):
                            for m in range(rotation[1]):
                                for n in range(rotation[2]):
                                    if(isValidPosition(cube, dimX, dimY, dimZ, i + l, j + m, k + n) == False):
                                        active = False
                                        break
                                if(active == False): break
                            if(active == False): break
                        if(active == True):
                            for o in range(rotation[0]):
                                for p in range(rotation[1]):
                                    for q in range(rotation[2]):
                                        for direction in directions:
                                            if(isValidPosition(cube, dimX, dimY, dimZ, i + o + direction[0], j + p + direction[1], k + q + direction[2]) == False):
                                                neighbours += 1
                            topList.append([i, j, k, rotation, neighbours])
    topList = sorted(topList, key = lambda x: x[4], reverse = True)
    while(len(topList) > 5):
         topList.pop(5)
    #print(topList)
    for entry in topList:
        fixList = []
        for r in range(entry[3][0]):
            for s in range(entry[3][1]):
                for t in range(entry[3][2]):
                    cube[entry[0] + r][entry[1] + s][entry[2] + t] = pieces[pieceNumber][3]
                    fixList.append([entry[0] + r, entry[1] + s, entry[2] + t])
        inputPiece(cube, pieces, dimX, dimY, dimZ, pieceNumber + 1)
        if(finished == False):
            for fix in fixList:
                cube[fix[0], fix[1], fix[2]] = ""
        if(finished == True):
            print("now returning")
            return cube, pieceNumber

    return cube, pieceNumber


def inputPieceOld(cube, pieces, dimX, dimY, dimZ, pieceNumber):
    global finished
    if(pieceNumber == len(pieces)):
                            finished = True
                            return cube, pieceNumber
    directions = [(pieces[pieceNumber][0], pieces[pieceNumber][1], pieces[pieceNumber][2]), (pieces[pieceNumber][1], pieces[pieceNumber][2], pieces[pieceNumber][0]), 
                (pieces[pieceNumber][2], pieces[pieceNumber][0], pieces[pieceNumber][1]), (pieces[pieceNumber][0], pieces[pieceNumber][2], pieces[pieceNumber][1]), 
                (pieces[pieceNumber][1], pieces[pieceNumber][0], pieces[pieceNumber][2]), (pieces[pieceNumber][2], pieces[pieceNumber][1], pieces[pieceNumber][0])]
    dimConstant = None
    if(pieces[pieceNumber][0] == pieces[pieceNumber][1] or pieces[pieceNumber][0] == pieces[pieceNumber][2] or pieces[pieceNumber][1] == pieces[pieceNumber][2]): dimConstant = 3
    if(pieces[pieceNumber][0] == pieces[pieceNumber][1] == pieces[pieceNumber][2]): dimConstant = 1
    for k in range(dimZ):
        for j in range(dimY):
            for i in range(dimX):
                if(isValidPosition(cube, dimX, dimY, dimZ, i, j, k)):
                    for direction in directions[:dimConstant]:
                        active = True
                        fixList = []
                        for l in range(direction[0]):
                            for m in range(direction[1]):
                                for n in range(direction[2]):
                                    if(isValidPosition(cube, dimX, dimY, dimZ, i + l, j + m, k + n)):
                                        cube[i + l][j + m][k + n] = pieces[pieceNumber][3]
                                        fixList.append([i + l, j + m, k + n])
                                    else:
                                        active = False
                                        for entry in fixList:
                                            cube[entry[0], entry[1], entry[2]] = ""
                                        break
                                if(active == False): break
                            if(active == False): break
                        if(active == True):
                            if(pieceNumber < 6):
                                 print(pieceNumber)
                            inputPiece(cube, pieces, dimX, dimY, dimZ, pieceNumber + 1)
                            if(finished == False):
                                for entry in fixList:
                                    cube[entry[0], entry[1], entry[2]] = ""
                            if(finished == True):
                                print("now returning")
                                return cube, pieceNumber

    return cube, pieceNumber

def printCube(cube):
    for i in range(len(cube[0][0][:])):
        for j in range(len(cube[0][:][0])):
            print(cube[:, j, i])
        print("")

def test(number):
    number = 1
    return number
def test2(number):
    number = 3
    test(number)
    return number

if __name__ == '__main__':
    cube, pieces, dimX, dimY, dimZ, numberOfPieces = inputCubeFromFile("Aufgabe_2/input/raetsel1.txt")
    print(dimX, dimY, dimZ)
    print(pieces)
    printCube(cube)
    #cube, pieceNumber = inputPiece(cube, pieces, dimX, dimY, dimZ, 0)
    printCube(cube)
    number = test2(2)
    print(number)