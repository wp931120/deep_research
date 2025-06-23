import os
from langchain_community.tools.tavily_search import TavilySearchResults

os.environ["TAVILY_API_KEY"] = "************"

web_search_tool = TavilySearchResults(k=3)

def web_search(queries: list):
    """Perform web search for the given query."""
    if not queries:
        return []
    query = queries[0]
    print(f"正在搜索: {query}\n")
    results = web_search_tool.invoke({"query": query})
    # The tool returns a list of dicts, each with 'url' and 'content'
    # We need to transform it to a list of dicts with 'source' and 'content'
    return [{"source": r.get("url"), "content": r.get("content")} for r in results]
    
