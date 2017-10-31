from django.db import models

class gamestate(models.Model):
    hash = models.TextField()
    wp = models.IntegerField()
    turn = models.IntegerField()
    gamestate = models.TextField()

def test():
    print 'test'

def queryBestAiMove(validMoves, token, board):
    win = 0. 
    bestMove = []
    for cord in validMoves:
        tmpBoard = board
        tmpBoard[cord[0]][cord[1]] = token
        boardString = boardToString(tmpBoard)
        for m in Move.objects.raw("SELECT win from table where gamestate = %s", boardString):
            print m
            if m == null:
                return false
            if m > win:
                win = m
                bestMove = [cord[0], cord[1]]
        
    return bestMove

def boardToString(board):
    tmpString = ""
    for i in range(0,8):
        for j in range(0,8):
            tmpString += str(board[i][j])

    return tmpString
