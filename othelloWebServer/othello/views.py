from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

import sys
sys.path.append('/home/djasek/othelloAI/othelloWebServer/othello/gameFiles')
import gameObject
import ctypes

def index2(request):
    return render(request, 'othello/index.html')

# GET request for main page creates a new game and stores it as a session variable 
def main(request):
    newGame = gameObject.Game()
    request.session['game'] = newGame
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
	response = {}
        gameObj = request.session.get('game')

        player = request.GET.get('player')
        if player == 'human':
            # put in more logic here
            response['result'] = True
        else:
            response['result'] = True
            
	return JsonResponse(response)

# On a POST, makes a new move
# On a GET, gets a new AI move
@csrf_exempt
def new_move(request):

	# NOTE: Assume P1 is 'O' (Black) and AI is 'X' (White)
	response = {}
        gameObj = request.session.get('game')

	# Player 1 makes a new_movee
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

			response['gamestate'] = gameObj.getBoardString()
			response['score'] = str(gameObj.getScore("O")) + " : " + str(gameObj.getScore("X"))
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

		response['gamestate'] = gameObj.getBoardString()
		response['score'] = str(gameObj.getScore("O")) + " : " + str(gameObj.getScore("X"))
		response['result'] = 'success'

                gameObj.getBoard()
                request.session['game'] = gameObj

	return JsonResponse(response)
