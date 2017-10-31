import psycopg2, hashlib

def dbInit():
  conn = psycopg2.connect(dbase = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
  cur = conn.cursor()
  return cur

def test():
    conn = psycopg2.connect(dbase = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
    cur = conn.cursor()
    for i in range(0,10):
        cur.execute("UPDATE gamestate set wp = " + str(i) + " where hash = 'test" + str(i) + "'")

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
            set wp = """ + str(move.wp) + """
            + (select wp from gamestate where hash = """ 
            + hashGamestate(move.gaemstate) + """) );""")


def valueMoves(moveList, win):
    if win:
        for i in range(0, moveList):
            moveList[i].wp = 0.005 * i**2
    else:
        for i in range(0, moveList):
            moveList[i].wp = -0.005 * i**2

    return moveList

def dumpGame(moveList, win):
    moveList = valueMoves(moveList, win)
    for move in moveList:
        insertDataObject(move)
