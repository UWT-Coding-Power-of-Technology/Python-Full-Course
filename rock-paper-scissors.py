import random

# Possible moves
moves = ["rock", "paper", "scissors"]

# Keep track of player history
player_history = []

# Scores
player_score = 0
ai_score = 0
ties = 0

def ai_move():
    """
    Fair AI strategy:
    - 50% chance to predict player's last move
    - 50% chance to pick randomly
    """
    if not player_history:
        return random.choice(moves)

    if random.random() < 0.5:
        last_move = player_history[-1]
        # Pick the move that beats player's last move
        if last_move == "rock":
            return "paper"
        elif last_move == "paper":
            return "scissors"
        elif last_move == "scissors":
            return "rock"
    else:
        return random.choice(moves)

def determine_winner(player, ai):
    if player == ai:
        return "Tie"
    elif (player == "rock" and ai == "scissors") or \
         (player == "paper" and ai == "rock") or \
         (player == "scissors" and ai == "paper"):
        return "Player"
    else:
        return "AI"

print("🎮 Welcome to Rock Paper Scissors with AI!")
print("Type 'rock', 'paper', or 'scissors' to play. Type 'quit' to exit.\n")

while True:
    player_choice = input("Your move: ").lower()

    if player_choice == "quit":
        print("\nThanks for playing!")
        print(f"Final Scores → You: {player_score} | AI: {ai_score} | Ties: {ties}")
        break
    elif player_choice not in moves:
        print("Invalid move. Try again.\n")
        continue

    # Save player's move
    player_history.append(player_choice)

    # AI chooses its move
    ai_choice = ai_move()
    print(f"AI chose: {ai_choice}")

    # Determine winner
    winner = determine_winner(player_choice, ai_choice)
    if winner == "Tie":
        print("It's a tie!\n")
        ties += 1
    elif winner == "Player":
        print("You win this round!\n")
        player_score += 1
    else:
        print("AI wins this round!\n")
        ai_score += 1

    # Show current score
    print(f"Scores → You: {player_score} | AI: {ai_score} | Ties: {ties}\n")
