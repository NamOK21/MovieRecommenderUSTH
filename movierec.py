import numpy as np
import pandas as pd

links_df = pd.read_csv('data/links.csv')
movies_df = pd.read_csv('data/movies.csv')
ratings_df = pd.read_csv('data/ratings.csv')
tags_df = pd.read_csv('data/tags.csv')

movies_rate_df = movies_df.merge(ratings_df, on='movieId')

movie_title = input('Input your fav movie name (with release year): ')

movie_in_db = movies_rate_df['title'] == movie_title

if not np.any(movie_in_db):
    # m = 'movie with title "{}", can\'t be found in the "data/movies.csv" file'
    # raise Exception(m.format(args.movie_name))
    similar_names_with_points = []
    added_titles = []
    movie_name_words = [w.strip() for w in movie_title.lower().split(' ')]

    # Exclude "the"
    if 'the' in movie_in_db:
        del movie_in_db[movie_in_db.index('the')]

    # Find the most similars by name
    for title in movies_rate_df['title'].values:
        points = 0

        for word in title.lower().split(' '):
            if word in movie_name_words:
                points += 1

        # Do not add movie to the list if it has already been added
        if title not in added_titles:
            similar_names_with_points.append((title, points,))
            added_titles.append(title)

    # Choose the biggest pointed five
    del added_titles, movie_name_words
    similar_names_with_points = sorted(similar_names_with_points, key=lambda x: x[1], reverse=True)[:5]

    # Ask user for input
    print()
    print('Movie with title "{}", can\'t be found in the "data/movies.csv" file.'.format(movie_title))
    print('These are the most similar movie titles:')
    print()
    print('-' * 30)
    print('Index\tMovie title')

    for i, title in enumerate(similar_names_with_points):
        print('[' + str(i + 1) + ']:\t' + title[0]) 
    
    print('-' * 30)
    print()
    print('Please choose the index for one of the movie above. (Choose index 0 to exit)')
    movie_index = input('Movie index: ')

    try:
        movie_index = int(movie_index)
    except ValueError:
        print('Wrong index, process terminated.')
        exit(1)

    if movie_index == 0:
        exit()
    else:
        movie_title = similar_names_with_points[movie_index - 1][0]

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
print()
print('-' * 30)
print()

for movie in rec_movies:
    print(movie)

print('-' * 30)
