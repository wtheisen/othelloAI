from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


def index2(request):
    #template = loader.get_template('othello/index.html')
    return render(request, 'othello/index.html')

def main(request):
    #template = loader.get_template('othello/index.html')
    return render(request, 'othello/board.html')

@csrf_exempt
def test_post(request):
    if request.method == 'POST':
        print "inside test_post"
        num = request.session.get('num')
        if not num:
            num = 1
        num += 1
        request.session['num'] = num
        print "num: ", num
        return render(request, 'othello/index.html')
