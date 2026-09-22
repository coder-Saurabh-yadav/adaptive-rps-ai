from collections import Counter


def print_score(player_score, ai_score, draws):
    print("=" * 35)
    print("📊 SCOREBOARD")
    print("=" * 35)
    print(f"👤 Player : {player_score}")
    print(f"🤖 AI     : {ai_score}")
    print(f"🤝 Draws  : {draws}")
    print("=" * 35)


def print_statistics(history):
    counter = Counter(history)

    print("\n📈 PLAYER MOVE STATISTICS")
    print("-" * 35)
    print(f"🪨 Rock     : {counter['rock']}")
    print(f"📄 Paper    : {counter['paper']}")
    print(f"✂️ Scissors : {counter['scissors']}")
    print("-" * 35)