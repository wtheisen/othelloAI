import psycopg2 


def test():
    conn = psycopg2.connect(database = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
    cur = conn.cursor()
    for i in range(0,10):
        cur.execute("INSERT into gamestate (hash, wp, turn, gamestate) values('test" + str(i) +"', 0, 0, 'xoxoxo')")
    conn.commit()
    conn.close()

def queryBestAiMove(validMoves, token, board):
    win = 0. 
    bestMove = []
    for cord in validMoves:
        tmpBoard = board
        tmpBoard[cord[0]][cord[1]] = token
        boardString = boardToString(tmpBoard)
        for m in Move.objects.raw("SELECT * from gamestate where hash = %s", hashGamestate(boardString)):
            print m
'''            if m == null:
                return false
            if m > win:
                win = m
                bestMove = [cord[0], cord[1]]'''
        
    #return bestMove

def boardToString(board):
    tmpString = ""
    for i in range(0,8):
        for j in range(0,8):
            tmpString += str(board[i][j])

    return tmpString

def hashGamestate(self, boardString):
    return  hashlib.md5(board.encode()).hexdigest() 
