# Helper functions to aid in your implementation. Can edit/remove
import re
import sys
from tracemalloc import start

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__ (self, type, currPos):
        self.type = type
        currPosAsList = []
        currPosAsList.append(int(currPos[1])) # row
        currPosAsList.append(ord(currPos[0]) - ord('a')) # col
        # print(currPos)
        self.currPos = currPosAsList
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
        return "Piece is of type " + str(self.type) + " and is currently at " + str(chr(self.currPos[1] + ord("a")) + str(self.currPos[0]))

    # adds enemy currPos + pieces that are one step away as obstacle pieces
    def possibleMoves(self, rows, cols):
        possibleMoveList = []
        for i in range (0, 9):
            tempList = []
            directionMag = self.moveDirectionMatrix[i]
            
            # move forward = rowIndex - 1
            if (i == 0):
                if (directionMag == 1):
                    tempList.append(self.currPos[0] - 1) # row
                    tempList.append(int(self.currPos[1])) # col
                    possibleMoveList.append(tempList)
                elif (directionMag == 2):
                    for j in range (-self.currPos[0], rows - self.currPos[0]):
                        tempList = []
                        tempList.append(self.currPos[0] - j) # row
                        tempList.append(int(self.currPos[1])) # col
                        possibleMoveList.append(tempList)
            
            # move diagonal right up = rowInd - 1 && colInd + 1
            elif (i == 1):
                if (directionMag == 1):
                    tempList.append(self.currPos[0] - 1) # row
                    tempList.append(int(self.currPos[1]) + 1) # col
                    possibleMoveList.append(tempList)
                elif (directionMag == 2):
                    if (rows > cols):
                        for j in range (-self.currPos[1], cols - self.currPos[1]):
                            tempList = []
                            tempList.append(self.currPos[0] - j) # row
                            tempList.append(int(self.currPos[1]) + j) # col
                            possibleMoveList.append(tempList)
                    else:
                        for j in range (-self.currPos[0], rows - self.currPos[0]):
                            tempList = []
                            tempList.append(self.currPos[0] - j) # row
                            tempList.append(int(self.currPos[1]) + j) # col
                            possibleMoveList.append(tempList)

            # move right = colInd + 1
            elif (i == 2):
                if (directionMag == 1):
                    tempList.append(self.currPos[0]) # row
                    tempList.append(int(self.currPos[1]) + 1) # col
                    possibleMoveList.append(tempList)
                if (directionMag == 2):
                    for j in range (-self.currPos[1], cols - self.currPos[1]):
                        tempList = []
                        tempList.append(self.currPos[0]) # row
                        tempList.append(int(self.currPos[1]) + j) # col
                        possibleMoveList.append(tempList)

            # move diagonal right down = rowInd + 1 && colInd + 1
            elif (i == 3):
                if (directionMag == 1):
                    tempList.append(self.currPos[0] + 1) # row
                    tempList.append(int(self.currPos[1]) + 1) # col
                    possibleMoveList.append(tempList)
                if (directionMag == 2):
                    if (rows > cols):
                        for j in range (-self.currPos[1], cols - self.currPos[1]):
                            tempList.append(self.currPos[0] + j) # row
                            tempList.append(int(self.currPos[1]) + j) # col
                            possibleMoveList.append(tempList)
                    else:
                        for j in range (-self.currPos[0], rows - self.currPos[0]):
                            tempList = []
                            tempList.append(self.currPos[0] + j) # row
                            tempList.append(int(self.currPos[1]) + j) # col
                            possibleMoveList.append(tempList)

            # move left = colInd - 1
            elif (i == 4):
                if (directionMag == 1):
                    tempList.append(self.currPos[0] + 1) # row
                    tempList.append(int(self.currPos[1])) # col
                    possibleMoveList.append(tempList)
                elif (directionMag == 2):
                    if (rows > cols):
                        for j in range (-self.currPos[1], cols - self.currPos[1]):
                            tempList = []
                            tempList.append(self.currPos[0] + j) # row
                            tempList.append(int(self.currPos[1])) # col
                            possibleMoveList.append(tempList)
                    else:
                        for j in range (-self.currPos[0], rows - self.currPos[0]):
                            tempList = []
                            tempList.append(self.currPos[0] + j) # row
                            tempList.append(int(self.currPos[1])) # col
                            possibleMoveList.append(tempList)

            # move diagonal left down = rowInd + 1 && colInd - 1
            elif (i == 5):
                if (directionMag == 1):
                    tempList.append(self.currPos[0] + 1) # row
                    tempList.append(int(self.currPos[1]) - 1) # col
                    possibleMoveList.append(tempList)
                elif (directionMag == 2):
                    if (rows > cols):                    
                        for j in range (-self.currPos[1], cols - self.currPos[1]):
                            tempList = []
                            tempList.append(self.currPos[0] + j) # row
                            tempList.append(int(self.currPos[1]) - j) # col
                            possibleMoveList.append(tempList)
                    else:
                        for j in range (-self.currPos[0], rows - self.currPos[0]):
                            tempList = []
                            tempList.append(self.currPos[0] + j) # row
                            tempList.append(int(self.currPos[1]) - j) # col
                            possibleMoveList.append(tempList)

            # move left = colInd - 1
            elif (i == 6):
                if (directionMag == 1):
                    tempList.append(self.currPos[0]) # row
                    tempList.append(int(self.currPos[1]) - 1) # col
                    possibleMoveList.append(tempList)
                elif (directionMag == 2):
                    for j in range (-self.currPos[1], cols - self.currPos[1]):
                        tempList = []
                        tempList.append(self.currPos[0]) # row
                        tempList.append(int(self.currPos[1]) - j) # col
                        possibleMoveList.append(tempList)
            
            # move diagonal left up = rowInd - 1 && colInd - 1
            elif (i == 7):
                if (directionMag == 1):
                    tempList.append(self.currPos[0] - 1) # row
                    tempList.append(int(self.currPos[1]) - 1) # col
                    possibleMoveList.append(tempList)
                elif (directionMag == 2):
                    if (rows > cols):
                        for j in range (-self.currPos[1], cols - self.currPos[1]):
                            tempList = []
                            tempList.append(self.currPos[0] - j) # row
                            tempList.append(int(self.currPos[1]) - j) # col
                            possibleMoveList.append(tempList)
                    else:
                        for j in range (-self.currPos[0], rows - self.currPos[0]):
                            tempList = []
                            tempList.append(self.currPos[0] - j) # row
                            tempList.append(int(self.currPos[1]) - j) # col
                            possibleMoveList.append(tempList)
            
            # move in L-shape (knights only)
            elif (i == 8):
                for j in range (0, 2):
                    coeff1 = (-1) ** j
                    
                    # vertical L-path
                    for k in range (0, 2):
                        coeff2 = (-1) ** k
                        tempList = []
                        tempList.append(self.currPos[0] + coeff1 * 2) # row
                        tempList.append(int(self.currPos[1]) + coeff2 * 1) # col
                        possibleMoveList.append(tempList)
                    
                    # horizontal L-path
                    for k in range (0, 2):
                        coeff2 = (-1) ** k
                        tempList = []
                        tempList.append(self.currPos[0] + coeff1 * 1) # row
                        tempList.append(int(self.currPos[1]) + coeff2 * 2) # col
                        possibleMoveList.append(tempList)

        return possibleMoveList

    def move(self, newPos):
        self.currPos = newPos

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
    def __init__(self, file):
        with open(file) as f:
            lines = f.readlines()
        lineCount = len(lines)

        self.start = None # pair of x, y coords

        self.rows = int("".join(lines[0][5:]))
        self.cols = int("".join(lines[1][5:]))

        self.boardRep = [[(" ", 1, False) for j in range(self.cols)] 
                        for i in range(self.rows)]
        self.pred = [[-1 for j in range(self.cols)] 
                        for i in range(self.rows)]

        # for updating self.boardRep with obstacle positions
        self.numObstacles = int("".join(lines[2][20:]))
        if (self.numObstacles > 0):
            self.splitCoordsAndEditBoardRep(lines[3], 38, 0, False, "X")

        self.totPathCost = 0
        self.orderOfNodes = []
        self.numNodesExplored = 0
        self.puzzleComplete = False
        self.queue = []

        # for updating self.boardRep with goal position(s)
        if (len(lines[-1][31:]) > 0):
            self.splitCoordsAndEditBoardRep(lines[-1], 31, 0, False, "G")

        # counting lines for end of pathCost list
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
            enemyStartPos.append(list(enemyPiecesAndLocation[1])[0]) # col
            enemyStartPos.append(list(enemyPiecesAndLocation[1])[1]) # row
            enemy = Piece(pieceType, enemyStartPos)
            # print(enemy.__str__())
            enemyThreatenedSpaces = enemy.possibleMoves(self.rows, self.cols)
            for j in range (0, len(enemyThreatenedSpaces)):
                spaceToCheck = []
                spaceToCheck.append(enemyThreatenedSpaces[j][0])
                spaceToCheck.append(enemyThreatenedSpaces[j][1])
                if self.isValid(spaceToCheck):    
                    tempList = list(self.boardRep[spaceToCheck[0]][spaceToCheck[1]])
                    tempList[0] = "X"
                    self.boardRep[spaceToCheck[0]][spaceToCheck[1]] = tuple(tempList)

        self.splitCoordsAndEditBoardRep(enemyPiecesLocation, 0, 0, True, enemyPieces)

        # establish ally piece type and position
        startOfallyPieceList = startOfEnemyPieceList + 2 + numberOfEnemyPieces
        allyPieceList = lines[startOfallyPieceList][64::].replace("\n","").split(" ")
        numberOfallyPieces = 0
        for i in range (0, len(allyPieceList)):
            numberOfallyPieces += int(allyPieceList[i])

        allyPieces = []
        allyPiecesLocation = ""
        for i in range (startOfallyPieceList + 2, startOfallyPieceList + 2 + numberOfallyPieces):
            
            allyPiecesAndLocation = lines[i].replace("[","").replace("]","").replace("\n","").split(",")
            allyPiecesLocation += allyPiecesAndLocation[1]
            allyPiecesLocation += " "
            
            pieceType = allyPiecesAndLocation[0]
            if (pieceType == "King"):
                allyPieces.append("Z")
            if (pieceType == "Queen"):
                allyPieces.append("X")
            if (pieceType == "Bishop"):
                allyPieces.append("C")
            if (pieceType == "Rook"):
                allyPieces.append("V")
            if (pieceType == "Knight"):
                allyPieces.append("B")
            
            allyStartPos = []
            # print("allyPiecesAndLocation[1] = {}".format(allyPiecesAndLocation[1]))
            newList = re.split("(\d+)", allyPiecesLocation.replace(" ", ""))
            print(newList)

            for i in range (0, len(newList) - 1, 2):
                row = int(newList[i+1])
                # print("row = {}".format(row))
                col = newList[i]
                # print("col = {}".format(col))
            allyStartPos.append(col) # col
            allyStartPos.append(row) # row
            # print("allyStartPos = {}".format(allyStartPos))
            self.ally = Piece(pieceType, allyStartPos)

        print(allyPiecesLocation)
        self.splitCoordsAndEditBoardRep(allyPiecesLocation, 0, 0, True, allyPieces)
        self.visitSquare(self.ally.currPos)
        self.queue.append(self.ally.currPos) # row, col
        
        # storing start position
        startPosList = re.split("(\d+)", allyPiecesLocation.replace(" ", ""))

        for i in range (0, len(startPosList) - 1, 2):
            row = int(startPosList[i+1])
            col = ord(startPosList[i]) - ord("a")
            startPos = []
            startPos.append(row)
            startPos.append(col)
            self.start = startPos
    
    # generation of adjacency matrix for piece at its current position
    def genNeighbour(self, pos):
        # print("pos in genAdjMatrix = {}".format(pos))
        for i in range (-1, 2):
            for j in range (-1, 2):
                coord = []
                coord.append(pos[0] + i) # row
                # print("pos[0] + i = {}".format(pos[0] + i))
                coord.append(pos[1] + j) # col
                # print("coord.append(pos[1] + j) = {}".format(coord.append(pos[1] + j)))
                if not (i == 0 and j == 0) and self.isValid(coord) and (not self.isVisited(coord)):
                    # print("coord = {}".format(coord))
                    return coord
    
    def movePiece(self, piece, newPos):
        currPos = piece.currPos
        move = []
        formattedCurrPos = (chr(currPos[1] + ord('a')), currPos[0])
        formattedNewPos = (chr(newPos[1] + ord('a')), newPos[0])
        move.append(formattedCurrPos)
        move.append(formattedNewPos)
        tempList = list(self.boardRep[currPos[0]][currPos[1]])
        tempList[0] = "O" # updated for pritning on board
        self.totPathCost += int(tempList[1]) # update cumulative path cost
        # tempList[2] = True # update visited status
        self.boardRep[currPos[0]][currPos[1]] = tuple(tempList)
        piece.move(newPos)

    def visitSquare(self, currPos):
        self.numNodesExplored += 1 # increment numnodesExplored
        # print ("self.boardRep[currPos[0]][currPos[1]] = {}".format(self.boardRep[currPos[0]][currPos[1]]))
        # print(self.boardRep[currPos[0]][currPos[1]])
        temp = self.boardRep[currPos[0]][currPos[1]]
        tempList = list(temp)
        # print(type(tempList))
        tempList[2] = True # update visited status
        self.boardRep[currPos[0]][currPos[1]] = tuple(tempList)
        # print("{} has been visited".format(currPos))

    def splitCoordsAndEditBoardRep(self, str, sliceInd, tuplePos, isList, input):
        newList = re.split("(\d+)", str[sliceInd:].replace(" ", ""))
        # print(newList)

        for i in range (0, len(newList) - 1, 2):
            row = int(newList[i+1])
            # print("row = {}".format(row))
            col = ord(newList[i]) - ord("a")
            # print("col = {}".format(col))
            tempList = list(self.boardRep[row][col])
            if isList:
                tempList[tuplePos] = input[int(i/2)]
            else:
                tempList[tuplePos] = input
            self.boardRep[row][col] = tuple(tempList)

    def isValid (self, coord):
        if (coord[0] >= 0 and coord[0] < self.rows and
                coord[1] >= 0 and coord[1] < self.cols):
                if (self.boardRep[coord[0]][coord[1]][0] == " " or self.boardRep[coord[0]][coord[1]][0] == "G"):
                    return True
    
    def isGoal(self, coord):
        return (self.boardRep[coord[0]][coord[1]][0] == "G")

    def isVisited(self, coord):
        return self.boardRep[coord[0]][coord[1]][2]

    def isComplete(self):
        return self.puzzleComplete
    
    def setComplete(self):
        self.puzzleComplete = True


def search(state, posToSearch):

    # print("generating adjacency matrix")
    adjMat = state.genAdjMatrix(posToSearch)
    # print("adjMat = {}".format(adjMat))
        
    if not state.isVisited(adjMat[0]):
        print("{} has not been visited".format(adjMat[0]))
        state.visitSquare(adjMat[0])
        state.pred[adjMat[0][0]][adjMat[0][1]] = posToSearch
        state.queue.append(adjMat[0])

        if state.isGoal(adjMat[0]):
            print("goal is at {}".format(adjMat[0]))
            goalTile = adjMat[0]
            state.setComplete()
    
    if state.isComplete():    
        crawl = goalTile # this should be the goal tile
        while (state.pred[crawl[0]][crawl[1]] != -1):
            state.orderOfNodes.append(state.pred[crawl[0]][crawl[1]])
            state.movePiece(state.ally, crawl)
            print("crawl = {}".format(crawl))
            crawl = state.pred[crawl[0]][crawl[1]]

    return state.orderOfNodes, state.numNodesExplored


def pop(list):
    newList = []
    if len(list) > 0:
        for i in range (1, len(list)):
            newList.append(list[i])
    return newList


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_DFS():
    # You can code in here but you cannot remove this function or change the return type

    state = State(sys.argv[1])
    board = Board(state)

    print("state.ally.currPos = {}".format(state.ally.currPos))
    state.orderOfNodes, state.numNodesExplored = search(state, state.ally.currPos) #For reference
    state.orderOfNodes = state.orderOfNodes[::-1]
    path = []
    for i in range(len(state.orderOfNodes) - 1):
        srcDestPair = []
        print("state.orderOfNodes[i] = {}".format(state.orderOfNodes[i]))
        srcDestPair.append(tuple(state.orderOfNodes[i]))
        srcDestPair.append(tuple(state.orderOfNodes[i + 1]))
        path.append(srcDestPair)
    
    board.printBoard()
    # print("path = {}".format(path))
    return path, state.numNodesExplored # Format to be returned
    
if __name__ == "__main__":

    run_DFS()