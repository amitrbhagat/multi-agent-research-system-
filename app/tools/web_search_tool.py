import asyncio
import json
import logging

from pydantic import BaseModel, ValidationError
from app.mcp.client import mcp_search_session

logger = logging.getLogger(__name__)


class WebSearchInput(BaseModel):
    query:str
    max_results: int=5


class WebSearchResultItem(BaseModel):
    title:str
    url:str
    snippet:str


class WebSearchOutput(BaseModel):
    result:list[WebSearchResultItem]        


async def _call_web_search_async(tool_input:WebSearchInput) -> WebSearchOutput:
    async with mcp_search_session() as session:
        response = await session.call_tool(
            "tavily_search",
            arguments={
                "query":tool_input.query,
                "max_results":tool_input.max_results
            },
        )

    raw_text = response.content[0].text
    parsed = json.loads(raw_text)    

    return WebSearchOutput(
        results = [
            WebSearchResultItem(
                title = item.get("title", ""),
                url = item.get("url", ""),
                snippet = item.get("content","")
            )
            for item in parsed.get("results", [])
        ]
    )


def call_web_search(query:str, max_results:int=5)->list[dict]:
    try:
        tool_input = WebSearchInput(query=query, max_results = max_results)
        output = asyncio.run(_call_web_search_async(tool_input))
        return [item.model_dump() for item in output.results]
    except (ValidationError, json.JSONDecodeError, Exception) as e:
        logger.error(f"web_search tool call failed: {e}")
        return []