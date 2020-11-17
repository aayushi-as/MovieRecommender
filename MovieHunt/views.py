from django.shortcuts import render
import joblib

# Create your views here.
def home(request):
    popular_movies = joblib.load('popularity_model.sav')
    popular_movies = popular_movies['title'].to_list()
    popular_movies = popular_movies[:10]
    return render(request, 'index.html', {"popular_movies": popular_movies})

def about(request):
    return render(request, "about.html")
