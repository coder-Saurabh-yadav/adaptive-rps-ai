import json
import os

from game import get_winner
from ai_engine import AdaptiveAI
from utils import print_score, print_statistics

# ---------------- AI ----------------
ai = AdaptiveAI()

player_score = 0
ai_score = 0
draws = 0
round_number = 1

HISTORY_FILE = "data/history.json"

os.makedirs("data", exist_ok=True)

match_history = []

print("=" * 50)
print("🤖 ADAPTIVE RPS AI — VERSION 3.0")
print("=" * 50)
print("🎮 Type: rock, paper, scissors")
print("❌ Type 'quit' anytime to exit.\n")

while True:

    print(f"\n{'='*18} ROUND {round_number} {'='*18}")

    player = input("👉 Your Move: ").lower().strip()

    if player == "quit":
        print("\n👋 GAME OVER")

        print_score(player_score, ai_score, draws)
        print_statistics(ai.get_history())

        with open(HISTORY_FILE, "w") as file:
            json.dump(match_history, file, indent=4)

        print("\n💾 Match history saved in data/history.json")
        break

    if player not in ["rock", "paper", "scissors"]:
        print("❌ Invalid move!")
        continue

    predicted = ai.predict_move()
    ai_move = ai.choose_move()

    if predicted is None:
        print("🧠 AI Status       : Learning your moves...")
    else:
        confidence = ai.get_confidence()
        print(f"🧠 AI Prediction   : {predicted}")
        print(f"🎯 Confidence      : {confidence}%")

    print(f"🤖 AI Played       : {ai_move}")

    result = get_winner(player, ai_move)

    if result == "player":
        print("✅ RESULT          : YOU WIN!")
        player_score += 1

    elif result == "ai":
        print("❌ RESULT          : AI WINS!")
        ai_score += 1

    else:
        print("🤝 RESULT          : DRAW!")
        draws += 1

    ai.update_history(player)

    match_history.append(
        {
            "round": round_number,
            "player_move": player,
            "ai_prediction": predicted,
            "ai_move": ai_move,
            "result": result,
        }
    )

    print_score(player_score, ai_score, draws)

    total_games = player_score + ai_score

    if total_games > 0:
        ai_rate = (ai_score / total_games) * 100
        player_rate = (player_score / total_games) * 100

        print(f"🤖 AI Win Rate     : {ai_rate:.1f}%")
        print(f"👤 Player Win Rate : {player_rate:.1f}%")

    print("\n📝 Player History")
    print("   " + " → ".join(ai.get_history()))

    round_number += 1