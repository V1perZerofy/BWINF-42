def inputFile(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        #split each line at , and append to list
        construction = [f.readline().strip().split(',') for _ in range(n)]
    return n, construction

def printConstruction(n, construction):   
    
    for i in range(n):
        print(construction[i])

def interpretConstruction(n, construction):
    for i in range(n):
        if construction[i][2] == ' ':


n, construction = inputFile("Input/tour1.txt")
printConstruction(n, construction)