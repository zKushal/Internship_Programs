from pathlib import Path
import os
import random

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel

PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")

MODEL_NAME = "groq:llama-3.1-8b-instant"


class DiceGameResult(BaseModel):
    player_name: str
    guess: int
    roll: int
    won: bool


agent = Agent(
    MODEL_NAME,
    deps_type=str,
    output_type=DiceGameResult,
    instructions=(
        "You are a dice game assistant. "
        "Use the available tools to roll one six-sided die and get the player's name. "
        "Read the user's guess from the prompt, compare it with the die roll, and return "
        "only structured output with these fields: player_name, guess, roll, won. "
        "Set won to true when guess and roll match, otherwise false. "
        "Do not include XML, HTML, markdown, or any extra text."
    ),
)


@agent.tool_plain
def roll_dice() -> str:
    """Roll a six-sided die and return the result."""
    return str(random.randint(1, 6))


@agent.tool
def get_player_name(ctx: RunContext[str]) -> str:
    """Return the player's name stored in the agent dependencies."""
    return ctx.deps


def format_result(result: DiceGameResult) -> str:
    if result.won:
        return (
            f"{result.player_name}, your guess of {result.guess} was correct. "
            f"You won. The dice rolled {result.roll}."
        )
    return (
        f"{result.player_name}, your guess of {result.guess} was incorrect. "
        f"You lost. The dice rolled {result.roll}."
    )


def main() -> None:
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "Missing GROQ_API_KEY in DiceGame/.env. Add your Groq API key and run again."
        )

    guess = input("Enter your guess (1-6): ").strip()
    if guess not in {"1", "2", "3", "4", "5", "6"}:
        raise ValueError("Guess must be a number from 1 to 6.")

    player_name = input("Enter your name: ").strip() or "Player"
    result = agent.run_sync(f"My guess is {guess}", deps=player_name)
    print(format_result(result.output))


if __name__ == "__main__":
    main()
