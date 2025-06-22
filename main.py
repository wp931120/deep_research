import traceback
from concurrent.futures import ThreadPoolExecutor
from app.agent.query_generator import generate_query
from app.agent.web_researcher import web_research_node
from app.agent.reflection import reflection_node
from app.agent.answer_finalizer import finalize_answer_node
from app.schemas.schemas import OverallState, WebSearchState
import warnings
warnings.filterwarnings("ignore")

def main(research_topic: str):
    """运行DeepResearch管道的主函数"""
    
    # 初始化状态
    initial_state: OverallState = {
        "messages": [{"role": "user", "content": research_topic}],
        "search_query": [],
        "follow_up_queries": [],
        "web_research_result": [],
        "sources_gathered": [],
        "initial_search_query_count": 2,
        "max_research_loops": 2,
        "research_loop_count": 0
    }
    
    print(f"## 开始研究: {research_topic}")
    
    # 主研究循环
    while initial_state['research_loop_count'] < initial_state['max_research_loops']:
        print(f"\n--- ## 研究轮次 {initial_state['research_loop_count'] + 1} ---")
        if initial_state['research_loop_count'] == 0:
            # 1. 生成查询
            query_state = generate_query(initial_state)
            queries = query_state.query_list
            print(f"Generated queries: {queries}")
            # 2. 对每个查询执行网络研究
            with ThreadPoolExecutor() as executor:
                # 准备WebSearchState对象列表用于并发执行
                web_search_states = [WebSearchState(search_query=query, id=i) for i, query in enumerate(queries)]
                # 并发提交web_research_node任务
                # map函数将web_research_node应用于web_search_states中的每个项目
                # 并返回一个迭代器，在任务完成时产生结果
                for research_results in executor.map(web_research_node, web_search_states):
                    initial_state['web_research_result'].extend(research_results['web_research_result'])
                    initial_state['search_query'].append(research_results['search_query'])
                    initial_state['sources_gathered'].append(research_results["sources_gathered"])

        else:
            # 4.后续查询搜索
            queries = initial_state['follow_up_queries']
            with ThreadPoolExecutor() as executor:
                # 准备WebSearchState对象列表用于并发执行
                web_search_states = [WebSearchState(search_query=query, id=i) for i, query in enumerate(queries)]

                # 并发提交web_research_node任务
                for research_results in executor.map(web_research_node, web_search_states):
                    initial_state['web_research_result'].extend(research_results['web_research_result'])
                    initial_state['search_query'].append(research_results['search_query'])
                    initial_state['sources_gathered'].append(research_results["sources_gathered"])

        
        # 3. 反思结果， 生成后续查询
        reflection_results = reflection_node(initial_state)
        initial_state['research_loop_count'] = reflection_results['research_loop_count']
        initial_state['follow_up_queries'] = reflection_results['follow_up_queries']
        if reflection_results['is_sufficient']:
            print("Information is sufficient. Finalizing answer.")
            break
        else:
            print(f"Knowledge gap: {reflection_results['knowledge_gap']}")
            print(f"Follow-up queries: {reflection_results['follow_up_queries']}")
        

    # 5. 最终答案生成
    final_answer = finalize_answer_node(initial_state)
    final_answer = final_answer[0]['messages'][0]['content']
    
    print("\n---## 最终报告 ---")
    print(final_answer)

if __name__ == "__main__":
    try:
        main("母婴博主怎么做")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())