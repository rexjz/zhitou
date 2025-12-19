"""Bocha web search tool for agentscope."""

import httpx
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse


class BoChaTools:
  def __init__(self, apikey: str):
    self.apikey = apikey
    self.base_url = "https://api.bocha.cn/v1"

  async def bocha_web_search(
    self,
    query: str,
    count: int = 10,
  ) -> ToolResponse:
    """Search the web using Bocha API and return results.

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

        # Format the response as text
        result_text = f"Search results for: {query}\n\n"

        # Add total estimated matches
        web_pages = data.get("webPages", {})
        total_matches = web_pages.get("totalEstimatedMatches", 0)
        result_text += f"Total estimated matches: {total_matches:,}\n\n"

        # Add web search results
        web_results = web_pages.get("value", [])
        if web_results:
          result_text += "Web Results:\n"
          for idx, item in enumerate(web_results, 1):
            name = item.get("name", "N/A")
            url_link = item.get("url", "N/A")
            snippet = item.get("snippet", "N/A")
            site_name = item.get("siteName", "")
            date_crawled = item.get("dateLastCrawled", "")

            result_text += f"{idx}. {name}\n"
            result_text += f"   URL: {url_link}\n"
            if site_name:
              result_text += f"   Site: {site_name}\n"
            result_text += f"   {snippet}\n"
            if date_crawled:
              result_text += f"   Last crawled: {date_crawled}\n"
            result_text += "\n"
        else:
          result_text += "No web results found.\n\n"

        # Add image results if present
        images = data.get("images", {})
        image_results = images.get("value", [])
        if image_results:
          result_text += f"\nImages found: {len(image_results)} images\n"
          for idx, img in enumerate(image_results[:5], 1):  # Show first 5 images
            img_url = img.get("contentUrl", "N/A")
            result_text += f"  {idx}. {img_url}\n"

        return ToolResponse(
          content=[
            TextBlock(
              type="text",
              text=result_text,
            ),
          ],
        )

    except httpx.HTTPStatusError as e:
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
      error_msg = f"Unexpected error occurred: {str(e)}"
      return ToolResponse(
        content=[
          TextBlock(
            type="text",
            text=f"Error: {error_msg}",
          ),
        ],
      )
