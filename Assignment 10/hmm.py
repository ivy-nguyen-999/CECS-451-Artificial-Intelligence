#import sys for reading input from the system
import sys

def parseVariables():
    sysInput = sys.argv
    fileName = str(sysInput[-1])
    
    #use with statement to close the file automatically
    with open(fileName) as textFile:
        #save all the lines as a list of strings
        lines = textFile.readlines()

    #create a list to contain all lines in the text file
    variables = []

    for line in lines:
        #add each line to the list
        variables.append(line.strip().split(','))

    return variables

def filtering(probabilities, evidence):
    #record the number of the evidence variables
    length = len(evidence)

    #extract data
    b, bNot = float(probabilities[1]), 1 - float(probabilities[1])
    c, cNot = float(probabilities[2]), 1 - float(probabilities[2])
    d, dNot = float(probabilities[3]), 1 - float(probabilities[3])
    f, fNot = float(probabilities[4]), 1 - float(probabilities[4])

    #find joint observation probability
    if evidence[-1] == 't':
        e, eNot = d, f
    else:
        e, eNot = dNot, fNot

    #base case:
    if length == 1:
        a, aNot = float(probabilities[0]), 1 - float(probabilities[0])
    #recursive
    else:
        #call the filtering function again
        a, aNot = filtering(probabilities, evidence[:length - 1])

    #calculate the function inside the summation
    x, xNot = a * b + aNot * c, a * bNot + aNot * cNot
    #multiply the function outside the summation
    true, false = e * x, eNot * xNot
    #normalize before return the result
    total = true + false
    
    #return as an array
    return [true/total, false/total]
        
def main():
    events = parseVariables()

    #calculate each event
    for event in events:
        probabilities = filtering(event[:5], event[5:])
        print(','.join(event) + "--><{:.4f},{:.4f}>".format(probabilities[0], probabilities[1]))

main()
