#!/usr/bin/env python3

import re
import sys

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    pass

class Board:
    def __init__(self, state):
        self.state = state
        self.boardRep = None
    
    def createBoard(self):
        rowRef = 0
        boardRowsRep = []
        # print ("self.state.rows = {}".format(self.state.rows))
        for i in range (0, 2 * self.state.rows + 2):
            boardColsRep = []
            if (i%2 == 0):    
                for j in range (0, 3 + self.state.cols * 4):
                    boardColsRep.append("-")            
            elif (i % 2 == 1 and i != 2 * self.state.rows + 1):
                # print("j = {}".format(j))
                boardColsRep.append(rowRef)
                for k in range (0, len(str(self.state.rows)) + 1
                                    - len(str(rowRef))):
                    boardColsRep.append(" ")
                boardColsRep.append("|")
                for j in range (0, self.state.cols):
                    # print("i = {}".format(i))
                    # print("j = {}".format(j))
                    boardColsRep.append(" ")
                    boardColsRep.append(
                        self.state.boardRep[int((i-1)/2)][j])
                    boardColsRep.append(" ")
                    boardColsRep.append("|")
                rowRef += 1
            else:
                for k in range (0, len(str(self.state.rows)) + 1):
                    boardColsRep.append(" ")
                boardColsRep.append("|")
                alphabet = 97
                for j in range (0, self.state.cols):
                    boardColsRep.append(" ")
                    boardColsRep.append("{}".format(chr(alphabet)))
                    boardColsRep.append(" ")
                    boardColsRep.append("|")
                    alphabet += 1
            boardRowsRep.append(boardColsRep)
        self.boardRep = boardRowsRep

    def printBoard(self):
        self.createBoard()
        # print("len(self.boardRep): {}".format(len(self.boardRep)))
        for i in range (0, len(self.boardRep)):
            row = self.boardRep[i]
            # print("len(row[{}]): {}".format(i, len(row[i])))
            for j in range (0, len(row)):
                print(row[j], end = "")
            print("")
            

            # print ("i = {}".format(i))
        #     print ("---", end = "")
        #     for j in range (0, self.state.cols):
        #         print ('----', end = "")
        #     print("")
        #     print ("{} |".format(rowRef), end = "")
        #     for j in range (0, self.state.cols):
        #         print ('   |', end = "")
        #     print("")
        #     rowRef += 1
        # print ("---", end = "")
        # for j in range (0, self.state.cols):
        #     print ('----', end = "")
        # print("")
        
        # print("  |", end = "")
        # alphabet = 97
        # for i in range (0, self.state.cols):
        #     print(" {} |".format(chr(alphabet)),end  = "")
        #     alphabet += 1
        # print("")

class State:
    rows = 0 # y
    cols = 0 # x
    numObstacles = 0
    start = None # pair of x, y coords
    goal = None  # pair of x, y coords

    def __init__(self, rows, cols, numObstacles, start, goal):
        self.rows = rows
        self.cols = cols
        self.boardRep = [[(" ", 1) for j in range(cols)] 
                        for i in range(rows)]
        self.numObstacles = numObstacles
        self.start = start
        self.goal = goal
        self.totPathCost = 0
        self.path = []
        self.nodesExplored = []

        # Storing of obstacles in self.boardRep
        if numObstacles > 0:
            obstaclePositions = input("")
            obstaclePositions = re.split("(\d+)", 
                                        obstaclePositions[38:]
                                        .replace(" ", ""))

            for i in range (0, self.numObstacles + 1, 2):
                col = ord(obstaclePositions[i]) - ord("a")
                row = int(obstaclePositions[i+1])
                self.boardRep[row][col][0] = "x"

        # Updating cost to move TO selected grid
            stepCosts = input("")
            stepCosts = re.split("(\d+)", 
                                        obstaclePositions[38:]
                                        .replace(" ", ""))

            for i in range (0, self.numObstacles + 1, 2):
                col = ord(obstaclePositions[i]) - ord("a")
                row = int(obstaclePositions[i+1])
                self.boardRep[row][col][0] = "x"

def search():
    pass


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_AStar():
    
    print('hi')
    
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored, pathCost= search() #For reference
    return moves, nodesExplored, pathCost #Format to be returned

if __name__ == "__main__":
    boardRows = int(input("Rows: "))
    boardCols = int(input("Cols: "))
    numObstacles = int(input("Number of obstacles: "))

    state = State(boardRows, boardCols, numObstacles, 0, 0)
    board = Board(state)
    board.printBoard()

    