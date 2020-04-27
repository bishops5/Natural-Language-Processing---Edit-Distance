# Project 3 T3 and T4
# CSC_470
# Sam Bishop

import sys
import nltk
import re
import xml.etree.ElementTree
import random




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


def normalizeSentence(sentence):
    # first need to normalize both sentences
    # lowercase the sentences
    sentence = sentence.lower()

    # removing extra whitespaces (via regex) in off chance there is any
    sentence = re.sub(' +', ' ', sentence)

    #expand contractions
    sentence = contrct_punct(sentence)

    #tokenize sentence
    sentence_token = nltk.word_tokenize(sentence)

    return sentence_token


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

    # Now it will return the Edit Distance Score along with the alignment string
    # EDScore = max(1 - edit-dist(M,C)/|M_{unigrams}|,0), so either some value or 0 will be returned

    edit_dist = table[rows - 1][columns - 1]
    # Below, start token is put into a set to have only unique words without any repetitions
    m_unigrams = set(start_tk)
    ed_score = 1 - (float(edit_dist) / len(m_unigrams))
    # For in the EDScore formula, only the max value of either ed_score or 0 should be returned
    if ed_score > 0:
        return ed_score, aliString
    else:
        return 0, aliString

# will give Percent Match value
counter = 0
def percentMatch(start_tk, end_tk):
    m_unigrams = set(start_tk)
    c_unigrams = set(end_tk)

    # finding the intersection of the 2 unigrams
    m_intersect_c = m_unigrams.intersection(c_unigrams)

    #percent match formula
    pm = (float(len(m_intersect_c))/len(m_unigrams))
    #return pm
    return pm


if __name__ == "__main__":
    # Parse tmx file to data list
    f = xml.etree.ElementTree.parse(sys.argv[1])
    f = f.find("body")
    data = []
    for pair in f:
        source = normalizeSentence(pair[0][0].text)
        trans = normalizeSentence(pair[1][0].text)
        data.append((source, trans))

    # Select 10k sentences for database
    database = random.sample(data, 10000)
    # Don't select 5 sentences that are in the database
    for pair in database:
        data.remove(pair)
    
    # 5 sentences to test randomly selected
    tests = random.sample(data, 5)

    for t in tests:
        topPMs = []
        topEDs = []
        for d in database:
            # PM
            pm = percentMatch(t[0], d[0])
            # Fill top 10 pm with first 10 sentences - Base case
            if len(topPMs) < 10:
                dictionary = {
                    "score": pm,
                    "source": d[0],
                    "translation": d[1]
                }
                topPMs.append(dictionary)
                topPMs.sort(key = lambda l: l["score"], reverse=True)
            # If more than 10 sentences then the pm needs to be better than the lowest
            elif topPMs[9]["score"] < pm:
                topPMs.pop(9)
                dictionary = {
                    "score": pm,
                    "source": d[0],
                    "translation": d[1]
                }
                topPMs.append(dictionary)
                topPMs.sort(key = lambda l: l["score"], reverse=True)
            # ED
            ed, aliString = computeEditDistance(t[0], d[0])
            # Fill top 10 ed with first 10 sentences - Base case
            if len(topEDs) < 10:
                dictionary = {
                    "score": ed,
                    "source": d[0],
                    "translation": d[1],
                    "alignment": aliString
                }
                topEDs.append(dictionary)
                topEDs.sort(key = lambda l: l["score"], reverse=True)
            # If more than 10 sentences then the ed needs to be better than the lowest
            elif topEDs[9]["score"] < ed:
                topEDs.pop(9)
                dictionary = {
                    "score": ed,
                    "source": d[0],
                    "translation": d[1],
                    "alignment": aliString
                }
                topEDs.append(dictionary)
                topEDs.sort(key = lambda l: l["score"], reverse=True)
        # Print out top 10 pm and ed results for this sentence here - Format this better*************************************************
        counter+=1
        print ('\n')
        print("THE FOLLOWING OUTPUT IS THE  " )
        print(counter)
        print ("PERCENT MATCH")
        print(topPMs)

        print('\n')
        print("THE FOLLOWING OUTPUT IS THE  " )
        print(counter)
        print ("EDIT DISTANCE")
        print(topEDs)
       
        









