from zhitou_agent.tools.browser_use_website_access import WebsiteAccessTool
from zhitou_agent.config import ZhitouAgentConfigLoader, config_logger
from zhitou_agent.tools.bocha_web_search import BoChaTools
from zhitou_agent.tools.time_tools import get_current_time
from zhitou_agent.prompt.system import system_prompt
from agentscope.formatter import DashScopeChatFormatter
from agentscope.tool import Toolkit, view_text_file
from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import DashScopeChatModel
from agentscope.plan import PlanNotebook
from agentscope.memory import InMemoryMemory

from loguru import logger


def post_reply_hook_function(*args):
  print("post_reply_hook_function: ", args, "\n")


# def pre_observe_hook_function(*args):
#   print("pre_observe_hook_function: ", args, "\n")


def post_acting_hook_function(*args):
  print("post_acting_hook_function: ", args, "\n")


plan_notebook = PlanNotebook()


async def agentscope_agent_cli():
  config = ZhitouAgentConfigLoader().load()
  logger.info(config)
  config_logger(config.logging)

  toolkit = Toolkit()
  bocha_tools = BoChaTools(apikey=config.bocha.apikey)
  # website_access_tools = WebsiteAccessTool(
  #   openai_apikey=config.dashscpope.apikey,
  #   openai_baseurl=config.dashscpope.openai_compatible_base_url,
  #   model="qwen-max",
  # )
  toolkit.register_tool_function(bocha_tools.bocha_web_search)
  toolkit.register_tool_function(view_text_file)
  toolkit.register_tool_function(get_current_time)
  # toolkit.register_tool_function(website_access_tools.access_website)
  llm = DashScopeChatModel(
    model_name="qwen-max",
    api_key=config.dashscpope.apikey,
    stream=True,
  )
  agent = ReActAgent(
    name="zhitou_agent",
    sys_prompt=system_prompt,
    model=llm,
    memory=InMemoryMemory(),
    formatter=DashScopeChatFormatter(),
    toolkit=toolkit,
    plan_notebook=plan_notebook,
  )

  # agent.register_instance_hook("post_reply", "hook1", post_reply_hook_function)

  # agent.register_instance_hook("post_acting", "hook2", post_acting_hook_function)

  user = UserAgent(name="user")
  agent
  msg = None
  while True:
    msg = await agent(msg)
    # print(json.dumps(agent.memory.state_dict(), indent=2, ensure_ascii=False))
    msg = await user(msg)
    if msg.get_text_content() == "exit":
      break
