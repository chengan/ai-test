import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # AI模型配置
    ZHIPU_API_KEY = os.getenv('ZHIPU_API_KEY')