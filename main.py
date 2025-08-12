import os

from fastapi import FastAPI

from src.api.router import router
from src.config import Config
from src.core.orchestrator import OrchestratorAgent

app = FastAPI(
    title="OpenAI Agents API",
    description="Multi-agent orchestrator on OpenAI Agents with HiveTrace",
    version="0.2.0",
)

app.include_router(router)

print(Config.HIVETRACE_APP_ID)


@app.on_event("startup")
async def startup_event() -> None:
    if not os.getenv("OPENAI_API_KEY") and not Config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    app.state.orchestrator = OrchestratorAgent()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
