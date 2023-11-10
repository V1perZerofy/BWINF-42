import random
from collections import deque

excluded = []

def is_valid_position(puzzle, x, y):
    # check if the cell is within the grid and is empty and is not part of an existing path
    return puzzle[x][y] == 0 and (x, y) not in excluded

def generator(n, numCount):
    puzzle = [[0 for _ in range(n)] for _ in range(n)]
    for num in range(1, numCount + 1):
        placed = False
        for _ in range(10000):  # 10000 attempts to place each number
            x1, y1 = random.randint(0, n-1), random.randint(0, n-1)
            x2, y2 = random.randint(0, n-1), random.randint(0, n-1)
            if (x1, y1) != (x2, y2) and is_valid_position(puzzle, x1, y1) and is_valid_position(puzzle, x2, y2) and doesPathExist(puzzle, (x1, y1), (x2, y2), excluded):
                puzzle[x1][y1] = num
                puzzle[x2][y2] = num
                placed = True
                break
        if not placed:
            return None  # Return None if couldn't place a number
    return puzzle

#save puzzle to file txt
def saveAsTxt(puzzle, n, numCount):
    f = open("puzzle.txt", "w")
    f.write(str(n) + "\n")
    f.write(str(numCount) + "\n")
    for row in puzzle:
        f.write(' '.join(map(str, row)) + "\n")
    f.close()


def print_puzzle(puzzle, n, numCount):
    print(n)
    print(numCount)
    for row in puzzle:
        print(' '.join(map(str, row)))

def doesPathExist(puzzle, start, end, excluded):
    n = len(puzzle)
    visited = set()
    queue = deque([(start, [])])
    while queue:
        current, path_so_far = queue.popleft()
        if current == end:
            excluded.extend(path_so_far + [end])
            return True
        visited.add(current)
        path_so_far = path_so_far + [current]
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = current[0] + dx, current[1] + dy
            next_cell = (x, y)
            
            if 0 <= x < n and 0 <= y < n:
                if next_cell in excluded or next_cell in visited:
                    continue
                
                if puzzle[x][y] == 0:
                    queue.append((next_cell, path_so_far))
                elif next_cell == end:
                    excluded.extend(path_so_far + [end])
                    return True

    return False

def main(n):
    numCount = random.randint(n//2 + 1, n)
    puzzle = generator(n, numCount)
    if puzzle is None:
        print('Failed to generate a puzzle')
    else:
        print_puzzle(puzzle, n, numCount)
        saveAsTxt(puzzle, n, numCount)
    
if __name__ == '__main__':
    main(25)