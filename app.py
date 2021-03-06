# -*- coding: utf-8 -*-
# Import the Libraries
# Work with Data - the main Python libraries
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageOps # Image processing
import pickle

# Modeling and Prediction
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

#Create a title and a sub-title
st.write("""
# EMG Based Silent Speech Interface
Helps Predict Speech communicated by paralyzed individuals using  Machine Learning
""")

#Open and Display an Image
#image = Image.open('Diabetes Detection.png')
#st.image(image, use_column_width=True) # caption = 'ML', 

# COMPUTATION
st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example CSV input file](https://drive.google.com/drive/folders/1qafer1fZK-lTtFl2uDESPQUp_dbpxTxk?usp=sharing)
""")

# Collects user input features into dataframe
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
  input_df = pd.read_csv(uploaded_file)
  
# Combines user input features with entire penguins dataset
# This will be useful for the encoding phase
  with st.spinner('Processing CSV.....'):
    letters_raw = pd.read_csv('Data.csv')
    
    st.subheader('Training Data')
    st.write(letters_raw)

    try:
      letters = letters_raw.drop(columns=['Letter'])
    except:
      letters = letters_raw

  df = pd.concat([input_df, letters],axis=0)

  df = df[:1] # Selects only the first row (the user input data)

  # Displays the user input features
  st.subheader('User Input features')

  st.write(df)

  with st.spinner('Loading Model.....'):
    # Reads in saved classification model
    load_clf = pickle.load(open('EMG_clf.pkl', 'rb'))

  with st.spinner('Making Prediction.....'):
    # Apply model to make predictions
    prediction = load_clf.predict(df)
    prediction_proba = load_clf.predict_proba(df)


  st.subheader('Prediction')
  prediction = str(prediction)

  if prediction == '[[\'A\']]':
    n=0
    prediction = 'A'
  elif prediction == '[[\'B\']]':
    n=1
    prediction = 'Blank'
  elif prediction == '[[\'E\']]':
    n=2
    prediction = 'E'
  elif prediction == '[[\'I\']]':
    n=3
    prediction = 'I'
  elif prediction == '[[\'O\']]':
    n=4
    prediction = 'O'
  elif prediction == '[[\'U\']]':
    n=5
    prediction = 'U'

  prediction_proba = prediction_proba[0][n]
  prediction_proba = prediction_proba * 100
  prediction_proba = str(prediction_proba)+'%'

  st.success(prediction)

  st.subheader('Prediction Probability')
  st.success(prediction_proba)
else:
  st.success("Please Upload CSV file to Continue")
  while uploaded_file is not None:
    st.spinner('Waiting for CSV input....')
