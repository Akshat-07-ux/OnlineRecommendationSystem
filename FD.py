import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

sns.set_style('white')

# Load the data
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
file_path = 'file.tsv'  # Ensure the file is in the same directory as your script or provide the correct path
df = pd.read_csv(file_path, sep='\t', names=column_names)

st.write("Head of the data:")
st.write(df.head())

# Load movie titles
movie_titles_url = 'https://media.geeksforgeeks.org/wp-content/uploads/Movie_Id_Titles.csv'
movie_titles = pd.read_csv(movie_titles_url)
st.write("Movie titles:")
st.write(movie_titles.head())

# Merge dataframes
data = pd.merge(df, movie_titles, on='item_id')
st.write("Merged data:")
st.write(data.head())

# Calculate mean rating and number of ratings for all movies
ratings = pd.DataFrame(data.groupby('title')['rating'].mean())
ratings['num of ratings'] = data.groupby('title')['rating'].count()

# Plot number of ratings
fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(ratings['num of ratings'], bins=70, ax=ax, color='blue')
st.pyplot(fig)

# Plot ratings
fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(ratings['rating'], bins=70, ax=ax, color='green')
st.pyplot(fig)

# Create a pivot table for collaborative filtering
moviemat = data.pivot_table(index='user_id', columns='title', values='rating')

# Filter out movies with fewer ratings
popular_movies = ratings[ratings['num of ratings'] > 100].index

# Compute correlation with similar movies for Star Wars and Liar Liar
starwars_user_ratings = moviemat['Star Wars (1977)'].dropna()
liarliar_user_ratings = moviemat['Liar Liar (1997)'].dropna()

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

similar_to_starwars = moviemat.corrwith(starwars_user_ratings)
similar_to_liarliar = moviemat.corrwith(liarliar_user_ratings)

# Create correlation DataFrame and filter out less popular movies
corr_starwars = pd.DataFrame(similar_to_starwars, columns=['Correlation'])
corr_starwars.dropna(inplace=True)
corr_starwars = corr_starwars.join(ratings['num of ratings'])
corr_starwars = corr_starwars[corr_starwars['num of ratings'] > 100].sort_values('Correlation', ascending=False)

corr_liarliar = pd.DataFrame(similar_to_liarliar, columns=['Correlation'])
corr_liarliar.dropna(inplace=True)
corr_liarliar = corr_liarliar.join(ratings['num of ratings'])
corr_liarliar = corr_liarliar[corr_liarliar['num of ratings'] > 100].sort_values('Correlation', ascending=False)

# Display top recommendations for Star Wars and Liar Liar
st.write("Top recommendations for Star Wars (1977):")
st.write(corr_starwars.head(10))
st.write("\nTop recommendations for Liar Liar (1997):")
st.write(corr_liarliar.head(10))

# Create a dashboard with Plotly
st.title('Movie Recommendations Dashboard')

# Scatter plot of average ratings vs number of ratings
fig = px.scatter(ratings, x='num of ratings', y='rating', size='num of ratings', hover_data=['rating'], title="Average Ratings vs Number of Ratings")
st.plotly_chart(fig)

# Bar chart of the top 10 most rated movies
top_10_most_rated = ratings.sort_values('num of ratings', ascending=False).head(10).reset_index()
fig = px.bar(top_10_most_rated, x='title', y='num of ratings', title='Top 10 Most Rated Movies', labels={'num of ratings': 'Number of Ratings', 'title': 'Movie Title'})
st.plotly_chart(fig)

# Heatmap of correlations between popular movies
corr_matrix = moviemat.corr()
top_10_corr_matrix = corr_matrix.loc[popular_movies, popular_movies].fillna(0)
fig = px.imshow(top_10_corr_matrix, title='Correlation Heatmap of Popular Movies')
st.plotly_chart(fig)

# Interactive table for top recommendations
st.write("Interactive Table of Top Recommendations for Star Wars (1977):")
st.dataframe(corr_starwars.head(10))

st.write("Interactive Table of Top Recommendations for Liar Liar (1997):")
st.dataframe(corr_liarliar.head(10))

# Add a sidebar for displaying movie images
st.sidebar.title("Recommended Movies")

# Dictionary to hold movie titles and their image URLs
movie_images = {
    "Star Wars (1977)": "https://helios-i.mashable.com/imagery/articles/01TcZde6d2fXgBbto4sNfjS/hero-image.fill.size_1248x702.v1623363315.jpg",
    "Return of the jedi (1983)": "https://m.media-amazon.com/images/M/MV5BOWZlMjFiYzgtMTUzNC00Y2IzLTk1NTMtZmNhMTczNTk0ODk1XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_.jpg",
    "Raiders of the Lost Ark (1981)": "https://prod-ripcut-delivery.disney-plus.net/v1/variant/disney/AC041259451A39F251FEC5422ACD641EE0ADA443C14A18217E7980F77800A27F/scale?width=1200&amp;aspectRatio=1.78&amp;format=webp",
    "empire strikes back (1980)": "https://prod-ripcut-delivery.disney-plus.net/v1/variant/disney/B92552B7CE9B7BB39BB3BDC551F35DB98C04740118F5B30975134814DF7A4E62/scale?width=1200&amp;aspectRatio=1.78&amp;format=webp",
    "Austin Powers: International Man of Mystery (1997)": "https://upload.wikimedia.org/wikipedia/en/d/d7/Austin_Powers_International_Man_of_Mystery_theatrical_poster.jpg",
    "Liar Liar (1997)": "https://resizing.flixster.com/r2nrUqJmu0He9fA_nfPbs5oQj2k=/fit-in/705x460/v2/https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p19140_v_h9_am.jpg",
    "batman forever (1994)": "https://upload.wikimedia.org/wikipedia/en/3/34/Batman_Forever_soundtrack.jpg",
    "The Mask(1994)": "https://m.media-amazon.com/images/S/pv-target-images/74573419559a87ea82fec35fef1bd03f3c30e997eb5fac374b25e58325006763.jpg",
    "Down Periscope (1996)": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/83e9dd50-d32e-47b6-9aa6-6212d34564b5/dfxf6p4-02856658-5edb-4609-ac29-ba1d01d17b9e.jpg/v1/fill/w_1280,h_1707,q_75,strp/2023_05_18downperiscope1996_by_jdandjc_dfxf6p4-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTcwNyIsInBhdGgiOiJcL2ZcLzgzZTlkZDUwLWQzMmUtNDdiNi05YWE2LTYyMTJkMzQ1NjRiNVwvZGZ4ZjZwNC0wMjg1NjY1OC01ZWRiLTQ2MDktYWMyOS1iYTFkMDFkMTdiOWUuanBnIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.Suwra5kwxoLQbgrJWhxP3g9OiA_Oem-b1yg_rCNAuU0",
    "Ace ventura (1994)": "https://m.media-amazon.com/images/M/MV5BY2U0NmM5NDEtYzk3OS00MGNhLWFjYmMtYWZhYmYxMzY4NDQyXkEyXkFqcGdeQXVyMjExMzc2MTY@._V1_.jpg",
}

for movie, img_url in movie_images.items():
    st.sidebar.image(img_url, caption=movie, use_column_width=True)
