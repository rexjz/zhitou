from zhitou_agent.config import ZhitouAgentConfigLoader, config_logger
from zhitou_agent.agent.agno import run_ango_agent
from loguru import logger
import agentscope
import warnings
import asyncio


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*PydanticDeprecatedSince20.*")
warnings.filterwarnings("ignore", message=".*PydanticDeprecatedSince211.*")


def main():
  print(f"agentscope: {agentscope.__version__}")


if __name__ == "__main__":
  main()

def cli():
  config = ZhitouAgentConfigLoader().load()
  logger.info(config)
  config_logger(config.logging)
  # asyncio.run(run_llamma_index_rect_agent(config))
  asyncio.run(run_ango_agent(config))
  
