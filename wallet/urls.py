from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    re_path('game/(?P<gameID>[0-9]{6})', views.game, name='game'),

    path('api/v1/', include('api.urls')),
]
