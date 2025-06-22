from re import search
from app.schemas.schemas import OverallState
from app.prompts.prompts import answer_instructions
from app.llm.llm import LLM
from datetime import datetime
import re

def finalize_answer_node(state: OverallState):
    """Synthesize the gathered information into a final answer."""
    print("形成最终答案...")
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    formatted_sources = state.get("sources_gathered", [])
    sources_map, summaries = mapping_source(state)

    formatted_prompt = answer_instructions.format(
        current_date=current_date,
        research_topic=state['messages'][-1]['content'],
        summaries=summaries,
        sources=formatted_sources
    )
    # LLM call
    llm = LLM()
    response = llm.chat(formatted_prompt)
    return {"messages": [{"role": "assistant", "content": response}]} , sources_map

def mapping_source(state: OverallState):
    sources_gathered = state.get("sources_gathered", [])
    search_results = state.get("web_research_result", [])
    sources_map = {}
    i = 1
    pattern = r'\[(\d+)\]'
    reformat_search_results = []
    for sources, search_result in zip(sources_gathered,search_results):
        reformat_search_result = re.sub(pattern, lambda m: f'[{int(m.group(1)) + i}]', search_result)
        reformat_search_results.append(reformat_search_result)
        for source in sources:
            sources_map[i] = source
            i += 1
    summaries = "\n\n---\n\n".join(reformat_search_results)
    return sources_map, summaries
