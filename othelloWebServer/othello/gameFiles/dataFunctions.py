import psycopg2, hashlib, gameFunctions as gf, copy, random, time
random.seed(time.time())


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
    learningWithRules = True
    win = 0.
    bestMove = []
    cur = dbInit()
    moves = []

    #print 'validmoves'  
    #print validMoves
    
    for cord in validMoves: 
        tmpBoard = ""
        tmpBoard = copy.deepcopy(board)
        tmpBoard = gf.flipTokens(gf.getTokensToFlip(cord[0], cord[1], token, tmpBoard), tmpBoard)
        tmpBoard[cord[0]][cord[1]] = token
        boardString = boardToString(tmpBoard)
        cur.execute("SELECT * from gamestate where hash = '" + hashGamestate(boardString) + "';")
        row = cur.fetchall()
        if len(row) == 0:
          continue
        for data in row:
            tup = (cord[0], cord[1], data[1])
#            print tup
#            print "total moves"
            moves.append(tup)
 #           print moves

    if token == "X":
      moves.sort(key=lambda x: -x[2]) 
      print "moves!"
      print moves
    else:
      moves.sort(key=lambda x: x[2])

  #  print 'top'
   # print moves

    for cord in validMoves:
        if learningWithRules:
          if cord[0] == 0 and cord[1] == 0:
     #       print 'Corner'
            bestMove = [cord[0], cord[1]]
            return bestMove
          if cord[0] == 7 and cord[1] == 0:
      #      print 'Corner' 
            bestMove = [cord[0], cord[1]]
            return bestMove
          if cord[0] == 0 and cord[1] == 7:
       #     print 'Corner'
            bestMove = [cord[0], cord[1]]
            return bestMove
          if cord[0] == 7 and cord[1] == 7:
        #    print 'Corner'
            bestMove = [cord[0], cord[1]]
            return bestMove

    if learningWithRules:
      if len(moves) > 0:

        if token == "X":
          if moves[0][2] < 0:
            potRand = []
            if len(moves) < len(validMoves):
              for cord in validMoves:
                tmp = True
                for move in moves:
                  if cord[0] == move[0] and cord[1] == move[1]:
                    tmp = False
                    break
                if tmp:
                  potRand.append(cord)
             
              if len(potRand) == 0:
                print "wtf"
              
              move = random.choice(potRand)
              bestMove = [move[0], move[1]]
              print "found a move better than neg best one for X"
              return bestMove
        else:
          if moves[0][2] > 0:
            potRand = []
            if len(moves) < len(validMoves):
              for cord in validMoves:
                tmp = True
                for move in moves:
                  if cord[0] == move[0] and cord[1] == move[1]:
                    tmp = False
                    break
                if tmp:
                  potRand.append(cord)
             
              if len(potRand) == 0:
                print "wtf"
              
              move = random.choice(potRand)
              bestMove = [move[0], move[1]]
              print "found a move better than neg best one for O"
              return bestMove

        
        for move in moves:
          if not leadsToCorner([move[0], move[1]], token, board):
            bestMove = [move[0], move[1]]
            break
        if len(bestMove) == 0:
          print moves
          bestMove = [moves[0][0], moves[0][1]]
    else:
      if len(moves) > 0:
        bestMove = [moves[0][0], moves[0][1]]

    if len(bestMove) == 0:
      if learningWithRules:
        move = []
        move = wallMove(validMoves, token, board)
        if move == 0:
          return False
        return move 

      return False
    else:
      
      return bestMove

def leadsToCorner(move, token, board):
  oToken = ""
  if token == 'X':
    oToken = 'O'
  else:
    oToken = 'X'
  tmpBoard = copy.deepcopy(board)
  tmpBoard[move[0]][move[1]] = token
  #if gf.checkValidMove(0, 0, oToken, tmpBoard):
  if tmpBoard[0][0] == " ":
    if move == [0,1] or move == [1,1] or move == [1,0]:
      return True
  #if gf.checkValidMove(0, 7, oToken, tmpBoard):
  if tmpBoard[0][7] == " ":
    if move == [1,6] or move == [1,7] or move == [0,6]:
      return True
  #if gf.checkValidMove(7, 0, oToken, tmpBoard):
  if tmpBoard[7][0] == " ": 
    if move == [6,1] or move == [6,0] or move == [7,1]:
      return True
  #if gf.checkValidMove(7, 7, oToken, tmpBoard):
  if tmpBoard[7][7] == " ":
    if move == [6,6] or move == [6,7] or move == [7,6]:
      return True

  return False

def wallMove(validMoves, token, board):
    for pair in validMoves:
      if pair[0] == 0 or pair[0] == 7 or pair[1] == 0 or pair[1] == 7:
        if leadsToCorner(pair, token, board):
          continue
        #print "wall chosen ",
        return pair
    return 0

def boardToString(board):
    tmpString = ""
    for i in range(0,8):
        for j in range(0,8):
            tmpString += str(board[i][j])

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
