import sys
import re
import heapq as hq
from copy import deepcopy
 
rows = 0
cols = 0
board = []
queue = []
pieceList = []
numFree = 0
numPieces = 0
obstacleList = []
 
class State:
    def __init__(self, numFree, remPieces, piecesPlaced, threatenedSpaces):
        # self.board = board
        self.numFree = numFree
        self.remPieces = remPieces
        self.piecesPlaced = piecesPlaced
        self.threatenedSpaces = threatenedSpaces
 
    def __lt__(self, other):
        return self.numFree < other.numFree
 
    def __le__(self, other):
        return self.numFree <= other.numFree
    
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
    
    while l[0] > 0:
        pieceList.append("King")
        l[0] -= 1
 
    while l[1] > 0:
        pieceList.append("Queen")
        l[1] -= 1
    
    while l[2] > 0:
        pieceList.append("Bishop")
        l[2] -= 1
        
    while l[3] > 0:
        pieceList.append("Rook")
        l[3] -= 1
 
    while l[4] > 0:
        pieceList.append("Knight")
        l[4] -= 1
    
def enemyKingThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    for i in range (-1, 2):
        for j in range (-1, 2):
            if 0 <= row + i < rows and 0 <= col + j < cols and not isObstacle(rowColToCoord(row + i, col + j)):
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
    while 0 <= row - i < rows and not isObstacle(rowColToCoord(row - i, col)):
        threatList.append(tuple(rowColToCoord(row - i, col)))
        i += 1
    
    i = 1
    while 0 <= row + i < rows and not isObstacle(rowColToCoord(row + i, col)):
        threatList.append(tuple(rowColToCoord(row + i, col)))
        i += 1
 
    i = 1
    while 0 <= col - i < cols and not isObstacle(rowColToCoord(row, col - i)):
        threatList.append(tuple(rowColToCoord(row, col - i)))
        i += 1
 
    i = 1
    while 0 <= col + i < cols and not isObstacle(rowColToCoord(row, col + i)):
        threatList.append(tuple(rowColToCoord(row, col + i)))
        i += 1
    
    return threatList
 
def enemyBishopThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and 0 <= col - i < cols and not isObstacle(rowColToCoord(row - i, col - i)):
        threatList.append(tuple(rowColToCoord(row - i, col - i)))
        i += 1
 
    i = 1
    while 0 <= row - i < rows and 0 <= col + i < cols and not isObstacle(rowColToCoord(row - i, col + i)):
        threatList.append(tuple(rowColToCoord(row - i, col + i)))
        i += 1
 
    i = 1
    while 0 <= row + i < rows and 0 <= col - i < cols and not isObstacle(rowColToCoord(row + i, col - i)):
        threatList.append(tuple(rowColToCoord(row + i, col - i)))
        i += 1
 
    i = 1
    while 0 <= row + i < rows and 0 <= col + i < cols and not isObstacle(rowColToCoord(row + i, col + i)):
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
            if 0 <= newRow < rows and 0 <= newCol < cols and not isObstacle(rowColToCoord(newRow, newCol)):
                threatList.append(tuple(rowColToCoord(newRow, newCol)))
 
            # horizontal L-path
            newRow = row + coeff1 * 1
            newCol = col + coeff2 * 2
            if 0 <= newRow < rows and 0 <= newCol < cols and not isObstacle(rowColToCoord(newRow, newCol)):
                threatList.append(tuple(rowColToCoord(newRow,newCol)))
 
    return threatList
 
def insertObstacles(lines):
    global board
    global numFree
    global obstacleList
 
    numObstacles = int(lines[2].split(":")[1])
    obstacles = lines[3].split(":")[1].rstrip("\n").split(" ")
    for i in range(0, numObstacles):
        obstacleList.append(tuple(coordStrToInt(obstacles[i])))
    numFree = rows * cols - numObstacles
 
def coordStrToInt(str):
    coord = []
    newList = re.split("(\d+)", str)
    row = int(newList[1])
    col = asciiToInt(newList[0])
    coord.append(row)
    coord.append(col)
    return coord
 
def coordToStrIntTuple(coord):
    coord = list(coord)
    row = coord[0]
    col = coord[1]
    temp = []
    temp.append(intToAscii(col))
    temp.append(row)
    return tuple(temp)
 
def isComplete(stateToCheck):
    global numPieces
    return len(stateToCheck.piecesPlaced) == numPieces
 
def isObstacle(coord):
    global obstacleList
    return tuple(coord) in obstacleList
 
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
 
def isOccupied(coord, stateToCheck):
    global obstacleList
    threatenedSpacesSet = set(stateToCheck.threatenedSpaces)
    obstaclesSet = set(obstacleList)
    l = list(threatenedSpacesSet.union(obstaclesSet))
    return tuple(coord) in l
 
def threatenIfInserted(tempPiecesPlaced, threatList):
    for elem in tempPiecesPlaced:
        if tuple(elem[1]) in threatList:
            return True
    return False
 
def pushNextPiece(l):
    tempList = deepcopy(l)
    piece = tempList.pop(0)
    return piece, tempList
 
def placePiece(stateToExpand, piece, remPieces):
    global queue
    global obstacleList
 
    placementQueue = []
    hq.heapify(placementQueue)
    for i in range(0, rows):
        for j in range(0, cols):
            coord = []
            coord.append(i)
            coord.append(j)
 
            if not isOccupied(coord, stateToExpand):
                if piece == "King": 
                    threatList = enemyKingThreat(coord)
                if piece == "Queen":
                    threatList = enemyQueenThreat(coord)
                if piece == "Bishop":
                    threatList = enemyBishopThreat(coord)
                if piece == "Rook":
                    threatList = enemyRookThreat(coord)
                if piece == "Knight":
                    threatList = enemyKnightThreat(coord)
                threatList.append(tuple(coord))
 
                if not threatenIfInserted(stateToExpand.piecesPlaced, threatList):
                    tempPiecesPlaced = []
                    tempPiecesPlaced.append((piece, tuple(coord)))
                    tempPiecesPlaced.extend(stateToExpand.piecesPlaced)
                    threatList.extend(stateToExpand.threatenedSpaces)
                    tempThreatenedSpacesSet = set(threatList)
                    tempThreatenedSpaces = list(tempThreatenedSpacesSet)
 
                    updatedNumFree = rows * cols - len(tempThreatenedSpaces) - len(obstacleList)
 
                    tempState = State(updatedNumFree, remPieces, tempPiecesPlaced, tempThreatenedSpaces)
                    hq.heappush(placementQueue, (-1 * tempState.numFree, tempState))
    
    limit = 3
    if len(placementQueue) < limit:
        limit = len(placementQueue)
    for i in range(0, limit):
        score, tempState = hq.heappop(placementQueue)
        queue.insert(0, (-1 * score, tempState))
 
def search():
    global pieceList
    global numFree
 
    initialRemPieces = deepcopy(pieceList)
    initialState = State(numFree, initialRemPieces, [], [])
 
    nextPiece, updatedRemPieces = pushNextPiece(initialState.remPieces)
    placePiece(initialState, nextPiece, updatedRemPieces)
 
    counter = 0
    while queue:
        score, stateToExpand = queue.pop(0)
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
    
    finalState, counter = search()
    if finalState:
        for elem in finalState.piecesPlaced:
            pieceType, coord = elem
            dict[coordToStrIntTuple(coord)] = pieceType
    return dict
 
if __name__ == "__main__":
    run_CSP()