import asyncio
import json
from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import DashScopeChatModel
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit, view_text_file
from loguru import logger
from zhitou_agent.config import AgentConfigLoader, config_logger
from zhitou_agent.tools.bocha_web_search import BoChaTools
from zhitou_agent.prompt.system import system_prompt

async def agent_test():
  
  config = AgentConfigLoader().load()  
  logger.info(config)
  config_logger(config.logging)

  toolkit = Toolkit()
  # toolkit.register_tool_function(execute_python_code)
  # toolkit.register_tool_function(execute_shell_command)

  # Register bocha web search tool
  bocha_tools = BoChaTools(apikey=config.bocha.apikey)
  toolkit.register_tool_function(bocha_tools.bocha_web_search)
  toolkit.register_tool_function(view_text_file)

  agent = ReActAgent(
    name="zhitou_agent",
    sys_prompt=system_prompt,
    model=DashScopeChatModel(
      model_name="qwen-max",
      api_key=config.dashscpope.apikey,
      stream=True,
    ),
    memory=InMemoryMemory(),
    formatter=DashScopeChatFormatter(),
    toolkit=toolkit,
  )

  user = UserAgent(name="user")

  msg = None
  while True:
    msg = await agent(msg)
    print(json.dumps(agent.memory.state_dict(), indent=2, ensure_ascii=False))
    msg = await user(msg)
    if msg.get_text_content() == "exit":
      break


def cli():
  asyncio.run(agent_test())

