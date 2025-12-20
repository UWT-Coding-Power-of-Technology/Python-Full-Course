# Simple AI-based Movie Recommendation System

# Content-based filtering using cosine similarity

from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd

# Movie dataset

data = {

"Movie": [

"Avengers", "Iron Man", "Titanic",

"The Notebook", "Interstellar", "Inception"

],

"Action": [1, 1, 0, 0, 0, 1],

"Romance": [0, 0, 1, 1, 0, 0],

"SciFi": [0, 0, 0, 0, 1, 1],

"Drama": [0, 0, 1, 1, 1, 0]

}

# Create DataFrame

df = pd.DataFrame(data)

# Compute similarity matrix

similarity = cosine_similarity(df.iloc[:, 1:])

# Recommendation function

def recommend(movie_name):
    if movie_name not in df["Movie"].values:
        print("Movie not found.")
        return
    
    index = df[df["Movie"] == movie_name].index[0]
    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    print(f"\nMovies recommended for '{movie_name}':")
    for i in scores[1:4]:
        print("- ", df.iloc[i[0]]["Movie"])

# User input

movie = input("Enter a movie you like: ")

recommend(movie)
