import dataFunctions
from random import randint


def aiRandomMove(validMoves):
    'Pick best of valid Moves'
    print "lol so randum"
    return validMoves[randint(0, len(validMoves))]

def aiDatabaseMove(validMoves, board, token):
    'Pick best of validMoves'
    move = dataFunctions.queryBestAiMove(validMoves, board, token)
    print "wow such AI"
    return False

def humanMove(row, col, token, board):
    'Actually Perform Moves'
    board[row][col] = token
    print "so hooman"
    'do database stuff (if any) here'
    return board 

