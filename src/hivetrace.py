from hivetrace import SyncHivetraceSDK
from src.config import Config

hivetrace_instance = SyncHivetraceSDK(
    config={
        "HIVETRACE_URL": Config.HIVETRACE_URL,
        "HIVETRACE_ACCESS_TOKEN": Config.HIVETRACE_ACCESS_TOKEN,
    }
)
