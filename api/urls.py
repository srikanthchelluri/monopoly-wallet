from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('game/create/', csrf_exempt(views.game_create), name='game-create'),
    path('game/join/', csrf_exempt(views.game_join), name='game-join'),
    path('game/refresh/', csrf_exempt(views.game_refresh), name='game-refresh'),
    path('game/transfer/', csrf_exempt(views.game_transfer), name='game-transfer'),
    path('game/bank/', csrf_exempt(views.game_bank), name='game-bank'),
    path('game/freeparking/', csrf_exempt(views.game_freeparking), name='game-freeparking'),
]
