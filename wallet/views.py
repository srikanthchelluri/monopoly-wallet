from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from api.models import Game

# Create your views here.
def index(request):
	return render(request, 'index.html')

def game(request, gameID):
	return render(request, 'game.html', {"gameID": gameID})