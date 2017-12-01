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
    #template = loader.get_template('othello/index.html')
    return render(request, 'othello/index.html')

def main(request):
    newGame = gameObject.Game()
    request.session['game'] = newGame
    #request.session['gameID'] = id(newGame)
    #gameID = request.session.get('gameID')
    #print "gameID: ", gameID
    #gameObj = ctypes.cast(gameID, ctypes.py_object).value
    #print "gameObj: ", gameObj
    #gameObj.getBoard()
    #obj = request.session.get('gameId')
    #obj2 = ctypes.cast(obj, ctypes.py_object).value
    #obj2.getBoard()
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


@csrf_exempt
def new_move(request):

	# NOTE: Assume P1 is 'O' (Black) and AI is 'X' (White)
	response = {}

        #gameID = request.session.get('gameID')
        #print "gameID: ", gameID
        #gameObj = ctypes.cast(gameID, ctypes.py_object).value
        #print "gameObj: ", gameObj

        gameObj = request.session.get('game')
        #gameObj.getBoard()

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
