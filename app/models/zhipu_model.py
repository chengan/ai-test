import os
from zhipuai import ZhipuAI
from .ai_model import BaseAIModel, AIModelException

class ZhipuModel(BaseAIModel):
    def __init__(self):
        self.api_key = os.getenv('ZHIPU_API_KEY')
        if not self.api_key:
            raise AIModelException("未找到智谱 API Key")
        self.client = ZhipuAI(api_key=self.api_key)
        self.model = "glm-4"  # 使用 GLM-4 模型
    
    def chat(self, message: str) -> str:
        """同步对话"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise AIModelException(f"智谱AI调用失败: {str(e)}")
    
    def chat_stream(self, message: str):
        """流式对话"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}],
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise AIModelException(f"智谱AI流式调用失败: {str(e)}") 