import requests

class OllamaTesterOpenAI:

    def __init__(self,base_url="http://localhost:11434/v1"):
        self.base_url = base_url


    def test_generate(self, model="qwen3:0.6b", prompt=[{"role": "user", "content": "你好，请十个字简单介绍一下自己"} ]):
        print(f"\n=== 测试文本生成 (模型: {model}) ===")
        payload = {
            "model": model,
            "messages": prompt,
            "stream": False
        }
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json=payload
        )

        if response.status_code == 200:
            result = response.json()
            # 安全提取内容，避免 KeyError
            reply = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"回复: {reply[:200]}...")
            return result
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None

if __name__ == "__main__":
    tester = OllamaTesterOpenAI()
    tester.test_generate()