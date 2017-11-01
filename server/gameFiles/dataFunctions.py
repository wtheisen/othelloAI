import psycopg2, hashlib, gameFunctions as gf, copy

def dbInit():
  conn = psycopg2.connect(dbname = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
  cur = conn.cursor()
  return cur

def test():
    conn = psycopg2.connect(dbname = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
    cur = conn.cursor()
    for i in range(0,10):
        cur.execute("UPDATE gamestate set wp = " + str(i) + " where hash = 'test" + str(i) + "'")

    conn.commit()
    conn.close()

def queryBestAiMove(validMoves, token, board):
    win = 0.
    bestMove = []
    cur = dbInit()

#    print "validMoves"
 #   print validMoves
    #i = 8
    for cord in validMoves:
        print "cord: " + str(cord[0]) + " " + str(cord[1])
        print "win: " + str(win)
        print bestMove
        tmpBoard = ""
        tmpBoard = copy.deepcopy(board)
        tmpBoard = gf.flipTokens(gf.getTokensToFlip(cord[0], cord[1], token, tmpBoard), tmpBoard)
        tmpBoard[cord[0]][cord[1]] = token
        boardString = boardToString(tmpBoard)
     #   print "bs " + boardString 
        cur.execute("SELECT * from gamestate where hash = '" + hashGamestate(boardString) + "';")
        #cur.execute("SELECT * from gamestate where hash = 'test" +str(i) + "'")
        row = cur.fetchall()
        if len(row) == 0:
          continue
        for data in row:
          if data[1] > win:
              win = data[1]
              bestMove = [cord[0], cord[1]]

    print "bestMoves"
    print bestMove
    if len(bestMove) == 0:
      return False
    else:
      return bestMove

def boardToString(board):
#    print "printing board in bts"
 #   print board
    tmpString = ""
  #  print "starting board to string"
    for i in range(0,8):
        for j in range(0,8):
    #        print "Index: " + str(i) + " " + str(j)
   #         print tmpString + "|"
            tmpString += str(board[i][j])

    #print "over"
    return tmpString

def hashGamestate(boardString):
    return  hashlib.md5(boardString.encode()).hexdigest()

def insertDataObject(move, conn):
    cur = conn.cursor()
    query = "INSERT INTO gamestate (hash, wp, gamestate) VALUES ('" + hashGamestate(move.gamestate) + "', " + str(move.wp) +  ", '" + move.gamestate + "');" 
    cur.execute("select * from gamestate where hash = '" + hashGamestate(move.gamestate) + "';")
    row = cur.fetchall()
    if len(row) is 0:
      cur.execute(query)
    else:      
      cur.execute("UPDATE gamestate set wp = " + str(move.wp + row[0][1]) + " where hash = '" + hashGamestate(move.gamestate) +  "';")
    conn.commit()

def valueMoves(moveList, win):
    if win:
        for i in range(0, len(moveList)):
            moveList[i].wp = 0.005 * i**2
    else:
        for i in range(0, len(moveList)):
            moveList[i].wp = -0.005 * i**2

    return moveList

def dumpGame(moveList, win):
    moveList = valueMoves(moveList, win)
    conn = psycopg2.connect(dbname = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
    for move in moveList:
        insertDataObject(move, conn)
    conn.close()
