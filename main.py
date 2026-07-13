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

@tool(approval_mode="never_require")
def convert_celsius_to_fahrenheit(
    celsius: Annotated[float, Field(description="Temperature in Celsius")]
) -> float:
    """Convert Celsius to Fahrenheit."""
    result = (celsius * 9/5) + 32
    print(f" [tool executed: convert_celsius_to_fahrenheit(celsius={celsius}) -> {result}]")
    return result

async def main():
    client = OpenAIChatCompletionClient(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.environ["GITHUB_TOKEN"],
        model=os.environ.get("GITHUB_MODEL", "gpt-4o-mini"),
    )

    agent = client.as_agent (
        name = "DiceAgent",
        instructions = "You are a helpful assistant. Use the roll_dice tool to roll dice when asked.",
        tools = [roll_dice, convert_celsius_to_fahrenheit],
    )

    session1 = agent.create_session()

    # Question to trigger the tool
    print ("Can you roll a 20-sided dice for me?")
    response = await agent.run("Can you roll a 20-sided dice for me?", session = session1)
    print(f"Agent response: {response}")

    # Question to not trigger the tool
    print("What is the capital of Japan?")
    result = await agent.run("What is the capital of Japan?", session = session1)
    print(f"Agent response: {result}")

    # Question to trigger the temperature conversion tool
    print("Convert 100 degrees Celsius to Fahrenheit.")
    result = await agent.run("Convert 100 degrees Celsius to Fahrenheit.", session = session1)
    print(f"Agent response: {result}")

    # Question to ask both tools
    print("Roll a 12-sided dice and convert 25 degrees Celsius to Fahrenheit.")
    result = await agent.run("Roll a 12-sided dice and convert 25 degrees Celsius to Fahrenheit.", session = session1)
    print(f"Agent response: {result}")

    # Checking if the bot remembers previous results

    print("Do you remember what the initial temperature and the result was of my temperature conversion, the very first one?")
    result = await agent.run("Do you remember what the initial temperature and the result was of my temperature conversion, the very first one?", session = session1)
    print(f"Agent response: {result}")

if __name__ == "__main__":
    asyncio.run(main())