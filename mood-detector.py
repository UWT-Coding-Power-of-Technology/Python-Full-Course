from textblob import TextBlob

def analyze_mood(text):
    """
    Analyzes the mood of a given text using TextBlob.

    Args:
        text (str): The text to analyze.

    Returns:
        tuple: A tuple containing the overall mood (positive, negative, or neutral) and the polarity score.
             Polarity score ranges from -1 (negative) to 1 (positive).
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        mood = "positive"
    elif polarity < 0:
        mood = "negative"
    else:
        mood = "neutral"

    return mood, polarity

text = input("Enter the text you want to analyze: ")
mood, polarity = analyze_mood(text)
print(f"Mood: {mood}")
print(f"Polarity: {polarity}")
