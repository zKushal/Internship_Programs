import random
from dataclasses import dataclass


@dataclass
class DiceGameResult:
    player_name: str
    guess: int
    roll: int
    won: bool


def roll_dice() -> int:
    """Roll a six-sided die and return the result."""
    return random.randint(1, 6)


def play_round(player_name: str, guess: int) -> DiceGameResult:
    roll = roll_dice()
    return DiceGameResult(
        player_name=player_name,
        guess=guess,
        roll=roll,
        won=guess == roll,
    )


if __name__ == "__main__":
    valid_guesses = {"1", "2", "3", "4", "5", "6"}
    exit_commands = {"exit", "quit", "stop", "end", "goodbye"}

    while True:
        guess = input("Enter your guess (1-6) or 'exit/quit/stop/end/goodbye' to quit: ").strip()
        if guess.lower() in exit_commands:
            print("Thank you for playing the dice game! Goodbye!")
            break

        if guess not in valid_guesses:
            print("Invalid guess. Please enter a number from 1 to 6.")
            continue

        player_name = input("Enter your name: ").strip() or "Player"
        result = play_round(player_name, int(guess))

        if result.won:
            print(
                f"{result.player_name}, your guess of {result.guess} was correct. "
                f"You won! The dice rolled {result.roll}."
            )
        else:
            print(
                f"{result.player_name}, your guess of {result.guess} was incorrect. "
                f"You lost. The dice rolled {result.roll}."
            )
