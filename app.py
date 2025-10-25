import pickle
import streamlit as st
import pandas as pd
import requests
import time
import os
import gdown

# ---------------------- Download similarity.pkl if missing ----------------------
if not os.path.exists("similarity.pkl"):
    print("Downloading similarity.pkl...")
    url = "https://drive.google.com/uc?id=1WxUdsXE3eooVYuyg0VoxWQx8OskDZbPJ"
    gdown.download(url, "similarity.pkl", quiet=False)


# ---------------------- Fetch movie poster ----------------------
@st.cache_data
def fetch_poster(movie_id):
    """
    Fetch the poster URL from TMDB API. Returns placeholder if not available.
    """
    api_key = os.environ.get("TMDB_API_KEY")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            print(f"No poster found for movie ID {movie_id}")
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"


# ---------------------- Recommend movies ----------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        # Ensure a valid URL is always added
        if not poster_url:
            poster_url = "https://via.placeholder.com/500x750?text=No+Poster+Available"
        recommended_posters.append(poster_url)
        time.sleep(0.001)

    return recommended_movies, recommended_posters


# ---------------------- Streamlit UI ----------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Type or select a movie title:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display movies and posters neatly
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx], use_container_width=True)

