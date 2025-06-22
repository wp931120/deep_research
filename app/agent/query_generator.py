from app.schemas.schemas import QueryGenerationState, OverallState
from app.prompts.prompts import query_writer_instructions
from app.schemas.schemas import QueryGenerationState
import json
from app.llm.llm import LLM
from app.utils import parse_nonstandard_json
from datetime import datetime

def generate_query(state: OverallState) -> QueryGenerationState:
    """Generate search queries based on the research topic."""
    # This is a placeholder for the actual implementation
    # In a real implementation, you would use a language model to generate queries
    print("思考待搜索的查询。")
    
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Format the prompt
    formatted_prompt = query_writer_instructions.format(
        current_date=current_date,
        research_topic=state['messages'][-1]['content'], # Assumes last message is the topic
        number_queries=state['initial_search_query_count']
    ) 
    queries = []
    try:
        # LLM call
        llm = LLM()
        response = llm.chat(formatted_prompt)
        # 尝试解析 JSON
        data = parse_nonstandard_json(response)
        queries = data["queries"]  # 直接获取列表
        return QueryGenerationState(query_list=queries)
    except Exception as e:
        print(f"{e}")
        return QueryGenerationState(query_list=queries)