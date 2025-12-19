import asyncio
from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import DashScopeChatModel
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit
from loguru import logger
from zhitou_agent.config import AgentConfigLoader

async def agent_test():
  toolkit = Toolkit()
  # toolkit.register_tool_function(execute_python_code)
  # toolkit.register_tool_function(execute_shell_command)

  config = AgentConfigLoader().load()  # noqa: F821
  logger.info(config)

  agent = ReActAgent(
    name="zhitou_agent",
    sys_prompt="You're a helpful assistant named Friday.",
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
    msg = await user(msg)
    if msg.get_text_content() == "exit":
      break

def cli():
  asyncio.run(agent_test())
