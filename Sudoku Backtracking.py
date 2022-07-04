import sys
import numpy as np
from scipy.stats import bernoulli as bn

# empty sudoku grid
grid = np.zeros((9, 9), int)


# checks if it's possible for n to be placed in the grid at position (y, x)
def possible(y, x, n):
    global grid
    if n in grid[y, :]:
        return False
    if n in grid[:, x]:
        return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[y0 + i][x0 + j] == n:
                return False
    return True


# generates a random, complete sudoku grid
def populate():
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                pos = [n for n in range(1, 10) if possible(y, x, n)]
                while len(pos) > 0:
                    index = np.random.randint(len(pos))
                    grid[y][x] = pos[index]
                    pos.remove(pos[index])
                    populate()
                    grid[y][x] = 0
                return
    delete_elements()


# prints sudoku board
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


# replaces some elements of grid with 0 (0 represents an empty space)
# the number of elements replaced is dependent on user input
def delete_elements():
    global grid
    try:
        p = float(input("\nDifficulty? (Number between 0.2-0.8, 0.2 is hardest, 0.8 is easiest)\n"))
        if p < 0.2 or p > 0.8:
            print("that's not a number between 0.2 and 0.8!")
            delete_elements()
    except ValueError:
        print("that's not a float!")
        delete_elements()
    flag = bn.rvs(p=p, size=(9, 9))
    grid *= flag
    print("\nhere is the puzzle board:\n")
    print_board(grid)
    print("\n")
    reveal_answer()


# asks user if they want the answer
def reveal_answer():
    input("provide any input for an answer\n")
    print("\n")
    solve()


# solves board
def solve():
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    print_board(grid)
    more_answers()


# asks user if they want more solutions
def more_answers():
    print("\nmore answers? (solutions may be repeated)")
    answer = input("type \"y\" or \"n\"\n")
    if answer == "y":
        solve()
    elif answer == "n":
        sys.exit()
    else:
        print("that's not a valid input!")
        more_answers()


populate()
