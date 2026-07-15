import asyncio
import os
import json
from random import randint
from typing import Annotated

from agent_framework import tool
from agent_framework import AgentSession
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

    with open("session.json") as f:
        session_dict = json.load(f)
    
    session1 = AgentSession.from_dict(session_dict)

    # question to test if previous chat was saved and successfully extracted into current session

    result = await agent.run("What were we discussing?", session = session1)

    print(f"{result}")

    session_dict = session1.to_dict()
    
    # end of conversation, dump convo into json file
    
    with open("session.json", "w") as f:
        json.dump(session_dict, f)
    

if __name__ == "__main__":
    asyncio.run(main())