
# CSC_470
# Project 3
# Normalization of words and stores the array of words.

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