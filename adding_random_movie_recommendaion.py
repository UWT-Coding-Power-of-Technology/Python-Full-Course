import random

# Movie database
movies = [
    {
        "title": "Inception",
        "genre": "Sci-Fi",
        "imdb": 8.8,
        "overview": "A thief who steals corporate secrets through dream-sharing technology.",
    },
    {
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "imdb": 8.6,
        "overview": "A team of explorers travel through a wormhole in space.",
    },
    {
        "title": "The Dark Knight",
        "genre": "Action",
        "imdb": 9.0,
        "overview": "Batman faces the Joker in Gotham City.",
    },
    {
        "title": "Forrest Gump",
        "genre": "Drama",
        "imdb": 8.8,
        "overview": "The story of a man with a kind heart and an extraordinary life.",
    }
]

def sentiment_analysis(text):
    positive_words = ["extraordinary", "kind", "explorers", "dream"]
    score = sum(word in text.lower() for word in positive_words)

    if score > 1:
        return "Positive 😊"
    elif score == 1:
        return "Neutral 😐"
    else:
        return "Neutral"

def random_movie_recommendation():
    movie = random.choice(movies)

    print("🎬 Random Movie Recommendation 🎬")
    print("-------------------------------")
    print(f"Title: {movie['title']}")
    print(f"Genre: {movie['genre']}")
    print(f"IMDb Rating: {movie['imdb']}")
    print(f"Overview: {movie['overview']}")
    print(f"Sentiment: {sentiment_analysis(movie['overview'])}")

# Run the recommendation
random_movie_recommendation()
