import gameFunctions
import moveFunctions

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
        self.board, move = moveFunctions.aiDatabaseMove(validMoves, self.board, self.token)
        self.moves.append(move)
        self.turn += 1
        return move

    def getBoard(self):
        gameFunctions.printBoard(self.board)

    def getScore(self, token):
        gameFunctions.getScore(token, self.board)

    def trainingMode(self):
        while (1):
            validMoves = gameFunctions.validMoves(self.token, self.board)
            if len(validMoves) == 0:
                break

            self.board, move = moveFunctions.aiRandomMove(validMoves)
            self.moves.append(moves)
            self.turn += 1

        return self.moves
