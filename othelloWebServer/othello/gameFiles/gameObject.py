import gameFunctions, moveFunctions, dataFunctions

class Game:

    def __init__(self):
        self.board = gameFunctions.initBoard()
        self.turn = 1
        self.token = 'X'
        self.moves = []

    def playerMove(self, row, col, token):
        #print "human move"

        if not gameFunctions.checkValidMove(row, col, token, self.board):
            return False

        self.board, move = moveFunctions.humanMove(row, col, token, self.board)
        self.moves.append(move)
        self.turn += 1

        return move

    def aiMove(self):
        print "AI move"
        validMoves = gameFunctions.validMoves(self.token, self.board)
        self.board, move = moveFunctions.aiDatabaseMove(validMoves, self.token, self.board)
        self.moves.append(move)
        self.turn += 1
        return move

    def getBoard(self):
        return gameFunctions.printBoard(self.board)
    
    def getBoardString(self):
        return dataFunctions.boardToString(self.board)

    def getScore(self, token):
        return gameFunctions.getScore(token, self.board)

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
            self.moves.append(moveObject)
            self.turn += 1

#            gameFunctions.printBoard(self.board)
            #raw_input("waiting")
            if curToken is 'O':
                curToken = 'X'
            else:
                curToken = 'O'

        return self.moves

    def trainingModeAi(self):
        curToken = 'O' 
        win = 0
        while 1:
            if self.gameEnd() == True:
              if self.getScore('X') > self.getScore('O'):
                win = 1
                print "x won!!!!!!!"
                break
              else:
                print "o won!!!"
                break
            validMoves = gameFunctions.validMoves(curToken, self.board)
            if len(validMoves) == 0:
                if curToken is 'O':
                    curToken = 'X'
                else:
                    curToken = 'O'
                continue
            if curToken == 'X':
              self.board, moveObject = moveFunctions.aiDatabaseMove(validMoves, curToken, self.board)
            else:
              self.board, moveObject = moveFunctions.aiRandomMove(validMoves, curToken, self.board)
#            gameFunctions.printBoard(self.board)
#            raw_input("waiting")
            self.moves.append(moveObject)
            self.turn += 1

            if self.turn >65:
              print "poooooooop"
              print self.turn
#            gameFunctions.printBoard(self.board)
            #raw_input("waiting")
            if curToken is 'O':
                curToken = 'X'
            else:
                curToken = 'O'

        return win

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


    
