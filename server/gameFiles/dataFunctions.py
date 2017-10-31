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
    cur = dbInit()

    #i = 8
    for cord in validMoves:
        tmpBoard = board
        tmpBoard[cord[0]][cord[1]] = token
        boardString = boardToString(tmpBoard)
        cur.execute("SELECT * from gamestate where hash = '" + hashGamestate(boardString) + "'")
        #cur.execute("SELECT * from gamestate where hash = 'test" +str(i) + "'")
        row = cur.fetchall()
        if len(row) is 0:
          return False
        for data in row:
          if data[1] > win:
              win = data[1]
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

def insertDataObject(move):
    cur = conn.cursor()
    cur.execute("""
            INSERT INTO gamestate
            (hash, wp, gamestate)
            VALUES
            (""" + hashGamestate(move.gamestate) + ","
               + str(move.wp) + ","
               + move.gamestate + """)
            ON CONFLICT(hash) DO UPDATE
            wp = excluded.""" + str(move.wp) + ");")


def valueMoves(moveList):
    print "meow"
    return moveList

def dumpGame(moveList):
    moveList = valueMoves(moveList)
    for move in moveList:
        insertDataObject(move)
