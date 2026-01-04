from typing import Optional
from agno.agent import Agent
from core.config.models import BochaConfig, DashsopeConfig, DatabaseConfig
from zhitou_agent.config import ZhitouAgentConfig
from zhitou_agent.tools.bocha_web_search import BoChaTools
from zhitou_agent.prompt.system import system_prompt
from agno.models.dashscope import DashScope
from agno.tools.reasoning import ReasoningTools

from agno.db.postgres import PostgresDb
from agno.agent import RunEvent


async def run_ango_agent(config: ZhitouAgentConfig):
  agent = create_agno_zhitou_agent(
    bocha=config.bocha,
    dashscpope=config.dashscpope,
    session_id="test1",
    postgres=config.database,
  )

  print("Agent initialized. Type 'quit' or 'exit' to stop.")
  print("-" * 50)

  while True:
    try:
      user_input = input("\nYou: ").strip()

      if not user_input:
        continue

      if user_input.lower() in ["quit", "exit"]:
        print("Goodbye!")
        break

      print("Agent: ", end="")
      event_stream = agent.arun(user_input)

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

    except KeyboardInterrupt:
      print("\n\nGoodbye!")
      break
    except Exception as e:
      print(f"\n[ERROR] {e}")
      print("Continuing...")


def create_agent_db(db: DatabaseConfig, schema="agno"):
  return PostgresDb(db.url, db_schema=schema)


# class Session


def get_session_chat_history(
  session_id: str, db_config: DatabaseConfig, last_n_runs: int = 10
):
  agent = Agent(db=create_agent_db(db_config))
  return agent.get_session_messages(session_id=session_id, last_n_runs=last_n_runs)


def create_plain_agno_zhitou_agent(
  postgres: DatabaseConfig,
):
  return Agent(
    name="zhitou_agent",
    max_tool_calls_from_history=3,
    db=create_agent_db(postgres),
    num_history_runs=15,
    add_history_to_context=True,
    add_datetime_to_context=True,
    timezone_identifier="Asia/Shanghai",
    markdown=True,
    stream=True,
    stream_events=True,
  )


def create_agno_zhitou_agent(
  bocha: BochaConfig,
  dashscpope: DashsopeConfig,
  postgres: DatabaseConfig,
  session_id: str,
  user_id: Optional[str] = None,
):
  bocha_tools = BoChaTools(apikey=bocha.apikey)

  agent = Agent(
    name="zhitou_agent",
    model=DashScope(
      base_url=dashscpope.openai_compatible_base_url,
      api_key=dashscpope.apikey,
      id="qwen3-max-preview",
    ),
    tools=[bocha_tools.web_search, ReasoningTools(add_instructions=True)],
    instructions=system_prompt,
    max_tool_calls_from_history=3,
    db=create_agent_db(postgres),
    num_history_runs=15,
    add_history_to_context=True,
    add_datetime_to_context=True,
    timezone_identifier="Asia/Shanghai",
    markdown=True,
    session_id=session_id,
    user_id=user_id,
    # reasoning=True,
    # reasoning_model=OpenAIChat(
    # ),
    stream=True,
    stream_events=True,
  )

  return agent
