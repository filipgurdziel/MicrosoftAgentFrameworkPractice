import asyncio
import os
from typing_extensions import Never

from agent_framework import WorkflowBuilder, WorkflowContext, AgentExecutorResponse, executor
from agent_framework.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()

@executor(id="word_counter")
async def count_words(response: AgentExecutorResponse, ctx: WorkflowContext[Never, str]) -> None:
    """Count the words in the poem and yield a summary as a final output."""
    poem = response.agent_response.text
    word_count = len(poem.split())
    print(f"WORD COUNTER EXECUTED. Words counted; {word_count}")
    await ctx.yield_output(f"Poem: {poem}, word count is: {word_count}")


async def main():
    client = OpenAIChatCompletionClient(
        base_url = "https://models.inference.ai.azure.com",
        api_key = os.environ["GITHUB_TOKEN"],
        model = os.environ.get("GITHUB_MODEL", "gpt-4o-mini"),
    )

    word_counter_agent = client.as_agent(
        id = "word_counter",
        name = "WordCounterAgent",
        instructions = "Write a simple poem about a given topic. Output only the poem, nothing else.",
    )

    workflow = (
        WorkflowBuilder(start_executor = word_counter_agent, output_from = [count_words])
        .add_edge(word_counter_agent, count_words)
        .build()
    )

    topic = input("Input a topic you want the poem to be about, the words in it will later be counted.")

    async for event in workflow.run(topic, stream=True):
        if event.type == "output":
            print(f"Workflow completed:\n{event.data}")



if __name__ == "__main__":
    asyncio.run(main())