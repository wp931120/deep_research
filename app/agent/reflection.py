from re import T
from app.schemas.schemas import ReflectionState, OverallState
from app.prompts.prompts import reflection_instructions
from app.llm.llm import LLM
from datetime import datetime
from app.utils import parse_nonstandard_json

def reflection_node(state: OverallState) -> ReflectionState:
    """Reflect on the gathered information and decide if more research is needed."""
    print("## 反思已收集的信息，决定是否需要更多的研究。")
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        formatted_prompt = reflection_instructions.format(
            current_date=current_date,
            research_topic=state['messages'][-1]['content'],
            summaries="\n\n---\n\n".join(state["web_research_result"])
        )
        # LLM call
        llm = LLM()
        response = llm.chat(formatted_prompt)
        # 尝试解析 JSON
        result = parse_nonstandard_json(response)

        return {
            "is_sufficient": result['is_sufficient'],
            "knowledge_gap": result['knowledge_gap'],
            "follow_up_queries": result['follow_up_queries'],
            "research_loop_count": state['research_loop_count'] + 1,
            "number_of_ran_queries": len(state['search_query'])
        }
    except Exception as e:
        print(f"Error during reflection: {e}")
        return {        
            "is_sufficient": False,
            "knowledge_gap": "Unknown",
            "follow_up_queries": [],
            "research_loop_count": state['research_loop_count'] + 1,
            "number_of_ran_queries": len(state['search_query'])
        }