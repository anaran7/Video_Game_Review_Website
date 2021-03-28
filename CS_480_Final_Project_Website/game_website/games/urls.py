from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='games-home'),
    path('login/', views.login, name='games-login'),
    path('register/', views.register, name='games-register'),
    path('user/', views.user, name='games-user'),
    path('singleGame/', views.singleGame, name='games-singleGame'),
    path('gameSearch/', views.gameSearch, name='games-gameSearch'),
    path('ESRB/', views.ESRB, name='games-esrb'),
    path('publisher/', views.publisher, name='games-publish'),
    path('releaseYear/', views.releaseYear, name='games-releaseYear'),
]