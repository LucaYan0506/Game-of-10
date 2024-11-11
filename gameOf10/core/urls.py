from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index_view, name="index"),
    path('profile/',views.showProfile, name="profile"),
    path('match/',views.match_view, name="match"),
    path('submit/',views.submitAction, name="submit"),
    path('getMyTurn/',views.getMyTurn, name="getTurnInfo"),
    path('discard/',views.discardCard, name="discardCard"),
    path('newGame/',views.newGameView, name="newGame"),
    path('login/',views.loginView, name="login"),
    path('register/',views.registerView, name="register"),
    path('sendCommand/',views.sendCommand, name="sendCommand"),
    path('commandDetected/',views.commandDetected, name="commandDetected"),

    #path('tutorial/',views.discardCard, name="discardCard"),
]