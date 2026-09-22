# 🪨📄✂️ Adaptive Rock-Paper-Scissors AI

A Rock-Paper-Scissors game where the AI opponent **learns your play patterns**
using a Markov chain model instead of choosing moves randomly. The longer you
play, the smarter it gets — watch its win rate climb over time.

**Live demo:** _add your deployed Streamlit link here after deploying_

---

## How it works

Most simple RPS "AI" opponents just pick a random move. This one is different:

1. **Cold start (first 5 rounds):** the AI has no data yet, so it plays randomly.
2. **Learning phase:** for every move you make, the app records what you played
   *right after* your previous move (a first-order Markov chain / transition table).
3. **Prediction:** once it has enough history, the AI looks at your last move,
   checks what you've historically played after that move most often, and
   predicts your next move.
4. **Counter:** it then plays the move that beats its prediction.

This means players with predictable habits (e.g. "I always switch away from
Rock after winning with it") get exploited by the model over time — which is
exactly the point, and a great thing to demo live.

## Features

- Clean, interactive Streamlit UI
- Live scoreboard (You / AI / Ties)
- Rolling AI win-rate chart, updated every round
- Full round-by-round history table
- Reset button to start a fresh game/session

## Tech stack

- **Python 3**
- **Streamlit** — UI and app framework
- **Pandas** — round history and chart data handling
- Core AI logic: a hand-rolled **Markov chain** predictor (no external ML libraries needed)

## Run locally

```bash
git clone <your-repo-url>
cd rps-ai
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Deploy for free

1. Push this project to a public GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) (Streamlit Community Cloud).
3. Connect your repo, point it at `app.py`, and deploy.
4. Add the live link back into this README.

## Possible extensions

- Track prediction accuracy explicitly (not just AI win rate)
- Try a higher-order Markov chain (look at last 2-3 moves instead of 1)
- Add a difficulty toggle (random-only vs. adaptive AI)
- Persist history across sessions with a small SQLite database
- Add multiplayer mode (two humans, AI just referees)

## Resume bullet

> Built an adaptive Rock-Paper-Scissors AI using a Markov chain model to
> predict and counter player move patterns, improving win rate over static
> random play; built with Python and Streamlit, deployed live.
