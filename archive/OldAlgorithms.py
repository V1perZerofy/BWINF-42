#Old Brute-Force-Algo for Die Goldene Mitte, that tries to find the best postions for the next piece and only tries the best to save runtime //Not finding a solution for 4/5
def inputPieceNew(cube, pieces, dimX, dimY, dimZ, pieceNumber):
    global finished
    global count, count2
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
                                            if(isInBounds(dimX, dimY, dimZ, i + o + direction[0], j + p + direction[1], k + q + direction[2]) == True):
                                                if(isValidPosition(cube, dimX, dimY, dimZ, i + o + direction[0], j + p + direction[1], k + q + direction[2]) == False):
                                                    neighbours += 0
                                                    #neighbours += 1000 / (ord(cube[i + o + direction[0], j + p + direction[1], k + q + direction[2]]) - 64)
                                                else:
                                                    neighbours -= 0
                                                neighbours -= 0
                                            else:
                                                neighbours += 0
                            topList.append([i, j, k, rotation, neighbours])
    topList = sorted(topList, key = lambda x: x[4], reverse = True)
    #print(topList)
    for entry in topList:
        fixList = []
        for r in range(entry[3][0]):
            for s in range(entry[3][1]):
                for t in range(entry[3][2]):
                    cube[entry[0] + r][entry[1] + s][entry[2] + t] = pieces[pieceNumber][3]
                    fixList.append([entry[0] + r, entry[1] + s, entry[2] + t])
        #if(pieceNumber < 10):
            #count += 1
            #print(pieceNumber)
        #if(pieceNumber > 17):
            #print(count2)
            #count2 += 1
        if(pieceNumber > 18):
            count += 1
            print(pieceNumber)
            print(cube)
        if(finished == True or count == 1):
            print("now returning")
            return cube, pieceNumber
        inputPieceNew(cube, pieces, dimX, dimY, dimZ, pieceNumber + 1)
        if(finished == False):
            for fix in fixList:
                cube[fix[0], fix[1], fix[2]] = ""
        if(finished == True or count == 25):
            print("now returning")
            return cube, pieceNumber

    return cube, pieceNumber

def isValidPosition(cube, dimX, dimY, dimZ, x, y, z):
    if(0 <= x < dimX and 0 <= y < dimY and 0 <= z < dimZ):
        return cube[x][y][z] == ""
    return False

def isInBounds(dimX, dimY, dimZ, x, y, z):
    if(0 <= x < dimX and 0 <= y < dimY and 0 <= z < dimZ):
        return True
    return False

def isGood(cube, dimX, dimY, dimZ, x, y, z):
    if(0 <= x < dimX and 0 <= y < dimY and 0 <= z < dimZ):
        return cube[x][y][z] == "A"
    return False

#Creates a new list that only contains the elements that have the same value in the first entry as an element in its first entry in the other list
def checkForNewStart(stopList):
    frontStops = [frontStop for frontStop in frontStops if any(frontStop[0] == backStop[0] for backStop in backStops)]
    backStops = [backStop for backStop in backStops if any(backStop[0] == frontStop[0] for frontStop in frontStops)]


#Newer Tests for Stadtführung after noticing necessary changes
def checkForLoop(stopList):
    removedStops = []
    totalSavedDistance = 0
    loops = []
    startPosition = None

    for i in range(len(stopList)):
        if stopList[i][2] == "X":
            startPosition = i
            break
    print(startPosition)
    
    startOfLoops, endOfLoops = [], []
    for i in range(startPosition, len(stopList)):
        if any(stopList[i][0] == entry[0] for entry in startOfLoops): endOfLoops.append(stopList[i])
        startOfLoops.append(stopList[i])
        if stopList[i][2] == "X":
            startOfLoops = [start for start in startOfLoops if any(start[0] == end[0] for end in endOfLoops)]
            for start in startOfLoops:
                for end in endOfLoops:
                    if(start[0] == end[0] and start != end):
                        loops.append((start, end))
            startOfLoops, endOfLoops = [], []
            startOfLoops.append(stopList[i])

            loops = sorted(loops, key = lambda x: x[0][4])

    return loops

def checkForNewerStart(stopList):
    removedStops = []
    totalSavedDistance = 0
    frontStops, backStops = [], []
    possibleStarts, loops = [], []

    if (stopList[0][2] != "X"):
        for stop in stopList:
            frontStops.append(stop)
            if(stop[2] == "X"):
                break
        for stop in reversed(stopList):
            backStops.append(stop)
            if(stop[2] == "X"):
                break
        for frontStop in frontStops:
            for backStop in backStops:
                if(frontStop[0] == backStop[0]):
                    possibleStarts.append((frontStop, backStop))
        startOfLoops, endOfLoops, loops = [], [], []
        for i in range(2):
            for i in range(len(stopList)):
                if any(stopList[i][0] == entry[0] for entry in startOfLoops): endOfLoops.append(stopList[i])
                startOfLoops.append(stopList[i])
                if stopList[i][2] == "X":
                    startOfLoops = [start for start in startOfLoops if any(start[0] == end[0] for end in endOfLoops)]
                    for start in startOfLoops:
                        for end in endOfLoops:
                            if(start[0] == end[0] and start != end):
                                loops.append((start, end))
                    startOfLoops, endOfLoops = [], []
                    stopList = list(reversed(stopList))
                    break

    return frontStops, backStops, possibleStarts, loops


#Old outdated Stadtführung
def checkForLoops(stopList):
    removedStops = []
    elementTested, positionOfElement =[-1], -1
    savedDistance = 0

    while True:
        for i in range(len(stopList)):
            if stopList[i][2] == "X" and stopList[i][0] == elementTested[0]:
                if(stopList[positionOfElement + 1][0] != elementTested[0]):
                    while(stopList[positionOfElement + 1][0] != elementTested[0]):
                        removedStops.append(stopList[positionOfElement + 1])
                        stopList.pop(positionOfElement + 1)
                    savedDistance += stopList[positionOfElement + 1][3] - elementTested[3]
                    savedDistanceATM = stopList[positionOfElement + 1][3] - elementTested[3]
                    for j in range(positionOfElement + 1, len(stopList)):
                        stopList[j][3] -= savedDistanceATM
                    elementTested, positionOfElement = [-1], -1
                    break
            if stopList[i][2] == "X":
                elementTested = stopList[i]
                positionOfElement = i
        else:
            return stopList, removedStops, savedDistance

def checkForNewStart(stopList):
    frontStops, backStops = [], []
    savedDistance = 0
    newStart, newEnd = [], []
    removedStopsStart, removedStopsEnd = [], []

    if (stopList[0][2] != "X"):
        for stop in stopList:
            if(stop[2] == "X"):
                break
            frontStops.append(stop)
        for stop in reversed(stopList):
            if(stop[2] == "X"):
                break
            backStops.append(stop)
        for frontStop in frontStops:
            for backStop in backStops:
                if(frontStop[0] == backStop[0] and frontStop[3] + (backStops[0][3] - backStop[3]) >= savedDistance):
                    savedDistance = frontStop[3] + (backStops[0][3] - backStop[3])
                    newStart, newEnd = frontStop, backStop
        while(stopList[0] != newStart):
            removedStopsStart.append(stopList[0])
            stopList.pop(0)
        while(stopList[len(stopList) - 1] != newEnd):
            removedStopsEnd.append(stopList[len(stopList) - 1])
            stopList.pop(len(stopList) - 1)
        cutDistance = stopList[0][3]
        for stop in stopList:
            stop[3] -= cutDistance
    else:
        newStart, newEnd = stopList[0], list(reversed(stopList))[0]
    return stopList, removedStopsStart, removedStopsEnd, newStart, newEnd, savedDistance

def printTour(stopList):
    for stop in stopList:
        print(stop)

#adds specific elements of a list to another list when condition is met
#vertex.append([potentialConnection for potentialConnection in graph
#                        if potentialConnection[0][4] < vertex[0][4] < potentialConnection[1][4]
#                        or vertex[0][4] < potentialConnection[0][4] < vertex[1][4]])

"""
    print(len(stopList))
    printTour(stopList)
    print("")
    stopList, removedStopsInLoops, savedDistanceLoops = checkForLoops(stopList)
    print(len(removedStopsInLoops))
    printTour(removedStopsInLoops)
    print("")
    print(len(stopList))
    printTour(stopList)
    print("")
    stopList, removedStopsInStart, removedStopsInEnd, newStart, newEnd, savedDistanceStartAndEnd = checkForNewStart(stopList)
    print(len(removedStopsInStart) + len(removedStopsInEnd))
    printTour(removedStopsInStart)
    print("")
    printTour(removedStopsInEnd)
    print("")
    print(newStart, newEnd)
    print("")
    print(len(stopList))
    printTour(stopList)
    print("")
    print(savedDistanceLoops, savedDistanceStartAndEnd, savedDistanceLoops + savedDistanceStartAndEnd)
"""