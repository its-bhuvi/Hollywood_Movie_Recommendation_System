import base64
import pickle
from io import BytesIO

import pandas as pd
import streamlit as st
import requests
import numpy
from PIL.Image import Image


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title(':gray[Movie Recommender System] :movie_camera: :clapper:')
#selected_movie_names = st.selectbox('Select the Name of Movie', movies['title'].values)
with open("background.jpg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode()
st.write(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{image_base64}");  # Replace with your image file path or base64 data
                background-size: cover;
                background-repeat: no-repeat;
                background-color: rgba(255, 255, 255, 0.9);

            }}

        </style>
        """,
        unsafe_allow_html=True,
)
#Title = st.markdown('<h1 style="color: #FFFFFF;">Movie Recommender System</h1>', unsafe_allow_html=True)

selected_movie_names = st.selectbox('Select the Name of Movie', movies['title'].values)
css = '''
<style>
    .stSelectbox [data-testid='stMarkdownContainer'] {
        color: #FFFFFF;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)

# Set the Streamlit app background using custom CSS
st.write(
    f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{image_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-color: rgba(255, 255, 255, 0.3);
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


def fetch_popularity(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=595c8ad66f3b89f4f113bfc6590a5d6d'.format(movie_id))
    data = response.json()
    popularity = data.get('popularity', 'N/A')  # Get popularity as a float or 'N/A' if not available
    return 'Popularity:- ' + str(round(popularity,2))

def fetch_vote_Avg(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=595c8ad66f3b89f4f113bfc6590a5d6d'.format(movie_id))
    data = response.json()
    vote_average = data.get('vote_average', 'N/A')  # Get popularity as a float or 'N/A' if not available
    return 'Rating :- ' + str(round(vote_average,2))


def fetch_release_date(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=595c8ad66f3b89f4f113bfc6590a5d6d'.format(movie_id))
    data = response.json()
    return 'Release Date:- ' + data['release_date']

def fetch_runtime(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=595c8ad66f3b89f4f113bfc6590a5d6d'.format(movie_id))
    data = response.json()
    runtime = data.get('runtime', 'N/A')  # Get popularity as a float or 'N/A' if not available
    return 'Runtime:- ' + str(runtime)+'min.'



def fetch_genres(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=595c8ad66f3b89f4f113bfc6590a5d6d')
    data = response.json()
    genres = [genre['name'] for genre in data['genres']]
    return 'Genres: ' + ', '.join(genres)



def fetch_tagline(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=595c8ad66f3b89f4f113bfc6590a5d6d'.format(movie_id))
    data = response.json()
    tagline = data.get('tagline')
    if tagline is not None:
        return 'Tagline:- ' + tagline
    else:
        return 'Tagline not available'

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=595c8ad66f3b89f4f113bfc6590a5d6d'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/original' + data['poster_path']

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = similarity[index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])
    recommend_list = []
    recommend_poster = []
    recommend_tagline= []
    recommend_genres= []
    recommend_runtimes = []
    recommend_popularities = []
    recommend_release_dates=[]
    recommend_vote_avg = []
    for i in movies_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_list.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
        recommend_tagline.append(fetch_tagline((movie_id)))
        recommend_genres.append(fetch_genres((movie_id)))
        recommend_runtimes.append(fetch_popularity(movie_id))
        #recommend_popularities.append(fetch_release_date(movie_id))
        recommend_release_dates.append(fetch_runtime(movie_id))
        recommend_vote_avg.append(fetch_vote_Avg(movie_id))
    return recommend_list, recommend_poster,recommend_tagline, recommend_genres, recommend_runtimes , recommend_release_dates, recommend_vote_avg


def fetch_movie_details(movie_name):
    # Use your API key and endpoint
    api_key = "595c8ad66f3b89f4f113bfc6590a5d6d"
    endpoint = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": api_key,
        "query": movie_name,
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if data.get("results"):
        movie = data["results"][0]
        id = movie.get("id", "N/A")
        title = movie.get("title", "N/A")
        tagline = movie.get("tagline", "N/A")
        release_date = movie.get("release_date", "N/A")
        genres=fetch_genres((id))
        overview = movie.get("overview", "N/A")
        vote_average = movie.get("vote_average", "N/A")
        poster_path = movie.get("poster_path")
        print("Genres:", genres)

        return title,tagline, release_date, genres, overview, vote_average, poster_path

    return None








#Title = st.markdown('<h1 style="color: #FFFFFF;">Movie Recommender System</h1>', unsafe_allow_html=True)

#page = st.experimental_get_query_params().get("page", "main")

if st.button('Enter'):
    selected_movie_details = fetch_movie_details(selected_movie_names)
    if selected_movie_details is not None:
        title,tagline, release_date, genres, overview, vote_average, poster_path = selected_movie_details

        st.write(f'<div style="display: flex; margin: 10px; ">\
                                 <div style="flex: 1; width: 200px;"><img src="https://image.tmdb.org/t/p/original{poster_path}" style="width: 200px;"></div>\
                                 <div style="flex: 2; text-align: left; margin-left:2em; margin-top:-1.4em; color: #FFFFFF;">\
                                     <h2 style="color: #FFFFFF;">{title}</h2>\
                                      <p> Rating: {round(vote_average, 2)}/10</p>\
                                     <p> Release date: {release_date}</p>\
                                     <p>Genres: {genres}</p>\
                                     <p style="max-height:250px">  {overview}</p>\
                                     </div>', unsafe_allow_html=True)
    else:
        st.write("Movie details not found.")

    names, posters, taglines, genres, runtime, release_date, vote_avg = recommend(selected_movie_names)


    st.write('<style>div.Widget.row-widget.stRadio div{flex-direction:row;}</style>', unsafe_allow_html=True)

    st.header(':gray[Top 5 Recommended Movies]', divider='rainbow')

    for i in range(5):
        if i < len(names) and i < len(posters):
            st.write(f'<div style="display: flex; margin: 10px; text-align: center;">\
                         <div style="flex: 1; width: 200px;"><img src="{posters[i]}" style="width: 200px;"></div>\
                         <div style="flex: 2; text-align: left; margin-left:2em; margin-top:-1.4em;color: #FFFFFF;">\
                             <h2 style="color: #FFFFFF;">{names[i]}</h2>\
                             <p>{taglines[i]}</p>\
                             <p>{genres[i] if i < len(genres) else ""}</p>\
                             <p>{runtime[i]}</p>\
                             <p>{vote_avg[i]}/10</p>\
                             <p>{release_date[i]}</p>\
                             <a target="_self" href={"details/home.html"}>google</a> </div>\
                       </div>', unsafe_allow_html=True)
        else:
            st.write(f'Data not available for recommendation {i + 1}')




# ... Your recommendation code ...

# Create a "View Details" section
