# main.py
import asyncio
from llama_index.llms.dashscope import DashScope
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from zhitou_agent.config import ZhitouAgentConfig, ZhitouAgentConfigLoader, config_logger
from zhitou_agent.tools.bocha_web_search import BoChaTools
from zhitou_agent.prompt.system import system_prompt
from zhitou_agent.tools.time_tools import get_current_time
from llama_index.core.memory import Memory
from llama_index.llms.openai_like import OpenAILike
from loguru import logger
from llama_index.core.agent.workflow.workflow_events import (
  AgentInput,
  AgentStream,
  AgentOutput,
  ToolCall,
  ToolCallResult,
)
from rich.console import Console
from rich.markdown import Markdown
from llama_index.core.workflow import Context

console = Console()


async def run_llamma_index_rect_agent(config: ZhitouAgentConfig):
  bocha_tools = BoChaTools(apikey=config.bocha.apikey)
  # website_access_tools = WebsiteAccessTool(
  #   openai_apikey=config.dashscpope.apikey,
  #   openai_baseurl=config.dashscpope.openai_compatible_base_url,
  #   model="qwen-max",
  # )
  # llm = DashScope(model_name="qwen-max", api_key=config.dashscpope.apikey)
  llm = OpenAILike(
    is_chat_model=True,
    api_base=config.dashscpope.openai_compatible_base_url,
    api_key=config.dashscpope.apikey,
    model="qwen-max",
  )
  tools = [bocha_tools.bocha_web_search, get_current_time]

  agent = ReActAgent(
    sys_prompt=system_prompt,
    verbose=True,
    tools=tools,
    llm=llm,
  )

  console.print("[bold blue]Agent CLI Ready! 输入 exit 退出[/bold blue]\n")

  memory = Memory.from_defaults(session_id="session1", token_limit=40000)
  while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ("exit", "quit"):
      print("Goodbye!")
      break

    # Prepare context with memory
    ctx = Context(agent)

    async def run_agent():
      handler = agent.run(
        user_msg=user_input, ctx=ctx, max_iterations=30, memory=memory
      )

      text_buffer = ""

      async for ev in handler.stream_events():
        # 用户输入事件
        if isinstance(ev, AgentInput):
          print("[INPUT]", ev)

        # 工具调用事件
        elif isinstance(ev, ToolCall):
          print("[TOOL CALL]", ev)

        # 工具调用结果
        elif isinstance(ev, ToolCallResult):
          print("[TOOL RESULT]", ev)

        # LLM 实时片段
        if isinstance(ev, AgentStream):
          print(ev.delta, end="", flush=True)
          text_buffer += ev.delta

        # 完整输出
        elif isinstance(ev, AgentOutput):
          print("\n[FINAL OUTPUT]", ev)

      # Wait for final structured response
      response = await handler

      return text_buffer, response

    # Execute the async run
    text_buffer, final_response = await run_agent()

    # Optionally store user/assistant in your memory (manual add)
    # memory.add_message({"role": "user",    "content": user_input})
    # memory.add_message({"role": "assistant","content": text_buffer})

    console.print(f"\n[bold blue]=== 回合结束 ===[/bold blue]")
    console.print(f"memory snapshot: {memory.get_all()}")


def cli():
  asyncio.run(run_llamma_index_rect_agent())


if __name__ == "__main__":
  cli()
