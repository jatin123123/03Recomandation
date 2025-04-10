import streamlit as st
import pickle
import pandas as pd
import requests
import streamlit.components.v1 as components
import time

# --- Page Config ---
st.set_page_config(
    page_title="🎬 Movie Recommender",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎥"
)

# --- Google Fonts + Custom CSS Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #141e30, #243b55);
        color: white;
    }

    .movie-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 12px;
        overflow: hidden;
        cursor: pointer;
    }

    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 20px rgba(255, 255, 255, 0.1);
    }

    .recommend-button {
        background-color: #e50914;
        color: white;
        padding: 10px 24px;
        border-radius: 5px;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s ease;
    }

    .recommend-button:hover {
        background-color: #f40612;
    }

    .sidebar .sidebar-content {
        background: #1c1c1c;
    }
    </style>
""", unsafe_allow_html=True)

# --- Function to fetch poster from TMDB ---
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=bca61a9444d38552cee7ff2a1f1a1d82&language=en-US'
    response = requests.get(url)
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# --- Load data ---
movie_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Sidebar Branding ---
with st.sidebar:
    st.markdown("## 🎬 Movie Recommender")
    st.write("Get top 5 similar movies based on your favorite picks. Built using TMDB & Streamlit.")
    st.markdown("---")

# --- Movie Selection ---
st.markdown("## 🔍 Select a Movie")
selected_movie_name = st.selectbox("Choose a movie you like:", movies['title'].values)

# --- Recommendation Logic ---
def recommended(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# --- Recommend Button ---
if st.button('🎯 Recommend', help="Get similar movies!"):
    with st.spinner("Finding awesome recommendations... 🍿"):
        time.sleep(1.5)
        names, posters = recommended(selected_movie_name)

    st.markdown("## 🎥 Top 5 Recommendations")

    # Responsive Card-Based Layout
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{posters[i]}" style="width:100%; border-radius:10px; transition: opacity 0.5s ease;" />
                    <h5 style="text-align:center; margin-top: 10px;">{names[i]}</h5>
                </div>
            """, unsafe_allow_html=True)
