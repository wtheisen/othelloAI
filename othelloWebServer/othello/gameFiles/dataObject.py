import hashlib, dataFunctions as df

# class for a data object to be inserted into the db
class DataObject:
  def __init__(self, gamestate):
    self.gamestate = gamestate
    self.wp = 0
    self.hash = df.hashGamestate(gamestate)
    self.nextPlayer = ""
