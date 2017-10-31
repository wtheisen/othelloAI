################################################################################

def printBoard(board):
    print "    0   1   2   3   4   5   6   7"
    print "  ================================="
    for i in range(0, 8):
        row = board[i]
        row_string =  str(i) + " | "
        for col in row:
            row_string += str(col) + " | "
        print row_string
        print "  ================================="

################################################################################

def checkValidMove(row, col, token, board):
    if token == 'X':
        oppToken = '0'
    else:
        oppToken = 'X'

    # check that the space is empty
    if board[row][col] != " ":
        return False

    # check horizontal
    if (col > 0 and board[row][col-1] == oppToken) or (col < 7 and board[row][col+1] == oppToken):
        for i in range(0, 8):
            if board[row][i] == token:
                return True

    # check vertical
    if (row < 7 and board[row+1][col] == oppToken) or (row > 0 and board[row-1][col] == oppToken):
        for i in range(0, 8):
            if board[i][col] == token:
                return True

    # check diagonal
    if row > 1 and col < 6 and board[row-1][col+1] == oppToken or row < 6 and col > 1 and board[row+1][col-1] == oppToken or row < 6 and col < 6 and board[row+1][col+1] == oppToken or row > 1 and col > 1 and board[row-1][col-1] == oppToken:

        currRow = row - 1
        currCol = col + 1
        while currRow >= 0 and currCol < 8:
            if board[currRow][currCol] == token:
                return True
            currRow -= 1
            currCol += 1

        currRow = row + 1
        currCol = col - 1
        while currRow < 8 and currCol >= 0:
            if board[currRow][currCol] == token:
                return True
            currRow += 1
            currCol -= 1

        currRow = row - 1
        currCol = col - 1
        while currRow >= 0 and currCol >= 0:
            if board[currRow][currCol] == token:
                return True
            currRow -= 1
            currCol -= 1

        currRow = row + 1
        currCol = col + 1
        while currRow < 8 and currCol < 8:
            if board[currRow][currCol] == token:
                return True
            currRow += 1
            currCol += 1

    return False

################################################################################

def flipTokens(r, c, board):
    token = board[r][c]

    if token == 'X':
        oppToken = '0'
    else:
        oppToken = 'X'

    if c < 6 and board[r][c+1] == oppToken and token in board[r][c+2:]:
        currCol = c+1
        while board[r][currCol] == oppToken:
            board[r][currCol] = token
            currCol += 1
    elif c > 1 and board[r][c-1] == oppToken and token in board[r][0:c-2]:
        currCol = c-1
        while board[r][currCol] == oppToken:
            board[r][currCol] = token
            currCol -= 1

    if r < 6 and board[r+1][c] == oppToken:
        for i in range(r+2, 8):
            if board[i][c] == token:
                currRow = r+1
                while board[currRow][c] == oppToken:
                    board[currRow][c] = token
                    currRow += 1
                break

    if r > 1 and board[r-1][c] == oppToken:
        for i in range(r-2, -1, -1):
            if board[i][c] == token:
                currRow = r-1
                while board[currRow][c] == oppToken:
                    board[currRow][c] = token
                    currRow -= 1
                break

    if r > 1 and c < 6 and board[r-1][c+1] == oppToken:
        row = r-2
        col = c+2
        while row >= 0 and col < 8:
            if board[row][col] == token:
                currRow = r-1
                currCol = c+1
                while board[currRow][currCol] == oppToken:
                    board[currRow][currCol] = token
                    currRow -= 1
                    currCol += 1
                break
            row -= 1
            col += 1

    if r < 6 and c > 1 and board[r+1][c-1] == oppToken:
        row = r+2
        col = c-2
        while row < 8 and col >= 0:
            if board[row][col] == token:
                currRow = r+1
                currCol = c-1
                while board[currRow][currCol] == oppToken:
                    board[currRow][currCol] = token
                    currRow += 1
                    currCol -= 1
                break
            row += 1
            col -= 1

    if r < 6 and c < 6 and board[r+1][c+1] == oppToken:
        row = r+2
        col = c+2
        while row < 8 and col < 8:
            if board[row][col] == token:
                currRow = r+1
                currCol = c+1
                while board[currRow][currCol] == oppToken:
                    board[currRow][currCol] = token
                    currRow += 1
                    currCol += 1
                break
            row += 1
            col += 1

    if r > 1 and c > 1 and board[r-1][c-1] == oppToken:
        row = r-2
        col = c-2
        while row >= 0 and col >= 0:
            if board[row][col] == token:
                currRow = r-1
                currCol = c-1
                while board[currRow][currCol] == oppToken:
                    board[currRow][currCol] = token
                    currRow -= 1
                    currCol -= 1
                break
            row -= 1
            col -= 1

    return board

################################################################################

def getScore(token, board):
    score = 0
    for r in board:
        for c in r:
            if c == token:
                score += 1
    return score

################################################################################

def validMoves(token, board):
    validMoves = []
    for row in range(0,8):
        for col in range(0,8):
            if checkValidMove(row, col, token, board):
                validMoves.append([row, col])

    return validMoves

################################################################################

def initBoard():
    board = [[" "]*8 for i in range(8)]
    board[3][3] = "X"
    board[4][4] = "X"
    board[3][4] = "0"
    board[4][3] = "0"

    return board

################################################################################

def endGame(board, turns):
    if not len(validMoves('X', board)) and not len(validMoves('O', board)):
        return True
    
    if not getScore('X', board) or not getScore('O', board):
        return True

    if turns >= 61:
        return True

    return False
