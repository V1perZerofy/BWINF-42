import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import uuid

def get_puzzle_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        puzzle = data["puzzle"]
        paths = data["solution"]
    return puzzle, paths

def draw_puzzle(grid, paths):
    n = len(grid)
    fig, ax = plt.subplots()
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect('equal', adjustable='box')
    
    # Draw grid
    for x in range(n + 1):
        ax.axhline(x, lw=2, color='k', zorder=5)
        ax.axvline(x, lw=2, color='k', zorder=5)

    # Draw paths
    for path in paths:
        for i in range(len(path) - 1):
            start, end = path[i], path[i + 1]
            ax.add_patch(patches.FancyArrowPatch((start[1]+0.5, n-start[0]-0.5), (end[1]+0.5, n-end[0]-0.5), arrowstyle='-', color='blue', lw=2))

    # Draw numbers
    for x in range(n):
        for y in range(n):
            if grid[x][y] != 0:
                ax.text(y + 0.5, n - x - 0.5, str(grid[x][y]), va='center', ha='center', fontweight='bold')

    #save the figure name is the puzzle size + number of numbers + random number for uniqueness + .png
    filename = str(uuid.uuid4())[:8]
    plt.savefig('arukone/exports/pictures/' + str(n) + "_" + filename + '.png', dpi=300, bbox_inches='tight', pad_inches=0)

    #save the figure as txt with the same name
    f = open('arukone/exports/pictures/' + str(n) + "_" + filename + '.txt', "w")
    f.write(str(n) + "\n")
    f.write(str(len(paths)) + "\n")
    for row in grid:
        f.write(' '.join(map(str, row)) + "\n")
    f.close()
    plt.axis('off')
    plt.show()

def main():
    # Get puzzle from .json file
    puzzle, paths = get_puzzle_from_json("arukone/exports/puzzle.json")
    draw_puzzle(puzzle, paths)

if __name__ == "__main__":
    main()