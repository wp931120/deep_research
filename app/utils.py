import re 
import json


def parse_nonstandard_json(json_str: str) -> dict:
    """
    解析包含任意换行符和非标准格式的JSON字符串
    
    参数:
        json_str: 包含JSON数据的非标准字符串
    
    返回:
        解析后的字典数据，如果失败则返回空字典
    """
    # 移除"json"前缀和多余空白字符
    cleaned_str = re.sub(r'^json\s*', '', json_str).strip()
    
    # 尝试直接解析
    try:
        return json.loads(cleaned_str)
    except json.JSONDecodeError:
        pass
    
    # 提取JSON对象的主体部分（从第一个{到最后一个}）
    try:
        start_idx = cleaned_str.index('{')
        end_idx = cleaned_str.rindex('}') + 1
        json_body = cleaned_str[start_idx:end_idx]
        return json.loads(json_body)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"JSON解析失败: {e}")
        return {}