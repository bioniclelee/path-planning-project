import sys
import random
import math


# Helper functions to aid in your implementation. Can edit/remove


class Piece:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def canMove(self, targetPos, friendlyPos, enemyPos):
        if (targetPos in friendlyPos):
            return False
        return True

    # Pass row e.g. 'a', and col e.g. '11' and obstacles set and return list of possible new positions
    def getMoves(self, row, col, obstacles):
        pass

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        if other == None:
            return False
        return self.pos == other.pos

    def __repr__(self):
        return self.pos

    def getRow(self, pos):
        return int(pos[1:])

    def getCol(self, pos):
        return ord(pos[0]) - 97

    def convertToPos(self, row, col):
        newCol = chr(col + 97)
        newRow = str(row)
        return newCol + newRow

    def convertPosToNums(self, pos):
        return (self.getRow(pos), self.getCol(pos))

    def getScore(self):
        return 0


class King(Piece):
    def canMove(self, targetPos, friendlyPos, enemyPos):
        if (not super().canMove(targetPos, friendlyPos, None)):
            return False
        row = super().getRow(self.pos)
        col = super().getCol(self.pos)
        (newRow, newCol) = super().convertPosToNums(targetPos)
        return abs(row - newRow) <= 1 and abs(col - newCol) <= 1

    def getMoves(self, row, col, friendlyPos, enemyPos):
        currRow = super().getRow(self.pos)
        currCol = super().getCol(self.pos)
        maxRow = row - 1
        maxCol = col - 1
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1),
                      (1, 0), (-1, 0), (0, 1), (0, -1)]
        moves = []
        for d in directions:
            newRow = currRow + d[0]
            newCol = currCol + d[1]
            if (newRow > maxRow or newCol > maxCol or newRow < 0 or newCol < 0):
                continue
            newPos = super().convertToPos(newRow, newCol)
            if (newPos in friendlyPos):
                continue
            moves.append(newPos)
        return moves


class Bishop(Piece):
    def canMove(self, targetPos, friendlyPos, enemyPos):
        if (not super().canMove(targetPos, friendlyPos, None)):
            return False
        row = super().getRow(self.pos)
        col = super().getCol(self.pos)
        (newRow, newCol) = super().convertPosToNums(targetPos)
        if abs(row - newRow) != (col - newCol):
            return False
        rowDiff = newRow - row
        colDiff = newCol - col
        rowDir = 1
        if rowDiff < 0:
            rowDir = -1
        colDir = 1
        if colDiff < 0:
            colDir = -1
        while row + rowDir != newRow and col + colDir != newCol:
            newPos = super().convertToPos(row, col)
            if newPos in friendlyPos:
                return False
            if newPos in enemyPos:
                return False
            row += rowDir
            col += colDir
        return True

    def getMoves(self, row, col, friendlyPos, enemyPos):
        currRow = super().getRow(self.pos)
        currCol = super().getCol(self.pos)
        maxRow = row - 1
        maxCol = col - 1
        moves = []
        while (currRow - 1 >= 0 and currCol - 1 >= 0):
            currRow -= 1
            currCol -= 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)

        currRow = super().getRow(self.pos)
        currCol = super().getCol(self.pos)
        while (currRow - 1 >= 0 and currCol + 1 <= maxCol):
            currRow -= 1
            currCol += 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)

        currRow = super().getRow(self.pos)
        currCol = super().getCol(self.pos)
        while (currRow + 1 <= maxRow and currCol - 1 >= 0):
            currRow += 1
            currCol -= 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)

        currRow = super().getRow(self.pos)
        currCol = super().getCol(self.pos)
        while (currRow + 1 <= maxRow and currCol + 1 <= maxCol):
            currRow += 1
            currCol += 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)

        return moves

    def getScore(self):
        return 3


class Rook(Piece):
    def canMove(self, targetPos, friendlyPos, enemyPos):
        if (not super().canMove(targetPos, friendlyPos, None)):
            return False
        currRow = super().getRow(self.pos)
        currCol = super().getCol(self.pos)
        (targetRow, targetCol) = super().convertPosToNums(targetPos)
        rowDiff = targetRow - currRow
        colDiff = targetCol - currCol
        if (rowDiff != 0 and colDiff != 0):
            return False
        rowDir = 0
        if rowDiff > 0:
            rowDir = 1
        elif rowDiff < 0:
            rowDir = -1
        colDir = 0
        if colDir > 0:
            colDir = 1
        elif colDir < 0:
            colDir = -1
        while (currRow + rowDir != targetRow or currCol + colDir != targetCol):
            currPos = super().convertToPos(currRow, currCol)
            if currPos in friendlyPos:
                return False
            if currPos in enemyPos:
                return False
            currRow += rowDir
            currCol += colDir
        return True

    def getMoves(self, row, col, friendlyPos, enemyPos):
        maxRow = row - 1
        maxCol = col - 1
        (currRow, currCol) = super().convertPosToNums(self.pos)
        moves = []
        while (currRow + 1 <= maxRow):
            currRow += 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)
        (currRow, currCol) = super().convertPosToNums(self.pos)
        while (currRow - 1 >= 0):
            currRow -= 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)
        (currRow, currCol) = super().convertPosToNums(self.pos)
        while (currCol + 1 <= maxCol):
            currCol += 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)
        (currRow, currCol) = super().convertPosToNums(self.pos)
        while (currCol - 1 >= 0):
            currCol -= 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)
        return moves

    def getScore(self):
        return 5


class Queen(Piece):
    def canMove(self, targetPos, friendlyPos, enemyPos):
        if (not super().canMove(targetPos, friendlyPos, None)):
            return False
        (newRow, newCol) = super().convertPosToNums(targetPos)
        (currRow, currCol) = super().convertPosToNums(self.pos)
        rowDiff = newRow - currRow
        colDiff = newCol - currCol
        if abs(rowDiff) != abs(colDiff) and rowDiff != 0 and colDiff != 0:
            return False
        rowDir = 0
        if rowDiff > 0:
            rowDir = 1
        elif rowDiff < 0:
            rowDir = -1
        colDir = 0
        if colDiff > 0:
            colDir = 1
        elif colDiff < 0:
            colDir = -1
        while currRow + rowDir != newRow or currCol + colDir != newCol:
            currPos = super().convertToPos(currRow, currCol)
            if currPos in friendlyPos:
                return False
            if currPos in enemyPos:
                return False
            currRow += rowDir
            currCol += colDir
        return True

    def getMoves(self, row, col, friendlyPos, enemyPos):
        maxRow = row - 1
        maxCol = col - 1
        (currRow, currCol) = super().convertPosToNums(self.pos)
        moves = []
        while currRow + 1 <= maxRow:
            currRow += 1
            newPos = super().convertToPos(currRow, currCol)
            if newPos in friendlyPos:
                break
            if newPos in enemyPos:
                moves.append(newPos)
                break
            moves.append(newPos)
        (currRow, currCol) = super().convertPosToNums(self.pos)
        while currRow - 1 >= 0:
            currRow -= 1
            newPos = super().convertToPos(currRow, currCol)
            if newPos in friendlyPos:
                break
            if newPos in enemyPos:
                moves.append(newPos)
                break
            moves.append(newPos)
        (currRow, currCol) = super().convertPosToNums(self.pos)
        while currCol + 1 <= maxCol:
            currCol += 1
            newPos = super().convertToPos(currRow, currCol)
            if newPos in friendlyPos:
                break
            if newPos in enemyPos:
                moves.append(newPos)
                break
            moves.append(newPos)
        (currRow, currCol) = super().convertPosToNums(self.pos)
        while (currCol - 1 >= 0):
            currCol -= 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)

        (currRow, currCol) = super().convertPosToNums(self.pos)
        while (currRow + 1 <= maxRow and currCol + 1 <= maxCol):
            currRow += 1
            currCol += 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)
        (currRow, currCol) = super().convertPosToNums(self.pos)
        while (currRow - 1 >= 0 and currCol + 1 <= maxCol):
            currRow -= 1
            currCol += 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)
        (currRow, currCol) = super().convertPosToNums(self.pos)
        while (currRow - 1 >= 0 and currCol - 1 >= 0):
            currRow -= 1
            currCol -= 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)
        (currRow, currCol) = super().convertPosToNums(self.pos)
        while (currRow + 1 <= maxRow and currCol - 1 >= 0):
            currRow += 1
            currCol -= 1
            newPos = super().convertToPos(currRow, currCol)
            if (newPos in friendlyPos):
                break
            if (newPos in enemyPos):
                moves.append(newPos)
                break
            moves.append(newPos)
        return moves

    def getScore(self):
        return 9


class Knight(Piece):
    def canMove(self, targetPos, friendlyPos, enemyPos):
        if not super().canMove(targetPos, friendlyPos, None):
            return False
        (currRow, currCol) = super().convertPosToNums(self.pos)
        (newRow, newCol) = super().convertPosToNums(targetPos)
        return (abs(currRow - newRow) == 2 and abs(currCol - newCol) == 1) or (
            abs(currRow - newRow) == 1 and abs(currCol - newCol) == 2)

    def getMoves(self, row, col, friendlyPos, enemyPos):
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                      (1, 2), (1, -2), (-1, 2), (-1, -2)]
        (currRow, currCol) = super().convertPosToNums(self.pos)
        maxRow = row - 1
        maxCol = col - 1
        moves = []
        for d in directions:
            newRow = currRow + d[0]
            newCol = currCol + d[1]
            if newRow < 0 or newRow > maxRow or newCol < 0 or newCol > maxCol:
                continue
            newPos = super().convertToPos(newRow, newCol)
            if newPos in friendlyPos:
                continue
            moves.append(newPos)
        return moves

    def getScore(self):
        return 3


class Pawn(Piece):
    def canMove(self, targetPos, friendlyPos, enemyPos):
        movesSet = set(self.getMoves(5, 5, friendlyPos, enemyPos))
        return targetPos in movesSet

    def getMoves(self, row, col, friendlyPos, enemyPos):
        (currRow, currCol) = super().convertPosToNums(self.pos)
        if self.color == 'White':
            diff = 1
        else:
            diff = -1
        newRow = currRow + diff

        newPos = super().convertToPos(newRow, currCol)
        if newRow >= row or newRow < 0:
            return []
        if newPos in friendlyPos or newPos in enemyPos:
            newPos = None
        moves = []
        if newPos is not None:
            moves.append(newPos)

        newCol = currCol + 1
        newPos = super().convertToPos(newRow, newCol)
        if newCol >= col or newCol < 0:
            newPos = None
        if newRow >= row or newRow < 0:
            newPos = None
        if newPos not in enemyPos:
            newPos = None
        if newPos is not None:
            moves.append(newPos)

        newCol = currCol - 1
        newPos = super().convertToPos(newRow, newCol)
        if newCol >= col or newCol < 0:
            newPos = None
        if newPos not in enemyPos:
            newPos = None
        if newPos is not None:
            moves.append(newPos)
        return moves

    def getScore(self):
        return 1


class State:
    def __init__(self, friendlyPieces, enemyPieces, friendlyPos, enemyPos):
        self.friendlyPieces = friendlyPieces
        self.enemyPieces = enemyPieces
        self.friendlyPos = friendlyPos
        self.enemyPos = enemyPos
        self.currColor = 'White'

    def swapColor(self):
        if self.currColor == 'White':
            self.currColor = 'Black'
        else:
            self.currColor = 'White'

    def __repr__(self):
        matrix = []
        for i in range(5):
            r = []
            for j in range(5):
                r.append(" ")
            matrix.append(r)

        for pos in self.friendlyPos:
            piece = self.friendlyPieces[pos]
            if isinstance(piece, King):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u265A"
            elif isinstance(piece, Queen):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u265B"
            elif isinstance(piece, Rook):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u265C"
            elif isinstance(piece, Bishop):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u265D"
            elif isinstance(piece, Knight):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u265E"
            elif isinstance(piece, Pawn):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u265F"

        for pos in self.enemyPos:
            piece = self.enemyPieces[pos]
            if isinstance(piece, King):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u2654"
            elif isinstance(piece, Queen):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u2655"
            elif isinstance(piece, Rook):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u2656"
            elif isinstance(piece, Bishop):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u2657"
            elif isinstance(piece, Knight):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u2658"
            elif isinstance(piece, Pawn):
                (rw, cl) = piece.convertPosToNums(piece.pos)
                matrix[rw][cl] = "\u2659"

        result = ""
        for i in matrix:
            result += str(i) + "\n"
        return result


# heuristics

def mobility(state):
    numActs = len(getActions(state))
    if state.currColor == 'White':
        return numActs
    return -numActs


def material(state):
    score = 0
    for p in state.friendlyPieces.values():
        score += p.getScore()
    for p in state.enemyPieces.values():
        score -= p.getScore()
    return score


# Implement your minimax with alpha-beta pruning algorithm here.


def getActions(state):
    actions = []
    if state.currColor == 'White':
        piecesToCheckFor = state.friendlyPieces
        friendlyPos = state.friendlyPos
        enemyPos = state.enemyPos
    else:
        piecesToCheckFor = state.enemyPieces
        friendlyPos = state.enemyPos
        enemyPos = state.friendlyPos
    for piecePos in piecesToCheckFor:
        piece = piecesToCheckFor[piecePos]
        moves = piece.getMoves(5, 5, friendlyPos, enemyPos)
        for move in moves:
            actions.append((piecePos, move))
    return actions


def transitionModel(state, action):
    originalPos = action[0]
    assert originalPos in state.friendlyPos or originalPos in state.enemyPos, 'Piece og pos not found in either pos sets'
    if originalPos in state.friendlyPos:
        friendlyPieces = state.friendlyPieces
        friendlyPos = state.friendlyPos
        enemyPieces = state.enemyPieces
        enemyPos = state.enemyPos
    else:
        friendlyPieces = state.enemyPieces
        friendlyPos = state.enemyPos
        enemyPieces = state.friendlyPieces
        enemyPos = state.friendlyPos
    newPos = action[1]
    pieceToUpdate = friendlyPieces.pop(originalPos)
    pieceToUpdate.pos = newPos
    friendlyPieces[newPos] = pieceToUpdate
    friendlyPos.remove(originalPos)
    friendlyPos.add(newPos)
    state.swapColor()

    if newPos not in enemyPos:
        return None

    eatenPiece = enemyPieces[newPos]
    enemyPieces.pop(newPos)
    enemyPos.remove(newPos)
    return eatenPiece


def reverseTransitionModel(state, action, capturedPiece):
    transitionModel(state, (action[1], action[0]))
    if capturedPiece == None:
        return
    originalPos = action[0]
    if originalPos in state.friendlyPos:
        enemyPieces = state.enemyPieces
        enemyPos = state.enemyPos
    else:
        enemyPieces = state.friendlyPieces
        enemyPos = state.friendlyPos
    enemyPiecePos = capturedPiece.pos
    enemyPieces[enemyPiecePos] = capturedPiece
    enemyPos.add(enemyPiecePos)


def eval(state):
    hadKing = False
    for piecePos in state.enemyPieces:
        piece = state.enemyPieces[piecePos]
        if piece.__class__.__name__ == 'King':
            hadKing = True
    if not hadKing:
        return math.inf

    hadKing = False
    for piecePos in state.friendlyPieces:
        piece = state.friendlyPieces[piecePos]
        if piece.__class__.__name__ == 'King':
            hadKing = True
    if not hadKing:
        return -math.inf
    return mobility(state) + material(state)


def containsKing(pieces):
    for pos in pieces:
        piece = pieces[pos]
        if piece.__class__.__name__ == 'King':
            return True
    return False


def isCutOff(state, d):
    if not (containsKing(state.enemyPieces) and containsKing(state.friendlyPieces)):
        return True

    return d >= 3


def getFinishMove(state):
    actions = getActions(state)
    if state.currColor == 'White':
        enemyPieces = state.enemyPieces
    else:
        enemyPieces = state.friendlyPieces
    for p in enemyPieces.values():
        if isinstance(p, King):
            enemyKingPos = p.pos
            break

    for a in actions:
        if a[1] == enemyKingPos:
            return a
    return None


def minVal(state, alpha, beta, d, cutOffFunc, evalFunc):
    if cutOffFunc(state, d):
        return evalFunc(state), None
    finishMove = getFinishMove(state)
    if finishMove:
        return -math.inf, finishMove
    newBeta = math.inf
    actions = getActions(state)
    resultMove = None
    for action in actions:
        capturedPiece = transitionModel(state, action)
        possibleBeta, possibleMove = maxVal(
            state, alpha, beta, d + 1, cutOffFunc, evalFunc)
        reverseTransitionModel(state, action, capturedPiece)
        if possibleBeta < newBeta:
            newBeta = possibleBeta
            resultMove = action
            beta = min(beta, newBeta)
        if newBeta <= alpha:
            return newBeta, resultMove
    return newBeta, resultMove


def maxVal(state, alpha, beta, d, cutOffFunc, evalFunc):
    if cutOffFunc(state, d):
        return evalFunc(state), None
    finishMove = getFinishMove(state)
    if finishMove:
        return math.inf, finishMove
    newAlpha = -math.inf
    actions = getActions(state)
    resultMove = None
    for action in actions:
        capturedPiece = transitionModel(state, action)
        possibleAlpha, possibleMove = minVal(
            state, alpha, beta, d + 1, cutOffFunc, evalFunc)
        reverseTransitionModel(state, action, capturedPiece)
        if possibleAlpha > newAlpha:
            newAlpha = possibleAlpha
            resultMove = action
            beta = max(beta, newAlpha)
        if newAlpha >= beta:
            return newAlpha, resultMove
    return newAlpha, resultMove


def ab(state):
    alpha, move = maxVal(state, -math.inf, math.inf, 0, isCutOff, eval)
    return convertMoveToOutput(move)


def enemyAb(state, cutOff, evalFunc):
    beta, move = minValEnemy(state, -math.inf, math.inf, 0, cutOff, evalFunc)
    return convertMoveToOutput(move)


def convertMoveToOutput(move):
    if move is None:
        return None
    firstPos = move[0]
    nextPos = move[1]
    return (firstPos[0], int(firstPos[1:])), (nextPos[0], int(nextPos[1:]))
    ### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
    # Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
    # Colours: White, Black (First Letter capitalized)
    # Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

    # Parameters:
    # gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
    # Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
    # Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
    # gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
    #
    # Return value:
    # move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
    # move example: (('a', 0), ('b', 3))


def greedyCutOff(state, d):
    if not (containsKing(state.enemyPieces) and containsKing(state.friendlyPieces)):
        return True
    return d >= 3


def greedyEval(state):
    hadKing = False
    for piecePos in state.enemyPieces:
        piece = state.enemyPieces[piecePos]
        if piece.__class__.__name__ == 'King':
            hadKing = True
    if not hadKing:
        return math.inf

    hadKing = False
    for piecePos in state.friendlyPieces:
        piece = state.friendlyPieces[piecePos]
        if piece.__class__.__name__ == 'King':
            hadKing = True
    if not hadKing:
        return -math.inf
    return 0


def greedy(board):
    state = createInitState(board, 'Black')
    if not containsKing(state.enemyPieces):
        return None
    (canCheckMate, move) = getCheckmateMove(state)
    if canCheckMate:
        return convertMoveToOutput(move)
    state.currColor = 'Black'
    actions = getActions(state)
    nonCheckedActions = []
    for a in actions:
        capturedPiece = transitionModel(state, a)
        if isinstance(capturedPiece, King):
            return convertMoveToOutput(a)
        if not isChecked(state):
            nonCheckedActions.append(a)
        reverseTransitionModel(state, a, capturedPiece)
    if not nonCheckedActions:
        return None
    return convertMoveToOutput(random.choice(nonCheckedActions))


def isChecked(state):
    if state.currColor == 'White':
        friendlyPieces = state.friendlyPieces
        friendlyPos = state.friendlyPos
        enemyPos = state.enemyPos
        for p in state.enemyPieces.values():
            if isinstance(p, King):
                enemyKingPos = p.pos
                break

    elif state.currColor == 'Black':
        friendlyPieces = state.enemyPieces
        friendlyPos = state.enemyPos
        enemyPos = state.friendlyPos
        for p in state.friendlyPieces.values():
            if isinstance(p, King):
                enemyKingPos = p.pos
                break

    for p in friendlyPieces.values():
        if p.canMove(enemyKingPos, friendlyPos, enemyPos):
            return True
    return False


def checkmateCutOff(state, d):
    if not (containsKing(state.enemyPieces) and containsKing(state.friendlyPieces)):
        return True
    return d >= 3


def checkmateEval(state):
    hadKing = False
    for piecePos in state.enemyPieces:
        piece = state.enemyPieces[piecePos]
        if piece.__class__.__name__ == 'King':
            hadKing = True
    if not hadKing:
        return math.inf

    hadKing = False
    for piecePos in state.friendlyPieces:
        piece = state.friendlyPieces[piecePos]
        if piece.__class__.__name__ == 'King':
            hadKing = True
    if not hadKing:
        return -math.inf
    return 0


def getCheckmateMove(state):
    if state.currColor == 'White':
        alpha, move = maxVal(state, -math.inf, math.inf, 0,
                             checkmateCutOff, checkmateEval)
        if alpha == math.inf:
            return True, move
        else:
            return False, None
    elif state.currColor == 'Black':
        beta, move = minVal(state, -math.inf, math.inf, 0,
                            checkmateCutOff, checkmateEval)
        if beta == -math.inf:
            return True, move
        else:
            return False, None


def smartEval(state, action):
    isWhite = state.currColor == 'White'
    factor = 1
    friendlyPieces = state.friendlyPieces
    enemyPieces = state.enemyPieces
    if not isWhite:
        factor = -1
        friendlyPieces = state.enemyPieces
        enemyPieces = state.friendlyPieces
    capturedPiece = transitionModel(state, action)
    movedPiece = friendlyPieces[action[1]]
    for enemyPiece in enemyPieces.values():
        if isinstance(enemyPiece, King):
            enemyKingPos = enemyPiece.pos
            break
    isChecking = movedPiece.canMove(
        enemyKingPos, friendlyPieces.keys(), enemyPieces.keys())
    reverseTransitionModel(state, action, capturedPiece)
    if isinstance(capturedPiece, King):
        return factor * math.inf
    if capturedPiece:
        capturedScore = capturedPiece.getScore()
    if isChecking and capturedPiece:
        return factor * (10 + capturedScore)
    if capturedPiece:
        return factor * capturedScore
    if isChecking:
        return 0
    return -1 * factor * math.inf


def minValEnemy(state, alpha, beta, d, cutOffFunc, evalFunc):
    finishMove = getFinishMove(state)
    if finishMove:
        return -math.inf, finishMove
    newBeta = math.inf
    actions = getActions(state)
    resultMove = None
    for action in actions:
        if cutOffFunc(state, d + 1):
            return smartEval(state, action), action
        capturedPiece = transitionModel(state, action)
        possibleBeta, possibleMove = maxValEnemy(
            state, alpha, beta, d + 1, cutOffFunc, evalFunc)
        reverseTransitionModel(state, action, capturedPiece)
        if possibleBeta < newBeta:
            newBeta = possibleBeta
            resultMove = action
            beta = min(beta, newBeta)
        if newBeta <= alpha:
            return newBeta, resultMove
    return newBeta, resultMove


def maxValEnemy(state, alpha, beta, d, cutOffFunc, evalFunc):
    finishMove = getFinishMove(state)
    if finishMove:
        return math.inf, finishMove
    newAlpha = -math.inf
    actions = getActions(state)
    resultMove = None
    for action in actions:
        if cutOffFunc(state, d + 1):
            return smartEval(state, action), action
        capturedPiece = transitionModel(state, action)
        possibleAlpha, possibleMove = minValEnemy(
            state, alpha, beta, d + 1, cutOffFunc, evalFunc)
        reverseTransitionModel(state, action, capturedPiece)
        if possibleAlpha > newAlpha:
            newAlpha = possibleAlpha
            resultMove = action
            beta = max(beta, newAlpha)
        if newAlpha >= beta:
            return newAlpha, resultMove
    return newAlpha, resultMove


def smart(state):
    finishMove = getFinishMove(state)
    if finishMove:
        return finishMove
    isCheckMateMove, move = getCheckmateMove(state, 'Black')
    if isCheckMateMove:
        return move
    actions = getActions(state, 'Black')
    minEval = math.inf
    chosenMove = None
    for a in actions:
        evalVal = smartEval(state, a)
        if evalVal < minEval:
            minEval = evalVal
            chosenMove = a
    return chosenMove


def minimaxCutOff(state, d):
    if not (containsKing(state.enemyPieces) and containsKing(state.friendlyPieces)):
        return True
    return d >= 4


def minimaxAgent(board):
    initState = createInitState(board, 'Black')
    print(initState)
    move = enemyAb(initState, minimaxCutOff, smartEval)
    return move


def studentAgent(board):
    initState = createInitState(board, 'White')
    move = ab(initState)
    return move  # Format to be returned (('a', 0), ('b', 3))


def createInitState(gameboard, color):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    enemyPos = set()
    friendlyPos = set()
    enemyPieces = {}
    friendlyPieces = {}
    for posKey in gameboard:
        pieceInfo = gameboard[posKey]
        pieceType = pieceInfo[0]
        pieceColor = pieceInfo[1]
        if pieceColor == 'White':
            piecesDict = friendlyPieces
            posSet = friendlyPos
        else:
            piecesDict = enemyPieces
            posSet = enemyPos
        newPos = posKey[0] + str(posKey[1])
        if pieceType == 'Queen':
            newPiece = Queen(newPos, pieceColor)
        elif pieceType == 'Bishop':
            newPiece = Bishop(newPos, pieceColor)
        elif pieceType == 'Rook':
            newPiece = Rook(newPos, pieceColor)
        elif pieceType == 'Knight':
            newPiece = Knight(newPos, pieceColor)
        elif pieceType == 'Pawn':
            newPiece = Pawn(newPos, pieceColor)
        else:
            newPiece = King(newPos, pieceColor)
        piecesDict[newPos] = newPiece
        posSet.add(newPos)
    initState = State(friendlyPieces, enemyPieces, friendlyPos, enemyPos)
    if color == 'Black':
        initState.swapColor()
    return initState


# board = {('a', 0): ('Pawn', 'White'), ('d', 1): (
#    'Knight', 'Black'), ('e', 4): ('Rook', 'White'), ('a', 1): ('King', 'White'), ('b', 4): ('King', 'Black')}
# while True:
#    newMove = studentAgent(board)
#    if newMove is None:
#        break
#    pieceInfo = board.pop(newMove[0])
#    board[newMove[1]] = pieceInfo

board = {('a', 1): ('Pawn', 'White'), ('b', 1): ('Pawn', 'White'), ('c', 1): ('Pawn', 'White'),
         ('d', 1): ('Pawn', 'White'), ('e', 1): ('Pawn', 'White'), ('a', 3): ('Pawn', 'Black'),
         ('b', 3): ('Pawn', 'Black'), ('c', 3): ('Pawn', 'Black'), ('d', 3): ('Pawn', 'Black'),
         ('e', 3): ('Pawn', 'Black'), ('a', 0): ('Rook', 'White'), ('b', 0): ('Knight', 'White'),
         ('c', 0): ('Bishop', 'White'), ('d', 0): ('Queen', 'White'), ('e', 0): ('King', 'White'),
         ('a', 4): ('Rook', 'Black'), ('b', 4): ('Knight', 'Black'), ('c', 4): ('Bishop', 'Black'),
         ('d', 4): ('Queen', 'Black'), ('e', 4): ('King', 'Black')}
whiteTurn = True
while True:
    if whiteTurn:
        newMove = studentAgent(board)
    else:
        newMove = greedy(board)
    if newMove is None:
        if whiteTurn:
            print("White lost")
        else:
            print("Black lost")
        break
    print(newMove)
    pieceInfo = board.pop(newMove[0])
    board[newMove[1]] = pieceInfo
    print(board)
    whiteTurn = not whiteTurn
end = time.time()
