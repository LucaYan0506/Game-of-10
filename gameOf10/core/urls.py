from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index_view, name="index"),
    path('test/',views.hello_guest, name="test"),
    path('match/',views.match_view, name="match"),
    path("convert/", include("guest_user.urls")),
]