from agents import Agent, Runner, function_tool, set_trace_processors

from hivetrace.adapters.openai_agents.tracing import (
    HivetraceOpenAIAgentProcessor,
)
from src.config import Config
from src.hivetrace import hivetrace_instance


def _setup_tracing_processor() -> None:
    """Attach HiveTrace OpenAI Agent tracing to the global processor list."""
    set_trace_processors(
        [
            HivetraceOpenAIAgentProcessor(
                application_id=Config.HIVETRACE_APP_ID,
                hivetrace_instance=hivetrace_instance,
            )
        ]
    )


@function_tool(description_override="Calculates the sum of two numbers")
def calculate_sum(a: int, b: int) -> int:
    return a + b


@function_tool(description_override="Counts words in a text")
def count_words(text: str) -> int:
    return len(text.split())


@function_tool(description_override="Formats text to sentence case")
def format_sentence(text: str) -> str:
    t = text.strip()
    if not t:
        return t
    return t[0].upper() + t[1:]


class OrchestratorAgent:
    """Orchestrator over specialized sub-agents using OpenAI Agents runtime."""

    def __init__(self) -> None:
        _setup_tracing_processor()

        self.math_agent = Agent(
            name="MathAgent",
            instructions="You are a math agent. Use calculate_sum when needed.",
            tools=[calculate_sum],
            model=Config.MODEL,
        )

        self.text_agent = Agent(
            name="TextAgent",
            instructions=(
                "You are a text agent. Use count_words and format_sentence when needed."
            ),
            tools=[count_words, format_sentence],
            model=Config.MODEL,
        )

        self.orchestrator = Agent(
            name="MainHub",
            model=Config.MODEL,
            instructions=(
                "You are a coordinator. Determine if the query is about math or text.\n"
                "- If it's about numbers/counting, delegate to MathAgent.\n"
                "- If it's about text/words/formatting, delegate to TextAgent.\n"
                "Return the consolidated answer."
            ),
            handoffs=[self.math_agent, self.text_agent],
        )

    async def arun(self, query: str) -> str:
        result = await Runner.run(self.orchestrator, query)
        return getattr(result, "final_output", "")

    def run(self, query: str) -> str:
        result = Runner.run_sync(self.orchestrator, query)
        return getattr(result, "final_output", "")
