import pickle
import streamlit as st
import pandas as pd
import requests
import time

# ✅ Cache API responses to reduce TMDB requests
@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    # Get the API key from Streamlit Secrets
    api_key = st.secrets["tmdb_api_key"]

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    for attempt in range(3):  # ✅ Retry up to 3 times
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()

            # ✅ Handle missing posters
            poster_path = data.get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
            else:
                return "https://via.placeholder.com/500x750?text=No+Poster+Available"

        except requests.exceptions.RequestException as e:
            print(f"Error fetching poster for ID {movie_id}: {e}")
            time.sleep(1)  # wait before retry

    # fallback if all attempts fail
    return "https://via.placeholder.com/500x750?text=Poster+Unavailable"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        time.sleep(0.001)  # ✅ Avoid hitting API too fast

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

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
