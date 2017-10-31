import dataFunctions
import dataObject
from random import randint


def aiRandomMove(validMoves, token, board):
    move = validMoves[randint(0, len(validMoves))]
    board[move[0]][move[1]] = token
    boardString = dataFunctions.boardToString(board)
    move = dataObject.dataObject(token, boardString, false)
    return gameFunctions.flipTokens(move[0], move[1], board), move


def aiDatabaseMove(validMoves, token, board):
    move = dataFunctions.queryBestAiMove(validMoves, token, board)
    if move is False:
        board, move = aiRandomMove(validMoves, token, board)
    board[move[0]][move[1]] = token
    boardString = dataFunctions.boardToString(board)
    move = dataObject.dataObject(token, boardString, false)
    return gameFunctions.flipTokens(move[0], move[1], board), move

def humanMove(row, col, token, board): 
    board[row][col] = token
    boardString = dataFunctions.boardToString(board)
    move = dataObject.dataObject(token, boardString, false)
    return gameFunctions.flipTokens(row, col, board), move  

