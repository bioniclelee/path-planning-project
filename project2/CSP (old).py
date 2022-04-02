import sys
import re
import heapq as hq
import math
import random
from copy import deepcopy
 
rows = 0
cols = 0
board = []
queue = []
pieceList = []
numFree = 0
numPieces = 0
numObstacles = 0
 
class State:
    def __init__(self, board, numFree, remPieces, piecesPlaced, threatenedSpaces):
        self.board = board
        self.numFree = numFree
        self.remPieces = remPieces
        self.piecesPlaced = piecesPlaced
        self.threatenedSpaces = threatenedSpaces

    def getScore(self):
        score = 0
        for i in range(0, rows):
            for j in range(0, cols):
                if self.board[i][j][0] == " ":
                    score += 1
        return score

    def __lt__(self, other):
        return self.getScore() < other.getScore()
 
    def __le__(self, other):
        return self.getScore() <= other.getScore()
    
    def __str__(self):
        return "Pieces remaining: " + str(self.pieceList) + "\n" + str(self.board)
 
def parseFile(file):
    global rows
    global cols
    global board
 
    with open(file) as f:
        lines = f.readlines()
    
    rows = int(lines[0].split(":")[1])
    cols = int(lines[1].split(":")[1])
    board = [[[" ",1, False] for j in range(cols)] 
                        for i in range(rows)] # board print, 1, explored status
    insertObstacles(lines)
    insertPieces(lines)
    
def insertPieces(lines):
    global board
    global pieceList
    global numPieces
    
    l = []
    for n in list((lines[4].rstrip("\n").split(":"))[1].split(" ")):
        l.append(int(n))
        numPieces += int(n)
    
    while l[1] > 0:
        # print("l[1] = {}".format(l[1]))
        pieceList.append("Queen")
        l[1] -= 1
    
    while l[2] > 0:
        # print("l[2] = {}".format(l[2]))
        pieceList.append("Bishop")
        l[2] -= 1
        
    while l[3] > 0:
        pieceList.append("Rook")
        l[3] -= 1

    while l[4] > 0:
        pieceList.append("Knight")
        l[4] -= 1
        
    while l[0] > 0:
        pieceList.append("King")
        l[0] -= 1
    
    # print("pieceList = {}".format(pieceList))
    
def enemyKingThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    for i in range (-1, 2):
        for j in range (-1, 2):
            if 0 <= row + i < rows and 0 <= col + j < cols:
                threatList.append(tuple(rowColToCoord(row + i, col + j)))
    threatList.remove(tuple(rowColToCoord(row, col)))
    return threatList
 
def enemyQueenThreat(pos):
    return enemyRookThreat(pos) + enemyBishopThreat(pos)
 
def enemyRookThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and board[row - i][col][0] != "X":
        threatList.append(tuple(rowColToCoord(row - i, col)))
        i += 1
    
    i = 1
    while 0 <= row + i < rows and board[row + i][col][0] != "X":
        threatList.append(tuple(rowColToCoord(row + i, col)))
        i += 1
 
    i = 1
    while 0 <= col - i < cols and board[row][col - i][0] != "X":
        threatList.append(tuple(rowColToCoord(row, col - i)))
        i += 1
 
    i = 1
    while 0 <= col + i < cols and board[row][col + i][0] != "X":
        threatList.append(tuple(rowColToCoord(row, col + i)))
        i += 1
    
    return threatList
 
def enemyBishopThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and 0 <= col - i < cols and board[row - i][col - i][0] != "X":
        threatList.append(tuple(rowColToCoord(row - i, col - i)))
        i += 1
 
    i = 1
    while 0 <= row - i < rows and 0 <= col + i < cols and board[row - i][col + i][0] != "X":
        threatList.append(tuple(rowColToCoord(row - i, col + i)))
        i += 1
 
    i = 1
    while 0 <= row + i < rows and 0 <= col - i < cols and board[row + i][col - i][0] != "X":
        threatList.append(tuple(rowColToCoord(row + i, col - i)))
        i += 1
 
    i = 1
    while 0 <= row + i < rows and 0 <= col + i < cols and board[row + i][col + i][0] != "X":
        threatList.append(tuple(rowColToCoord(row + i, col + i)))
        i += 1
    
    return threatList
 
def enemyKnightThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
 
    for i in range (0, 2):
        coeff1 = (-1) ** i
        
        for j in range (0, 2):
            # vertical L-path
            coeff2 = (-1) ** j
            newRow = row + coeff1 * 2
            newCol = col + coeff2 * 1
            if 0 <= newRow < rows and 0 <= newCol < cols and board[newRow][newCol][0] != "X":
                threatList.append(tuple(rowColToCoord(newRow, newCol)))
 
            # horizontal L-path
            newRow = row + coeff1 * 1
            newCol = col + coeff2 * 2
            if 0 <= newRow < rows and 0 <= newCol < cols and board[newRow][newCol][0] != "X":
                threatList.append(tuple(rowColToCoord(newRow,newCol)))
 
    return threatList
 
def insertObstacles(lines):
    global board
    global numFree
    global numObstacles

    numObstacles = int(lines[2].split(":")[1])
    obstacleList = lines[3].split(":")[1].rstrip("\n").split(" ")
    for i in range(0, numObstacles):
        coord = coordStrToInt(obstacleList[i])
        board[coord[0]][coord[1]][0] = "O"
    numFree = rows * cols - numObstacles
 
def removePiece(pos):
    global board
    board[pos[0]][pos[1]][0] = " "
 
def coordStrToInt(str):
    coord = []
    newList = re.split("(\d+)", str)
    row = int(newList[1])
    col = asciiToInt(newList[0])
    coord.append(row)
    coord.append(col)
    return coord
 
def coordToStrIntTuple(coord):
    row = coord[0]
    col = coord[1]
    temp = []
    temp.append(intToAscii(col))
    temp.append(row)
    return tuple(temp)
 
def printBoard(tempBoard):
    rowRef = 0
    boardRowsRep = []
    for i in range (0, 2 * rows + 2):
        boardColsRep = []
        if (i%2 == 0):    
            for j in range (0, 4 + cols * 4):
                boardColsRep.append("-")            
        elif (i % 2 == 1 and i != 2 * rows + 1):
            boardColsRep.append(rowRef)
            for k in range (0, len(str(rows)) + 1
                                - len(str(rowRef))):
                boardColsRep.append(" ")
            boardColsRep.append("|")
            for j in range (0, cols):
                boardColsRep.append(" ")
                boardColsRep.append(
                    tempBoard[int((i-1)/2)][j][0])
                boardColsRep.append(" ")
                boardColsRep.append("|")
            rowRef += 1
        else:
            for k in range (0, len(str(rows)) + 1):
                boardColsRep.append(" ")
            boardColsRep.append("|")
            alphabet = 97
            for j in range (0, cols):
                boardColsRep.append(" ")
                boardColsRep.append("{}".format(chr(alphabet)))
                boardColsRep.append(" ")
                boardColsRep.append("|")
                alphabet += 1
        boardRowsRep.append(boardColsRep)
    for i in range (0, len(boardRowsRep)):
        row = boardRowsRep[i]
        for j in range (0, len(row)):
            print(row[j], end = "")
        print("")
 
def cleanBoard(tempBoard):
    for i in range(0, rows):
        for j in range(0, cols):
            if tempBoard[i][j][0] == "X":
                tempBoard[i][j][0] = " "
    insertObstacles(getLines())

def isComplete(stateToCheck):
    global numPieces
    return len(stateToCheck.piecesPlaced) == numPieces
 
def isEmpty(tempBoard, coord):
    return (tempBoard[coord[0]][coord[1]][0] == " ")
 
def isObstacle(tempBoard, coord):
    return tempBoard[coord[0]][coord[1]][0] == "O"

def isThreatened(tempBoard, coord):
    return tempBoard[coord[0]][coord[1]][0] == "X"
 
def asciiToInt(c):
    return ord(c) - ord('a')
 
def intToAscii(n):
    return chr(n + ord('a'))
 
def rowColToCoord(row, col):
    coord = []
    coord.append(row)
    coord.append(col)
    return coord
 
def getLines():
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    return lines

def threatens(tempPiecesPlaced, threatList):
    for elem in tempPiecesPlaced:
        # print (elem[1])
        # print(threatList)
        if tuple(elem[1]) in threatList:
            # print("is threatened")
            return True
    
    return False

def pushNextPiece(l):
    tempList = deepcopy(l)
    piece = tempList.pop(0)
    return piece, tempList

def placePiece(stateToExpand, piece, remPieces):
    global queue
    global numObstacles
    # print("piece to be placed = {}".format(piece))

    placementQueue = []
    hq.heapify(placementQueue)
    for i in range(0, rows):
        for j in range(0, cols):

            tempBoard = deepcopy(stateToExpand.board)
            tempPiecesPlaced = deepcopy(stateToExpand.piecesPlaced)
            tempThreatenedSpaces = deepcopy(stateToExpand.threatenedSpaces)

            coord = []
            coord.append(i)
            coord.append(j)

            if isEmpty(tempBoard, coord):
                # print("placing {} at {},{}".format(piece,i,j))
                if piece == "King": 
                    enemyBoardInput = "K"
                    threatList = enemyKingThreat(coord)
                if piece == "Queen":
                    enemyBoardInput = "Q"
                    threatList = enemyQueenThreat(coord)
                if piece == "Bishop":
                    enemyBoardInput = "B"
                    threatList = enemyBishopThreat(coord)
                if piece == "Rook":
                    enemyBoardInput = "R"
                    threatList = enemyRookThreat(coord)
                if piece == "Knight":
                    enemyBoardInput = "H"
                    threatList = enemyKnightThreat(coord)
                
                if not threatens(tempPiecesPlaced, threatList):
                    # print('not threatens')
                    tempPiecesPlaced.append((piece, coord))
                    tempBoard[coord[0]][coord[1]][0] = enemyBoardInput
                    for coord in threatList:
                        if isEmpty(tempBoard, coord) or isThreatened(tempBoard, coord):
                            tempBoard[coord[0]][coord[1]][0] = "X"

                    tempThreatenedSpacesSet = set(tempThreatenedSpaces)
                    threatListSet = set(threatList)
                    tempThreatenedSpacesSet = tempThreatenedSpacesSet.union(threatListSet)
                    tempThreatenedSpaces = list(tempThreatenedSpacesSet)

                    updatedNumFree = rows * cols - len(tempThreatenedSpaces) - numObstacles

                    tempState = State(tempBoard, updatedNumFree, remPieces, tempPiecesPlaced, tempThreatenedSpaces)
                    # print("score of state = {} | piecesPlaced = {} | remPieces = {}".format(tempState.numFree, tempState.piecesPlaced, tempState.remPieces))
                    hq.heappush(placementQueue, (-1 * tempState.numFree, tempState))
    
    limit = 3
    if len(placementQueue) < limit:
        limit = len(placementQueue)
    for i in range(0, limit):
        score, tempState = hq.heappop(placementQueue)
        queue.insert(0, (-1 * score, tempState))

def search():
    global board
    global pieceList
    global numFree

    initialBoard = deepcopy(board)
    initialRemPieces = deepcopy(pieceList)
    initialState = State(initialBoard, numFree, initialRemPieces, [], [])

    nextPiece, updatedRemPieces = pushNextPiece(initialState.remPieces)
    placePiece(initialState, nextPiece, updatedRemPieces)

    counter = 0
    while queue:
        score, stateToExpand = queue.pop(0)
        # if len(stateToExpand.piecesPlaced) == 12:
        #     print("score of state = {} | piecesPlaced = {} | remPieces = {}".format(stateToExpand.numFree, stateToExpand.piecesPlaced, stateToExpand.remPieces))
        #     return stateToExpand, counter
        if isComplete(stateToExpand):
            return stateToExpand, counter
        if score > 0 and len(stateToExpand.remPieces) > 0 and score >= len(stateToExpand.remPieces):
            nextPiece, updatedRemPieces = pushNextPiece(stateToExpand.remPieces)
            placePiece(stateToExpand, nextPiece, updatedRemPieces)
        counter += 1

    return None, 0

def run_CSP():
    dict = {}
    parseFile(sys.argv[1])
    
    # print("before search:")
    # printBoard(board)
    
    finalState, counter = search()

    if finalState:
        for i in range(0, rows):
            for j in range(0, cols):
                entry = finalState.board[i][j][0]
                if entry != " " and entry != "X" and entry != "O":
                    if entry == "K": 
                        pieceType = "King"
                    if entry == "Q":
                        pieceType = "Queen"
                    if entry == "B":
                        pieceType = "Bishop"
                    if entry == "R":
                        pieceType = "Rook"
                    if entry == "H":
                        pieceType = "Knight"
                
                    coord = []
                    coord.append(i)
                    coord.append(j)
                    dict[coordToStrIntTuple(coord)] = pieceType

        # print("\nAfter search")
        # cleanBoard(finalState.board)
        # printBoard(finalState.board)
        # print("counter = {}".format(counter))
        # print("dict = {}".format(dict))
    
    return dict
 
if __name__ == "__main__":
    # print(run_local())
    run_CSP()