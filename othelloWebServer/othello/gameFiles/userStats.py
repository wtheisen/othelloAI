#userStats.py

import psycopg2, hashlib, random, time
random.seed(time.time())

# initiates a connection with the database
def dbInit():
    conn = psycopg2.connect(dbname = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
    cur = conn.cursor()
    return cur

# executes a query on the database
def queryExec(query):
    cur = dbInit()
    cur.execute(query)
    return cur.fetchall()

# computes the md5 hash of a gamestate string
def hashGamestate(boardString):
    return  hashlib.md5(boardString.encode()).hexdigest()

# computes a number of global game statistics using a series of database calls
def queryUserStats(user):
    results = {}
    
    # number of wins / losses / ties
    query = "SELECT count(*) FROM games JOIN users ON users.user_id::varchar(20)=games.user_id where users.username='"+user+"' and games.winner='O';"
    result = queryExec(query)
    results['nWins'] = result[0]
    query = "SELECT count(*) FROM games JOIN users ON users.user_id::varchar(20)=games.user_id where users.username='"+user+"' and games.winner='X';"
    result = queryExec(query)
    results['nLosses'] = result[0]
    query = "SELECT count(*) FROM games JOIN users ON users.user_id::varchar(20)=games.user_id where users.username='"+user+"' and games.winner='T';"
    result = queryExec(query)
    results['nTies'] = result[0]
    
    # average score
    query = "SELECT avg(games.opp_score) FROM games JOIN users ON users.user_id::varchar(20)=games.user_id where users.username='"+user+"';"
    result = queryExec(query)
    results['avgScore'] = result[0]
    
    # number of games played and win pct vs n games played
    winPct = {}
    query = "SELECT count(*) FROM games JOIN users ON users.user_id::varchar(20)=games.user_id where users.username='"+user+"';"
    result = queryExec(query)
    nGames = int(result[0][0])
    results['nGames'] = nGames
    lmt = 10.
    if nGames < 10: lmt = float(nGames)
    for i in range(1 + (nGames/10)):
        query = "SELECT count(*) FROM (SELECT * FROM games JOIN users ON users.user_id::varchar(20)=games.user_id where users.username='"+user+"' ORDER BY timestmp LIMIT "+str(lmt)+") where games.winner='O';"
        result = queryExec(query)
        winPct[str(lmt)] = float(result[0][0])/lmt
        lmt = lmt + 10
    results['winPcts'] = winPct
    
    # return results dictionary
    return results
