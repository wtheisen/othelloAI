import gameObject, signal 
# this file trains the AI
class TimeoutException(Exception):
  pass

def timeout_handler(signun, frame):
  raise TimeoutException

game = gameObject.Game()

wins = 0
games = 0

signal.signal(signal.SIGALRM, timeout_handler)

for i in range(0,1000000):  
  signal.alarm(12)
  games += 1
  try:
    game = gameObject.Game()
    tot = game.trainingModeAi("notRandom")
    wins += tot
    print "wins " + str(wins)
    print "games " + str(games)
    print str(float(wins) / float(games))
  except TimeoutException:
    games -= 1
    continue
  else:
    print "yo"
    signal.alarm(8)


