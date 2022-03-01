# Call sys.path() to get a list of strings that specifies the search
# paths for modules. Call list.append(dir) wirh dir as "." to add the
# current directory as a path to search for modules.
import sys
sys.path.append(".")
# import time to calculate the running time
import time
# import copy to copy the board
import copy
# import random for randomness of the genetic
import random
# import numpy for pick selection
import numpy as np
# import Board from given file
from board import Board

MUTATIONRATE = 0.05

def createStates():
    # a list to contain 8 states
    states = []
    for state in range(8):
        # generate 8 5-queens boards
        tempBoard = Board(5)
        states.append(tempBoard)
    
    return states

def boardToArray(qBoard):
    # initialize an array to contain the column index of each queen
    sequence = [0, 0, 0, 0, 0]
    
    # for each row
    for row in range(5):
        # find the column of the current queen
        column = qBoard.get_map()[row].index(1)
        sequence[row] = column
        
    return sequence

def selection(boards):
    chanceOfSelection = []
    total = 0

    # finding the survival rate of each gene
    for index in range(8):
        # use 5C2 - get_fitness() to find number of none attacking pair
        numOfNoneAttackingPair = 10 - boards[index].get_fitness()
        chanceOfSelection.append(numOfNoneAttackingPair)
        total = numOfNoneAttackingPair + total
    
    # use np.random.choice to pick random board base on probability
    probability = [(chance / total) for chance in chanceOfSelection]
    selectedBoards = np.random.choice(boards, 8, p = probability).tolist()
    
    return selectedBoards

def crossOver(boards):
    crossoveredBoards = []
    for pairs in range(4):
        # random cross over position
        rand = random.randrange(5)
        # two pairs
        firstBoard = boardToArray(boards[pairs * 2])
        secondBoard = boardToArray(boards[pairs * 2 + 1])
        # perform cross over
        for index in range(rand, 5):
            firstBoard[index], secondBoard[index] = secondBoard[index], firstBoard[index]
        # change to boards
        tempFirst = arrayToBoard(firstBoard)
        crossoveredBoards.append(tempFirst)
        tempSecond = arrayToBoard(secondBoard)
        crossoveredBoards.append(tempSecond)
        
    return crossoveredBoards
        
    
def mutation(boards):
    mutatedBoards = []
    #Loop thru each board
    for eachBoard in boards:
        # change to array code
        sequence = boardToArray(eachBoard)
        for row in range(5):
            # for each number in a sequence, there is an arbitrary mutation
            # rate: 0.05 of changing to a different number
            if random.random() < MUTATIONRATE:
                #0-4
                sequence[row] = random.randrange(5)
        # change to board
        tempBoard = arrayToBoard(sequence)
        mutatedBoards.append(tempBoard)
            
    return mutatedBoards

def arrayToBoard(sequence):
    # create an empty board
    tempMap = [[0 for j in range(5)] for i in range(5)]
    
    # add queen to the board
    for row in range(5):
        tempMap[row][sequence[row]] = 1

    # make a board then replace the board
    returnBoard = Board(5)
    returnBoard.map = copy.deepcopy(tempMap)
    
    return returnBoard

def geneticAlgorithm(boards):
    # selection
    selectedBoards = selection(boards)

    # cross over
    crossoveredBoards = crossOver(selectedBoards)

    # mutation
    mutatedBoards = mutation(crossoveredBoards)

    # next boards
    newGen = mutatedBoards

    # add old boards
    for oldBoard in boards:
        newGen.append(oldBoard)

    # use sorted()[:8] to get the best gen
    newGen = sorted(newGen, key = lambda eachBoard:(10 - eachBoard.get_fitness()), reverse = True)[:8]

    return newGen

def main():
    # starting time
    start = time.time()

    # program body starts
    # initialize 8 states
    boards = createStates()

    # perform the genetic algorithm
    isSolved = False
    solution = Board(5)
    
    while not isSolved:
        boards = geneticAlgorithm(boards)
        for eachBoard in boards:
            numOfAttackingPairs = eachBoard.get_fitness()
            if numOfAttackingPairs == 0:
                solution = eachBoard
                isSolved = True
                break
    
    # program body ends
    # end time
    end = time.time()

    # print out the result
    # total time taken
    totalTime = int(round((end - start) * 1000))
    print(f"Running time: {totalTime}ms")
    solution.show_map()
    return

main()
