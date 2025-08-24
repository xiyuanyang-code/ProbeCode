import httpx
import os
import asyncio
from ddgs import DDGS


def web_search_english(query: str, max_results: int = 5) -> str:
    """
    Performs a web search for English content using the DuckDuckGo API.

    This function serves as a tool for searching English-language content on the internet.
    It should only be used when the user's query is in English and a web search is explicitly requested.

    Args:
        query: The English content to search for.
        max_results: The maximum number of results to return.

    Returns:
        A formatted string of search results (title, snippet, and URL).

    Examples:
        **Positive Examples:**
        1. **User Request:** "Find me the latest news on artificial intelligence breakthroughs from sources in the US."
           **Explanation:** The user's request is in English and directly asks for "news" and "breakthroughs," indicating a clear need for a web search. The query is specific and actionable.
           **Tool Call:** `web_search_english(query="latest news on artificial intelligence breakthroughs")`
        2. **User Request:** "What is the capital of France, and what is its current population? Please search the web for this."
           **Explanation:** The user explicitly asks the system to "search the web" for information. The query is in English, and the request is specific and factual, making it a perfect use case for a web search tool.
           **Tool Call:** `web_search_english(query="capital of France and current population")`

        **Negative Examples:**
        1. **User Request:** "我想了解上海的天气。"
           **Explanation:** The user's query is in Chinese. This tool is designed exclusively for English searches. Using this tool would return irrelevant results or an error. The correct action is to call the `web_search_chinese` tool instead.
           **Correct Response:** The system should determine the language of the query is Chinese and call `web_search_chinese` with the query "上海的天气".
        2. **User Request:** "I'm looking for a file named 'report.pdf' on my computer."
           **Explanation:** The user is asking to find a local file, not to perform an internet search. Using a web search tool for this request would be incorrect and would not yield the desired result.
           **Correct Response:** "I can only search the internet. To find a file on your computer, please use a local file search command."
    """
    try:
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
    Performs a web search for Chinese content.

    This function serves as a tool for searching Chinese-language content on the internet.
    It should only be used when the user's query is in Chinese and a web search is explicitly requested.

    Args:
        query: The Chinese content to search for.

    Returns:
        A summary of the search results.

    Examples:
        **Positive Examples:**
        1. **User Request:** "请帮我搜索2024年北京奥运会的相关新闻。"
           **Explanation:** 用户的请求是中文，并且明确要求“搜索”与“北京奥运会”相关的“新闻”。这是一个清晰、具体的指令，可以直接调用该工具。
           **Tool Call:** `web_search_chinese(query="2024年北京奥运会新闻")`
        2. **User Request:** "我想知道深圳今天的气温是多少，请帮我在网上查一下。"
           **Explanation:** 用户明确要求“在网上查一下”，并给出了具体的查询内容“深圳今天的气温”。请求语言是中文，指令清晰，适合调用此工具。
           **Tool Call:** `web_search_chinese(query="深圳今天的气温")`

        **Negative Examples:**
        1. **User Request:** "What is the best way to learn Python?"
           **Explanation:** 用户的请求是英文。此工具专用于中文搜索。如果调用此工具，可能会因为语言不匹配而返回错误或不相关的结果。正确的做法是调用 `web_search_english` 工具。
           **Correct Response:** The system should determine the language of the query is English and call `web_search_english` with the query "best way to learn Python".
        2. **User Request:** "这本书写的怎么样？"
           **Explanation:** 用户的请求是模糊的，没有提供书名，无法进行精确的搜索。如果直接调用工具，会得到不相关的结果。系统应先向用户询问具体的书名。
           **Correct Response:** "您指的是哪本书？请提供具体的书名以便我进行搜索。"
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