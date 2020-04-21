
# CSC_470
# Project 3
# Back trace pointer file

class Pointer():
    def __init__(self, i, j, initialChar, goalChar, cost):
        self.i = i
        self.j = j
        self.initialChar = initialChar
        self.goalChar = goalChar
        self.cost = cost
    
    def getAction(self):
        return f"{self.initialChar}->{self.goalChar} {self.cost}"