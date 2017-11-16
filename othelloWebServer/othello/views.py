from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json

import sys
sys.path.append('/home/djasek/othelloAI/othelloWebServer/othello/gameFiles')
import gameObject 

def index2(request):
    #template = loader.get_template('othello/index.html')
    return render(request, 'othello/index.html')

def main(request):
    #template = loader.get_template('othello/index.html')
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
def new_move(request):

	# NOTE: Assume P1 is 'O' (Black) and AI is 'X' (White)

	response = {}

	# Player 1 makes a new_movee
	if request.method == 'POST':
		row = request.POST['row']
		column = request.POST['column']

		if playerMove(row, column, "O"):

			response['end'] = 'false'

			if gameEnd():
				response['end'] = 'true'

			response['gamestate'] = Object.gamestate
			response['score'] = str(getScore("O")) + " : " + str(getScore("X"))
			response['result'] = 'success'

		else:
			response['result'] = 'failure'
			response['message'] = 'Invalid move!'

	# AI makes a move
	elif request.method == 'GET':

		aiMove()

		response['end'] = 'false'
		
		if gameEnd():
			response['end'] = 'true'

		response['gamestate'] = Object.gamestate
		response['score'] = str(getScore("O")) + " : " + str(getScore("X"))
		response['result'] = 'success'

	return JsonResponse(response)
