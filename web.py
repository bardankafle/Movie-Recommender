import streamlit as st
import pickle
import pandas as pd
import requests
import config

with open('style.css') as f:
    st.markdown(f'<style>{(f.read())}<style>', unsafe_allow_html=True)


movies_dict = pickle.load(open('model/movie_dict.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])

    recommend_list = []
    recommend_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_posters.append(get_poster(movie_id))
        recommend_list.append(movies.iloc[i[0]].title)

    return recommend_list,recommend_posters

def get_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US".format(movie_id = movie_id, API_KEY = config.API_KEY)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

st.title('Movie Recommender System')

movie_option = st.selectbox(
    'What movie would you like a recommendation of?',
    movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(movie_option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])