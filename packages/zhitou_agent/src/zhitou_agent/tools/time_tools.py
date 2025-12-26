from datetime import datetime
from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

def get_current_time() -> ToolResponse:
  """get current time date str, in format %Y-%m-%d %H:%M

  Returns:
      str: date str
  """
  return ToolResponse(
    content=[
      TextBlock(
        type="text",
        text=f"current time is {datetime.now().strftime('%Y-%m-%d %H:%M')}",
      ),
    ],
  )
