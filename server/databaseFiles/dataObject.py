class dataObject:
    'object for storing data to be inserted in the DB'

    def __init__(self, token, gamestate, win):
        self.token = token
        self.gamestate = gamestate
        self.win = win

    def hashGamestate(self):
        self.hash = 'aaaa'
