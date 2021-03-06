import streamlit as st
import requests
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff


URL = "https://netflix-4zrwqiad6a-ew.a.run.app/predict?"  # call the API hosted by Docker
page_list = ['Movie Search','Build Your Own']


#Adding the title with markdown which allows you to edit the colour and font 
st.markdown("<h1 style='text-align: center; color: Black;'>Movie Score Prediction</h1>", unsafe_allow_html=True)

#Add the sidebar which will include all the pages included in the above page_list 
view = st.sidebar.selectbox('Select',options = page_list)

# below is the code for the first page_list -> Movie Search
if view == page_list[0]:
    # add here input information 
    movie_title = st.text_input('Input movie title :')
    
    if movie_title: 
        #Editting the visual to be made of 2 columns 
        c1, c2 = st.beta_columns(2)
        
        # 1st step make IMDB API call 
        IMDb_url = f'http://www.omdbapi.com/?t={movie_title}&apikey=ef5507df'
        response = requests.get(IMDb_url).json()
        # st.write(response) 
        
        #Adding the poster image
        c1.image(response["Poster"]) 
        
        #Adding the fetaures in the params dictionary
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
                "age": response.get("Year", 2021),
                "plot": response.get("Plot", "unavailable"),
                }
            
        
        c2.write(f'**Movie Title**: {response["Title"]}')
        c2.write(f'**Year of Release**: {response["Year"]}')
        c2.write(f'**Length of Movie**: {response["Runtime"]}')
        c2.write(f'**Country of Origin**: {response["Country"]}')
        c2.write(f'**Director**: {response["Director"]}')
        c2.write(f'**Actors**: {response["Actors"]}')
        c2.write(f'**Language**: {response["Language"]}')
        c2.write(f'**PG Rating**: {response["Rated"]}')
        c2.write(f'{response["Plot"]}')

        # call our IMDB API with param dictinary made from IMDB response 
        response = requests.get(URL, params = params).json()
        
        ## Assigning green color for good prediciton movies and red color for bad prediction movies
        url = "merged_movies_by_index.csv" #Note that this is a file saved locally
        df = pd.read_csv(url)
        x = df['avg_review_score']
        
        
        if response["prediction"] > 3:
            st.markdown('<style>h1{color: green;}</style>', unsafe_allow_html=True)
            st.subheader(f' The predicted score is {round(response["prediction"], 2)}/5') 
            
            st.markdown("<h3 style='text-align: left; color: Green;'> Investment Confirmed</h1>", unsafe_allow_html=True)
            #st.balloons()
            
            distribution = st.button('show review score distribution')
            if distribution:
    
                arr = x
                fig, ax = plt.subplots()
        
                
                sns.distplot(df["avg_review_score"],hist = False, color = "r",ax = ax)
                ax.axvline(x=response["prediction"], c="b")
                st.pyplot(fig)
                
                percentile = round(1 - (df['avg_review_score'] > response["prediction"]).mean(),2)
                percentile = '{:.0%}'.format(percentile)
                st.subheader(f"This movie has a better review score than {percentile} of movies available on Netflix")
                
                    
        
        else:
            st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)
            st.subheader(f' The predicted score is {round(response["prediction"], 2)}/5') 
 
            st.markdown("<h3 style='text-align: left; color: Red;'> Investment Declined</h1>", unsafe_allow_html=True)
            
            distribution = st.button('show review score distribution')
            if distribution:
    
                arr = x
                fig, ax = plt.subplots()
            
                
                sns.distplot(df["avg_review_score"],hist = False, color = "r",ax = ax)
                ax.axvline(x=response["prediction"], c="b")
                st.pyplot(fig)
                
                percentile = round(1 - (df['avg_review_score'] > response["prediction"]).mean(),2)
                percentile = '{:.0%}'.format(percentile)
                st.subheader(f"This movie has a better review score than {percentile} of movies available on Netflix")     

    else:
        
        #showing welcome picture
        st.image('final_pic.png')

# below is the code for the other page_list -> Build Your Own
elif view == page_list[1]:
    
    st.header('Build Your Own')
    runtime = st.slider('Total runtime of movie in minutes', min_value = 60, max_value = 200, step = 5)
    c1, c2 = st.beta_columns(2)
     
    rated = c1.selectbox('PG Rating', options = ["PG-13", "R", "Unrated", "E", "18 and over"])
    country = c1.selectbox('Country of Origin: ', options = ["Africa", "Asia", "Australia", "Europe", "South America", "United States", "New Zealand"])
    language = c1.multiselect("Language:",["Arabic","Chinese","English", "French", "German", "Italian", "Russian", "Spanish", "Thai", "Vietnamese"])
    writer = c1.selectbox('Input Name of Writer:',options = ["Quentin Tarantino","Steven Spielberg","Martin Scorsese","Francis Ford Coppola","Stanley Kubrick"])
    director = c2.selectbox("Select Names of Director:",options = ['Woody Allen','Alfred Hitchcock','Steven Spielberg', 'Clint Eastwood','Mike van Diem','Kirby Dick','Yasuhiro Horiuchi','Elliott Nugent','Dwight Hemion, Peter Israelson'])
    actors = c2.multiselect('Select Names of Actors', options= ['Jack Nicholson','Arnold Schwarzenegger', 'Sylvester Stallone','Robin Williams','Robert De Niro',' Scott Sampson','Jan Decleir',' Fedja van Hu??t',' Betty Schuurman',' Tamar van den Dop'])
    genre = c2.multiselect('Select Genre of Movie:', options= ["Documentary", "Animation", "Family" , "Crime", "Drama", "Mystery", "Comedy", "Crime", "Sci-Fi", "Thriller"])
    production =c2.selectbox('Select Production of Movie:', options= ['Almerica Film', 'Jersey Films', "Columbia Pictures Corporation", 'Miramax Films' ,
                                                                       'Bedford Falls Productions', 'Universal Pictures',
                                                                       'First Snow Production', 'Capitol Films', 'Sony Pictures Classics'])
  
    button = c1.button('Rate my movie ???? ')
    
    
    if button:
   
        params_model = dict(
        year=2021,
        runtime=runtime,
        rated=rated,
        country=country,
        language=language,
        released="November",
        writer=writer,
        director=director,
        actors=actors,
        genre=genre,
        production=production, 
        age=0,
        )
        
        # flask api
        
        response = requests.get(URL, params=params_model).json()
        
        
        if response["prediction"] > 3:
            
            st.markdown('<style>h1{color: green;}</style>', unsafe_allow_html=True)
            st.subheader(f' The predicted score is {round(response["prediction"], 2)}/5') 
            st.markdown("<h3 style='text-align: left; color: Green;'> Investment Confirmed</h1>", unsafe_allow_html=True)
            #st.balloons()
            
    
        
        else:
            st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)
            st.subheader(f' The predicted score is {round(response["prediction"], 2)}/5') 
            st.markdown("<h3 style='text-align: left; color: Red;'> Investment Declined</h1>", unsafe_allow_html=True)
            
    
        
       
        
    
 