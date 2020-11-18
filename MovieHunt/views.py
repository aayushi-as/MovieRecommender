from django.shortcuts import render
import joblib

# Create your views here.
def home(request):
    popular_movies = joblib.load('popularity_model.sav')
    popular_movies = popular_movies['title'].to_list()
    popular_movies = popular_movies[:6]

    movie_posters = ["The_shawshank_redemption.jpg", "The_godfather.jpg", "Dilwale_Dulhania_Le_Jayenge_poster.jpg", 
    "The_dark_knight.jpg","Fight club.jpg", "Pulp_fiction.jpg"
    ]

    return render(request, 'index.html', {"popular_movies": popular_movies, "movie_posters": movie_posters})


def about(request):
    return render(request, "about.html")
