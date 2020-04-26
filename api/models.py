from django.db import models

# Create your models here.
class Game(models.Model):
	gameID = models.CharField(max_length=6)
	freeParking = models.IntegerField(default=0)

class Player(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	cookie = models.CharField(max_length=16)
	
	name = models.CharField(max_length=16)
	holdings = models.IntegerField(default=1500)

class Transfer(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)

	fromPrincipal = models.CharField(max_length=16)
	toPrincipal = models.CharField(max_length=16)
	amount = models.IntegerField()
