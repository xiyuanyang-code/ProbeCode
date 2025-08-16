import httpx
import os
import asyncio
from ddgs import DDGS


def web_search_english(query: str, max_results: int = 5) -> str:
    """
    Search the internet for content using the DuckDuckGo API, only for english content

    Args:
        query: The content to search for, for English content only.
        max_results: The maximum number of results to return.

    Returns:
        A formatted string of search results (title, snippet, and URL).
    """
    try:
        # The DuckDuckGo API is free and does not require an API key.
        # It's a synchronous library, so it runs directly.
        results = DDGS().text(
            query=query, region="us-en", safesearch="off", max_results=max_results
        )

        if not results:
            return "No English search results found."

        formatted_results = []
        for result in results:
            title = result.get("title", "No title")
            snippet = result.get("body", "No description")
            link = result.get("href", "No URL")
            formatted_results.append(
                f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n"
            )

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"An error occurred during the request: {e}"


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
    asyncio.run(web_search_chinese("上海交通大学"))
    # print(duckduckgo_web_search("ShangHai Jiao Tong University")
    pass
