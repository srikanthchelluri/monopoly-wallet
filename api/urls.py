"""wallet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),

    path('game/create/', views.game_create, name='game-create'),
    path('game/join/', views.game_join, name='game-join'),
    path('game/refresh/', views.game_refresh, name='game-refresh'),
    path('game/transfer/', views.game_transfer, name='game-transfer'),
    path('game/bank/', views.game_bank, name='game-bank'),
    path('game/freeparking/', views.game_freeparking, name='game-freeparking'),
]
