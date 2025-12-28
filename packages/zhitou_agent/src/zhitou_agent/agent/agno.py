from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from zhitou_agent.config import ZhitouAgentConfig
from zhitou_agent.tools.bocha_web_search import BoChaTools
from zhitou_agent.prompt.system import system_prompt
from agno.db.sqlite import SqliteDb
from agno.agent import RunEvent


async def run_ango_agent(config: ZhitouAgentConfig):
  bocha_tools = BoChaTools(apikey=config.bocha.apikey)

  agent = Agent(
    model=OpenAILike(
      base_url=config.dashscpope.openai_compatible_base_url,
      api_key=config.dashscpope.apikey,
      id="qwen-max",
    ),
    tools=[bocha_tools.web_search],
    instructions=system_prompt,
    max_tool_calls_from_history=3,
    db=SqliteDb(db_file="/home/rexjz/Workspace/dianzhang/zhitou/.logs/agno.db"),
    add_history_to_context=True,
    add_datetime_to_context=True,
    timezone_identifier="Asia/Shanghai",
    markdown=True,
    session_id="test1",
  )

  event_stream = agent.arun(
    "what are you doing just now", stream=True, stream_events=True
  )

  async for event in event_stream:
    if event.event == RunEvent.run_content:
      print(f"{event.content}", end="")
    elif event.event == RunEvent.tool_call_started:
      print(f"\n[TOOL_CALL_START] {event.tool.tool_name}{event.tool}")
    elif event.event == RunEvent.tool_call_completed:
      print(f"\n[TOOL_CALL_DONE] {event}")
    elif event.event == RunEvent.reasoning_step:
      print(f"[REASONING] {event.reasoning_content}")
    elif event.event == RunEvent.run_completed:
      print("\n[RUN COMPLETED]")
