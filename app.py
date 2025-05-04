import pickle
import streamlit as st
import requests
import time


# Function to fetch poster image for a movie
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)  # Added timeout for the request
        response.raise_for_status()  # Raises an error if the status code is not 200
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"  # Placeholder if no poster found
    except requests.exceptions.RequestException as e:
        # Handle request errors gracefully
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"


# Function to recommend movies based on the selected movie
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        print(f"Error during recommendation: {e}")
        return [], []


# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# Loading the model data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

movie_list = movies['title'].values

# Selectbox for movie selection
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Button to trigger movie recommendation
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names:
        # Display recommended movies and their posters
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
    else:
        st.write("Sorry, no recommendations available. Please try again later.")

# Footer Section
st.markdown("""<hr style="margin-top: 50px;">
<div style="text-align: center;">
    <p>Created by <b>Rishabh</b> ⚡</p>
    <p>Email: <a href="mailto:lakhedarishabh7@gmail.com">lakhedarishabh7@gmail.com</a> | 
    Instagram: <a href="https://instagram.com/ya_sh5365" target="_blank">@ya_sh5365</a></p>
</div>""", unsafe_allow_html=True)

#streamlit run app.py
