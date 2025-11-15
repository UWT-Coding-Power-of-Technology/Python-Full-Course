import re
import random

memory = {
    "user_name": Usairim-Kamal,
    "mood": None,
    "facts": [],     # stores things user says about their life
    "topics": []     # stores topics user talked about
}

long_replies = True  # allows detailed chatbot responses

topics = {
    "school": ["school", "class", "homework", "teacher", "exam"],
    "games": ["game", "gaming", "playstation", "xbox", "minecraft", "roblox"],
    "food": ["food", "eat", "pizza", "burger", "snacks", "restaurant"],
    "family": ["family", "mom", "dad", "sister", "brother"],
    "music": ["music", "song", "singer", "rap", "guitar"],
}

easter_eggs = {
    "i feel empty": "You just unlocked **Deep Talk Mode** 😶‍🌫 — I'm here for everything you don't tell others. Talk freely.",
    "tell me a secret": "ThinkChatMe secret: I pretend I understand humans but I'm still learning... don't expose me 🤫",
    "do you love me": "Love? I don't feel emotions, but I care that you're here 💙"
}

def detect_topic(text):
    text = text.lower()
    for topic, words in topics.items():
        for w in words:
            if w in text:
                return topic
    return None

def detect_mood(text):
    text = text.lower()
    if any(word in text for word in ["happy","excited","great"]):
        return "happy"
    if any(word in text for word in ["sad","cry","upset","alone"]):
        return "sad"
    if any(word in text for word in ["angry","mad","furious"]):
        return "angry"
    return None

def reply(text):
    text = text.lower().strip()

    # Easter eggs
    for phrase, response in easter_eggs.items():
        if phrase in text:
            return response

    # Name saving
    match = re.search(r"(my name is|i am) (.*)", text)
    if match:
        name = match.group(2).strip()
        memory["user_name"] = name
        return f"Nice to meet you {name} 😎 — I’ll remember that!"

    # Mood detection
    mood = detect_mood(text)
    if mood:
        memory["mood"] = mood
        if mood == "happy":
            return "I love that you're happy 😄 Keep that energy alive."
        elif mood == "sad":
            return "I’m sorry you're sad 😢 Wanna talk about what's going on?"
        elif mood == "angry":
            return "I get that you're angry 😤 — I’m here to listen without judging."

    # Topic detection
    topic = detect_topic(text)
    if topic:
        memory["topics"].append(topic)
        if long_replies:
            return f"Ohh you're talking about **{topic}** — I like this topic! Tell me more, I'm actually curious 👀"
        return f"You mentioned {topic}."

    # Fact storage
    if text.endswith("."):
        memory["facts"].append(text[:-1])
        return "That's interesting 🤔 — I’ll remember that."

    # Personalized responses if name known
    if memory["user_name"]:
        return random.choice([
            f"I'm listening, {memory['user_name']} 👀",
            f"Go on {memory['user_name']}, I'm here.",
            f"I'm honestly curious, {memory['user_name']}."
        ])

    # General fallback
    return random.choice([
        "I'm thinking about what you said… tell me more.",
        "Hmm… that’s deep. Explain a little more.",
        "I'm still learning humans — help me understand?"
    ])


print("🤖 ThinkChatMe (ULTRA LEVEL) is online — type 'bye' anytime to exit.\n")

while True:
    user = input("You: ")
    if re.search(r"(bye|exit|quit|goodbye)", user.lower()):
        print("ThinkChatMe: I’ll be here when you come back. Stay safe 🌙")
        break
    print("ThinkChatMe:", reply(user))
