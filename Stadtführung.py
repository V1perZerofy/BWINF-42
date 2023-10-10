#!/usr/bin/python
# -*- coding: utf-8 -*-


def inputRouteFromFile(file):
    f = open(file, "r", encoding = 'utf-8')
    stopNumber = int(f.readline().strip())
    stopList = []
    for _ in range(stopNumber):
        stopList.append(f.readline().strip().split(","))
    return stopList, stopNumber

def checkForLoops(stopList):
    removedStops, elementTested, positionOfElement = [], [-1], -1

    while True:
        for i in range(len(stopList)):
            if stopList[i][2] == "X" and stopList[i][0] == elementTested[0]:
                if(stopList[positionOfElement + 1][0] != elementTested[0]):
                    while(stopList[positionOfElement + 1][0] != elementTested[0]):
                        removedStops.append(stopList[positionOfElement + 1])
                        stopList.pop(positionOfElement + 1)
                    elementTested, positionOfElement = [-1], -1
                    break
            if stopList[i][2] == "X":
                elementTested = stopList[i]
                positionOfElement = i
        else:
            return stopList, removedStops
        
def checkForNewStart(stopList):
    frontStops, backStops = [], []
    mostSavedDistance = -1

    if (stopList[0][2] != "X"):
        for stop in stopList:
            if(stop[2] == "X"):
                break
            frontStops.append(stop)
        for stop in reversed(stopList):
            if(stop[2] == "X"):
                break
            backStops.append(stop)
        
        return frontStops, backStops
    return frontStops, backStops

def printTour(stopList):
    for stop in stopList:
        print(stop)

if __name__ == '__main__':
    stopList, stopNumber = inputRouteFromFile("input2/tour4.txt")
    print(len(stopList))
    printTour(stopList)
    print("")
    stopList, removedStops = checkForLoops(stopList)
    print(len(removedStops))
    printTour(removedStops)
    print("")
    print(len(stopList))
    printTour(stopList)
    print("")
    frontStops, backStops = checkForNewStart(stopList)
    printTour(frontStops)
    print("")
    printTour(backStops)