# DeepResearch

## 项目概述

DeepResearch 是一个基于大型语言模型（LLM）的深度研究代理。它能够根据用户提供的主题，自动生成研究查询，执行网络搜索，对搜索结果进行反思，并最终生成一份全面的研究报告。该系统旨在自动化和优化信息收集与分析的过程，为用户提供深入的洞察。
支持本地ollama ,vllm, 以及openrouter 等大模型调用方式。
## 功能特点
主要实现下方流程图
![image](https://github.com/user-attachments/assets/c0f22ff7-c236-40b5-86a9-faec43652d6a)
   
- **智能查询生成**：根据研究主题自动生成多轮查询。
- **网络研究**：通过网络搜索获取相关信息和数据。
- **结果反思**：对搜索结果进行分析和反思，识别知识空白并生成后续查询。
- **迭代研究**：支持多轮研究循环，逐步深化研究内容。
- **最终报告生成**：综合所有研究结果，生成结构化且全面的最终报告。
- **结果溯源**：生成的报告内容，都能索引到信息来源。
## 安装

在开始之前，请确保您已安装 Python 3.8 或更高版本。

1. **克隆仓库**：

   ```bash
   git clone https://github.com/your-repo/deep_research.git
   cd deep_research
   ```

2. **创建并激活虚拟环境**（推荐）：

   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **安装依赖**：

   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` 文件包含以下依赖：
   - `fastapi`
   - `uvicorn`
   - `python-dotenv`
   - `requests`
   - `langchain-google-genai`
   - `langchain-community`
   - `tavily-python`


## 使用

要运行 DeepResearch 代理，您可以直接运行 `main.py` 文件并传入您的研究主题。

```bash
python main.py
```

在 `main.py` 中，您可以修改 `main("母婴博主怎么做")` 来指定您的研究主题。

```python
# main.py

if __name__ == "__main__":
    try:
        main("您的研究主题") # 修改此处
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        print(traceback.format_exc())
```

## 项目结构

```
.deep_research/
├── app/                     # 应用程序核心逻辑
│   ├── agent/               # 代理模块，包含查询生成、网络研究、反思和答案整理等逻辑
│   │   ├── __init__.py
│   │   ├── query_generator.py
│   │   ├── web_researcher.py
│   │   ├── reflection.py
│   │   └── answer_finalizer.py
│   ├── llm/                 # LLM相关配置和接口
│   ├── prompts/             # 提示模板
│   ├── schemas/             # 数据模型定义（如OverallState, WebSearchState）
│   ├── tools/               # 外部工具集成
│   └── utils.py             # 辅助工具函数
├── main.py                  # 项目入口文件，包含主研究管道
├── requirements.txt         # 项目依赖列表
└── Readme.md                # 项目说明文档
```
