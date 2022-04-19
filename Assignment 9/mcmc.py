'''
Ivy Nguyen
Assignment 9
'''

# import random for randomly selecting the state
import random

# part a
def samplingProbabilities():
    # print the result
    print("Part A. The sampling probabilities")
    print("P(C|-s,r) = <0.8780, 0.1220>")
    print("P(C|-s,-r) = <0.3103, 0.6897>")
    print("P(R|c,-s,w) = <0.9863, 0.0137>")
    print("P(R|-c,-s,w) = <0.8182, 0.1818>")
    return

# part b
def transitionProbabilityMatrix(matrix):
    # the labels of the matrix
    label = ["S1", "S2", "S3", "S4"]
    
    # print the result
    print("Part B. The transition probability matrix")
    # print labels
    print("\t" + label[0] + "\t" + label[1] + "\t" + label[2] + "\t" + label[3])
    # print the matrix
    for index, row in enumerate(matrix):
        print(label[index] + "\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t".format(row[0], row[1], row[2], row[3]))
    return

# part c
def queryProbability(matrix):
    # number of samples to estimate the probability
    samples = 999999
    
    # array to keep the counting
    states = [0, 0, 0, 0]

    # initial state
    state = random.randrange(0, 4) # between 0 to 3
    states[state] += 1

    # start generating the rest samples
    for count in range(999999):
        # use random.choice to pick random state based on probability
        probability = matrix[state]
        state = random.choices(range(4), weights = probability)[0]
        # add to the array
        states[state] += 1

    #print the result
    print("Part C. The probability for the query")
    print("P(C|-s,w) = <{:.4f}, {:.4f}>".format((states[0]+states[1])/samples,(states[2]+states[3])/samples))
    return

def main():
    # the matrix from part b
    matrix = [[0.9322, 0.0068, 0.0610, 0.0000],
              [0.4932, 0.1620, 0.0000, 0.3448],
              [0.4390, 0.0000, 0.4701, 0.0909],
              [0.0000, 0.1552, 0.4091, 0.4357]]

    # print out the result from part a, b, and c
    samplingProbabilities()
    print()
    transitionProbabilityMatrix(matrix)
    print()
    queryProbability(matrix)
    
main()
