import numpy as np
import pandas as pd
import ast
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv') 
movies = movies.merge(credits,on='title')
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

def convert(text):
    new_list = []
    for i in ast.literal_eval(text):
        new_list.append(i['name']) 
    return new_list 
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert)
movies['cast'] = movies['cast'].apply(lambda x:x[0:3])

def get_director(text):
    director_name = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            director_name.append(i['name'])
    return director_name
movies['crew'] = movies['crew'].apply(get_director)

movies['overview'] = movies['overview'].apply(lambda x:x.split())

def collapse(the_list):
    new_list = []
    for i in the_list:
        new_list.append(i.replace(" ",""))
    return new_list
movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new = movies.drop(columns=['overview','genres','keywords','cast','crew'])

new['tags'] = new['tags'].apply(lambda x: " ".join(x))

ps = PorterStemmer()
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new['tags'] = new['tags'].apply(stem)

cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(new['tags']).toarray()

similarity = cosine_similarity(vectors, Y=None)