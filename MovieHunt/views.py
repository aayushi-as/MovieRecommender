from django.shortcuts import render, redirect
from django.http import HttpResponse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from .models import popularMovies
import pandas as pd
from .models import CollaborativeMovies

movie_attributes = joblib.load('contentBased_model.sav')
similarity_df = joblib.load('collaborative_model.sav')

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
	print(recommendation)
	return render(request, 'search.html',{"recommendation":recommendation})


def recommend(movie_user_likes):
    new_set = list()
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
            return new_set

Users = {"1":"movie","2":"movie","3":"movie","4":"movie"}
def signin(request):
    uid = request.GET["uname"]
    password = request.GET["psw"]
    for key,value in Users.items():
        if key == uid:
            if value == password:
                rated_movies = []
                rated_results = []
                movie_ratings = pd.read_csv("ratings_small.csv")
                title_data = pd.read_csv("title_data.csv")

                movie_ratings = movie_ratings.drop(["timestamp"], axis=1)
                movie_ratings = movie_ratings.loc[movie_ratings['user_id'] == 1]

                ids = movie_ratings['movie_id'].to_list()
                ratings = movie_ratings['rating'].to_list()

                title_data = title_data.fillna(0, axis=1)
                title_data['movie_id'] = title_data['movie_id'].astype(int)

                
                for i in ids:
                    movie = title_data.loc[title_data.movie_id.eq(i), 'title'].item()
                    rated_movies.append(movie)

                for i in range(5):
                    obj = CollaborativeMovies()
                    obj.name = rated_movies[i]
                    obj.rating = ratings[i]
                    rated_results.append(obj)

                similar_movies = pd.DataFrame()

                # for movie, rating in rated_movies:
                for i in range(5):
                    similar_movies = similar_movies.append(get_similar_item(rated_movies[i], ratings[i]), ignore_index = True)

                similar_movies = similar_movies.sum().sort_values(ascending=False)
                similar_movies = similar_movies.to_frame()
                similar_movies['title'] = similar_movies.index
                List = similar_movies['title'].tolist()

                collaborative_results = []

                for movie in List:
                    if movie not in rated_movies:
                        collaborative_results.append(movie)
                        
                return render(request,'signin.html',{"rated_results": rated_results, "UserId": uid, "collaborative_results": collaborative_results})

        else:
            return render(request,'index.html')
            
def get_similar_item(title, rating):
    similarity_score = similarity_df[title]*(rating - 2.5)
    similarity_score = similarity_score.sort_values(ascending = False)
    return similarity_score.head(5)
                
def logout(request):
    return redirect('/')