#import unidecode from unidecode


def inputRouteFromFile(file):
    f = open(file, "r")
    stopNumber = int(f.readline().strip())
    stopList = []
    for _ in range(stopNumber):
        stopList.append(f.readline().strip().split(","))
    #for i in range(stopNumber):
        #stopList[i][0] = unidecode(stopList[i][0])
    return stopList, stopNumber

def checkForLoops(stopList):
    removedStops, elementTested, positionOfElement = [], [-1], -1
    done = False

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
            return removedStops
        
def checkForNewStart(stopList):
    print("jo")

if __name__ == '__main__':
    stopList, stopNumber = inputRouteFromFile("input2/tour1.txt")
    print(len(stopList))
    removedStops = checkForLoops(stopList)
    print(len(removedStops))
    print(removedStops)
    print(stopList)
    print(len(stopList))