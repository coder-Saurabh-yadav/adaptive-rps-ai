import tkinter as tk
from tkinter import messagebox

from ai_engine import AdaptiveAI
from game import get_winner

# ---------------- AI ----------------
ai = AdaptiveAI()

player_score = 0
ai_score = 0
draw_score = 0
round_number = 1

# ---------------- Window ----------------
root = tk.Tk()
root.title("Adaptive RPS AI")
root.geometry("650x700")
root.configure(bg="#111827")
root.resizable(False, False)

# ---------------- Colors ----------------
BG = "#111827"
CARD = "#1F2937"
BLUE = "#38BDF8"
GREEN = "#22C55E"
RED = "#EF4444"
YELLOW = "#F59E0B"
WHITE = "#F9FAFB"

# ---------------- Title ----------------
title = tk.Label(
    root,
    text="🤖 ADAPTIVE RPS AI",
    bg=BG,
    fg=BLUE,
    font=("Segoe UI", 24, "bold")
)
title.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Learn • Predict • Counter",
    bg=BG,
    fg="gray",
    font=("Segoe UI", 11)
)
subtitle.pack()

# ---------------- Round ----------------
round_label = tk.Label(
    root,
    text="🎮 ROUND 1",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI", 16, "bold")
)
round_label.pack(pady=10)

# ---------------- AI Status ----------------
prediction_label = tk.Label(
    root,
    text="🧠 AI is learning...",
    bg=BG,
    fg=YELLOW,
    font=("Segoe UI", 13)
)
prediction_label.pack()

move_label = tk.Label(
    root,
    text="🤖 AI Played : ?",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI", 15)
)
move_label.pack(pady=10)

result_label = tk.Label(
    root,
    text="",
    bg=BG,
    fg=GREEN,
    font=("Segoe UI", 18, "bold")
)
result_label.pack()

# ---------------- Scoreboard ----------------
score_frame = tk.Frame(root, bg=CARD)
score_frame.pack(pady=20, padx=20, fill="x")

player_label = tk.Label(
    score_frame,
    text="👤 Player : 0",
    bg=CARD,
    fg=GREEN,
    font=("Segoe UI", 13, "bold")
)
player_label.pack(pady=5)

ai_label = tk.Label(
    score_frame,
    text="🤖 AI : 0",
    bg=CARD,
    fg=RED,
    font=("Segoe UI", 13, "bold")
)
ai_label.pack(pady=5)

draw_label = tk.Label(
    score_frame,
    text="🤝 Draw : 0",
    bg=CARD,
    fg=WHITE,
    font=("Segoe UI", 13, "bold")
)
draw_label.pack(pady=5)

# ---------------- History ----------------
history_title = tk.Label(
    root,
    text="📝 Move History",
    bg=BG,
    fg=BLUE,
    font=("Segoe UI", 14, "bold")
)
history_title.pack()

history_box = tk.Text(
    root,
    height=6,
    width=55,
    bg=CARD,
    fg=WHITE,
    font=("Consolas", 11)
)
history_box.pack(pady=10)
history_box.config(state="disabled")


# ---------------- Game Logic ----------------
def play(player_move):
    global player_score, ai_score, draw_score, round_number

    predicted = ai.predict_move()
    ai_move = ai.choose_move()

    if predicted is None:
        prediction_label.config(
            text="🧠 AI Status : Learning your moves...",
            fg=YELLOW
        )
    else:
        confidence = ai.get_confidence()
        prediction_label.config(
            text=f"🧠 Prediction : {predicted} ({confidence}% confidence)",
            fg=BLUE
        )

    move_label.config(text=f"🤖 AI Played : {ai_move}")

    result = get_winner(player_move, ai_move)

    if result == "player":
        player_score += 1
        result_label.config(text="✅ YOU WIN!", fg=GREEN)

    elif result == "ai":
        ai_score += 1
        result_label.config(text="❌ AI WINS!", fg=RED)

    else:
        draw_score += 1
        result_label.config(text="🤝 DRAW!", fg=YELLOW)

    ai.update_history(player_move)

    player_label.config(text=f"👤 Player : {player_score}")
    ai_label.config(text=f"🤖 AI : {ai_score}")
    draw_label.config(text=f"🤝 Draw : {draw_score}")

    history_box.config(state="normal")
    history_box.delete("1.0", tk.END)
    history_box.insert(
        tk.END,
        " → ".join(ai.get_history())
    )
    history_box.config(state="disabled")

    round_number += 1
    round_label.config(text=f"🎮 ROUND {round_number}")


# ---------------- Buttons ----------------
button_frame = tk.Frame(root, bg=BG)
button_frame.pack(pady=20)

rock_btn = tk.Button(
    button_frame,
    text="🪨 ROCK",
    width=15,
    bg="#2563EB",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    command=lambda: play("rock")
)
rock_btn.grid(row=0, column=0, padx=10, pady=10)

paper_btn = tk.Button(
    button_frame,
    text="📄 PAPER",
    width=15,
    bg="#16A34A",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    command=lambda: play("paper")
)
paper_btn.grid(row=0, column=1, padx=10, pady=10)

scissor_btn = tk.Button(
    button_frame,
    text="✂️ SCISSORS",
    width=15,
    bg="#EA580C",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    command=lambda: play("scissors")
)
scissor_btn.grid(row=1, column=0, columnspan=2, pady=10)

# ---------------- Reset ----------------
def reset_game():
    global player_score, ai_score, draw_score, round_number

    player_score = 0
    ai_score = 0
    draw_score = 0
    round_number = 1

    ai.player_history.clear()

    player_label.config(text="👤 Player : 0")
    ai_label.config(text="🤖 AI : 0")
    draw_label.config(text="🤝 Draw : 0")

    prediction_label.config(text="🧠 AI is learning...", fg=YELLOW)
    move_label.config(text="🤖 AI Played : ?")
    result_label.config(text="")
    round_label.config(text="🎮 ROUND 1")

    history_box.config(state="normal")
    history_box.delete("1.0", tk.END)
    history_box.config(state="disabled")

reset_btn = tk.Button(
    root,
    text="🔄 RESET GAME",
    bg="#DC2626",
    fg="white",
    width=20,
    font=("Segoe UI", 12, "bold"),
    command=reset_game
)
reset_btn.pack(pady=15)

root.mainloop()