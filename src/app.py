import pickle
import streamlit as st
import requests
import os

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"http://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            full_path = "https://via.placeholder.com/500x750?text=No+Image"
        print(f"Poster URL: {full_path}")  # Debug statement
        return full_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies_name = []
        recommended_movies_poster = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]]['movie_id']
            recommended_movies_poster.append(fetch_poster(movie_id))
            recommended_movies_name.append(movies.iloc[i[0]].title)
        return recommended_movies_name, recommended_movies_poster
    except Exception as e:
        st.error(f"Error during recommendation: {e}")
        return [], []

# Streamlit app
st.header("Film Recommendation System using Machine Learning")

# Load data
movies = pickle.load(open(os.path.join('C:/Users/KIIT01/Desktop/project/artificats/movie_list.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join('C:/Users/KIIT01/Desktop/project/artificats/similarity.pkl'), 'rb'))

# User input
movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a film to get a recommendation',
    movie_list
)

# Show recommendations
if st.button('Show Recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    if recommended_movies_name:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.text(recommended_movies_name[i])
                st.image(recommended_movies_poster[i])
