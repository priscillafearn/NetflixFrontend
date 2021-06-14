import streamlit as st
import requests
from streamlit.proto.Selectbox_pb2 import Selectbox
import pandas as pd
import os 


# home path
home = os.getcwd()

# df path
df_path = os.path.join(home,"data/df_train.csv")

df = pd.read_csv(df_path)
#st.write(df.shape)


page_list = ['Movie Search','Build Your Own']

st.header('Movie Score Prediction')
view = st.sidebar.selectbox('Select',options = page_list)

# below is the code for the first page_list -> Movie Search
if view == page_list[0]:
    # add here input information 
    movie_title = st.text_input('Input movie name')
    # 1st step make IMDB API call 
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey=ef5507df'
    response = requests.get(url).json()
    # st.write(response) 
    
    # printing the poster image
    st.image(response["Poster"]) 
    
    # # parse response to get the information that I want 
    # put fetaures in the params dictionary
    params = {"year":response["Year"],
              "rated":response["Rated"],
              "Released":response["Released"],
              "runtime":response["Runtime"],
   #           "Genre":"Drama, Romance",
              "Director":response["Director"],
              "Writer": response["Writer"],
              "Actors": response["Actors"],
              "Language":response["Language"],
              "country":response["Country"]}
    
    # response
    # response = requests.get(url, params = params).json()
    # st.write(response)
    st.write(f'Title: ', response["Title"])
    st.write(f'Year of release: ', response["Year"])
    st.write(f'Length of movie: ', response["Runtime"])
    st.write(f'Country of origin: ', response["Country"])
    st.write(f'Director: ', response["Director"])
    st.write(f'Actor: ', response["Actors"])
    st.write(f'Language: ', response["Language"])
    st.write(f'PG Rating: ', response["Rated"])

    


    # call our IMDB API with param dictinary made from IMDB response 
    url = "http://127.0.0.1:8000/predict?"
    response = requests.get(url, params = params).json()
    st.write(response)


# below is the code for the other page_list -> Build Your Own
elif view == page_list[1]:
    
    st.text('Build Your Own')  
    
    #vadd here input information
    #year = st.text_input('Year of movie release')
    # movie_title = st.text_input('Input movie name')
    # movie_title = st.text_input('Input movie name')
    # movie_title = st.text_input('Input movie name')
    # movie_title = st.text_input('Input movie name')
    # movie_title = st.text_input('Input movie name')
    
    
    year = st.slider("Year of movie release", min_value = 1950, max_value= 2022, step=1)
    runtime = st.slider('Total runtime of movie in minutes', min_value = 30, max_value = 500, step = 5)
    rated = st.selectbox('PG Rating', options = ["PG13", "teens", "kids"])
    country = st.selectbox('Is this an American movie?', options = ["Yes", "No"])
    language = st.text_input('Input language here')
    released = st.text_input('Input month of released here')
    writer = st.text_input('Input name of writer here')
    director = st.text_input('Input name of director here')
    
   
    params_model = dict(
    year=year,
    runtime=runtime,
    rated=rated,
    country=country,
    language=language,
    released=released,
    writer=writer,
    director=director
    )
    
 
    # enter here the address of your flask api
   

    url_model = "http://127.0.0.1:8000/predict?"
    
    response = requests.get(url_model, params=params_model()).json()

    prediction = response

    pred = prediction['prediction']

    pred