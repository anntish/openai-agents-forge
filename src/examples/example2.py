"""
This example shows how to use hivetrace with multiple agents.

"""

from agents import (
    Agent,
    Runner,
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
            application_id=Config.HIVETRACE_APP_ID,
            hivetrace_instance=hivetrace_instance,
        )
    ]
)


@function_tool(description_override="Calculates the sum of two numbers")
def calculate_sum(a: int, b: int) -> int:
    return a + b


@function_tool
async def sum_agent_tool(query: str) -> str:
    sum_agent = Agent(
        name="SumAgent",
        instructions="You are a sum agent. Use the calculate_sum tool.",
        tools=[calculate_sum],
        model=Config.MODEL,
    )
    result = await Runner.run(sum_agent, query)
    return result.final_output


@function_tool(description_override="Shows weather in the city")
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny with 25°C."


@function_tool
async def weather_agent_tool(query: str) -> str:
    weather_agent = Agent(
        name="WeatherAgent",
        instructions="You are a weather agent. Use the get_weather tool.",
        tools=[get_weather],
        model=Config.MODEL,
    )
    result = await Runner.run(weather_agent, query)
    return result.final_output


orchestrator_agent_example2 = Agent(
    name="OrchestratorAgent",
    model=Config.MODEL,
    instructions=(
        "You have two tools: weather_agent_tool and sum_agent_tool "
        "Use them to form your response."
    ),
    tools=[weather_agent_tool, sum_agent_tool],
)
