import httpx
import os
import argparse

from mcp.server.fastmcp import FastMCP
from serpapi import GoogleSearch


def _get_api_key():
    api_key = os.environ.get("SERPAPI_API_KEY", None)
    return api_key


# mcp settings
mcp = FastMCP("web_search")
SERPAPI_API_KEY = _get_api_key()


@mcp.tool()
def google_search(query: str) -> str:
    params = {"engine": "google", "q": query, "api_key": SERPAPI_API_KEY}
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    return organic_results


@mcp.tool()
async def web_search_chinese(query: str) -> str:
    """
    Search the internet for content for Chinese

    Args:
        query: The content to search for, only support chinese queries.

    Returns:
        A summary of the search results.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://open.bigmodel.cn/api/paas/v4/tools",
            headers={"Authorization": os.getenv("ZHIPU_API_KEY")},
            json={
                "tool": "web-search-pro",
                "messages": [{"role": "user", "content": query}],
                "stream": False,
            },
        )

        res_data = []
        for choice in response.json()["choices"]:
            for message in choice["message"]["tool_calls"]:
                search_results = message.get("search_result")
                if not search_results:
                    continue
                for result in search_results:
                    res_data.append(result["content"])
        return "\n\n\n".join(res_data)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Web Search Server")
    parser.add_argument(
        "transport",
        nargs="?",
        default="stdio",
        choices=["stdio", "sse", "streamable-http"],
        help="Transport type (stdio, sse, or streamable-http)",
    )
    args = parser.parse_args()

    # run mcp
    mcp.run(transport=args.transport)
