# Owen Stanski, Jack Taylor, Andre Le
# 4/26/20
# CSC_470
# Project 3
# This class is used to maintain a pointer-like object to maintain the backtrace through an edit distance table

class Pointer():
    def __init__(self, i, j, initialChar, goalChar, cost):
        self.i = i
        self.j = j
        self.initialChar = initialChar
        self.goalChar = goalChar
        self.cost = cost
    
    def getAction(self):
        return f"{self.initialChar}->{self.goalChar} {self.cost}"