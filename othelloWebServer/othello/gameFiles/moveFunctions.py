import dataFunctions, gameFunctions as gf, dataObject, random, time
random.seed(time.time())

# makes a random move and returns a dataObject
def aiRandomMove(validMoves, token, board):
    print "random chosen"
    move = random.choice(validMoves)
    board = gf.flipTokens(gf.getTokensToFlip(move[0], move[1], token, board), board)
    board[move[0]][move[1]] = token 
    boardString = dataFunctions.boardToString(board)
    dObject = dataObject.DataObject(boardString)
    return board, dObject

# picks the best possible weighted move (if that move isn't negative)
# otherwise, returns a random move
def aiDatabaseMove(validMoves, token, board):
    move = dataFunctions.queryBestAiMove(validMoves, token, board)
#    print token,
#    print "move"
#    print move
    if move == False:
 #       print "random chosen"
        board, dObject = aiRandomMove(validMoves, token, board)
    else:
  #      print "best chosen"
        board = gf.flipTokens(gf.getTokensToFlip(move[0], move[1], token, board), board) 
        board[move[0]][move[1]] = token 
        boardString = dataFunctions.boardToString(board)
        dObject = dataObject.DataObject(boardString)
    return board, dObject

'''def aiDatabaseMoveAsAi(validMoves, token, board):
    tmpBoard = copy.deepcopy(board)
    for i in range(0,8):
      for j in range(0,8):
        if tmpBoard[i][j] == "X":
          tmpBoard[i][j] = "O"
        elif tmpBoard[i][j] == "O":
          tmpBoard[i][j] = "X"
   ''' 
   
# implements a human move and returns a dataObject   
def humanMove(row, col, token, board):
    'move is not validated' 
    board = gf.flipTokens(gf.getTokensToFlip(row, col, token, board), board)
    board[row][col] = token 
  
  
  
    boardString = dataFunctions.boardToString(board)
    dObject = dataObject.DataObject(boardString)
    return board, dObject
