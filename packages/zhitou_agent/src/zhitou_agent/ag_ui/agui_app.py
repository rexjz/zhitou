from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from zhitou_agent.agent.agno import create_agno_zhitou_agent
from zhitou_agent.config import ZhitouAgentConfigLoader
from loguru import logger
import time

def create_agui_agno_app(session_id, user_id):
  start_time = time.time()
  # logger.info(f"Starting AGUI agno app creation for session_id={session_id}, user_id={user_id}")

  config = ZhitouAgentConfigLoader().load()

  agent = create_agno_zhitou_agent(
    session_id=session_id,
    user_id=user_id,
    bocha=config.bocha,
    dashscpope=config.dashscpope
  )
  agui_interface = AGUI(agent=agent)
  agent_os = AgentOS(agents=[agent], interfaces=[agui_interface])
  app = agent_os.get_app()

  elapsed_time = time.time() - start_time
  logger.info(f"AGUI agno app created successfully in {elapsed_time:.3f} seconds (session_id={session_id}, user_id={user_id})")

  return app