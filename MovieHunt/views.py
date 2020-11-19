from django.shortcuts import render, redirect
from django.http import HttpResponse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

from .models import popularMovies

new_set = list()

movie_attributes = joblib.load('contentBased_model.sav')

# Create your views here.
def home(request):
	popular_movies = joblib.load('popularity_model.sav')
	popular_movies = popular_movies['title'].to_list()
	popular_movies = popular_movies[:10]
	movies = list()
	movie_posters = [
		"The_shawshank_redemption.jpg", "The_godfather.jpg", "Dilwale_Dulhania_Le_Jayenge_poster.jpg",
		"The_dark_knight.jpg","Fight club.jpg", "Pulp_fiction.jpg", "Schildlers_list.jpg", "Whiplash.jpg",
        "Spirited_away.jpg", "LifeisBeautiful.jpg"
	]
		
	for i in range(10) :
		movie_obj = popularMovies()
		movie_obj.name = popular_movies[i]
		movie_obj.image = movie_posters[i]
		movies.append(movie_obj)
	
	return render(request, 'index.html', {"movies": movies})


def about(request):
	return render(request, "about.html")

def combine_features(row):
	try:
		return row['genres']+" "+row['overview']+" "+row['tagline']
	except:
		print("error",row) 

def get_title_from_index(index):
	return movie_attributes[movie_attributes.index==index]["title"].values[0]

def get_index_from_title(title):
	return movie_attributes[movie_attributes.title==title]["index"].values[0]

def search_movie(request):
	search_field = request.GET["search_field"]
	recommendation = recommend(search_field)
	recommendation = recommendation[:10]
	movie_posters = ["The_shawshank_redemption.jpg"]
	return render(request, 'search.html',{"recommendation":recommendation, "movie_posters":movie_posters})


def recommend(movie_user_likes):
    
    features = ['genres','overview','tagline']
    
    #create a column in df which combines all selected feature
    for feature in features:
        movie_attributes[feature] = movie_attributes[feature].fillna('')
        
    #each row individually
    movie_attributes["combine_features"] = movie_attributes.apply(combine_features,axis=1) 
    
    #create count matrix from this new combined column
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(movie_attributes["combine_features"])
    
    #compute the cosine similarity based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix)
    movie_index = get_index_from_title(movie_user_likes)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
    i=0
    for movie in sorted_similar_movies:
        new_set.append(get_title_from_index(movie[0]))
        i=i+1
        if(i>11):
            return list(new_set)	

Users = {"1":"movie","2":"movie","3":"movie","4":"movie"}
def signin(request):
    
    username = request.POST["uname"]
    password = request.POST["psw"]
    for key,value in Users.items():
        if key == username:
            if value == password:
                return render(request,'signin.html')

        else:
            return render(request,'index.html')

                
def logout(request):
    return redirect('/')