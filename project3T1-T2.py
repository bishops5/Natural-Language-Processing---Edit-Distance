import sys
from pointer import Pointer
# Edit Distance
# CSC_470
# Project 3



# Compute edit distance
# Parameters are as follows: String initial, String goal
# We return Int editDistance, Pointer[][] ptrTable
def computeEditDistance(initial, goal):
    # edit distance table
    rows = len(initial) + 1
    columns = len(goal) + 1
    table = [[0 for x in range(columns)] for y in range(rows)]

    # pointer table (this is used for the backtrace pointer, found in point.py)
    ptrTable = [[None for x in range(columns)] for y in range(rows)]
    
    # Initialize tables
    for i in range(columns):
        table[0][i] = i
        if i > 0:
            ptrTable[0][i] = Pointer(0, i-1, "*", goal[i-1], 1)
    for i in range(rows):
        table[i][0] = i
        if i > 0:
            ptrTable[i][0] = Pointer(i-1, 0, initial[i-1], "*", 1)

    #Complete edit distance table using Dynamic Programming outlined in class
    for i in range(1, rows):
        for j in range(1, columns):
            # Costs for edit operations (given in class)
            deletionCost = table[i-1][j] + 1
            insertionCost = table[i][j-1] + 1
            # Additional cost for subsitution is 2
	    # 0 if same character
            subActionCost = 2 if initial[i-1] != goal[j-1] else 0
            substitutionCost = table[i-1][j-1] + subActionCost
            # Min cost of edit distance table overall
            minCost = min(deletionCost, insertionCost, substitutionCost)
            table[i][j] = minCost
            # Backtrace pointer table utilizing the ptrTable created earlier
            if substitutionCost == minCost:
                ptrTable[i][j] = Pointer(i-1, j-1, initial[i-1], goal[j-1], subActionCost)
            elif insertionCost == minCost:
                ptrTable[i][j] = Pointer(i, j-1, "*", goal[j-1], 1)
            else:
                ptrTable[i][j] = Pointer(i-1, j, initial[i-1], "*", 1)

    # Now it will return the edit table along with the ptr table showing the methods used
    return table[rows-1][columns-1], ptrTable

# Alignment String building
def aliString(ptrTable):
    # Retrive the full edit distance position
    ptr = ptrTable[len(ptrTable)-1][len(ptrTable[len(ptrTable)-1])-1]
    # Build a string of alignments
    xxx = ""
    # Iterate until the full alignment has been created
    while ptr != None:
        if xxx == "":
            xxx = ptr.getAction()
        else:
            # will print aligments followed by a "," that seperates them
            xxx = f"{ptr.getAction()}, {xxx}"
        # Update the pointer
        ptr = ptrTable[ptr.i][ptr.j]
    # Return full alignment string
    return xxx

# Compute edit distance between two words
# Input your inital word and then your goal word
if __name__ == "__main__":
    # Ensure 3 arguments (program_name word1 word2)
    if len(sys.argv) != 3:
        print("Invalid number of argments")
    
    # Get argument words
    initial = sys.argv[1]
    goal = sys.argv[2]

    # Compute and output edit distance
    editDistance, ptrTable = computeEditDistance(initial, goal)
    print(f"The edit distance from '{initial}' to '{goal}' is {editDistance}")

    # Output alignment
    print(f"The alignment from '{initial}' to '{goal}' is: ")
    print(aliString(ptrTable))