import json
from zhitou_agent.config import ZhitouAgentConfigLoader, config_logger
from zhitou_agent.agent.agno import create_agent_db, run_ango_agent
from loguru import logger
import agentscope
import warnings
import asyncio
from agno.agent import Agent

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
  
def test_get_history():
  config = ZhitouAgentConfigLoader().load()
  logger.info(config)
  agent = Agent(
    name="zhitou_agent",
    max_tool_calls_from_history=3,
    db=create_agent_db(config.database),
    num_history_runs=15,
    add_history_to_context=True,
    add_datetime_to_context=True,
    timezone_identifier="Asia/Shanghai",
    markdown=True,
    stream=True,
    stream_events=True,
  )
  messages = agent.get_session_messages(session_id="session_1767549621369_5chrmc6qtk", last_n_runs=5)
  json_list =  [m.model_dump() for m in messages]
  print(json_list)