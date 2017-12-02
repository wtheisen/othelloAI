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

# checks is a move is valid by checking if it flips any tokens
def checkValidMove(row, col, token, board):
  if len(getTokensToFlip(row, col, token, board)) > 0:
    return True
  else:
    return False

################################################################################

# gets the tokens that will need to be flipped if a certain move is played
def getTokensToFlip(r, c, token, board):
     
    if token == 'X':
        oppToken = 'O'
    else:
        oppToken = 'X'
 
    tokensToFlip = []
 
    # prevent moving somewhere where there is already a piece by returning an empty list
    if board[r][c] != " ":
        return []
 
    # horizontal checks
 
    # horizontal right
    if c < 6 and board[r][c+1] == oppToken: #opponent token adjacent to the right
        possibleFlips = [] # create list to store all possible flips if this scenario works out
        currCol = c+1
        while currCol < 8: # move right, adding coordinates to flip to a list
            if board[r][currCol] == oppToken:
                possibleFlips.append((r, currCol))
            # if we find one of our tokens immediately after an opponent token, we know this is a valid move
            elif board[r][currCol] == token:
                tokensToFlip.extend(possibleFlips) # add all the "possible" pieces to flip to the real list
                break
            else: # an empty space was encountered before one of our own pieces, this move is invalid
                break
            currCol += 1
    
    # horizontal left
    if c > 1 and board[r][c-1] == oppToken:
        possibleFlips = []
        currCol = c-1
        
        while currCol >= 0:
            if board[r][currCol] == oppToken:
                possibleFlips.append((r, currCol))
            elif board[r][currCol] == token:
                tokensToFlip.extend(possibleFlips)
                break
            else:
                break
            currCol -= 1
    # vertical checks
 
    # vertical down
    if r < 6 and board[r+1][c] == oppToken:
        possibleFlips = []
        currRow = r+1
        while currRow < 8:
            if board[currRow][c] == oppToken:
                possibleFlips.append((currRow, c))
            elif board[currRow][c] == token:
                tokensToFlip.extend(possibleFlips)
                break
            else:
                break
            currRow += 1
 
    # vertical up
    if r > 1 and board[r-1][c] == oppToken:
        possibleFlips = []
        currRow = r-1
        while currRow >= 0:
            if board[currRow][c] == oppToken:
                possibleFlips.append((currRow, c))
            elif board[currRow][c] == token:
                tokensToFlip.extend(possibleFlips)
                break
            else:
                break
            currRow -= 1
    # diagonal checks
 
    # down and right
    if r < 6 and c < 6 and board[r+1][c+1] == oppToken:
        possibleFlips = []
        currRow = r+1
        currCol = c+1
        while currRow < 8 and currCol < 8:
            if board[currRow][currCol] == oppToken:
                possibleFlips.append((currRow, currCol))
            elif board[currRow][currCol] == token:
                tokensToFlip.extend(possibleFlips)
                break
            else:
                break
            currRow += 1
            currCol += 1
 
    # down and left
    if r < 6 and c > 1 and board[r+1][c-1] == oppToken:
        possibleFlips = []
        currRow = r+1
        currCol = c-1
        while currRow < 8 and currCol >= 0:
            if board[currRow][currCol] == oppToken:
                possibleFlips.append((currRow, currCol))
            elif board[currRow][currCol] == token:
                tokensToFlip.extend(possibleFlips)
                break
            else:
                break
            currRow += 1
            currCol -= 1
 
    # up and right
    if r > 1 and c < 6 and board[r-1][c+1] == oppToken:
        possibleFlips = []
        currRow = r-1
        currCol = c+1
        while currRow >= 0 and currCol < 8:
            if board[currRow][currCol] == oppToken:
                possibleFlips.append((currRow, currCol))
            elif board[currRow][currCol] == token:
                tokensToFlip.extend(possibleFlips)
                break
            else:
                break
            currRow -= 1
            currCol += 1
 
    # up and left
    if r > 1 and c > 1 and board[r-1][c-1] == oppToken:
        possibleFlips = []
        currRow = r-1
        currCol = c-1
        while currRow >= 0 and currCol >= 0:
            if board[currRow][currCol] == oppToken:
                possibleFlips.append((currRow, currCol))
            elif board[currRow][currCol] == token:
                tokensToFlip.extend(possibleFlips)
                break
            else:
                break
            currRow -= 1
            currCol -= 1
    
    return tokensToFlip

################################################################################

# flips all the tokens in a list on the board
def flipTokens(tokens, board):
    for r, c in tokens:
        if board[r][c] == 'X':
            board[r][c] = 'O'
        else:
            board[r][c] = 'X'
    return board

################################################################################

# calculates the score for a given token on the board
def getScore(token, board):
    score = 0
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j] == token:
                score = score + 1
    return score

################################################################################

# returns a list of valid moves for a given token
def validMoves(token, board):
    validMovesList = []
    for row in range(0,8):
        for col in range(0,8):
            if checkValidMove(row, col, token, board):
                validMovesList.append([row, col])

    return validMovesList

################################################################################

def initBoard():
    board = [[" "]*8 for i in range(8)]
    board[3][3] = "X"
    board[4][4] = "X"
    board[3][4] = "O"
    board[4][3] = "O"

    return board

################################################################################

def endGame(board, turns):
    if validMoves('X', board) == [] and validMoves('O', board) == []:
        print 'no more moves for either'
        return True
    
    if getScore('X', board) == 0 or getScore('O', board) == 0:
        print 'one of yall got zero tiles left'
        return True

    if turns >= 60:
        print 'no more moves yall'
        return True

    return False

################################################################################

def stringToBoard(gamestate):
    board = [[" "]*8 for i in range(8)]
    for i in range(0,8):
      for j in range(0,8):
        board[i][j] = gamestate[i*8 + j]

    return board

################################################################################

