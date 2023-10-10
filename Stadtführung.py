def inputFile(filename):
    #first line of input file is n
    #other lines have to be split into a 2d array of strings 
    #each line is split at ,
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        #split each line at , and append to list
        construction = [f.readline().strip().split(',') for _ in range(n)]
    return n, construction

def printConstruction(n, construction):
    for i in range(n):
        print(construction[i])

n, construction = inputFile("Input/tour1.txt")
printConstruction(n, construction)