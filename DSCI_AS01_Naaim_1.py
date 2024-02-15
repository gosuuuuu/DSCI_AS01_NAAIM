import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(layout="wide")
col1, col2 = st.columns([0.5, 0.5])

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

# Visualization 1
with col1:

    # Filter
    st.subheader('Visualization 1')
    all_genres = [genre for sublist in m_data['Genre'] for genre in sublist]
    no_genre = pd.Series(all_genres).value_counts()
    genre_selected = st.selectbox("Filter by Genre:",
    options=["Show All"] + all_genres ,
    index=0 )

    if genre_selected != "Show All":
        filtered_data = m_data[m_data['Genre'].apply(lambda genres: genre_selected in genres)]
    else:
        filtered_data = m_data.copy() 

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1 = sns.barplot(x = no_genre.values, y = no_genre.index, 
                    palette=np.where(no_genre.values == np.max(no_genre.values), '#B9484E','#5A86AD'))
    ax1.bar_label(ax1.containers[0], padding=5)
    ax1.set_xlabel('No of Genre')
    plt.title('Genres in Top 1000 IMBD Movies')
    st.pyplot(fig)

# Visulization 2
# st.write("Visualization 1")
# top10_gross = m_data[['Director','Gross']].groupby('Director').agg(sum_grossed = ('Gross','sum'))
# top10_gross = top10_gross.reset_index().sort_values('sum_grossed',ascending=False).head(10)
# top10_gross

# all_stars = m_data[['Star1', 'Star2', 'Star3', 'Star4']].apply(lambda row: ''.join(row), axis=1)

# fig, ax = plt.subplots(figsize=(10, 5))
# stars = all_stars.head(10)
# ax = sns.barplot(x = top10_gross['sum_grossed'], y = top10_gross['Director'],
#                  palette=np.where(top10_gross['sum_grossed'] == np.max(top10_gross['sum_grossed']), '#2a9d8f','#264653'))

# ax.set_xlabel('Total (in Thousand Dollar)')
# labels, location = plt.xticks()
# plt.xticks(labels, (labels/1000).astype('int'))
# plt.title('Top 10 Directors who earned the highest Grossed Revenue')
# st.pyplot(fig)

with col2:
    st.subheader('Visualization 2')
    df_scatter = m_data.copy()
    # df_scatter['Multiple_genre'] = m_data['Genre'].apply(lambda x: str(len(x)) + ' Genre' )

    fig, ax2 = plt.subplots(figsize=(8, 5))
    ax2=sns.scatterplot(df_scatter, x='Gross', y='IMDB_Rating')
    #ax2.grid(True, alpha=0.5)
    #plt.xlim(0,3000000)
    plt.title('Scatterplot Grossed in $ Vs IMDb Rating')
    st.pyplot(fig)

col3, col4 = st.columns([0.5,0.5])

with col3:

    fig, ax3 = plt.subplots()
    ax3.pie(all_genres, autopct='%.2f%%', labels=all_genres.index)
    ax3.legend(title = 'Genres', loc = 'right', bbox_to_anchor=(1.2, .5))
    plt.title('Multiple Genre in Top 1000 IMDB Movies', fontdict={'fontsize':14})
    st.pyplot(fig)