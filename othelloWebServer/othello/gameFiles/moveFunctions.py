import dataFunctions, gameFunctions as gf, dataObject, random, time
random.seed(time.time())

def aiRandomMove(validMoves, token, board):
    move = random.choice(validMoves)
    board = gf.flipTokens(gf.getTokensToFlip(move[0], move[1], token, board), board)
    board[move[0]][move[1]] = token 
    boardString = dataFunctions.boardToString(board)
    dObject = dataObject.DataObject(boardString)
    return board, dObject

def aiDatabaseMove(validMoves, token, board):
    move = dataFunctions.queryBestAiMove(validMoves, token, board)
#    print "move"
#    print move
    if move == False:
        print "random chosen"
        board, dObject = aiRandomMove(validMoves, token, board)
    else:
        print "best chosen"
        board = gf.flipTokens(gf.getTokensToFlip(move[0], move[1], token, board), board) 
        board[move[0]][move[1]] = token 
        boardString = dataFunctions.boardToString(board)
        dObject = dataObject.DataObject(boardString)
    return board, dObject

def humanMove(row, col, token, board):
    'move is not validated' 
    board = gf.flipTokens(gf.getTokensToFlip(row, col, token, board), board)
    board[row][col] = token 
    boardString = dataFunctions.boardToString(board)
    dObject = dataObject.DataObject(boardString)
    return board, dObject
