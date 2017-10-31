import gameFunctions, moveFunctions, dataFunctions

class Game:

    def __init__(self):
        self.board = gameFunctions.initBoard()
        self.turn = 1
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
        self.board, move = moveFunctions.aiDatabaseMove(validMoves, self.token, self.board)
        self.moves.append(move)
        self.turn += 1
        return move

    def getBoard(self):
        gameFunctions.printBoard(self.board)

    def getScore(self, token):
        gameFunctions.getScore(token, self.board)

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

            self.board, move = moveFunctions.aiRandomMove(validMoves, curToken, self.board)
            self.moves.append(move)
            self.turn += 1

            gameFunctions.printBoard(self.board)
            input("waiting")
            if curToken is 'O':
                curToken = 'X'
            else:
                curToken = 'O'

        return self.moves

    def gameEnd(self):
        if gameFunctions.endGame(self.board, self.turn):
            if self.getScore('X') > self.getScore('O'):
                dataFunctions.dumpGame(self.moves, True)
            else:
                dataFunctions.dumpGame(self.moves, False)
            return True

        return False


    
