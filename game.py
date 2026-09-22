CHOICES = ["rock", "paper", "scissors"]

def get_winner(player, ai):
    if player == ai:
        return "draw"

    if (
        (player == "rock" and ai == "scissors") or
        (player == "paper" and ai == "rock") or
        (player == "scissors" and ai == "paper")
    ):
        return "player"

    return "ai"