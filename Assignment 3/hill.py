# Call sys.path() to get a list of strings that specifies the search
# paths for modules. Call list.append(dir) wirh dir as "." to add the
# current directory as a path to search for modules.
import sys
sys.path.append(".")
# import time to calculate the running time
import time
# import copy to copy the board
import copy
# import Board from given file
from board import Board

def hillClimbing(qBoard):
    # use recursion for this
    minBoard = qBoard
    minCost = 10 + 1 # all pairs attacking each other + 1 (5C2)

    # for each row
    for row in range(5):
        # find the index of the current queen
        queen = qBoard.get_map()[row].index(1)

        #flip the value
        qBoard.flip(row, queen)

        #for each column
        for column in range(5):

            # if the this position is not the current queen's position
            if column != queen:
                # flip the value to 1
                qBoard.flip(row, column)

                # calculate number of attacking pairs
                cost = qBoard.get_fitness()

                # compare with the min cost
                # if it is less than or equal the current min cost
                if cost <= minCost:
                    minCost = cost
                    minBoard = copy.deepcopy(qBoard)
                    # return if there is no attacking pair
                    if minCost == 0:
                        return minBoard

                # flip the value back to 0
                qBoard.flip(row, column)
        # if there is no cost that less than the current cost,
        # flip the value back to 1 and move to the next row
        qBoard.flip(row, queen)

    # return if there is no attacking pair
    if minCost == 0:
        return minBoard

    # restart the procedure
    return hillClimbing(minBoard)
                

def main():
    # starting time
    start = time.time()

    # program body starts
    # initialize the board
    initialBoard = Board(5)
    
    # use hill climbing algorithm
    finalBoard = hillClimbing(initialBoard)
    
    # program body ends
    # end time
    end = time.time()

    # print out the result
    # total time taken
    totalTime = int(round((end - start) * 1000))
    print(f"Running time: {totalTime}ms")
    # the final map
    finalBoard.show_map()
    return

main()
