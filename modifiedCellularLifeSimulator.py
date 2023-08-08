# This program executes a modified cellular life simulator, where the
# input is a file that contains a starting cellular matrix, then simulates
# the next 100 time-steps of the cellular matrix

import sys
import argparse
import os.path

from os import path
from multiprocessing import Pool

# main function
def main():

    # command line arguments
    parser = argparse.ArgumentParser(description = 'Execute modified cellular life simulator')
    parser.add_argument('-i', dest= 'df', required = True, help= 'input a file containing a matrix', metavar='FILE')
    parser.add_argument('-o', dest = 'of', required = True, help = 'input a file to write new matrix', metavar = 'FILE')
    parser.add_argument('-n', dest = 'ts', required = True, help = 'input an int for number of timesteps', metavar = 'INT')
    parser.add_argument('-t', dest = 'threadNum', required = False, nargs = '?', const = 1, type = int, help = 'input a number of threads to use')
    args = parser.parse_args()

    # sets input file to matrix if the file has valid syntax and characters
    matrix = validate(args.df)
    # runs the main program at a specified timestep (timestep given in range())
    matrix = timeStep(matrix, args.threadNum, args.ts)
    # writes the final matrix to the output file specified
    outputMatrix(matrix,args.of)
#########################################################

def timeStep(matrix, processes, tStep):
    tStep = int(tStep)
    # create Pool
    processPool = Pool(processes)
    # loops through timesteps
    for steps in range(tStep):
        poolData = list()
        for row in range(len(matrix)):
            data = [matrix, row]
            poolData.append(data)
        mixData = processPool.map(simulate, poolData)
        matrix = sortData(mixData)
        del (poolData)
    return matrix
#########################################################

# sorts the data from the pool and inserts into new matrix
def sortData(data):
    newMatrix = [''] * len(data)
    for i in range(len(data)):
        newMatrix[data[i][1]] = data[i][0]
    return newMatrix
#########################################################

# determines if file is valid
def validate(df):
    if(path.exists(df) == False):
        print('File path does not exist\n')
        exit()
# if file is valid, opens and stores contents in an array
    else:
        with open(df, 'rt') as infile:
            matrix = [list(line.strip()) for line in infile.readlines()]
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if matrix[row][column] != '.':
                if matrix[row][column] != 'O':
                    if matrix[row][column] != '\n':
                        print(f"Character is invalid :'{matrix[row][column]}'")
                        exit()
    return matrix
#########################################################

# simulates the next step in the algorithm
def simulate(data):
    matrix = data[0]
    rowNum = data[1]
    row = matrix[rowNum]
    newRow = list()
    for i in row:
      newRow.append(i)
    for column in range(len(row)):
        alive = findNeighbors(matrix, rowNum, column)
        if row[column] == '.':
            if (alive == 2 or alive == 4 or alive == 6 or alive == 8):
                newRow[column] = 'O'
        elif row[column] == 'O':
            if alive == 2 or alive == 3 or alive == 4:
                newRow[column] = 'O'
            else:
                newRow[column] = '.'
    return [newRow, rowNum]
#########################################################

# finds neighbors of the current cell and returns number of alive cells
def findNeighbors(matrix, row, column):
    counter = 0
    #above
    if(matrix[row-1][column-1]) == 'O':
        counter += 1
    if(matrix[row-1][column]) == 'O':
        counter += 1
    if(matrix[row-1][column+1-len(matrix[0])]) == 'O':
        counter += 1

    #same row
    if(matrix[row][column-1]) == 'O':
        counter += 1
    if(matrix[row][column+1-len(matrix[0])]) == 'O':
        counter += 1

    #below
    if(matrix[row+1-len(matrix)][column-1]) == 'O':
        counter += 1
    if(matrix[row+1-len(matrix)][column]) == 'O':
        counter += 1
    if(matrix[row+1-len(matrix)][column+1-len(matrix[0])]) == 'O':
        counter += 1
    return counter
#########################################################

# writes the matrix to the output file
def outputMatrix(output_matrix, output_file):
    output_str = ''
    for i in output_matrix:
        str = ''.join(i)
        output_str += str
        output_str += '\n'
    output_str = output_str[:-1]
    with open(output_file, 'w') as outFile:
        sys.stdout = outFile
        print(output_str)
#########################################################

# calls main function
if __name__ == '__main__':
    main()
