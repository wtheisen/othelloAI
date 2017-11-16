import hashlib, dataFunctions as df

class DataObject:
    'object for storing data to be inserted in the DB'

    def __init__(self, gamestate):
        self.gamestate = gamestate
        self.wp = 0
        self.hash = df.hashGamestate(gamestate)
