import httpx
import os

async def web_search(query: str) -> str:
    """
    Search the internet for content.

    Args:
        query: The content to search for.

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
