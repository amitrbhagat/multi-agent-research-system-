import asyncio

# from app.mcp.client import mcp_search_session


# async def main():
#     async with mcp_search_session() as session:
#         print("MCP connection established!")

#         tools = await session.list_tools()

#         print("Available MCP tools:")

#         for tool in tools.tools:
#             print(f"- {tool.name}")



from app.tools.web_search_tool import call_web_search


def test_web_search_normal_query():
    results = call_web_search("current weather in Mumbai")
    assert isinstance(results, list)
    if results:
        assert "title" in results[0]
        assert "url" in results[0] 
    return results    


# def test_web_search_specific_factual_query():
#     results = call_web_search("who won the 2024 US presidential election")
#     assert isinstance(results, list)
#     return results


# def test_web_search_ambiguous_query():
#     results = call_web_search("python")
#     assert isinstance(results, list)
#     return results


# def test_web_search_empty_query():
#     results = call_web_search("")
#     # should not crash — either returns [] or handles gracefully
#     assert isinstance(results, list)
#     return results



if __name__ == "__main__":
    # asyncio.run(main())
    
    print(test_web_search_normal_query())
    # print(test_web_search_specific_factual_query())
    # print(test_web_search_ambiguous_query())
    # print(test_web_search_empty_query())

