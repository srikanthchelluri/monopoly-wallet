from django.shortcuts import render
from django.http import JsonResponse
from api.models import Game, Player, Transfer
import math, random

# Create your views here.
def game_create(request):
	if request.method == "POST":
		# Generate a random, 6-digit number
		gameID = 0
		while gameID < 100000 or gameID > 999999:
			gameID = math.floor(random.random() * 10**6)

		# Create the game model
		game = Game(
			gameID = gameID
		)
		game.save()

		# Create the player model
		playerID = request.POST.get("playerID", "")
		playerName = request.POST.get("playerName", "")
		player = Player(
			game = game,
			cookie = playerID,
			name = playerName,
			holdings = 1500
		)
		player.save()

		return JsonResponse({
			"status": "success",
			"data": {
				"gameID": gameID
			}
		})
	else:
		return JsonResponse({
			"status": "error",
			"data": None
		})

def game_join(request):
	if request.method == "POST":
		gameID = request.POST.get("gameID", "")
		playerID = request.POST.get("playerID", "")
		playerName = request.POST.get("playerName", "")

		try:
			game = Game.objects.get(gameID = gameID)
			player = Player(
				game = game,
				cookie = playerID,
				name = playerName,
				holdings = 1500
			)
			player.save()

			return JsonResponse({
				"status": "success",
				"data": None
			})
		except Exception as e:
			return JsonResponse({
				"status": "error",
				"data": e
			})
	else:
		return JsonResponse({
			"status": "error",
			"data": None
		})

def game_refresh(request):
	if request.method == "POST":
		gameID = request.POST.get("gameID", "")

		try:
			game = Game.objects.get(gameID = gameID)

			players = []
			player_set = game.player_set.all()
			for p in player_set:
				players.append({
					"name": p.name,
					"holdings": p.holdings,
					"cookie": p.cookie
				})

			transfers = [{
					'fromPrincipal': t.fromPrincipal,
					'toPrincipal': t.toPrincipal,
					'amount': t.amount
				}
				for t in Transfer.objects.filter(game = game).order_by("-time")[:8]]

			return JsonResponse({
				"status": "success",
				"data": {
					"gameID": gameID,
					"players": players,
					"transfers": transfers,
					"freeParking": game.freeParking,
				}
			})
		except Exception as e:
			return JsonResponse({
				"status": "error",
				"data": e
			})
	else:
		return JsonResponse({
			"status": "error",
			"data": None
		})

def game_transfer(request):
	if request.method == "POST":
		gameID = request.POST.get("gameID", "")
		playerID = str(request.POST.get("playerID", ""))
		recipientID = str(request.POST.get("recipientID", ""))
		amount = int(request.POST.get("amount", ""))

		try:
			game = Game.objects.get(gameID = gameID)
			fromPlayer = Player.objects.get(cookie = playerID)
			fromPlayer.holdings -= amount
			fromPlayer.save()

			transfer = Transfer(
				game = game,
				fromPrincipal = fromPlayer.name,
				amount = amount
			)

			if recipientID == "-1": # Bank
				transfer.toPrincipal = "Bank"
				transfer.save()
			elif recipientID == "-2": # Free parking
				game = Game.objects.get(gameID = gameID)
				game.freeParking += amount
				game.save()

				transfer.toPrincipal = "Free parking"
				transfer.save()
			else:
				toPlayer = Player.objects.get(cookie = recipientID)
				toPlayer.holdings += amount
				toPlayer.save()

				transfer.toPrincipal = toPlayer.name
				transfer.save()

			return JsonResponse({
				"status": "success",
				"data": None
			})
		except Exception as e:
			return JsonResponse({
				"status": "error",
				"data": e
			})
	else:
		return JsonResponse({
			"status": "error",
			"data": None
		})

def game_bank(request):
	if request.method == "POST":
		gameID = request.POST.get("gameID", "")
		playerID = str(request.POST.get("playerID", ""))
		amount = int(request.POST.get("amount", ""))

		try:
			game = Game.objects.get(gameID = gameID)

			toPlayer = Player.objects.get(cookie = playerID)
			toPlayer.holdings += amount
			toPlayer.save()

			transfer = Transfer(
				game = game,
				fromPrincipal = "Bank",
				toPrincipal = toPlayer.name,
				amount = amount
			)
			transfer.save()

			return JsonResponse({
				"status": "success",
				"data": None
			})
		except Exception as e:
			return JsonResponse({
				"status": "error",
				"data": e
			})
	else:
		return JsonResponse({
			"status": "error",
			"data": None
		})

def game_freeparking(request):
	if request.method == "POST":
		gameID = request.POST.get("gameID", "")
		playerID = str(request.POST.get("playerID", ""))

		try:
			game = Game.objects.get(gameID = gameID)

			toPlayer = Player.objects.get(cookie = playerID)
			toPlayer.holdings += game.freeParking
			toPlayer.save()

			transfer = Transfer(
				game = game,
				fromPrincipal = "Free parking",
				toPrincipal = toPlayer.name,
				amount = game.freeParking
			)
			transfer.save()

			game.freeParking = 0
			game.save()
			
			return JsonResponse({
				"status": "success",
				"data": None
			})
		except Exception as e:
			return JsonResponse({
				"status": "error",
				"data": e
			})
	else:
		return JsonResponse({
			"status": "error",
			"data": None
		})
