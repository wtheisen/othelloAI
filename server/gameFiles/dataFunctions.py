"""from django.db import models

class Gamestate(models.Model):
    hash = models.TextField()
    wp = models.IntegerField()
    turn = models.IntegerField()
    gamestate = models.TextField()"""
import psycopg2 


def test():
    conn = psycopg2.connect(database = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
    cur = conn.cursor()
    cur.execute("INSERT into gamestate (hash, wp, turn, gamestate) values('test', 0, 0, 'xoxoxo')")
    conn.commit()
    conn.close()
    ###Gamestate.objects.raw("INSERT into gamestate (hash, wp, turn, gamestate) values('test', 0, 0, 'xoxoxo')")

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

def hashGamestate(self, boardString):
    return  hashlib.md5(board.encode()).hexdigest() 
