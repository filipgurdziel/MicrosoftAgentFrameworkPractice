import asyncio
import os
from random import randint
from typing import Annotated

from agent_framework import tool
from agent_framework_openai import OpenAIChatCompletionClient
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

async def main():
    client = OpenAIChatCompletionClient(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.environ["GITHUB_TOKEN"],
        model=os.environ.get("GITHUB_MODEL", "gpt-4o-mini"),
    )

    agent = client.as_agent (
        name = "DiceAgent",
        instructions = "You are a helpful assistant. Use the roll_dice tool to roll dice when asked.",
        tools = [roll_dice],
    )

    # Question to trigger the tool
    print ("Can you roll a 20-sided dice for me?")
    response = await agent.run("Can you roll a 20-sided dice for me?")
    print(f"Agent response: {response}")

    # Question to not trigger the tool
    print("What is the capital of Japan?")
    result = await agent.run("What is the capital of Japan?")
    print(f"Agent response: {result}")


if __name__ == "__main__":
    asyncio.run(main())