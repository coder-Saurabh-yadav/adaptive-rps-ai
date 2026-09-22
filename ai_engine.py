import random

CHOICES = ["rock", "paper", "scissors"]


class AdaptiveAI:
    def __init__(self):
        self.player_history = []
        self.last_prediction = None
        self.confidence = 0

    def predict_move(self):
        if len(self.player_history) < 2:
            self.last_prediction = None
            self.confidence = 0
            return None

        last_move = self.player_history[-1]
        next_moves = []

        for i in range(len(self.player_history) - 1):
            if self.player_history[i] == last_move:
                next_moves.append(self.player_history[i + 1])

        if next_moves:
            prediction = max(set(next_moves), key=next_moves.count)

            self.last_prediction = prediction
            self.confidence = round(
                next_moves.count(prediction) / len(next_moves) * 100
            )

            return prediction

        self.last_prediction = None
        self.confidence = 0
        return None

    def choose_move(self):
        predicted = self.predict_move()

        if predicted is None:
            return random.choice(CHOICES)

        counter = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock",
        }

        return counter[predicted]

    def update_history(self, move):
        self.player_history.append(move)

    def get_history(self):
        return self.player_history

    def get_confidence(self):
        return self.confidence