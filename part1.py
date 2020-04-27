import sys
import nltk
import re

def computeEditDistance(start_tk, end_tk):
    rows = len(start_tk) + 1
    columns = len(end_tk) + 1
    table = [[0 for x in range(columns)] for y in range(rows)]
    # backtrace table - Tuples of (i, j, cost)
    alitab = [[None for x in range(columns)] for y in range(rows)]

    # Initialize tables
    for i in range(columns):
        table[0][i] = i
        if i > 0:
            alitab[0][i] = (0, i - 1, 1)
    for i in range(rows):
        table[i][0] = i
        if i > 0:
            alitab[i][0] = (i - 1, 0, 1)

    # Complete edit distance table using Dynamic Programming outlined in class
    # Will use EDScore instead of edit distance
    # EDScore = max(1 - edit-dist(M,C)/|M_{unigrams}|,0)
    for i in range(1, rows):
        for j in range(1, columns):
            # Costs for all edit operations is now 1
            delete = table[i - 1][j] + 1
            insert = table[i][j - 1] + 1
            subcost = 1 if start_tk[i - 1] != end_tk[j - 1] else 0
            sub = table[i - 1][j - 1] + subcost
            # Min cost of edit distance table overall
            minCost = min(delete, insert, sub)
            table[i][j] = minCost
            # Backtrace backtrace table utilizing the alitab created earlier
            if sub == minCost:
                alitab[i][j] = (i - 1, j - 1, subcost)
            elif insert == minCost:
                alitab[i][j] = (i, j - 1, 1)
            else:
                alitab[i][j] = (i - 1, j, 1)

    # Building alignment string
    i = len(alitab)-1
    j = len(alitab[0])-1
    aliString = ""
    while (i, j) != (0, 0):
        next_i = alitab[i][j][0]
        next_j = alitab[i][j][1]
        cost = alitab[i][j][2]
        if aliString == "":
            # Substitution
            if i == next_i+1 and j == next_j+1:
                aliString = f"{start_tk[i-1]}->{end_tk[j-1]} {cost}"
            # Insertion
            elif i == next_i and j == next_j+1:
                aliString = f"*->{end_tk[j-1]} {cost}"
            # Deletion
            else:
                aliString = f"{start_tk[i-1]}->* {cost}"
        else:
            # Substitution
            if i == next_i+1 and j == next_j+1:
                aliString = f"{start_tk[i-1]}->{end_tk[j-1]} {cost}, {aliString}"
            # Insertion
            elif i == next_i and j == next_j+1:
                aliString = f"*->{end_tk[j-1]} {cost}, {aliString}"
            # Deletion
            else:
                aliString = f"{start_tk[i-1]}->* {cost}, {aliString}"
        i = next_i
        j = next_j

    return table[rows-1][columns-1], aliString

if __name__ == "__main__":
    # makes sure you have 3 inputs such as program name then intial and end_tk words
    if len(sys.argv) != 3:
        print("Invalid number of argments")
    
    # Get argument words (REQUIRES INPUT AT TERMINAL)
    start_tk = sys.argv[1]
    end_tk = sys.argv[2]
  

    editDistance, aliString = computeEditDistance(start_tk, end_tk)
    print(f"The edit distance from '{start_tk}' to '{end_tk}' is {editDistance}")

    print(f"The alignment from '{start_tk}' to '{end_tk}' is:")
    print(aliString)
