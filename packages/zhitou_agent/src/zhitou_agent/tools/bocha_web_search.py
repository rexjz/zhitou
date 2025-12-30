"""Bocha web search tool for agentscope."""

import json
import httpx
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse
from loguru import logger


class BoChaTools:
  def __init__(self, apikey: str):
    self.apikey = apikey
    self.base_url = "https://api.bocha.cn/v1"

  async def bocha_web_search(self, *args, **kwargs):
    return self.web_search(*args, **kwargs)

  async def web_search(
    self,
    query: str,
    count: int = 10,
  ) -> ToolResponse:
    """Search the web using Bocha API and return results. You shuold always call this tool why you are not 100% sure about facts

    Args:
      query (`str`):
        The search query string.
      count (`int`, defaults to `10`, bounded in [1, 50]):
        The number of search results to return.

    Returns:
      `ToolResponse`:
          The response containing the search results from Bocha API,
          including web pages and images.
    """

    headers = {
      "Authorization": f"Bearer {self.apikey}",
      "Content-Type": "application/json",
    }
    payload = {
      "query": query,
      "summary": True,
      "freshness": "noLimit",
      "count": count,
    }

    try:
      async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
          f"{self.base_url}/web-search", json=payload, headers=headers
        )
        response.raise_for_status()
        result = response.json()

        # Check API response code
        if result.get("code") != 200:
          error_msg = result.get("msg", "Unknown error from Bocha API")
          return ToolResponse(
            content=[
              TextBlock(
                type="text",
                text=f"API Error: {error_msg}",
              ),
            ],
          )

        data = result.get("data", {})

        # Format the response as JSON
        web_pages = data.get("webPages")
        web_results = web_pages.get("value", []) if web_pages else []

        # Structure web results
        formatted_web_results = []
        for item in web_results:
          formatted_web_results.append(
            {
              "name": item.get("name", "N/A"),
              "url": item.get("url", "N/A"),
              "snippet": item.get("snippet", "N/A"),
              "siteName": item.get("siteName", ""),
              "dateLastCrawled": item.get("dateLastCrawled", ""),
            }
          )

        # Structure image results
        images = data.get("images")
        image_results = images.get("value", []) if images else []
        formatted_image_results = []
        for img in image_results:
          formatted_image_results.append(
            {
              "contentUrl": img.get("contentUrl", "N/A"),
              "thumbnailUrl": img.get("thumbnailUrl", ""),
              "name": img.get("name", ""),
            }
          )

        # Create JSON response
        json_result = {
          "query": query,
          "totalEstimatedMatches": web_pages.get("totalEstimatedMatches", 0)
          if web_pages
          else 0,
          "webResults": formatted_web_results,
          "imageResults": formatted_image_results,
        }

        return json.dumps(json_result, indent=2) # 这里注意要返回合法JSON String，不然agui前端tool call reponse组件比较难处理

    except httpx.HTTPStatusError as e:
      logger.exception("")
      error_msg = f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
      return ToolResponse(
        content=[
          TextBlock(
            type="text",
            text=f"Error: {error_msg}",
          ),
        ],
      )
    except httpx.RequestError as e:
      logger.exception("")
      error_msg = f"Request error occurred: {str(e)}"
      return ToolResponse(
        content=[
          TextBlock(
            type="text",
            text=f"Error: {error_msg}",
          ),
        ],
      )
    except Exception as e:
      logger.exception("")
      error_msg = f"Unexpected error occurred: {str(e)}"
      return ToolResponse(
        content=[
          TextBlock(
            type="text",
            text=f"Error: {error_msg}",
          ),
        ],
      )
