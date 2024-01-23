from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_view, name="index"),
    path('match/',views.match_view, name="match"),
]