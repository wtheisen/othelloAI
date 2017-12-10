import gameFunctions, moveFunctions, dataFunctions, globalStats

class Game:

    def __init__(self):
        self.board = gameFunctions.initBoard()
        self.turn = 0
        self.token = 'X'
        self.moves = []
    
    def playerMove(self, row, col, token):
        print "human move"

        if not gameFunctions.checkValidMove(row, col, token, self.board):
            return False

        self.board, move = moveFunctions.humanMove(row, col, token, self.board)
        self.moves.append(move)
        self.turn += 1

        return move

    def aiMove(self):
        print "AI move"
        validMoves = gameFunctions.validMoves(self.token, self.board)
        if len(validMoves) == 0:
          return False
        self.board, move = moveFunctions.aiDatabaseMove(validMoves, self.token, self.board)
        self.moves.append(move)
        self.turn += 1
        return move

    def getBoard(self):
        return gameFunctions.printBoard(self.board)

    # converts a board object to a string representation
    def boardToString(self):
        tmpString = ""
        for i in range(0,8):
            for j in range(0,8):
                tmpString += str(self.board[i][j])
        return tmpString

    def getScore(self, token):
        return gameFunctions.getScore(token, self.board)

    def getValidMoves(self, token):
        return gameFunctions.validMoves(token, self.board)

    # plays a game with random moves in order to train the AI
    def trainingMode(self):
        curToken = 'O' 
        while not self.gameEnd():
            validMoves = gameFunctions.validMoves(curToken, self.board)
            if len(validMoves) == 0:
                if curToken is 'O':
                    curToken = 'X'
                else:
                    curToken = 'O'
                continue

            self.board, moveObject = moveFunctions.aiRandomMove(validMoves, curToken, self.board)
            if (curToken == 'X'):
              self.moves.append(moveObject)
            self.turn += 1

#            gameFunctions.printBoard(self.board)
            #raw_input("waiting")
            if curToken is 'O':
                curToken = 'X'
            else:
                curToken = 'O'
        return self.moves

    # allows us to specify if we want to train randomly or based on data already in the database
    def trainingModeAi(self, mode):
        curToken = 'O' 
        win = 0
        while 1:
            if self.gameEnd() == True:
              if self.getScore('X') > self.getScore('O'):
                win = 1
                print "x won!!!!!!!"
                dataFunctions.saveWinner("Female AI", "X")
                break
              else:
                print "o won!!!"
                dataFunctions.saveWinner("Female AI", "O")
                break
            validMoves = gameFunctions.validMoves(curToken, self.board)
            if len(validMoves) == 0:
                if curToken is 'O':
                    curToken = 'X'
                else:
                    curToken = 'O'
                continue
            if curToken == 'X':
                if mode == "random":
                  print "random chosen"
                  self.board, moveObject = moveFunctions.aiRandomMove(validMoves, curToken, self.board)
                else:
                  self.board, moveObject = moveFunctions.aiDatabaseMove(validMoves, curToken, self.board)
            else:
              self.board, moveObject = moveFunctions.aiDatabaseMove(validMoves, curToken, self.board)
            
            if self.turn >65:
              print "poooooooop"
              print self.turn
            if curToken is 'O':
                curToken = 'X'
            else:
                curToken = 'O'
            
            moveObject.nextPlayer = curToken 
            self.moves.append(moveObject)
            self.turn += 1
            
        return win
  
    # check if game has ended
    def gameEnd(self):
        if gameFunctions.endGame(self.board, self.turn):

            if self.getScore('X') > self.getScore('O'):
                print 'x wins'
                dataFunctions.dumpGame(self.moves, True)
            else:
                print 'o wins'
                dataFunctions.dumpGame(self.moves, False)
            return True

        return False

    # rollback to a previous turn
    def stateRollBack(self, turn):
        times = len(self.moves) - turn
        if turn < 0 or turn > self.turn:
          print "incorrect turn"
          return 

        if turn == 0:
          self.board = gameFunctions.initBoard()
          self.turn = 0
          self.token = 'X'
          self.moves = []
          return "O"
        else:
          for i in range(0, times):
            del self.moves[-1]
          self.board = gameFunctions.stringToBoard(self.moves[turn - 1].gamestate)
        
        self.turn = turn
        return self.moves[turn - 1].nextPlayer

    # get stats
    def getStats(self):
      return globalStats.queryGlobalStats()
