
from random import randint
from typing import Annotated

from agent_framework import tool
from agent_freamwork.openai import OpenAiChatClient
from dotenv import load_dotenv
from pydantic import Field

load_dotenv()

# defining the tool

@tool(approval_mode="never_require")
def roll_dice(
    sides: Annotated[int, Field(description="Number of sides on the dice")] = 6,
) -> str:
    """Roll a dice with the given number of sides and return the results."""
    result = randint(1, sides)
    print(f" [tool executed: roll_dice(sides={sides}) -> {result}]")
    return f"Rolled a {sides}-sided dice and got: {result}"

