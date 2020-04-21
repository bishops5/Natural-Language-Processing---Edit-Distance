import sys
from pointer import Pointer
# Owen Stanski, Jack Taylor, Andre Le
# 4/26/20
# CSC_470
# Project 3
# This class computes the edit distance and displays the alignment between the two words
# This fulfills T1 and T2 of project 3

# Compute the edit distance from an initial string to a goal string
# @Params: String initial, String goal
# @Return: Int editDistance, Pointer[][] ptrTable
def computeEditDistance(initial, goal):
    # Define edit distance table
    rows = len(initial) + 1
    columns = len(goal) + 1
    table = [[0 for x in range(columns)] for y in range(rows)]

    # Define pointer table
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

    # Dynamically fill in edit distance table
    for i in range(1, rows):
        for j in range(1, columns):
            # Compute costs for edit operations
            deletionCost = table[i-1][j] + 1
            insertionCost = table[i][j-1] + 1
            # Additional cost for subsitution is 2 if the new character is different and 0 if it is the same
            subActionCost = 2 if initial[i-1] != goal[j-1] else 0
            substitutionCost = table[i-1][j-1] + subActionCost
            # Update edit distance table with minimum cost value
            minCost = min(deletionCost, insertionCost, substitutionCost)
            table[i][j] = minCost
            # Update the pointer table with new pointer objects to create a backtrace
            if substitutionCost == minCost:
                ptrTable[i][j] = Pointer(i-1, j-1, initial[i-1], goal[j-1], subActionCost)
            elif insertionCost == minCost:
                ptrTable[i][j] = Pointer(i, j-1, "*", goal[j-1], 1)
            else:
                ptrTable[i][j] = Pointer(i-1, j, initial[i-1], "*", 1)

    # Return edit distance and pointer table
    return table[rows-1][columns-1], ptrTable

# Builds a string of alignments from a pointer table
# @Params: Pointer[][] ptrTable
# @Return: String alignments
def buildAlignmentString(ptrTable):
    # Get the pointer at the end position (full edit distance position)
    ptr = ptrTable[len(ptrTable)-1][len(ptrTable[len(ptrTable)-1])-1]
    # Build a string of alignments
    out = ""
    # Iterate until the full alignment has been created
    while ptr != None:
        if out == "":
            # First alignment does not need a ", " added to it
            out = ptr.getAction()
        else:
            # All subsequent alignments are prepended to the full alignment string and separated by ", "
            out = f"{ptr.getAction()}, {out}"
        # Update the pointer
        ptr = ptrTable[ptr.i][ptr.j]
    # Return full alignment string
    return out

# Main function of the project to compute the edit distance between two words
# Takes two arguments, "<initial_word> <goal_word>"
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
    print(buildAlignmentString(ptrTable))