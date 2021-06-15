import streamlit as st
import requests
import pandas as pd
import os 
from PIL import Image

URL = "https://netflix-4zrwqiad6a-ew.a.run.app/predict?"  # call the API hosted by Docker
page_list = ['Movie Search','Build Your Own']


#showing a header
st.header('Movie Score Prediction')
view = st.sidebar.selectbox('Select',options = page_list)


# below is the code for the first page_list -> Movie Search
if view == page_list[0]:
    # add here input information 
    movie_title = st.text_input('Input movie name')
    
    #showing welcome picture
    image = Image.open('FrontEnd.jpg')
    st.image(image, caption='Netflix Movie Prediction', use_column_width=True)
    
    c1, c2 = st.beta_columns(2)
    
    # 1st step make IMDB API call 
    IMDb_url = f'http://www.omdbapi.com/?t={movie_title}&apikey=ef5507df'
    response = requests.get(IMDb_url).json()
    # st.write(response) 
    
    # printing the poster image
    c1.image(response["Poster"]) 
    
    # # parse response to get the information that I want 
    # put fetaures in the params dictionary
    params = {"year":response.get("Year", 2021),
              "rated":response.get("Rated", "Unrated"),
              "released":response.get("Released", "unavailable"),
              "runtime":response.get("Runtime", "120 min"),
              "genre": response.get("Genre", "unkown"),
              "director":response.get("Director", "unknown"),
              "writer": response.get("Writer", "unknown"),
              "actors": response.get("Actors", "unkonw"),
              "language":response.get("Language", "unkown"),
              "country":response.get("Country", "unkonw"),
              "production": response.get("Production", "unavailable"),
              "age": response.get("Year", 2021)
              }
           
    
    c2.write(f'Movie Tttle: {response["Title"]}')
    #c2.markdown(<*font color=‘red’>THIS TEXT WILL BE RED</*font>)
    c2.write(f'Year of release: {response["Year"]}')
    c2.write(f'Length of movie: {response["Runtime"]}')
    c2.write(f'Country of origin: {response["Country"]}')
    c2.write(f'Director: {response["Director"]}')
    c2.write(f'Actor: {response["Actors"]}')
    c2.write(f'Language: {response["Language"]}')
    c2.write(f'PG Rating: {response["Rated"]}')
    

    # call our IMDB API with param dictinary made from IMDB response 
    response = requests.get(URL, params = params).json()
    st.write(f'**The predicted score of the movie {movie_title} is {round(response["prediction"], 2)}**')


    

# below is the code for the other page_list -> Build Your Own
elif view == page_list[1]:
    
    st.text('Build Your Own')  
    
    # year = st.slider("Year of movie release", min_value = 1950, max_value= 2022, step=1)
    # runtime = st.number_input('Insert the runtime of the movie in minutes')
    runtime = st.slider('Total runtime of movie in minutes', min_value = 60, max_value = 200, step = 5)
    rated = st.selectbox('PG Rating', options = ["PG-13", "R", "Unrated", "E", "18 and over"])
    country = st.selectbox('Country of origin: ', options = ["Africa", "Asia", "Australia", "Europe", "South America", "United States", "New Zealand"])
    language = st.multiselect("Language:",["Arabic","Chinese","English", "French", "German", "Italian", "Russian", "Spanish", "Thai", "Vietnamese"])
    released = st.selectbox('Input month of movie release:', options=["January", "February", "March", "April", "May", "June", "July", " August", "September", "October", "November", "December"])
    # age = st.number_input('Insert here how many years ago was the movie luanched')
    writer = st.text_input('Input name of writer:')
    director = st.text_input('Input name of director:')
    actors = st.selectbox('Select names of actors', options= ["Christian Slater", "Scott Sampson",'Jan Decleir', 'Fedja van Huêt', 'Betty Schuurman', 'Tamar van den Dop'])
    genre = st.selectbox('Select genre of movie:', options= ["Documentary", "Animation", "Family" , "Crime", "Drama", "Mystery", "Comedy", "Crime", "Sci-Fi", "Thriller"])
    production =st.selectbox('Select production of movie:', options= ['Almerica Film', 'Jersey Films', "Columbia Pictures Corporation", 'Miramax Films' ,
                                                                       'Bedford Falls Productions', 'Universal Pictures',
                                                                       'First Snow Production', 'Capitol Films', 'Sony Pictures Classics'])
  
  
  

    # actors = st.text_input('Input names of actors here')
    button = st.button('Rate my movie 🚀 ')
    
    if button:
   
        params_model = dict(
        year=2021,
        runtime=runtime,
        rated=rated,
        country=country,
        language=language,
        released=released,
        writer=writer,
        director=director,
        actors=actors,
        genre=genre,
        production=production, 
        age=0,
        )
        
    
        # enter here the address of your flask api
    

        
        response = requests.get(URL, params=params_model).json()
        
        st.write(f'The predicted score of your movie creation is of {round(response["prediction"], 2)}')
        
    
 