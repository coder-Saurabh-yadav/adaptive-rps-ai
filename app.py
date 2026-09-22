"""
Adaptive Rock-Paper-Scissors AI
--------------------------------
A Rock-Paper-Scissors game where the AI opponent learns the player's
move patterns using a simple Markov chain model, instead of playing
randomly. The more you play, the more the AI adapts to you.

Run with:
    streamlit run app.py
"""

import random
import streamlit as st
import pandas as pd

# ----------------------------
# Config
# ----------------------------
MOVES = ["Rock", "Paper", "Scissors"]
BEATS = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}  # key beats value
EMOJI = {"Rock": "🪨", "Paper": "📄", "Scissors": "✂️"}
COLD_START_ROUNDS = 5  # number of rounds AI plays randomly before using the model


# ----------------------------
# Game logic
# ----------------------------
def get_winner(player_move: str, ai_move: str) -> str:
    """Return 'player', 'ai', or 'tie'."""
    if player_move == ai_move:
        return "tie"
    if BEATS[player_move] == ai_move:
        return "player"
    return "ai"


def counter_move(move: str) -> str:
    """Return the move that beats the given move."""
    for k, v in BEATS.items():
        if v == move:
            return k
    return random.choice(MOVES)


def predict_next_move(history: list[str], transition_counts: dict) -> str:
    """
    Predict the player's next move using a first-order Markov chain:
    look at what the player tends to play after their last move.
    """
    if not history:
        return random.choice(MOVES)

    last_move = history[-1]
    counts = transition_counts[last_move]
    total = sum(counts.values())

    if total == 0:
        # No data for this transition yet — fall back to random
        return random.choice(MOVES)

    # Pick the most frequently played move after this last move
    predicted = max(counts, key=counts.get)
    return predicted


def ai_choose_move(history: list[str], transition_counts: dict, round_num: int) -> tuple[str, bool]:
    """
    Decide the AI's move.
    Returns (move, used_prediction) where used_prediction indicates
    whether the model was used (True) or it was a random cold-start move (False).
    """
    if round_num <= COLD_START_ROUNDS or not history:
        return random.choice(MOVES), False

    predicted_player_move = predict_next_move(history, transition_counts)
    return counter_move(predicted_player_move), True


def update_transition_counts(transition_counts: dict, history: list[str]):
    """Update transition counts after a new player move is added to history."""
    if len(history) >= 2:
        prev_move = history[-2]
        curr_move = history[-1]
        transition_counts[prev_move][curr_move] += 1


# ----------------------------
# Streamlit session state init
# ----------------------------
def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []  # player's move history
    if "transition_counts" not in st.session_state:
        st.session_state.transition_counts = {m: {m2: 0 for m2 in MOVES} for m in MOVES}
    if "round_num" not in st.session_state:
        st.session_state.round_num = 0
    if "score" not in st.session_state:
        st.session_state.score = {"player": 0, "ai": 0, "tie": 0}
    if "log" not in st.session_state:
        st.session_state.log = []  # list of dicts for the results table / chart
    if "ai_wins_rolling" not in st.session_state:
        st.session_state.ai_wins_rolling = []  # 1 if AI won that round, else 0


def reset_game():
    st.session_state.history = []
    st.session_state.transition_counts = {m: {m2: 0 for m2 in MOVES} for m in MOVES}
    st.session_state.round_num = 0
    st.session_state.score = {"player": 0, "ai": 0, "tie": 0}
    st.session_state.log = []
    st.session_state.ai_wins_rolling = []


def play_round(player_move: str):
    st.session_state.round_num += 1
    round_num = st.session_state.round_num

    ai_move, used_prediction = ai_choose_move(
        st.session_state.history, st.session_state.transition_counts, round_num
    )

    winner = get_winner(player_move, ai_move)
    st.session_state.score[winner] += 1

    # Update history + transition model AFTER using them for this round's AI move
    st.session_state.history.append(player_move)
    update_transition_counts(st.session_state.transition_counts, st.session_state.history)

    st.session_state.log.append(
        {
            "Round": round_num,
            "You": f"{EMOJI[player_move]} {player_move}",
            "AI": f"{EMOJI[ai_move]} {ai_move}",
            "Result": {"player": "You win", "ai": "AI wins", "tie": "Tie"}[winner],
            "AI mode": "Predicting" if used_prediction else "Warming up",
        }
    )
    st.session_state.ai_wins_rolling.append(1 if winner == "ai" else 0)


# ----------------------------
# UI
# ----------------------------
st.set_page_config(page_title="Adaptive RPS AI", page_icon="🪨", layout="centered")
init_state()

st.title("🪨📄✂️ Adaptive Rock-Paper-Scissors AI")
st.caption(
    "This AI doesn't play randomly — it learns your patterns using a Markov chain "
    "model and tries to predict (then counter) your next move."
)

with st.expander("How does the AI work?", expanded=False):
    st.markdown(
        f"""
- For the first **{COLD_START_ROUNDS} rounds**, the AI plays randomly (it has no data on you yet).
- After that, it looks at what you tend to play **after your previous move** 
  (a first-order Markov chain) and predicts your next move.
- It then plays the move that **beats** its prediction.
- The more predictable your patterns are, the better the AI gets over time.
- Try to beat it by mixing up your strategy — that's the fun part!
"""
    )

st.divider()

col1, col2, col3 = st.columns(3)
if col1.button(f"{EMOJI['Rock']} Rock", use_container_width=True):
    play_round("Rock")
if col2.button(f"{EMOJI['Paper']} Paper", use_container_width=True):
    play_round("Paper")
if col3.button(f"{EMOJI['Scissors']} Scissors", use_container_width=True):
    play_round("Scissors")

st.divider()

# ----------------------------
# Scoreboard
# ----------------------------
s = st.session_state.score
total_rounds = st.session_state.round_num

sc1, sc2, sc3, sc4 = st.columns(4)
sc1.metric("Rounds played", total_rounds)
sc2.metric("You", s["player"])
sc3.metric("AI", s["ai"])
sc4.metric("Ties", s["tie"])

if total_rounds > 0:
    ai_win_rate = s["ai"] / total_rounds * 100
    st.progress(min(int(ai_win_rate), 100), text=f"AI win rate: {ai_win_rate:.1f}%")

# ----------------------------
# Rolling AI win-rate chart
# ----------------------------
if total_rounds >= 3:
    window = 5
    rolling = pd.Series(st.session_state.ai_wins_rolling).rolling(window, min_periods=1).mean() * 100
    chart_df = pd.DataFrame({"Round": range(1, total_rounds + 1), "AI win rate (%)": rolling})
    st.subheader("AI win rate over time")
    st.line_chart(chart_df.set_index("Round"))
    st.caption(
        f"Rolling average over the last {window} rounds. Watch this trend up as the AI "
        "learns your patterns — that's the model working."
    )

# ----------------------------
# Round log
# ----------------------------
if st.session_state.log:
    st.subheader("Round history")
    st.dataframe(
        pd.DataFrame(st.session_state.log).sort_values("Round", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

st.divider()
if st.button("🔄 Reset game"):
    reset_game()
    st.rerun()
