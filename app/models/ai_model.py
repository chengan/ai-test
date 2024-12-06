from abc import ABC, abstractmethod

class AIModelException(Exception):
    """AI模型调用异常的基类"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class BaseAIModel(ABC):
    """AI模型的抽象基类"""
    
    @abstractmethod
    def chat(self, message: str) -> str:
        """同步对话方法"""
        pass
    
    @abstractmethod
    def chat_stream(self, message: str):
        """流式对话方法"""
        pass 