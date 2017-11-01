from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    #template = loader.get_template('othello/index.html')
    return render(request, 'othello/index.html')
