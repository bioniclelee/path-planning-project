#!/usr/bin/env python3

import re
import sys
from tracemalloc import start

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__ (self, type, currPos):
        self.type = type
        self.currPos = currPos
        self.moveDirectionMatrix = []

        # Storing of movement direction and extent
        # matrix indices: index 1-8 for each octal direction starting at 12 o'clock
        # 9 for knight movement
        # cell value: 0 = no movement, 1 = 1 step, 2 = unlimited movement
        if (self.type == "King"):
            for i in range (0, 9):
                self.moveDirectionMatrix.append(1)
            self.moveDirectionMatrix.append(0)
        elif (self.type == "Queen"):
            for i in range (0, 9):
                self.moveDirectionMatrix.append(2)
            self.moveDirectionMatrix.append(0)
        elif (self.type == "Bishop"):
            for i in range (1, 9, 2):
                self.moveDirectionMatrix.append(2)
            self.moveDirectionMatrix.append(0)
        elif (self.type == "Rook"):
            for i in range (0, 9, 2):
                self.moveDirectionMatrix.append(2)
            self.moveDirectionMatrix.append(0)
        elif (self.type == "Knight"):
            for i in range (0, 9):
                self.moveDirectionMatrix.append(0)
            self.moveDirectionMatrix.append(1)

    def __str__ (self):
        return "Piece is of type " + str(self.type) + " and is currently at " + str(self.currPos[0] + self.currPos[1])


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
                for j in range (0, 4 + self.state.cols * 4):
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


class State:
    rows = 0 # y
    cols = 0 # x
    numObstacles = 0
    start = None # pair of x, y coords
    goal = None  # pair of x, y coords

    def __init__(self, file):
        with open(file) as f:
            lines = f.readlines()
        
        lineCount = len(lines)

        self.rows = int("".join(lines[0][5:]))
        self.cols = int("".join(lines[1][5:]))

        self.boardRep = [[(" ", 1) for j in range(self.cols)] 
                        for i in range(self.rows)]

        # for updating self.boardRep with obstacle positions
        self.numObstacles = int("".join(lines[2][20:]))
        if (self.numObstacles > 0):
            self.splitCoordsAndEditBoardRep(lines[3], 38, 0, False, "X")

        # for updating self.boardRep with goal position(s)
        if (len(lines[-1][31:]) > 0):
            self.splitCoordsAndEditBoardRep(lines[-1], 31, 0, False, "G")

        # Counting lines for end of pathCost list
        endOfPathCostList = 0
        for i in range (4, lineCount):
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

        # establish enemy piece type and position, and spawn in enemy objects
        startOfEnemyPieceList = endOfPathCostList
        enemyPieceList = lines[startOfEnemyPieceList][66::].replace("\n","").split(" ")
        numberOfEnemyPieces = 0
        for i in range (0, len(enemyPieceList)):
            numberOfEnemyPieces += int(enemyPieceList[i])

        enemyPieces = []
        enemyPiecesLocation = ""
        for i in range (startOfEnemyPieceList + 2, startOfEnemyPieceList + 2 + numberOfEnemyPieces):
            enemyPiecesAndLocation = lines[i].replace("[","").replace("]","").replace("\n","").split(",")
            enemyPiecesLocation += enemyPiecesAndLocation[1]
            enemyPiecesLocation += " "
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

            enemyStartPos = []
            enemyStartPos.append(list(enemyPiecesLocation)[0])
            enemyStartPos.append(list(enemyPiecesLocation)[1])
            enemy = Piece(pieceType, enemyStartPos)
            print(enemy.__str__())

            enemyPieces = []
            enemyPiecesLocation = ""

        self.splitCoordsAndEditBoardRep(enemyPiecesLocation, 0, 0, True, enemyPieces)

        # updating own piece type and position
        startOfOwnPieceList = startOfEnemyPieceList + 2 + numberOfEnemyPieces
        ownPieceList = lines[startOfOwnPieceList][64::].replace("\n","").split(" ")
        numberOfOwnPieces = 0
        for i in range (0, len(ownPieceList)):
            numberOfOwnPieces += int(ownPieceList[i])

        ownPieces = []
        ownPiecesLocation = ""
        for i in range (startOfOwnPieceList + 2, startOfOwnPieceList + 2 + numberOfOwnPieces):
            
            ownPiecesAndLocation = lines[i].replace("[","").replace("]","").replace("\n","").split(",")
            ownPiecesLocation += ownPiecesAndLocation[1]
            ownPiecesLocation += " "
            
            pieceType = ownPiecesAndLocation[0]
            if (pieceType == "King"):
                ownPieces.append("Z")
            if (pieceType == "Queen"):
                ownPieces.append("X")
            if (pieceType == "Bishop"):
                ownPieces.append("C")
            if (pieceType == "Rook"):
                ownPieces.append("V")
            if (pieceType == "Knight"):
                ownPieces.append("B")   

        self.splitCoordsAndEditBoardRep(ownPiecesLocation, 0, 0, True, ownPieces)

        self.totPathCost = 0
        self.path = []
        self.nodesExplored = []

    def splitCoordsAndEditBoardRep(self, str, sliceInd, tuplePos, isList, input):
        newList = re.split("(\d+)", str[sliceInd:].replace(" ", ""))

        for i in range (0, len(newList) - 1, 2):
            col = ord(newList[i]) - ord("a")
            row = int(newList[i+1])
            tempList = list(self.boardRep[row][col])
            if isList:
                tempList[tuplePos] = input[int(i/2)]
            else:
                tempList[tuplePos] = input
            self.boardRep[row][col] = tuple(tempList)

    def isValid (self, coord):
        return (coord[0] >= 0 and coord[0] <= self.rows and
                coord[1] >= 0 and coord[1] <= self.cols)


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

    state = State(sys.argv[1])
    board = Board(state)
    board.printBoard()
    