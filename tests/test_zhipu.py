import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI

def test_zhipu_api():
    # 加载环境变量
    load_dotenv()
    
    # 获取 API Key
    api_key = os.getenv('ZHIPU_API_KEY')
    if not api_key:
        print("错误：未找到 ZHIPU_API_KEY 环境变量")
        return
    
    try:
        # 初始化客户端
        client = ZhipuAI(api_key=api_key)
        
        # 测试同步调用
        print("测试同步调用...")
        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=[{"role": "user", "content": "你好，请做个自我介绍"}]
        )
        print("同步调用响应:", response.choices[0].message.content)
        
        # 测试流式调用
        print("\n测试流式调用...")
        response_stream = client.chat.completions.create(
            model="glm-4-plus",
            messages=[{"role": "user", "content": "讲个笑话"}],
            stream=True
        )
        
        print("流式调用响应:")
        for chunk in response_stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end='')
        
        print("\n\n测试完成！")
        
    except Exception as e:
        print(f"错误：{str(e)}")

if __name__ == "__main__":
    test_zhipu_api() 