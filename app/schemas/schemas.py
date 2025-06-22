
from typing import Dict, List, TypedDict, Annotated, Any
import operator
from pydantic import BaseModel

class OverallState(TypedDict):
    messages: Annotated[list, operator.add]
    search_query: Annotated[list, operator.add]
    follow_up_queries: Annotated[list, operator.add]
    web_research_result: Annotated[list, operator.add]
    sources_gathered: Annotated[list, operator.add]
    initial_search_query_count: int
    max_research_loops: int
    research_loop_count: int

class QueryGenerationState(BaseModel):
    query_list: List[str]

class WebSearchState(TypedDict):
    search_query: str
    id: int

class WebSearchResult(TypedDict):
    web_research_result: List[str]
    sources_gathered: List[Dict[Any, Any]]
    search_query: str

class ReflectionState(TypedDict):
    is_sufficient: bool
    knowledge_gap: str
    follow_up_queries: List[str]
    research_loop_count: int
    number_of_ran_queries: int