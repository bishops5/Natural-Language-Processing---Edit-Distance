# Project 3 T3
# CSC_470
# Sam Bishop and Yash Dhayal

import sys
import nltk
import re
from pointer import Pointer


# Compute edit distance
# Parameters are as follows: String initial, String goal
# We return , Pointer[][] ptrTable

# function to remove contractions and then punctuation
def contrct_punct(str):
    #contractions first
    if "'re" in str:
        str = str.replace("'re", " are")
    if "can't" in str:
        str = str.replace("can't", "can not")
    if "shan't" in str:
        str = str.replace("shan't", "shall not")
    if "won't" in str:
        str = str.replace("won't", "will not")
    if "n't" in str:
        str = str.replace("n't", " not")
    if "it's" in str:
        str = str.replace("it's", "it is")
    if "that's" in str:
        str = str.replace("that's", "that is")
    if "she's" in str:
        str = str.replace("she's", "she is")
    if "he's" in str: # had to make this separate, since 'he' is part of 'she'
        str = str.replace("he's", "he is")
    if "'d" in str:
        str = str.replace("'d", " would")
    if "'ve" in str:
        str = str.replace("'ve", " have")
    if "'ll" in str:
        str = str.replace("'ll", " will")

    #next is punctuation
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in str:
        if x in punctuation:
            str = str.replace(x, '')

    return str


def computeEditDistance(initial, goal):
    # first need to normalize both sentences
    # lowercase the sentences
    initial = initial.lower()
    goal = goal.lower()

    # removing extra whitespaces (via regex) in off chance there is any
    initial = re.sub(' +', ' ', initial)
    goal = re.sub(' +', ' ', goal)

    #expand contractions
    initial = contrct_punct(initial)
    goal = contrct_punct(goal)

    initial_token = nltk.word_tokenize(initial)
    goal_token = nltk.word_tokenize(goal)

    rows = len(initial_token) + 1
    columns = len(goal_token) + 1
    table = [[0 for x in range(columns)] for y in range(rows)]
    # pointer table (this is used for the backtrace pointer, found in pointer.py)
    ptrTable = [[None for x in range(columns)] for y in range(rows)]

    # Initialize tables
    for i in range(columns):
        table[0][i] = i
        if i > 0:
            ptrTable[0][i] = Pointer(0, i - 1, "*", goal_token[i - 1], 1)
    for i in range(rows):
        table[i][0] = i
        if i > 0:
            ptrTable[i][0] = Pointer(i - 1, 0, initial_token[i - 1], "*", 1)

    # Complete edit distance table using Dynamic Programming outlined in class
    # Will use EDScore instead of edit distance
    # EDScore = max(1 - edit-dist(M,C)/|M_{unigrams}|,0)
    for i in range(1, rows):
        for j in range(1, columns):
            # Costs for all edit operations is now 1
            deletionCost = table[i - 1][j] + 1
            insertionCost = table[i][j - 1] + 1
            subActionCost = 1 if initial_token[i - 1] != goal_token[j - 1] else 0
            substitutionCost = table[i - 1][j - 1] + subActionCost
            # Min cost of edit distance table overall
            minCost = min(deletionCost, insertionCost, substitutionCost)
            table[i][j] = minCost
            # Backtrace pointer table utilizing the ptrTable created earlier
            if substitutionCost == minCost:
                ptrTable[i][j] = Pointer(i - 1, j - 1, initial_token[i - 1], goal_token[j - 1], subActionCost)
            elif insertionCost == minCost:
                ptrTable[i][j] = Pointer(i, j - 1, "*", goal_token[j - 1], 1)
            else:
                ptrTable[i][j] = Pointer(i - 1, j, initial_token[i - 1], "*", 1)

    # Now it will return the Edit Distance Score along with the ptr table showing the methods used
    # EDScore = max(1 - edit-dist(M,C)/|M_{unigrams}|,0), so either some value or 0 will be returned

    edit_dist = table[rows - 1][columns - 1]
    # Below, initial is put into a set to have only unique words without any repetitions
    m_unigrams = set(initial_token)
    ed_score = 1 - (float(edit_dist) / len(m_unigrams))
    # For in the EDScore formula, only the max value of either ed_score or 0 should be returned
    if ed_score > 0:
        return ed_score, ptrTable
    else:
        return 0, ptrTable

# Alignment String building
def aliString(ptrTable):
    # Retrieve the full edit distance position
    ptr = ptrTable[len(ptrTable) - 1][len(ptrTable[len(ptrTable) - 1]) - 1]

    # Build a string of alignments
    x = ""
    # Iterate until the full alignment has been created
    while ptr is not None:
        if x == "":
            x = ptr.getAction()
        else:
            # will print alignments followed by a "," that separates them
            x = f"{ptr.getAction()}, {x}"
        # Update the pointer
        ptr = ptrTable[ptr.i][ptr.j]
    # Return full alignment string
    return x


# Compute edit distance between two words
# Input your initial word and then your goal word
if __name__ == "__main__":
    # Get argument sentences
    initial = input("Enter first sentence: ")
    goal = input("Enter second sentence: ")

    # Compute and output edit distance
    editDistance, ptrTable = computeEditDistance(initial, goal)
    print(f"The edit distance score from '{initial}' to '{goal}' is {editDistance}")

    # Output alignment
    print(f"The alignment from '{initial}' to '{goal}' is: ")
    print(aliString(ptrTable))
