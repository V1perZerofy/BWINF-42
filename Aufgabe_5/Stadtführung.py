#BWINF Runde_1 Aufgabe_5
import time as t



#inputs route from a valid file
def inputRouteFromFile(file):

    #the file is opened and the first line containing the number of stops is saved
    f = open(file, "r", encoding = 'utf-8')
    stopNumber = f.readline().strip()

    #if the first line did not contain an integer an error message is returned
    if stopNumber.isdigit() is False: return "first line has to contain the number of stops"
    stopNumber = int(stopNumber)

    #an empty list route is filled with the information of the input file
    route = []
    for i in range(stopNumber):

        #the data in the current line is read, stripped of additional spaces and devided into the individual entries
        route.append(f.readline().strip().split(","))

        #if a line does not contain the accepted number of data entries an error message is returned
        if len(route[i]) != 4: return "data of stop has wrong number of entries"

        #if a line of the input is not a valid an error message is returned
        yearOfStop, importanceOfStop, distanceValueOfStop = route[i][1], route[i][2], route[i][3]
        if yearOfStop.isdigit() is False or (importanceOfStop == " " or importanceOfStop == "X") is False or distanceValueOfStop.isdigit() is False: return "data of stop has wrong syntax"

        #an additional index is added for each entry
        route[i].append(i)

    #the distance of each stop is converted to an integer
    for point in route: point[3] = int(point[3])

    #the filled list is returned
    return route



#returns every possible combination of elements from a list
#works by recursivly getting all combinations of smaller parts of the list starting with length 0 and incrementing by 1 till length n
#for a list of length n there are 2^n combinations
def getAllCombinationsFromList(list):

    #if the input list is empty an empty list is returned
    if len(list) == 0:
        return [[]]
    
    #for every combination of a list, that is the current input list without the first entry,
    #the combination itself and the combination + the first entry of the current input list are added to the return list
    combinations = []
    for combination in getAllCombinationsFromList(list[1:]):
        combinations += [combination]
        combinations += [combination+[list[0]]]

    #the list containing the combinations is returned
    return combinations



#returns loops and their individual intersections with other loops in certain segment
#can be used for loop finding between important points as well as for finding new start/end possibilities
def findLoopsAndIntersectionsInSegment(segmentForStartOfLoops, segmentForEndOfLoops):

    #return list is initialized, can be understood as a graph with the vertices being loops and edges being the intersections
    graph = []

    #adds loop / new start/end to return list when the names of the start and end possibility are equal and the end possibility is located behind the start possibility
    for startPossibilty in segmentForStartOfLoops:
        for endPossibility in segmentForEndOfLoops:
            nameOfStartOption, nameOfEndOption, indexOfStartOption, indexOfEndOption = startPossibilty[0], endPossibility[0], startPossibilty[4], endPossibility[4]
            if nameOfStartOption == nameOfEndOption and indexOfStartOption < indexOfEndOption:

                #for normal loop finding between two important points // start segment and end segment are identical
                #loop contains index placeholder, length and start index as well as end index
                routeLengthToStartOption, routeLengthToEndOption, routeLength = startPossibilty[3], endPossibility[3], segmentForEndOfLoops[-1][3]
                if segmentForStartOfLoops == segmentForEndOfLoops: graph.append([None, routeLengthToEndOption - routeLengthToStartOption, indexOfStartOption, indexOfEndOption])

                #for finding new start/end possibilities // start segment and end segment are different
                #new start/end contains index placeholder, length of route till new start, length of route from new end till end and new start index as well as new end index
                if segmentForStartOfLoops != segmentForEndOfLoops: graph.append([None, routeLengthToStartOption, routeLength - routeLengthToEndOption, indexOfStartOption, indexOfEndOption])

    #gets element as well as index, that is directly placed at the placeholder, from the created graph
    for i, loop1stDegree in enumerate(graph):
        loop1stDegree[0] = i

        #if the function is used for loop finding the indices of loops that intersect the current loop are saved in the loop
        if segmentForStartOfLoops == segmentForEndOfLoops:
            loop1stDegree.append([])
            for j, loop2ndDegree in enumerate(graph):

                #it is necessary to check all four option as the main and checked loop start/end index can be identical
                mainLoopStartIndex, mainLoopEndIndex, checkedLoopStartIndex, checkedLoopEndIndex = loop1stDegree[2], loop1stDegree[3], loop2ndDegree[2], loop2ndDegree[3]
                if checkedLoopStartIndex < mainLoopStartIndex < checkedLoopEndIndex or checkedLoopStartIndex < mainLoopEndIndex < checkedLoopEndIndex or mainLoopStartIndex < checkedLoopStartIndex < mainLoopEndIndex or mainLoopStartIndex < checkedLoopEndIndex < mainLoopEndIndex:
                    loop1stDegree[4].append(j)

    #the list containing all loops or start/end options and their intersections is returned
    return graph



#returns best combination of non-intersecting loops that are saved in the input list
def findBestIndependentSetInGraph(graph):

    #return list and list containing every of the possible 2^n combinations of all elements of the input list are initialized
    removableLoops = [[], 0]
    sets = getAllCombinationsFromList(graph)

    #brute-force iteration through all possibile combinations
    for set in sets:

        #checks for every loop, contained in the current combination, if every other loop in the combination is valid / not saved as intersecting
        for i, loop1stDegree in enumerate(set):
            for loop2ndDegree in set[i + 1:]:

                #if the index of the checked loop is contained in the main loops intersections, a break occurs
                listOfIndecesOfIntersectingLoops, checkedLoopIndex = loop1stDegree[4], loop2ndDegree[0]
                if any(checkedLoopIndex == loopIndex for loopIndex in listOfIndecesOfIntersectingLoops):
                    break
            
            #if the checked loop does not intersect, the continue statement skips the following break statement, so that the loop can continue
            else:
                continue

            #this break statement is only executed when two loops in the combination are intersecting, causing a skip to the next combination
            break

        #if all loops in the combination are non-intersecting, the combination is tested on the total saved length
        else:
            
            #the sum of all distances in the combination is calculated
            savedDistance = sum([loop[1] for loop in set])

            #if the saved distance of the current combination is greater than the previous best, the previous best is overwritten
            currentSavedDistance = removableLoops[1]
            if(currentSavedDistance < savedDistance):
                removableLoops[1] = savedDistance

                #the new best combination/set of loops is saved
                #only distance, start and end of each loop is saved as the rest of the information is not needed anymore
                newRemovableLoops = []
                for newRemovableLoop in set:
                    newRemovableLoops += [newRemovableLoop[1:4]]
                removableLoops[0] = newRemovableLoops

    #the list containing the best set of loops is returned
    print(removableLoops)
    return removableLoops



#returns the best combination of start/end and removable loops before the first and after the last important stop
def findBestStart(route, posOfX):

    #return list is initialized and all possible start/end combinations are found using the multi-purpose function: findLoopsAndIntersectionsInSegment()
    removableLoops = [[], 0]
    startEndOptions = findLoopsAndIntersectionsInSegment(route[:posOfX[0] + 1], route[posOfX[-1]:])

    #iteration trough all start/end combinations
    for option in startEndOptions:

        #the best combination of loops in front of the first and after the last important stop, for the current start option, is saved
        possibleStart, possibleEnd, firstImportantStop, lastImportantStop = option[3], option[4], posOfX[0], posOfX[-1]
        graph = findLoopsAndIntersectionsInSegment(route[possibleStart:firstImportantStop + 1], route[possibleStart:firstImportantStop + 1])
        graph += findLoopsAndIntersectionsInSegment(route[lastImportantStop:possibleEnd + 1], route[lastImportantStop:possibleEnd + 1])
        bestSet = findBestIndependentSetInGraph(graph)

        #the saved distance of the current start/end is calculated
        savedDistanceFromLoops, savedDistanceFromNewStart, savedDistanceFromNewEnd = bestSet[1], option[1], option[2]
        currentSavedDistance = savedDistanceFromLoops + savedDistanceFromNewStart + savedDistanceFromNewEnd

        #if the saved distance of the current start/end is greater than the previous best, the previous best is overwritten
        if removableLoops[1] < currentSavedDistance:
            removableLoops[1] = currentSavedDistance

            #the new removable loops are saved
            newRemovableLoops = bestSet[0]
            removableLoops[0] = newRemovableLoops

            #if there is a new start, a loop containing all points before the new start is created / start is set to -1 as previous start also has to be removed
            #if there is a new end, a loop containing all points after the new end is created / end is set to index of last stop + 1 as previous end also has to be removed
            newStartIndex, newEndIndex, indexOfLastElement = option[3], option[4], len(route) - 1
            if newStartIndex != 0: removableLoops[0] += [[savedDistanceFromNewStart, -1, newStartIndex]]
            if newEndIndex != indexOfLastElement: removableLoops[0] += [[savedDistanceFromNewEnd, newEndIndex, len(route)]]

    #the list containing the best start/end and removable loops is returned
    return removableLoops



#main function that combines the individual functions to find the shortest route
#returns the modified route
def findShortestRoute(route):

    #lists saving the removable loops and the indeces of important stops are initialized
    removableLoops, posOfX = [], []

    #return list of removed points and integer saving the total saved distance are initialized
    removedPoints, totalSavedDistance = [], 0

    #fills the list containing the indeces of important stops and prints the information to the console
    for i in range(len(route)):
        if route[i][2] == "X": posOfX.append(i)
    print(posOfX), print("")

    #if there is no important point in the route all stops between the start and end are deleted and the necessary information is returned
    if posOfX == []:
        totalSavedDistance = route[-1][3]
        route[-1][3], route[-1][4] = 0, 1
        removedPoints = route[1:-1]
        return [route[0], route[-1]], removedPoints, totalSavedDistance 
    
    #for every interval between two important points, all loops are found and the best set of them is added to the removable loops list
    for i in range(len(posOfX) - 1):
        startOfInterval, endOfInterval = posOfX[i], posOfX[i + 1]
        graph = findLoopsAndIntersectionsInSegment(route[startOfInterval:endOfInterval + 1], route[startOfInterval:endOfInterval + 1])

        #as the total saved distance of the best set of loops is not required in the deletion process, only the loops are saved
        removableLoops += findBestIndependentSetInGraph(graph)[0]

    #the best start/end/loop before first and after last important stop combination is added to the removable loops list
    #as the total saved distance of the best set of start/end/loops is not required in the deletion process, only the loops are saved
    removableLoops += findBestStart(route, posOfX)[0]

    #the removable loops are sorted in reverse order by their starting index and printed to the console
    removableLoops = sorted(removableLoops, key = lambda x: x[1], reverse = True)
    print(removableLoops)

    #iteration through all removable loops
    for loop in removableLoops:
        savedDistanceFromLoop, loopStart, loopEnd = loop[0], loop[1], loop[2]

        #the total saved distance is increased by the loop length
        totalSavedDistance += savedDistanceFromLoop

        #for every route entry from the end of the loop on, the index is adjusted by the number of removable stops in that loop
        for entry in route[loopEnd:]:
            entry[3] -= loop[0]
            entry[4] -= loopEnd - (loopStart + 1)

        #the removable stops are removed in reversed order and added to the removed points list
        for index in range(loopEnd - 1, loopStart, -1):
            removedPoints.append(route[index])
            route.pop(index)

    #the final route, the list of removed points and the total saved distance is returned
    return route, removedPoints, totalSavedDistance



#prints current route to console
def printRoute(route):
    for point in route:
        print(point)



#main
if __name__ == '__main__':

    #the time calculation starts and the input layout is read
    start = t.perf_counter()
    route = inputRouteFromFile("Aufgabe_5/input/tour2.txt")

    #the error message is printed to the console if an error occured
    if isinstance(route, str) is True:
        print("Error")
        print(route)

    #execution of code if no error occured
    else:

        #the input route is printed to the console
        printRoute(route), print("")
        
        #the best route is calculated and printed to the console
        route, removedPoints, totalSavedDistance = findShortestRoute(route)
        print(""), printRoute(route), print("")

        #the removed points, the new distance and the saved distance as well as the taken time are printed to the console
        print(removedPoints)
        print(totalSavedDistance)
        end = t.perf_counter()
        print(end - start)