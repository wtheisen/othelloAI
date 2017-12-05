from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import psycopg2

import sys
#sys.path.append('/home/djasek/othelloAI/othelloWebServer/othello/gameFiles')
#sys.path.append('gameFiles')
#import gameObject
from gameFiles import gameObject
from gameFiles import userFunctions
import ctypes

def index2(request):
    return render(request, 'othello/index.html')

# GET request for main page creates a new game and stores it as a session variable 
def main(request):
    newGame = gameObject.Game()
    request.session['game'] = newGame
    request.session['username'] = 'guest'
    return render(request, 'othello/board_debug.html')

@csrf_exempt
def test_post(request):
    if request.method == 'POST':
        game = gameObject.Game()
        game.getBoard()
        print "inside test_post"
        num = request.session.get('num')
        if not num:
            num = 1
        num += 1
        request.session['num'] = num
        print "num: ", num
        return render(request, 'othello/index.html')

# Function to check if a certain player (human or AI) has any valid moves
@csrf_exempt
def check_valid_moves(request):
        print "inside check valid moves"
	response = {}
        gameObj = request.session.get('game')

        player = request.GET.get('player')
        if player == 'human':
            # put in more logic here
            response['result'] = True
        else:
            response['result'] = True
            
	return JsonResponse(response)

@csrf_exempt
def get_global_stats(request):
        gameObj = request.session.get('game')
        stats = gameObj.getStats()
	return JsonResponse(stats)

# On a POST, makes a new move
# On a GET, gets a new AI move
@csrf_exempt
def new_move(request):

        print "inside new move"

	# NOTE: Assume P1 is 'O' (Black) and AI is 'X' (White)
	response = {}
        gameObj = request.session.get('game')

	# Player 1 makes a new_move
	if request.method == 'POST':
		row = int(request.POST['row'])
		column = int(request.POST['column'])
                print "row: ", row
                print "col: ", column

                moveResult = gameObj.playerMove(row, column, "O")  
                print "moveResult: ", moveResult
		if bool(moveResult) != False:

			response['end'] = 'false'

			if gameObj.gameEnd():
				response['end'] = 'true'

			response['gamestate'] = gameObj.boardToString()
			response['score'] = str(gameObj.getScore("O")) + " : " + str(gameObj.getScore("X"))
                        response['validAIMoves'] = gameObj.getValidMoves("X")
                        response['validHumanMoves'] = gameObj.getValidMoves("O")
			response['result'] = 'success'

                        gameObj.getBoard()
                        request.session['game'] = gameObj

		else:
			response['result'] = 'failure'
			response['message'] = 'Invalid move!'

	# AI makes a move
	elif request.method == 'GET':

		gameObj.aiMove()

		response['end'] = 'false'
		
		if gameObj.gameEnd():
			response['end'] = 'true'

		response['gamestate'] = gameObj.boardToString()
		response['score'] = str(gameObj.getScore("O")) + " : " + str(gameObj.getScore("X"))
                response['validHumanMoves'] = gameObj.getValidMoves("O")
		response['result'] = 'success'

                gameObj.getBoard()
                request.session['game'] = gameObj

	return JsonResponse(response)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        
	response = {}
        if userFunctions.login(request.POST["username"], request.POST["password"]):
          print "in here"
          response['result'] = 'success'
          request.session['username'] = request.POST["username"]
          return JsonResponse(response)

        print "going to fail"
        response['result'] = 'failure'
        return JsonResponse(response)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        
	response = {}
        print request
        if userFunctions.createUser(request.POST["username"], request.POST["password"]):
          response['result'] = 'success'
          request.session['username'] = request.POST["username"]
          return JsonResponse(response)

        response['result'] = 'failure'
        return JsonResponse(response)
  
@csrf_exempt
def post_game_stats(request):
    if request.method == 'POST':
	response = {}
        conn = psycopg2.connect(dbname = 'fuzzytoads', user = 'fuzzytoad', password='databases', host = '127.0.0.1')
        cur = conn.cursor()
        query = "INSERT INTO games VALUES ('" + request.session['username'] + "', '" + request.POST["token"] + "', CURRENT_TIMESTAMP, ' ');"
        cur.execute(query)
        conn.commit()
        conn.close()
        
        response['result'] = 'success'
        return JsonResponse(response)
