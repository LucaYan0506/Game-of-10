from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index_view, name="index"),
    path('guest/',views.generateGuestUser, name="guest"),
    path('match/',views.match_view, name="match"),
    path('submit/',views.submitAction, name="submit"),
    path('getMyTurn/',views.getMyTurn, name="getTurnInfo"),
]