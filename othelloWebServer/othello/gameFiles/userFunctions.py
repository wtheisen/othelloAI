import psycopg2, hashlib, gameFunctions as gf, copy, random, time
from hashlib import sha256

def getPassword(user): 
  conn = psycopg2.connect(dbname = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
  cur = conn.cursor()
  query = "SELECT * FROM users where username = '" + user + "';"
  cur.execute(query)
  row = cur.fetchall()
 # conn.commit()
 # conn.close()
  print len(row)
  print "howdy \n"
  print row[0][1]
  return row[0][1]

def login(user, password):
  print "here"
  if checkUser(user):
    pw = getPassword(user) 

    hashpw = str(sha256(password).hexdigest())

    if pw == hashpw:
      return True
    print "db:"
    print pw
    print "pw input:"
    print hashpw
    return False
  console.log("-1")
  return -1

def checkUser(user):
  conn = psycopg2.connect(dbname = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
  cur = conn.cursor()
  query = "SELECT * FROM users where username = '" + user + "';"
  cur.execute(query)
  row = cur.fetchall()
  conn.commit()
  conn.close()
  if len(row) is 0:
    return False

  return True 

def createUser(user, password):
  if checkUser(user):
    print "user name exists"
    return False

  hPass = sha256(password).hexdigest()
  conn = psycopg2.connect(dbname = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
  cur = conn.cursor()
  query = "INSERT INTO users VALUES ('" + user + "', '" + hPass + "');"
  cur.execute(query)
  conn.commit()
  conn.close()
  return True
      
