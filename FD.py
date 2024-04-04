import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

sns.set_style('white') 
%matplotlib inline 

# Get the data 
column_names = ['user_id', 'item_id', 'rating', 'timestamp'] 

path = 'https://media.geeksforgeeks.org/wp-content/uploads/file.tsv'

df = pd.read_csv(path, sep='\t', names=column_names) 

# Check the head of the data 
df.head() 

# Check out all the movies and their respective IDs 
movie_titles = pd.read_csv('https://media.geeksforgeeks.org/wp-content/uploads/Movie_Id_Titles.csv') 
movie_titles.head() 

data = pd.merge(df, movie_titles, on='item_id') 
data.head() 

# Calculate mean rating of all movies 
ratings = pd.DataFrame(data.groupby('title')['rating'].mean()) 
ratings['num of ratings'] = data.groupby('title')['rating'].count() 

# Plot graph of 'num of ratings' column 
plt.figure(figsize=(10, 4)) 
sns.histplot(ratings['num of ratings'], bins=70) 

# Plot graph of 'ratings' column 
plt.figure(figsize=(10, 4)) 
sns.histplot(ratings['rating'], bins=70) 

# Create a pivot table for collaborative filtering 
moviemat = data.pivot_table(index='user_id', columns='title', values='rating') 

# Filter out movies with fewer ratings 
popular_movies = ratings[ratings['num of ratings'] > 100].index 

# Compute correlation with similar movies for Star Wars and Liar Liar
starwars_user_ratings = moviemat['Star Wars (1977)'].dropna() 
liarliar_user_ratings = moviemat['Liar Liar (1997)'].dropna() 

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
print("Top recommendations for Star Wars (1977):")
print(corr_starwars.head(10))
print("\nTop recommendations for Liar Liar (1997):")
print(corr_liarliar.head(10))
