from browser_use import Agent, Browser, ChatOpenAI
from agentscope.tool import ToolResponse
from agentscope.message import TextBlock


class WebsiteAccessTool:
  """Tool for accessing websites and extracting information using browser automation."""

  def __init__(self, model: str, openai_apikey: str, openai_baseurl: str):
    """Initialize the website access tool.
    Args:
      openai_apikey: OpenAI API key for the LLM
      openapi_baseurl: OpenAI API base URL
    """
    self.model = model
    self.openai_apikey = openai_apikey
    self.openai_baseurl = openai_baseurl

  async def access_website(self, url: str, extraction_task: str) -> ToolResponse:
    async def _access():
      browser = Browser(headless=True)

      llm = ChatOpenAI(
        model=self.model,
        api_key=self.openai_apikey,
        base_url=self.openai_baseurl,
      )

      task = f"Go to {url} and {extraction_task}"

      agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
      )

      history = await agent.run()

      result = (
        history.final_result() if hasattr(history, "final_result") else str(history)
      )

      return result

    try:
      result = await _access()
      return ToolResponse(
        content=[
          TextBlock(
            type="text",
            text=f"Extracted from {url}: {result}",
          )
        ]
      )
    except Exception as e:
      return ToolResponse(
        content=[
          TextBlock(
            type="text",
            text=f"Error accessing {url}: {str(e)}",
          )
        ]
      )
