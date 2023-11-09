#BWINF Runde_1 Aufgabe_5



def inputRouteFromFile(file):
    f = open(file, "r", encoding = 'utf-8')
    stopNumber = int(f.readline().strip())
    route = []
    for i in range(stopNumber):
        route.append(f.readline().strip().split(","))
        route[i].append(i)
    for point in route: point[3] = int(point[3])
    return route


def getAllCombinationsFromList(list):
    if len(list) == 0:
        return [[]]
    combinations = []
    for combination in getAllCombinationsFromList(list[1:]):
        combinations += [combination+[list[0]]]
        combinations += [combination]
    return combinations


def findLoopsAndIntersectionsInSegment(segmentForStartOfLoops, segmentForEndOfLoops):
    graph = []

    for startPoint in segmentForStartOfLoops:
        for endPoint in segmentForEndOfLoops:
            if endPoint[0] == startPoint[0] and endPoint[4] > startPoint[4]:
                if segmentForStartOfLoops == segmentForEndOfLoops: graph.append([None, endPoint[3] - startPoint[3], startPoint[4], endPoint[4]])
                if segmentForStartOfLoops != segmentForEndOfLoops: graph.append([None, startPoint[3], segmentForEndOfLoops[-1][3] - endPoint[3], startPoint[4], endPoint[4]])

    for i, vertex in enumerate(graph):
        vertex[0] = i
        if segmentForStartOfLoops == segmentForEndOfLoops:
            vertex.append([])
            for j, vertex2nd in enumerate(graph):
                if vertex2nd[2] < vertex[2] < vertex2nd[3] or vertex[2] < vertex2nd[2] < vertex[3]:
                    vertex[4].append(j)

    return graph


def findBestIndependentSetInGraph(graph):
    removablePoints = [[], 0]
    combinations = getAllCombinationsFromList(graph)

    for combination in combinations:
        for loop in combination:
            for loop2nd in combination:
                if any(loop2nd[0] == loopNumber for loopNumber in loop[4]):
                    break
            else:
                savedDistance = sum([loopForDistance[1] for loopForDistance in combination])
                if(removablePoints[1] < savedDistance):
                    removablePoints[1] = savedDistance
                    newIndeces = []
                    for loopForIndeces in combination:
                        newIndeces += [loopForIndeces[1:4]]
                    removablePoints[0] = newIndeces
            break

    return removablePoints


def findShortestRoute(route):
    removablePoints, removedPoints = [], []
    totalSavedDistance = 0
    posOfX = []

    for i in range(len(route)):
        if route[i][2] == "X": posOfX.append(i)
    print(posOfX), print("")

    if posOfX == []:
        totalSavedDistance = route[-1][3]
        route[-1][3], route[-1][4] = 0, 1
        return [route[0], route[-1]], route[1:-1], totalSavedDistance 
    
    for i in range(len(posOfX) - 1):    
        graph = findLoopsAndIntersectionsInSegment(route[posOfX[i]:posOfX[i + 1] + 1], route[posOfX[i]:posOfX[i + 1] + 1])
        removablePoints += findBestIndependentSetInGraph(graph)[0]

    startOptions = findLoopsAndIntersectionsInSegment(route[:posOfX[0] + 1], route[posOfX[-1]:])
    pointsToBeRemoved = [[], 0]

    for point in startOptions:
        graph = findLoopsAndIntersectionsInSegment(route[point[3]:posOfX[0] + 1], route[point[3]:posOfX[0] + 1])
        graph += findLoopsAndIntersectionsInSegment(route[posOfX[-1]:point[4] + 1], route[posOfX[-1]:point[4] + 1])
        bestset = findBestIndependentSetInGraph(graph)
        currentSavedDistance = bestset[1] + point[1] + point[2]
        if pointsToBeRemoved[1] < currentSavedDistance:
            pointsToBeRemoved[1] = currentSavedDistance
            pointsToBeRemoved[0] = bestset[0]
            if point[3] != 0: pointsToBeRemoved[0] += [[point[1], -1, point[3]]]
            if point[4] != route[-1][4]: pointsToBeRemoved[0] += [[point[2], point[4], len(route)]]
    removablePoints += pointsToBeRemoved[0]

    removablePoints = sorted(removablePoints, key = lambda x: x[1], reverse = True)
    print(removablePoints)
    for loop in removablePoints:
        totalSavedDistance += loop[0]
        for entry in route[loop[2]:]:
            entry[3] -= loop[0]
            entry[4] -= loop[2] - (loop[1] + 1)
        for index in range(loop[2] - 1, loop[1], -1):
            removedPoints.append(route[index])
            route.pop(index)

    return route, removedPoints, totalSavedDistance


def printRoute(route):
    for point in route:
        print(point)


if __name__ == '__main__':
    route = inputRouteFromFile("Aufgabe_5/input/tour5.txt")
    printRoute(route), print("")
    route, removedPoints, totalSavedDistance = findShortestRoute(route)
    print(""), print(route), print("")
    print(removedPoints)
    print(route[-1][3])
    print(totalSavedDistance)