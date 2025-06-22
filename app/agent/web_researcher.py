from app.schemas.schemas import WebSearchState, WebSearchResult
from app.tools.tools import web_search
from app.llm.llm import LLM
from app.prompts.prompts import summarizer_instructions

def web_research_node(state: WebSearchState) -> WebSearchResult:
    """
    Perform web search for the given query, summarize the results, and provide sources.
    """
    try:
        # 1. Perform web search
        query = state['search_query']
        search_results = web_search([query])
        
        if not search_results:
            return {
                "web_research_result": [],
                "sources_gathered": [],
                "search_query": query
            }

        sources_gathered = [{"source": res['source'], "content": res['content']} for res in search_results]
        # 2. Format search results for the summarizer prompt
        formatted_results = "\n\n".join([f"[{i+1}] {res['content']}" for i, res in enumerate(search_results)])
        # 3. Create the prompt for the LLM
        prompt = summarizer_instructions.format(query=query, results=formatted_results)
        # 4. Call the LLM to generate a summary
        llm = LLM()
        summary = llm.chat(prompt)
        # 5. Return the summarized result and sources
        return {
            "web_research_result": [summary],  # Wrap in list to match schema
            "sources_gathered": sources_gathered,
            "search_query": query
        }
    except Exception as e:
        print(f"Error during web research: {e}")
        return {
            "web_research_result": [],
            "sources_gathered": [],
            "search_query": state['search_query']
        }