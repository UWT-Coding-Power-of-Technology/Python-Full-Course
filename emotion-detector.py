# Basic Emotion Detector

# Ask user for a sentence
sentence = input("Enter a sentence: ").lower()

# Define emotion keywords
happy_words = ["happy", "joy", "glad", "excited", "great", "love", "awesome"]
sad_words = ["sad", "unhappy", "cry", "down", "depressed", "bad"]
angry_words = ["angry", "mad", "furious", "annoyed", "irritated", "hate"]

# Detect emotion
emotion = "neutral"  # default

for word in happy_words:
    if word in sentence:
        emotion = "happy"
        break

for word in sad_words:
    if word in sentence:
        emotion = "sad"
        break

for word in angry_words:
    if word in sentence:
        emotion = "angry"
        break

# Show result
print(f"The emotion detected is: {emotion}")
print("Thank you for using the Emotion Detector!")
