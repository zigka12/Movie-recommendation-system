import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬")


# Custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load data
movies = pd.DataFrame(pickle.load(open('movies.pkl', 'rb')))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("🎬 Movie Recommender")

# OMDb API
OMDB_API_KEY = "9aee29da"

def fetch_poster(title):
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}")
    data = response.json()
    return data['Poster'] if data['Response'] == 'True' and data['Poster'] != 'N/A' else None

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return [], []
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_titles = []
    recommended_posters = []
    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        recommended_titles.append(title)
        recommended_posters.append(fetch_poster(title))
    return recommended_titles, recommended_posters

selected_movie = st.selectbox("Choose a movie", movies['title'].tolist())

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    
    if names:
        st.subheader("Top 5 similar movies:")
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            if posters[idx]:
                col.image(posters[idx], caption=names[idx], use_container_width=True)
            else:
                col.write(names[idx])
    else:
        st.warning("Movie not found in the dataset.")
