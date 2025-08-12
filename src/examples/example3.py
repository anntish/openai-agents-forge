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
            application_id=Config.HIVETRACE_APP_ID,
            hivetrace_instance=hivetrace_instance,
        )
    ]
)


@function_tool
def calculate_sum(a: int, b: int) -> int:
    return a + b


@function_tool
def calculate_complex(a: int, b: int) -> int:
    return a * b


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny with 25°C."


complex_agent = Agent(
    name="ComplexAgent",
    instructions="You are a complex agent. Use the calculate_complex tool.",
    tools=[calculate_complex],
    model=Config.MODEL,
)


sum_agent = Agent(
    name="SumAgent",
    instructions="You are a sum agent. Use the calculate_sum tool.",
    tools=[calculate_sum],
    model=Config.MODEL,
)

math_agent = Agent(
    name="MathAgent",
    instructions="""You are a router. If the part of the request belongs to mathematics — solve it.
If the part of the request doesn't belong to you — don't answer yourself, but return it to the top,
so that another agent can handle it.
""",
    model=Config.MODEL,
    handoffs=[sum_agent, complex_agent],
)

weather_agent = Agent(
    name="WeatherAgent",
    instructions="You are a weather agent. Use the get_weather tool.",
    tools=[get_weather],
    model=Config.MODEL,
    tool_use_behavior="stop_on_first_tool",
)


orchestrator_agent_instructions = (
    "Ты маршрутизатор. Делай следующее:\n"
    "- Раздели входной запрос на независимые части, если он содержит несколько задач.\n"
    "- Для каждой части выбери подходящего агента из списка.\n"
    "- Собери результаты от агентов и верни общий ответ.\n"
    "Если запрос про сумму или числа — передай MathAgent.\n"
    "Если про погоду или город — передай WeatherAgent."
)

orchestrator_agent_example3 = Agent(
    name="OrchestratorAgent",
    model=Config.MODEL,
    instructions=orchestrator_agent_instructions,
    handoffs=[math_agent, weather_agent],
)
