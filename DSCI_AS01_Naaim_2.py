import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
#st.set_page_config(layout="wide")
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


# 1st Visualization
st.subheader('1st Visualization')

m_data['IMDB_Rating'] = m_data['IMDB_Rating'].astype(float)
m_data['Gross'] = m_data['Gross'].str.replace(',', '').astype(float)
rating = st.slider('Maximum Rating', min_value=7.0, max_value=10.0, step=0.1, value=7.0)

filtered_data = m_data[(m_data['IMDB_Rating'] >= rating)]

plt.figure(figsize=(10,5))
sns.scatterplot(data= filtered_data, x='Gross', y='IMDB_Rating')
plt.grid(True, alpha=0.5)
plt.xlabel('Gross')
plt.ylabel('IMDB Rating')
st.pyplot(plt)


# 2nd Visualization 
st.subheader('2nd Visualization')
top10_gross = m_data[['Director', 'Gross']].groupby('Director').agg(sum_grossed=('Gross', 'sum'))
top10_gross = top10_gross.reset_index().sort_values('sum_grossed', ascending=False).head(10)

all_stars_counts = pd.concat([m_data['Star1'], m_data['Star2'], m_data['Star3']]).value_counts()

# Filter Diretor
selected_director = st.selectbox("Select Director", ["All"] + list(m_data['Director']))
if selected_director != "All":
    filtered_data = m_data[m_data['Director'] == selected_director]
    st.write(filtered_data)
else:
    plt.figure(figsize=(10, 5))

    # Filter Gross
top10_gross = m_data[['Director', 'Gross']].groupby('Director').agg(sum_grossed=('Gross', 'sum'))
top10_gross = top10_gross.reset_index().sort_values('sum_grossed', ascending=False).head(10)

gross_min = int(top10_gross['sum_grossed'].min())
gross_max = int(top10_gross['sum_grossed'].max())
gross_range = st.slider("Gross Total Range", gross_min, gross_max, (gross_min, gross_max))

filtered_data = top10_gross[(top10_gross['sum_grossed'] >= gross_range[0]) & (top10_gross['sum_grossed'] <= gross_range[1])]

    # Custom palette based on the maximum gross revenue
palette = np.where(filtered_data['sum_grossed'].values == np.max(filtered_data['sum_grossed'].values), '#2a9d8f', '#264653')

ax = sns.barplot(x='sum_grossed', y='Director', data=filtered_data, palette=palette)

ax.set_xlabel('Total Gross (in Thousand Dollars)')
plt.xticks()
plt.title('Directors by Grossed Revenue')
st.pyplot(plt)

# 3rd Visualization
st.subheader('3rd Visualization')
m_data['Runtime'] = m_data['Runtime'].str.replace(' min', '').astype(int)
top10_longest = m_data[['Series_Title','Runtime']].sort_values('Runtime', ascending=False).head(10)

# Filter 
# Add a filter for the maximum runtime of movies with a step size of 50
max_runtime = st.slider('Maximum Runtime', min_value=50, max_value=int(m_data['Runtime'].max()), value=int(m_data['Runtime'].max()))

# Filter the DataFrame based on the selected maximum runtime
filtered_data = m_data[m_data['Runtime'] <= max_runtime]

# Sort and get the top 10 longest movies
top10_longest = filtered_data[['Series_Title','Runtime']].sort_values('Runtime', ascending=False).head(10)

plt.figure(figsize=(10,5))
ax = sns.barplot(x = top10_longest['Runtime'], y = top10_longest['Series_Title'], 
                 palette=np.where(top10_longest['Runtime'] == np.max(top10_longest['Runtime']), '#2a9d8f','#264653'))

plt.title('Top 10 Movies with the Longest Duration')
st.pyplot(plt) 

# 4th Visualization
st.subheader('4th Visualization')
all_genres = [genre for sublist in m_data['Genre'] for genre in sublist]
genre_counts = pd.Series(all_genres).value_counts()

genres = ['All'] + genre_counts.index.tolist()

# Create a Streamlit radio button to select genre
selected_genres = st.multiselect("Select Genre", genres, default=['All'])

# Filter data based on selected genre
if 'All' in selected_genres:
    filtered_genre_counts = genre_counts
else:
    filtered_genre_counts = genre_counts[selected_genres]

plt.figure(figsize=(10,5))
ax = sns.barplot(x=filtered_genre_counts.index, y=filtered_genre_counts.values, 
                 palette=np.where(filtered_genre_counts.values == np.max(filtered_genre_counts.values), '#2a9d8f', '#264653'))
ax.bar_label(ax.containers[0], padding=5)
ax.set_ylabel('Total')
plt.title(f'Genres in Top 1000 IMBD Movies')
plt.xticks(rotation=45)  # Rotate x-labels for better readability
st.pyplot(plt)

# Visualization 5th
st.subheader('5th Visualization')

# Filter for runtime
runtime_filter = st.radio("Select Runtime Filter", ['All', 'Longger Than 1 Hours', 'Less Than 1 Hours'])

# Filtered data based on selected filter
if runtime_filter == 'All':
    filtered_data = m_data['Runtime']
elif runtime_filter == '>=120':
    filtered_data = m_data[m_data['Runtime'] >= 120]['Runtime']
else:
    filtered_data = m_data[m_data['Runtime'] < 120]['Runtime']

plt.figure(figsize=(10,5))
ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_data)
plt.grid(True, linestyle='dashed', alpha=0.5)
st.pyplot(plt)


# Visualization 6th
st.subheader('6th Visualization')
plt.figure(figsize=(10,5))
sns.scatterplot(x=m_data['Runtime'], y=m_data['IMDB_Rating'], alpha=0.7)
plt.xlabel('Runtime')
plt.ylabel('IMDB Rating')
st.pyplot(plt)


# Visualization 7th
st.subheader('7th Visualization')

certificates = m_data['Certificate'].unique()

# Create a boxplot for each certificate category
plt.figure(figsize=(10, 6))
boxplot_data = [m_data[m_data['Certificate'] == certificate]['IMDB_Rating'] for certificate in certificates]
plt.boxplot(boxplot_data, labels=certificates)
plt.xlabel('Certificate')
plt.ylabel('IMDB Rating')
plt.title('IMDB Rating Distribution by Certificate')
st.pyplot(plt)

# Visualization 8th
st.subheader('8th Visualization')
top_directors = m_data['Director'].value_counts().head(10)
# Create a pie chart
plt.figure(figsize=(10, 8))
plt.pie(top_directors, labels=top_directors.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Director Distribution')
st.pyplot(plt)


# Visualization 9th
st.subheader('9th Visualization')
plt.figure(figsize=(8, 8))
st.line_chart(m_data.groupby('Released_Year')['No_of_Votes'].mean())

# Visualization 10th
st.subheader('10th Visualization')