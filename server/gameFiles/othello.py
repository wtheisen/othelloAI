import gameFunctions

board = [[" "]*8 for i in range(8)]
board[3][3] = "X"
board[4][4] = "X"
board[3][4] = "0"
board[4][3] = "0"

turn = 1

while True:

    if turn == 60:
        break

    if turn %2 == 1:
        playerToken = 'X'
    else:
        playerToken = '0'

    gameFunctions.printBoard(board)
    print "Player X score: " + str(gameFunctions.getScore('X', board)) + "   Player 0 score: " + str(gameFunctions.getScore('0', board))
    print "Player " + playerToken + ": Enter move row/column:",

    while True:
        move = str(input())
        r = int(move[0])
        c = int(move[1])

        if gameFunctions.checkValidMove(r, c, playerToken, board):
            board[r][c] = playerToken
            gameFunctions.flipTokens(r, c, board)
            break
        else:
            print "Invalid move, please try again: ",

    turn += 1
