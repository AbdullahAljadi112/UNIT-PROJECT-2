
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("tournaments/", views.tournaments, name="tournaments"),
    path("toggle-theme/", views.toggle_theme, name="toggle_theme"),
]
