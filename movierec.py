import numpy as np
import pandas as pd

links_df = pd.read_csv('data/links.csv')
movies_df = pd.read_csv('data/movies.csv')
ratings_df = pd.read_csv('data/ratings.csv')
tags_df = pd.read_csv('data/tags.csv')

movies_rate_df = movies_df.merge(ratings_df, on='movieId')

movie_title = input('Input your favorite movie name (with release year) (example: John Wick (2014)): ')
rec_movies = []

movies_db = movies_rate_df[movies_rate_df['title'] == movie_title].sort_values(by='rating', ascending=False)

#10 people rated this movie highest
for userId in movies_db.iloc[:10]['userId'].values:
    #list of rated movies of this user
    rate_movies = movies_rate_df[movies_rate_df['userId'] == userId]
    #3 highest rated movies of this user, excluding the movie from input
    rate_movies = rate_movies[rate_movies['title'] != movie_title].sort_values(by='rating', ascending=False).iloc[:3]
    
    rec_movies.extend(list(rate_movies['title'].values))

rec_movies = np.unique(rec_movies)
    
#Soft movies in the recommend list by genres similarity
input_genres = movies_rate_df[movies_rate_df['title'] == movie_title].iloc[0]['genres'].split('|')
similar_genre_counter = {}

for movie in rec_movies:
    movie_genres = movies_rate_df[movies_rate_df['title'] == movie].iloc[0]['genres'].split('|')
    sgc = 0
    
    for genre in input_genres:
        if genre in movie_genres:
            sgc += 1
    
    similar_genre_counter[movie] = sgc
    
    
rec_movies = sorted(similar_genre_counter, key=lambda x: similar_genre_counter[x], reverse=True)
print('\nWe have found these movies for you: ')
for movie in rec_movies:
    print(movie)