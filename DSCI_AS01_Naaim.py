print('Assignment1')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

m_data = pd.read_csv("imdb_top_1000.csv")
st.write("BEFORE")
st.write(m_data)

# DATA CLEANING

# Check Missing Value
# st.write("Misising Value")
# count_missing = st.write(m_data.isna().sum().sort_values(ascending=False))

# Check Duplicate
# st.write("Duplicate")
#st.write(m_data.duplicated().sum())

# Drop Poster Link (Unnessary)
m_data.drop('Poster_Link', axis = 1, inplace=True)

# Replace Missing Value Metascore to Average number in Whole Number 
m_data['Meta_score'].fillna(m_data['Meta_score'].mean().round(0), inplace=True)

# Replace Null Gross into 0
#m_data['Gross'].fillna(0, inplace=True)

# Drop empty Rows without Certificates and Griss
m_data.dropna(subset=['Certificate'], inplace=True)
m_data.dropna(subset=['Gross'], inplace=True)
# st.write(m_data)

# Listing Movie Genre
m_data['Genre'] = m_data['Genre'].apply(lambda x: x.split(', '))

# Check Missing Value after Cleaning
# st.write("Misising Value")
# count_missing = st.write(m_data.isna().sum().sort_values(ascending=False))

st.write("AFTER")
st.write(m_data)

# Visualization

all_genres = [genre for sublist in m_data['Genre'] for genre in sublist]
genre_counts = pd.Series(all_genres).value_counts()
genre_counts.index