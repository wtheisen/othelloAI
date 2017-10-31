import hashlib, dataFunctions as df

class dataObject:
    'object for storing data to be inserted in the DB'

    def __init__(self, gamestate, turn):
        self.gamestate = gamestate
        self.wp = 0
        self.hash = df.hashGamestate(df.boardToString(gamestate))
