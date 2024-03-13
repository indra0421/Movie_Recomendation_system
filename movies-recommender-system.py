# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:36:14 2024

@author: ASUS
"""
import numpy as np
import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(movie_title):
    response = requests.get('https://www.omdbapi.com/?apikey=40bd8a1a&t={}'.format(movie_title))
    data = response.json()
    return data['Poster']


    

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True , key = lambda x:x[1])[1:11]
    recommended_movies = []
    for i in movies_list:
        movie_id = i[0]
        recommended_movies_posters = []
        # fetching poster based on id --> from API call
        recommended_movies.append(movies_df['title'][movie_id])
        recommended_movies_posters.append(fetch_poster(movies_df['title'][movie_id]))
    
    return recommended_movies
        

# similarity = pickle.load(open("C:/Users/ASUS/Desktop/ML Projects/Movie Recomendation System/movie-recommender-system/similarity.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl",'rb'))
# movies_df = pd.read_pickle("C:/Users/ASUS/Desktop/ML Projects/Movie Recomendation System/movie-recommender-system/movies.pkl")
movies_df = pd.read_pickle("movies.pkl")
movies_list = movies_df['title'].values

recommend('Avatar')


st.title('Movie Recommender System')

# select box 
# selecting a particular movie --> and list of all movie list
selected_movie = st.selectbox(
    'Select your Movie',
    movies_list
 )

if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    st.title('Recommended Movies')
    
    num_cols = 3 # Adjust the number of columns per row here
    
    for i in range(0, len(recommendations), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            if i + j < len(recommendations):                
                cols[j].image(fetch_poster(recommendations[i + j]), use_column_width=True)
               
                cols[j].write(recommendations[i + j])