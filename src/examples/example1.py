"""
This example shows how to use hivetrace with a simple agent with tools.

"""

from agents import (
    Agent,
    function_tool,
    set_trace_processors,
)

from hivetrace.adapters.openai_agents.tracing import HivetraceOpenAIAgentProcessor
from src.config import Config
from src.hivetrace import hivetrace_instance

# NOTE: In this example, we pass the hivetrace_instance (which was defined earlier) to the HivetraceTracingProcessor
set_trace_processors(
    [
        HivetraceOpenAIAgentProcessor(
            application_id=Config.APPLICATION_ID,
            hivetrace_instance=hivetrace_instance,
        )
    ]
)


@function_tool(description_override="Calculates the sum of two numbers")
def calculate_sum(a: int, b: int) -> int:
    return a + b


@function_tool(description_override="Shows weather in the city")
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny with 25°C."


orchestrator_agent_example1 = Agent(
    name="SystemAgent",
    model=Config.MODEL,
    instructions=(
        "You have two tools: calculate_sum and get_weather "
        "Use them to form your response."
    ),
    tools=[calculate_sum, get_weather],
)
