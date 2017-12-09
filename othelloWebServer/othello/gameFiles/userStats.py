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
    query = "SELECT count(*) FROM (games JOIN users ON users.user_id::varchar(20)=games.user_id) a where a.username='"+user+"' and a.winner='O';"
    result = queryExec(query)
    results['nWins'] = result[0][0]
    query = "SELECT count(*) FROM (games JOIN users ON users.user_id::varchar(20)=games.user_id) a where a.username='"+user+"' and a.winner='X';"
    result = queryExec(query)
    results['nLosses'] = result[0][0]
    query = "SELECT count(*) FROM (games JOIN users ON users.user_id::varchar(20)=games.user_id) a where a.username='"+user+"' and a.winner='T';"
    result = queryExec(query)
    results['nTies'] = result[0][0]
    
    # average score
    query = "SELECT avg(a.opp_score) FROM (games JOIN users ON users.user_id::varchar(20)=games.user_id) a where a.username='"+user+"';"
    result = queryExec(query)
    if (result[0][0]): results['avgScore'] = float(result[0][0])
    else: results['avgScore'] = -1
    
    # return an array of user's scores for every game played in historical order
    query = "SELECT a.opp_score FROM (games JOIN users ON users.user_id::varchar(20)=games.user_id) a where a.username='"+user+"' ORDER BY a.timestmp;"
    result = queryExec(query)
    scores = [int(i[0]) for i in result]
    results['gameScores'] = scores
    
    # return results dictionary
    return results
