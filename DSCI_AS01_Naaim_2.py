import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(layout="wide")
#col1, col2 = st.columns([0.5, 0.5])

m_data = pd.read_csv("imdb_top_1000.csv")

#  Data Cleaning
m_data.drop('Poster_Link', axis = 1, inplace=True)

m_data['Meta_score'].fillna(m_data['Meta_score'].mean().round(0), inplace=True)

m_data.dropna(subset=['Certificate','Gross'], inplace=True)

m_data['Genre'] = m_data['Genre'].apply(lambda x: x.split(', '))

# Visualization

st.title('Movie Analysis')
st.write('This app analyses Movie in IMDB Dataset')
st.subheader('Scatter Plot')

# Filter
rating = st.slider('Maximum Rating', min_value=7.0, max_value=10.0, step=0.1, value=7.0)
gross = st.slider('Maximum Gross', min_value=0, max_value=800, step=100, value=0)

m_data['IMDB_Rating'] = m_data['IMDB_Rating'].astype(float)
m_data['Gross'] = m_data['Gross'].str.replace(',', '').astype(float)

filtered_data = m_data[(m_data['IMDB_Rating'] >= rating) & (m_data['Gross'] >= gross)]

plt.figure(figsize=(12,4))
sns.scatterplot(data= filtered_data, x='Gross', y='IMDB_Rating')
plt.grid(True, alpha=0.5)
plt.xticks(ticks=range(0, 850, 50), labels=[str(x) for x in range(0, 850, 50)])
plt.title('Scatterplot Grossed in $ Vs IMDb Rating')
st.pyplot(plt) 

