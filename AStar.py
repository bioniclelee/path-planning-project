#!/usr/bin/env python3

import re
import sys
from tracemalloc import start

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__ (self, type):
        self.type = type
    
    # returns moveList of possible moves from current position based on self.type
    def possibleMoveList(self, currPos):
        if (self.type == "King"):
            pass
        elif (self.type == "Queen"):
            pass
        elif (self.type == "Bishop"):
            pass
        elif (self.type == "Rook"):
            pass
        elif (self.type == "Knight"):
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
                        self.state.boardRep[int((i-1)/2)][j][0])
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

    def __init__(self, file):
        # print("file = {}".format(str(file)))
        with open(file) as f:
            lines = f.readlines()
        
        lineCount = len(lines)
        # print(lineCount)
        # for line in file:
        #     if line != "\n":
        #         lineCount += 1
        # print("lineCount = {}".format(lineCount))

        self.rows = int("".join(lines[0][5:]))
        self.cols = int("".join(lines[1][5:]))

        self.boardRep = [[(" ", 1) for j in range(self.cols)] 
                        for i in range(self.rows)]

        self.numObstacles = int("".join(lines[2][20:]))
        # for updating self.boardRep with obstacle positions
        if (self.numObstacles > 0):
            self.splitCoordsAndEditBoardRep(lines[3], 38, 0, False, "X")

        # for updating self.boardRep with start position
        if (len(lines[-2]) > 0):
            self.splitCoordsAndEditBoardRep(lines[-2]
                                            .split(",")[-1]
                                            .split("]")[0], 0, 0, False, "S")

        # for updating self.boardRep with goal position(s)
        if (len(lines[-1][31:]) > 0):
            self.splitCoordsAndEditBoardRep(lines[-1], 31, 0, False, "G")

        # Counting lines for end of pathCost list
        endOfPathCostList = 0
        for i in range (4, lineCount):
            # print((lines[i].split(" "))[0])
            firstWord = (lines[i].split(" "))[0]
            if (firstWord == 'Number'):
                endOfPathCostList = i
                break

        # updating pathCost to self.boardRep
        rawList = list(lines[endOfPathCostList - lineCount -1:4:-1])
        self.posStr = ""
        self.pathCostList = []
        for i in range (0, len(rawList)):
            rawEntry = rawList[i].rstrip("\n").replace("[","").replace("]","").split(",")
            self.posStr += str(rawEntry[0])
            if (i != len(rawList) - 1):
                self.posStr += " "
            self.pathCostList.append(rawEntry[1])
        
        self.splitCoordsAndEditBoardRep(self.posStr, 0, 1, True, self.pathCostList)

        # updating enemy piece type and position
        startOfEnemyPieceList = endOfPathCostList
        enemyPieceList = lines[startOfEnemyPieceList][66::].replace("\n","").split(" ")
        numberOfEnemyPieces = 0
        for i in range (0, len(enemyPieceList)):
            numberOfEnemyPieces += int(enemyPieceList[i])
        
        print(numberOfEnemyPieces)
        # print(lines[startOfEnemyPieceList])

        enemyPieces = []
        enemyPiecesLocation = ""
        for i in range (startOfEnemyPieceList + 2, startOfEnemyPieceList + 2 + numberOfEnemyPieces):
            # print((lines[i].replace("[","").replace("]","").split(","))[0])
            enemyPiecesAndLocation = lines[i].replace("[","").replace("]","").replace("\n","").split(",")
            print("enemyPiecesAndLocation[1] = {}".format(enemyPiecesAndLocation[1]))
            enemyPiecesLocation += enemyPiecesAndLocation[1]
            enemyPiecesLocation += " "
            print (enemyPiecesLocation)
            pieceType = enemyPiecesAndLocation[0]
            if (pieceType == "King"):
                enemyPieces.append("K")
            if (pieceType == "Queen"):
                enemyPieces.append("Q")
            if (pieceType == "Bishop"):
                enemyPieces.append("B")
            if (pieceType == "Rook"):
                enemyPieces.append("R")
            if (pieceType == "Knight"):
                enemyPieces.append("H")   

        self.splitCoordsAndEditBoardRep(enemyPiecesLocation, 0, 0, True, enemyPieces)

        # str(str(str(str(str(str(lines[-7:4:-1])
        #                     .replace("]\\n",""))
        #                     .replace("[",""))
        #                     .replace("'",""))
        #                     .split(","))
        #                     .split(", "))

        
        # posList = []
        # pathCostList = []
        # for i in range (0, len(pathCostAndPosList),2):
        #     posList.append(pathCostAndPosList[i])
        #     pathCostList.append(pathCostAndPosList[i+1])
        
        # print (str(posList))
        # self.splitCoordsAndEditBoardRep(str, 31, 0, False, "G")

        self.totPathCost = 0
        self.path = []
        self.nodesExplored = []

        # Storing of obstacles in self.boardRep
        # if self.numObstacles > 0:
        #     obstaclePositions = lines[3]
        #     obstaclePositions = re.split("(\d+)", 
        #                                 obstaclePositions[38:]
        #                                 .replace(" ", ""))

        #     for i in range (0, self.numObstacles + 1, 2):
        #         col = ord(obstaclePositions[i]) - ord("a")
        #         row = int(obstaclePositions[i+1])
        #         tempList = list(self.boardRep[row][col])
        #         tempList[0] = "x"
        #         self.boardRep[row][col] = tuple(tempList)

        # Updating cost to move TO selected grid
        # stepCosts = input("")
        # stepCosts = re.split("(\d+)", 
        #                             obstaclePositions[38:]
        #                             .replace(" ", ""))

        # for i in range (0, self.numObstacles + 1, 2):
        #     col = ord(obstaclePositions[i]) - ord("a")
        #     row = int(obstaclePositions[i+1])
        #     self.boardRep[row][col][0] = "x"

    def splitCoordsAndEditBoardRep(self, str, sliceInd, tuplePos, isList, input):
        newList = re.split("(\d+)", str[sliceInd:].replace(" ", ""))
        # print(newList)

        for i in range (0, len(newList) - 1, 2):
            col = ord(newList[i]) - ord("a")
            row = int(newList[i+1])
            tempList = list(self.boardRep[row][col])
            if isList:
                tempList[tuplePos] = input[int(i/2)]
            else:
                tempList[tuplePos] = input
            self.boardRep[row][col] = tuple(tempList)

def search():
    pass


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_AStar():

    # You can code in here but you cannot remove this function or change the return type
    
    # state = State(sys.argv[1])
    # board = Board(state)
    # board.printBoard()

    moves, nodesExplored, pathCost= search() #For reference
    return moves, nodesExplored, pathCost #Format to be returned

if __name__ == "__main__":

    # run_AStar()
    # boardRows = int(input("Rows: "))
    # boardCols = int(input("Cols: "))
    # numObstacles = int(input("Number of obstacles: "))

    state = State(sys.argv[1])
    board = Board(state)
    board.printBoard()
    