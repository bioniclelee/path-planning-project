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
    def __init__(self, piecePos, moves, score):
        self.piecePos = piecePos
        self.moves = moves
        self.score = score
 
    def __lt__(self, other):
        return self.score < other.score
 
    def __le__(self, other):
        return self.score <= other.score
    
    def __str__(self):
        return str(self.piecePos)
 
def parseFile(file):
    global rows
    global cols
    global board
 
    with open(file) as f:
        lines = f.readlines()
    
    rows = int(lines[0].split(":")[1])
    cols = int(lines[1].split(":")[1])
    insertPieces(lines)
    
def insertPieces(state):

    if state.piecePos:
        print("true")
        state.piecePos[coordToStrIntTuple((4, 4))] = ('King', 'White')
        state.piecePos[coordToStrIntTuple((4, 3))] = ('Queen', 'White')
        state.piecePos[coordToStrIntTuple((4, 2))] = ('Knight', 'White')
        state.piecePos[coordToStrIntTuple((4, 1))] = ('Rook', 'White')
        for i in range(0, 5):
            state.piecePos[coordToStrIntTuple((3, i))] = ('Pawn', 'White')

        state.piecePos[coordToStrIntTuple((0, 4))] = ('King', 'White')
        state.piecePos[coordToStrIntTuple((0, 3))] = ('Queen', 'White')
        state.piecePos[coordToStrIntTuple((0, 2))] = ('Knight', 'White')
        state.piecePos[coordToStrIntTuple((0, 1))] = ('Rook', 'White')
        for i in range(0, 5):
            state.piecePos[coordToStrIntTuple((1, i))] = ('Pawn', 'White')
    else:
        print("false")

    # # enemy pieces
    # state.piecePos.append(("King", tuple(coordStrToInt("e4")), "White"))
    # state.piecePos.append(("Queen", tuple(coordStrToInt("d4")), "White"))
    # state.piecePos.append(("Bishop", tuple(coordStrToInt("c4")), "White"))
    # state.piecePos.append(("Knight", tuple(coordStrToInt("b4")), "White"))
    # state.piecePos.append(("Rook", tuple(coordStrToInt("a4")), "White"))
    # for i in range(0, 5):
    #     state.piecePos.append(("Pawn", tuple(coordStrToInt(intToAscii(i) + "3")), "White"))

    # # friendly pieces
    # state.piecePos.append(("King", tuple(coordStrToInt("e0")), "White"))
    # state.piecePos.append(("Queen", tuple(coordStrToInt("d0")), "White"))
    # state.piecePos.append(("Bishop", tuple(coordStrToInt("c0")), "White"))
    # state.piecePos.append(("Knight", tuple(coordStrToInt("b0")), "White"))
    # state.piecePos.append(("Rook", tuple(coordStrToInt("a0")), "White"))
    # for i in range(0, 5):
    #     state.piecePos.append(("Pawn", tuple(coordStrToInt(intToAscii(i) + "1")), "White"))
    
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

#Implement your minimax with alpha-beta pruning algorithm here.
def ab():
    initialState = State({}, {}, 0)
    insertPieces(initialState)
    print(initialState)


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, White (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'White'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    # config = sys.argv[1] #Takes in config.txt Optional

    move = (None, None)
    return move #Format to be returned (('a', 0), ('b', 3))

if __name__ == "__main__":
    ab()
