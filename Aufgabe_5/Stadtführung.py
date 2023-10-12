#BWINF Runde_1 Aufgabe_5


def inputRouteFromFile(file):
    f = open(file, "r", encoding = 'utf-8')
    stopNumber = int(f.readline().strip())
    stopList = []
    for _ in range(stopNumber):
        stopList.append(f.readline().strip().split(","))
    for stop in stopList:
        stop[3] = int(stop[3])
    return stopList, stopNumber

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
        frontStops = [frontStop for frontStop in frontStops if any(frontStop[0] == backStop[0] for backStop in backStops)]
        backStops = [backStop for backStop in backStops if any(backStop[0] == frontStop[0] for frontStop in frontStops)]
        for frontStop in frontStops:
            for backStop in backStops:
                if(frontStop[0] == backStop[0] and frontStop[3] + (backStops[0][3] - backStop[3]) >= savedDistance):
                    savedDistance = frontStop[3] + (backStops[0][3] - backStop[3])
                    newStart, newEnd = frontStop, backStop
        while(stopList[0] != newStart):
            removedStopsStart.append(stopList[0])
            stopList.pop(0)
        while(list(reversed(stopList))[0] != newEnd):
            removedStopsEnd.append(list(reversed(stopList))[0])
            stopList.pop(len(stopList) - 1)
        for stop in list(reversed(stopList)):
            stop[3] -= stopList[0][3]
    else:
        newStart, newEnd = stopList[0], list(reversed(stopList))[0]
    return stopList, removedStopsStart, removedStopsEnd, newStart, newEnd, savedDistance

def printTour(stopList):
    for stop in stopList:
        print(stop)

if __name__ == '__main__':
    stopList, stopNumber = inputRouteFromFile("input/tour5.txt")
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