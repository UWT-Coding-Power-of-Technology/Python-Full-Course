# Sentiment Spy: Mission Report
# How AI Works: From Data to Smart Models
# Author: Usairim Kamal Azfar Wakeel

from textblob import TextBlob

# Data storage
conversation_history = []
sentiment_stats = {"positive": 0, "negative": 0, "neutral": 0}

def analyze_sentiment(text):
    """Analyze sentiment and return classification."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

def show_stats():
    """Display current sentiment stats."""
    total = sum(sentiment_stats.values())
    print("\n📊 Sentiment Stats:")
    for mood, count in sentiment_stats.items():
        print(f"  {mood.capitalize()}: {count}")
    print(f"  Total messages analyzed: {total}\n")

def reset_data():
    """Reset all stored data."""
    conversation_history.clear()
    for key in sentiment_stats:
        sentiment_stats[key] = 0
    print("🧹 All data has been reset!\n")

def show_history():
    """Display conversation history."""
    print("\n💬 Conversation History:")
    if not conversation_history:
        print("  (No messages yet!)")
    else:
        for msg, sentiment in conversation_history:
            print(f"  You: {msg} → Sentiment: {sentiment}")
    print()

def generate_report():
    """Generate a final report."""
    print("\n🕵️‍♂️ Sentiment Spy: Final Mission Report")
    print("--------------------------------------")
    show_stats()
    print("✅ Mission Complete. Report Saved (in memory).")

def main():
    print("🤖 Welcome to Sentiment Spy!")
    print("Type anything and I’ll analyze how it feels.")
    print("Commands: /stats, /reset, /history, /exit\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "/exit":
            generate_report()
            break
        elif user_input.lower() == "/stats":
            show_stats()
        elif user_input.lower() == "/reset":
            reset_data()
        elif user_input.lower() == "/history":
            show_history()
        else:
            sentiment = analyze_sentiment(user_input)
            sentiment_stats[sentiment] += 1
            conversation_history.append((user_input, sentiment))
            print(f"🧠 Sentiment: {sentiment}\n")

if __name__ == "__main__":
    main()
