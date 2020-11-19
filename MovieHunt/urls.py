from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name="about"),
    path('search_movie/', views.search_movie, name="search_movie"),
    path('signin/',views.signin, name = 'signin'),
    path('logout/',views.logout, name = 'logout')
]