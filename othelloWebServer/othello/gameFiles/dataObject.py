import hashlib, dataFunctions as df
 
class DataObject:
  def __init__(self, gamestate):
    self.gamestate = gamestate
    self.wp = 0
    self.hash = df.hashGamestate(gamestate)
