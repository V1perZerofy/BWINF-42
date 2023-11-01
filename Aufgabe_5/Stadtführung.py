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


def findLoopsAndIntersectionsInSegment(segmentForStartOfLoops, segmentForEndOfLoops):
    startOfLoops, endOfLoops, graph = [], [], []
    print(segmentForStartOfLoops)
    if segmentForStartOfLoops != segmentForEndOfLoops: print(segmentForEndOfLoops)

    for startPoint in segmentForStartOfLoops:
        for endPoint in segmentForEndOfLoops:
            if endPoint[0] == startPoint[0] and endPoint[4] > startPoint[4]:
                if segmentForStartOfLoops == segmentForEndOfLoops: graph.append([startPoint[0], endPoint[3] - startPoint[3], startPoint[4], endPoint[4]])
                if segmentForStartOfLoops != segmentForEndOfLoops: graph.append([startPoint[0], startPoint[3] + segmentForEndOfLoops[-1][3] - endPoint[3], startPoint[4], endPoint[4]])

    for vertex in graph:
        vertex.append([])
        for i in range(len(graph)):
            if graph[i][2] < vertex[2] < graph[i][3] or vertex[2] < graph[i][2] < vertex[3]:
                vertex[4].append(i)
        print(vertex)
    print("")

    return graph


def findBestIndependentSetInGraph(graph):
    removablePoints = [[], 100]

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
        #removablePoints += findBestIndependentSetInGraph(graph)

    startOptions = findLoopsAndIntersectionsInSegment(route[:posOfX[0] + 1], route[posOfX[-1]:])
    maxSavedDistance = 0
    pointsToBeRemoved = []

    for point in startOptions:
        graph = findLoopsAndIntersectionsInSegment(route[point[2]:posOfX[0] + 1], route[posOfX[-1]:point[3]])
        bestset = findBestIndependentSetInGraph(graph)
        if maxSavedDistance < bestset[1] + point[1]:
            maxSavedDistance = bestset[1] + point[1]
            pointsToBeRemoved = list(range(point[2])) + list(range(point[3] + 1, startOptions[-1][3] + 1)) + bestset[0]
    removablePoints += pointsToBeRemoved

    print(removablePoints)
    for point in removablePoints:
            if point - 1 >= 0: savedDistance = route[point][3] - route[point - 1][3]
            else: savedDistance = route[point][3]
            totalSavedDistance += savedDistance
            for i in range(point + 1, len(route)):
                route[i][3] -= savedDistance
                route[i][4] -= 1
            removedPoints.append(route[point])
            route.pop(point)

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