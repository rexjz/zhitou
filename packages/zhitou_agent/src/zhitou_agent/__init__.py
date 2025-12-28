import asyncio
import agentscope
from loguru import logger
from zhitou_agent.agent.agent_scope import agentscope_agent_cli
from zhitou_agent.agent.agno import run_ango_agent
from zhitou_agent.agent.llamma_index import run_llamma_index_rect_agent
import warnings

from zhitou_agent.config import ZhitouAgentConfigLoader, config_logger

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
  
