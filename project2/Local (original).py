import sys
import re
import heapq as hq
import math
 
rows = 0
cols = 0
k = 0
board = []
queue = []
piecePosList = []
pieceList = []
 
# class Piece:
 
#     pos = 0
#     type = None
#     threatList = None
 
#     def __init__(self, pos, type, threatList):
#         self.pos = pos
#         self.type = type
#         self.threatList = threatList  
 
 
def parseFile(file):
    global rows
    global cols
    global board
 
    with open(file) as f:
        lines = f.readlines()
    
    rows = int(lines[0].split(":")[1])
    cols = int(lines[1].split(":")[1])
    board = [[[" ", 1, False] for j in range(cols)] 
                        for i in range(rows)] # board print, path cost, visited status
    insertObstacles(lines)
    insertK(lines)
    insertPieces(lines)
 
def insertK(lines):
    global k
    k = int(lines[4].split(":")[1])
    
def insertPieces(lines):
    global board
    global piecePosList
    
    numPieces = 0
    for n in list((lines[5].rstrip("\n").split(":"))[1].split(" ")):
        numPieces += int(n)
 
    lineNum = 7
    while lineNum < len(lines):
        threatList = []
        # print(lineNum)
        # print("{} when lineNum = {}".format(lines[lineNum], lineNum))
        rawEntry = lines[lineNum].rstrip("\n").replace("[","").replace("]","").split(",")
        
        coord = coordStrToInt(rawEntry[1])
        piecePosList.append(coord)
        if rawEntry[0] == "King": 
            enemyBoardInput = "K"
            threatList = enemyKingThreat(coord)
        if rawEntry[0] == "Queen":
            enemyBoardInput = "Q"
            threatList = enemyQueenThreat(coord)
        if rawEntry[0] == "Bishop":
            enemyBoardInput = "B"
            threatList = enemyBishopThreat(coord)
        if rawEntry[0] == "Rook":
            enemyBoardInput = "R"
            threatList = enemyRookThreat(coord)
        if rawEntry[0] == "Knight":
            enemyBoardInput = "H"
            threatList = enemyKnightThreat(coord)
        board[coord[0]][coord[1]][0] = enemyBoardInput
        
        pieceList.append((rawEntry[0], coord, threatList))
 
        lineNum += 1
 
def enemyKingThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    for i in range (-1, 2):
        for j in range (-1, 2):
            if 0 <= row + i < rows and 0 <= col + j < cols:
                threatList.append(rowColToCoord(row + i, col + j))
    
    return threatList
 
def enemyQueenThreat(pos):
    return enemyRookThreat(pos) + enemyBishopThreat(pos)
 
def enemyRookThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and board[row - i][col][0] != "X":
        threatList.append(rowColToCoord(row - i, col))
        i += 1
    
    i = 1
    while 0 <= row + i < rows and board[row + i][col][0] != "X":
        threatList.append(rowColToCoord(row + i, col))
        i += 1
 
    i = 1
    while 0 <= col - i < cols and board[row][col - i][0] != "X":
        threatList.append(rowColToCoord(row, col - i))
        i += 1
 
    i = 1
    while 0 <= col + i < cols and board[row][col + i][0] != "X":
        threatList.append(rowColToCoord(row, col + i))
        i += 1
    
    return threatList
 
def enemyBishopThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and 0 <= col - i < cols and board[row - i][col - i][0] != "X":
        threatList.append(rowColToCoord(row - i, col - i))
        i += 1
 
    i = 1
    while 0 <= row - i < rows and 0 <= col + i < cols and board[row - i][col + i][0] != "X":
        threatList.append(rowColToCoord(row - i, col + i))
        i += 1
 
    i = 1
    while 0 <= row + i < rows and 0 <= col - i < cols and board[row + i][col - i][0] != "X":
        threatList.append(rowColToCoord(row + i, col - i))
        i += 1
 
    i = 1
    while 0 <= row + i < rows and 0 <= col + i < cols and board[row + i][col + i][0] != "X":
        threatList.append(rowColToCoord(row + i, col + i))
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
            if 0 <=  newRow < rows and 0 <= newCol < cols and board[newRow][newCol][0] != "X":
                threatList.append(rowColToCoord(newRow, newCol))
 
            # horizontal L-path
            newRow = row + coeff1 * 1
            newCol = col + coeff2 * 2
            if 0 <=  newRow < rows and 0 <= newCol < cols and board[newRow][newCol][0] != "X":
                threatList.append(rowColToCoord(newRow,newCol))
 
    return threatList
 
def insertObstacles(lines):
    global board
    numObstacles = int(lines[2].split(":")[1])
    obstacleList = lines[3].split(":")[1].rstrip("\n").split(" ")
    for i in range(0, numObstacles):
        coord = coordStrToInt(obstacleList[i])
        board[coord[0]][coord[1]][0] = "X"
 
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
 
# def printBoard(board):
#     rowRef = 0
#     boardRowsRep = []
#     for i in range (0, 2 * rows + 2):
#         boardColsRep = []
#         if (i%2 == 0):    
#             for j in range (0, 4 + cols * 4):
#                 boardColsRep.append("-")            
#         elif (i % 2 == 1 and i != 2 * rows + 1):
#             boardColsRep.append(rowRef)
#             for k in range (0, len(str(rows)) + 1
#                                 - len(str(rowRef))):
#                 boardColsRep.append(" ")
#             boardColsRep.append("|")
#             for j in range (0, cols):
#                 boardColsRep.append(" ")
#                 boardColsRep.append(
#                     board[int((i-1)/2)][j][0])
#                 boardColsRep.append(" ")
#                 boardColsRep.append("|")
#             rowRef += 1
#         else:
#             for k in range (0, len(str(rows)) + 1):
#                 boardColsRep.append(" ")
#             boardColsRep.append("|")
#             alphabet = 97
#             for j in range (0, cols):
#                 boardColsRep.append(" ")
#                 boardColsRep.append("{}".format(chr(alphabet)))
#                 boardColsRep.append(" ")
#                 boardColsRep.append("|")
#                 alphabet += 1
#         boardRowsRep.append(boardColsRep)
#     for i in range (0, len(boardRowsRep)):
#         row = boardRowsRep[i]
#         for j in range (0, len(row)):
#             print(row[j], end = "")
#         print("")
 
def isComplete():
    global queue
    global k
 
    if len(queue) == k:
        for elem in queue:
            if elem[0] != 0:
                return False
        return True
 
def isEmpty(coord):
    return (board[coord[0]][coord[1]][0] == " ")
 
def isObstacle(coord):
    return (board[coord[0]][coord[1]][0] == "X")
 
def asciiToInt(c):
    return ord(c) - ord('a')
 
def intToAscii(n):
    return chr(n + ord('a'))
 
def rowColToCoord(row, col):
    coord = []
    coord.append(row)
    coord.append(col)
    return coord
 
def getScore(posList, threatList):
    # print("score = {}".format(len([x for x in threatList if x in posList and x in threatList])))
    return len([x for x in threatList if x in posList and x in threatList])
 
def listMatch(l1, l2):
    return not [x for x in l1 + l2 if x not in l1 or x not in l2]
 
def getLines():
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    return lines
 
def search():
    global queue
    global k
    global board
 
    tempPieceList = []
    tempPiecePosList = []
 
    for i in range(0, len(pieceList)):
        tempPieceList.append(pieceList[i])
        tempPiecePosList.append(piecePosList[i])
 
    # set to -1 to let a normal heapq iteration run first
    counter = -1
 
    for i in range(0, len(pieceList)):
        pieceType, piecePos, pieceThreatList = pieceList[i]
        # print("piecePosList = {}".format(piecePosList))
        # print("pieceThreatList[i] = {}".format(pieceThreatList[i]))
        # print("pieceTypeList[i] = {}".format(pieceTypeList[i]))
        hq.heappush(queue, (-1 * getScore(piecePosList, pieceThreatList), pieceType, piecePos))
 
    while not isComplete():
 
        # print("normal heapq run")
 
        # print("length of queue = {}".format(len(queue)))
        # print("length of pieceList = {}".format(len(pieceList)))
 
        if len(queue) == k:
            # for elem in queue:
                # print("score for {} = {}".format(elem[1], elem[0]))
            # print("entering remove")
            counter += 1
            # print("counter = {}".format(counter))
            
            tempPieceList = []
            tempPiecePosList = []
            for i in range(0, len(pieceList)):
                tempPieceList.append(pieceList[i])
                tempPiecePosList.append(piecePosList[i])
 
            if -1 < counter < len(pieceList):
                # print("tempPieceList[{}] = {}".format(counter, tempPieceList[counter]))
                del tempPieceList[counter]
                del tempPiecePosList[counter]
                
            queue = []
            for j in range(0, len(tempPieceList)):
                pieceType, piecePos, pieceThreatList = tempPieceList[j]
                hq.heappush(queue, (-1 * getScore(tempPiecePosList, pieceThreatList), pieceType, piecePos))
            
            # print("length of queue in remove = {}".format(len(queue)))
 
        pieceScore, pieceType, piecePos = hq.heappop(queue)
        # print("{} at {} with score {} is removed".format(pieceType, piecePos, pieceScore))
        removePiece(piecePos)
 
        h = 0
        for elem in tempPieceList:
            if piecePos == elem[1]:
                break
            h += 1
        # print("h = {}".format(h))
        del tempPieceList[h]
        del tempPiecePosList[h]
 
        queue = []
 
        for i in range(0, len(tempPieceList)):
            # print("piecePosList = {}".format(piecePosList))
            # print("pieceThreatList = {}".format(pieceThreatList))
            # print("pieceType = {}".format(pieceType))
            pieceType, piecePos, pieceThreatList = tempPieceList[i]
            hq.heappush(queue, (-1 * getScore(tempPiecePosList, pieceThreatList), pieceType, piecePos))
            if (pieceType == "Knight"):
                pieceRepr = "H"
            else:
                pieceRepr = pieceType[0]
            board[piecePos[0]][piecePos[1]][0] = pieceRepr
 
        if counter == len(piecePosList) -1 and len(queue) == k and not isComplete():
            # print("length of queue = {}".format(len(queue)))
            return None
    return queue
 
def run_local():
    dict = {}
 
    parseFile(sys.argv[1])
    
    if search() != None:
        while queue:
            pieceScore, pieceType, piecePos = hq.heappop(queue)
            # print("{} at {} with score {} remains".format(pieceType, piecePos, pieceScore))
            coordString = coordToStrIntTuple(piecePos)
            newCoord = []
            newCoord.append(coordString[0])
            newCoord.append(int(coordString[1]))
            dict[tuple(newCoord)] = pieceType
    
    # printBoard(board)
    # print(dict)
    
    return dict
 
if __name__ == "__main__":
    run_local()