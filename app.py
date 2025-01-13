import streamlit as st
import pickle
import pandas as pd
import requests
import time

# Fetch poster with retries and error handling
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            poster_path = data.get('poster_path', '')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
            else:
                return "https://via.placeholder.com/500"  # Default image for missing posters
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            st.error(f"Failed to fetch poster for movie ID {movie_id} after {max_retries} attempts. Error: {e}")
            return "https://via.placeholder.com/500"  # Return default image on persistent failure

# Recommend movies
def recommend(movie):
    try:
        movie_index = movies[movies["title"] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movie_list:
            movie_id = movies.iloc[i[0]].movie_id

            recommended_movies.append(movies.iloc[i[0]].title)
            # Fetch poster from API
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    except Exception as e:
        st.error(f"An error occurred while generating recommendations: {e}")
        return [], []

# Load data safely
try:
    movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
except FileNotFoundError:
    st.error("The file 'movie_dict.pkl' was not found. Please check the file path.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading 'movie_dict.pkl': {e}")
    st.stop()

try:
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("The file 'similarity.pkl' was not found. Please check the file path.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading 'similarity.pkl': {e}")
    st.stop()

# Create dataframe from loaded dictionary
movies = pd.DataFrame(movie_dict)

# Streamlit App
st.title('Movie Recommendation System')

# Dropdown to select movie
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    if not names:
        st.error("No recommendations could be generated. Please try again later.")
    else:
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.text(name)
                st.image(poster)
