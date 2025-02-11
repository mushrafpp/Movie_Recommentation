Movie Recommendation System
This repository contains a Movie Recommendation System built using Python and Streamlit. 
The application recommends movies to users based on their input and provides detailed insights with movie posters fetched dynamically from an API.

Features
Personalized Recommendations: Suggests movies similar to the user's selected choice.
Dynamic Posters: Fetches movie posters in real-time using The Movie Database (TMDB) API.
Interactive UI: Built with Streamlit for an easy-to-use interface.
Error Handling: Handles API and file-loading errors gracefully.

Files
app.py: Core Streamlit application code for the recommendation system.
movie_dict.pkl: Dictionary containing movie details (required).
similarity.pkl: Precomputed similarity matrix for recommendations (required).
