#globalStats.py

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
    row = cur.fetchall()

# computes the md5 hash of a gamestate string
def hashGamestate(boardString):
    return  hashlib.md5(boardString.encode()).hexdigest()

# computes a number of global game statistics using a series of database calls
def queryGlobalStats():
    results = {}
    
    # number of entries in the database
    query = "SELECT count(*) FROM gamestate;"
    result = queryExec(query)
    results['nEntries'] = result[0][0]
    
    # query speed
    query = "SELECT * FROM gamestate WHERE hash= '67861af76445a34e8703b9edfcc00150';"
    sTime = time.time()
    result = queryExec(query)
    eTime = time.time()
    results['querySpeedIdx'] = eTime - sTime
    query = "SELECT * FROM gamestate WHERE gamestate = '                  X     OXOXO   O  OOO  O   OX                  ';"
    sTime = time.time()
    result = queryExec(query)
    eTime = time.time()
    results['querySpeedNoIdx'] = eTime - sTime
    
    # board states with the highest/lowest win pct
    query = "SELECT gamestate, wp FROM gamestate ORDER BY wp DESC LIMIT 1;"
    result = queryExec(query)
    results['highestWin'] = result[0]
    query = "SELECT gamestate, wp FROM gamestate ORDER BY wp LIMIT 1;"
    result = queryExec(query)
    results['lowestWin'] = result[0]

    # number of games played and win pct vs n games played
    winPct = {}
    query = "SELECT count(*) FROM games;"
    result = queryExec(query)
    nGames = result[0][0]
    results['nGames'] = nGames
    lmt = 10
    for i in range(nGames%10):
        query = "SELECT count(*) FROM (SELECT * FROM games ORDER BY timestmp LIMIT " + lmt + ") AS a WHERE winner='X';"
        result = queryExec(query)
        winPct[lmt] = (result[0][0])/lmt
        lmt = lmt + 10
    results['winPcts'] = winPct

    # return results dictionary
    return results
