import asyncio
import json
import logging

from pydantic import BaseModel, ValidationError

from app.mcp.client import mcp_fetch_session
from app.tools.retry_utils import with_retry

logger = logging.getLogger(__name__)


class PageFetchInput(BaseModel):
    url:str


class PageFetchOutput(BaseModel):
    url:str
    content:str


@with_retry(max_attempts=3)
async def _call_page_fetch_async(tool_input: PageFetchInput) -> PageFetchOutput:
    async with mcp_fetch_session() as session:
        response = await session.call_tool(
            "fetch", arguments={"url": tool_input.url}
        )

        raw_text = response.content[0].text
        return PageFetchOutput(url=tool_input.url, content=raw_text)


def call_page_fetch(url:str) -> dict|None:
    try:
        tool_input = PageFetchInput(url)
        output = asyncio.run(_call_page_fetch_async(tool_input))
        return output.model_dump()
    except Exception as e:
        logger.error(f"page_fetch tool call failed: {e}")
        return None

