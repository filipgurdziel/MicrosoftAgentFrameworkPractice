
import asyncio
from typing_extensions import Never

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler, executor


class UpperCase(Executor):
    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert input to uppercase and forward it to the next node."""
        result = text.upper()
        print(f"    [UpperCase executed] '{text}' -> '{result}'")
        await ctx.send_message(result)


# WorkflowContext[Never, str] means:
#   Never -> this executor does NOT send a message onward (it's the end of the line)
#   str   -> it YIELDS a str as the workflow's final output instead

@executor(id="reverse_text_executor")
async def reverse_text(text: str, ctx: WorkflowContext[Never, str]) -> None:
    """Reverse the text and yield it as the workflow's output."""
    result = text[::-1]
    print(f"    [reverse_text executed] '{text}' -> '{result}'")
    await ctx.yield_output(result)


async def main():
    upper_case = UpperCase(id="upper_case_executor")

    workflow = (
        WorkflowBuilder(start_executor=upper_case, output_from=[reverse_text])
        .add_edge(upper_case, reverse_text)
        .build()
    )

    print("Running workflow with input: 'Hello, World!'\n")

    async for event in workflow.run("Hello, World!", stream=True):
        print(f"Event: {event}")
        if event.type == "output":
            print(f"\nWorkflow completed with result: {event.data}")


if __name__ == "__main__":
    asyncio.run(main())