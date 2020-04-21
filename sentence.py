# Owen Stanski, Jack Taylor, Andre Le
# 4/26/20
# CSC_470
# Project 3
# This class is used to maintain an entry in the TMR

class Sentence():
    # TODO: Normalize the sentences
    # @Params: String sentence
    # @Return: String[] tokens
    def __normalize(self, sentence):
        return sentence.split()

    # Takes a source string and a translation string - Stores as array of words
    def __init__(self, source, translation):
        self.source = self.__normalize(source)
        self.translation = self.__normalize(translation)