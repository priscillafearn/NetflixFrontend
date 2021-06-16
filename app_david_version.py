import streamlit as st
import requests
import numpy as np
import pandas as pd

st.header("Movie Score Prediction")

analysis = st.sidebar.selectbox ('Select an Option', ['Search For a Movie', 'Select Movie Features'])

if analysis == "Search For a Movie":
      #st.selectbox ('Select A Movie ', ['Inception', 'Fast and Furious','Mamma Mia'])
      movie = st.text_input("Enter the Movie Name") 
      movie
      #if(st.button('Submit')): 
        #result = movie.title() 
        #st.success(result) 
      url = f'http://www.omdbapi.com/?t={movie}&apikey=ef5507df'
      response = requests.get(url).json()
      st.image(response["Poster"])
      params = {"year" : response["Year"],
                "rated":response["Rated"],
                "runtime" :response["Runtime"],
                "country" : response["Country"]
                }
      
      st.write(response["Year"])
      st.write(response["Rated"])
      st.write(response["Runtime"])
      st.write(response["Country"])
      
      response = requests.get(url, params = params).json()
      
      #st.write(response)
      
      
elif analysis == "Select Movie Features":
      
        kids = ['TV-G', 'TV-PG', 'Kid', 'TV-Y7', 'TV-Y7-FV', 'TV-Y', 'E']
        teens = ['TV-13', 'TV-14', 'PG-13', 'PG', 'M']
        over_17 = ['TV-MA', 'NC-17', 'R', '18 and over', 'Unrated', 'UNRATED']
      
      year = st.text_input("Year") 
      runtime = st.slider ("runtime (min)",1,400,1)
      rated = st.selectbox([kids,teens,over_17])
      country = st.text_input("country")
      
      url = "http://127.0.0.1:8000/predict?"
      params = {"year":year, "runtime":runtime, "rated":rated, "country":country}
      response = requests.get(url, params = params).json()
      st.write(response)
      
      
      
      
      #genre = st.multiselect("genre:",["Drama","Comedie","Thriller"])
      
      #actors = st.multiselect("actors:",["Leonardo Di Caprio","The Rock","Bruce Willis"])
      
      #directors = st.multiselect("directors:",["Leonardo Di Caprio","The Rock","Bruce Willis"])
      
      
      

      
      
      
      


