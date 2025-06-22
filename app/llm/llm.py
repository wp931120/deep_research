import openai
import traceback

class LLM:
    def __init__(
        self, ollama=False,vllm=True
    ):  
    

        if ollama:
            self.client = openai.OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
            )
            self.model =  "modelscope.cn/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF:latest"
        elif vllm:
            self.client = openai.OpenAI(
                base_url="http://localhost:8000/v1",
                api_key="vllm",
            )
            self.model = "./Qwen3-4B/"
        else:
            self.client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key="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",
            )
            self.model = "moonshotai/kimi-dev-72b:free"
        self.temperature = 0.7
        self.max_tokens = 1000

    def chat(self, prompt: str) -> str:
        """
        使用 OpenAI 客户端与 Ollama 模型进行对话
        """
        messages = [{"role": "user", "content": prompt}]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}},
            )
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error: {str(e)}\n{traceback.format_exc()}"
