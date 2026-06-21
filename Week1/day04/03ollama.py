import requests
import json
import time


class OllamaTester:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def test_version(self):
        print("\n=== 测试版本接口 ===")
        response = requests.get(f"{self.base_url}/api/version")
        print(f"版本: {response.json()}")
        return response.json()

    def test_tags(self):
        print("\n=== 测试本地模型列表 ===")
        response = requests.get(f"{self.base_url}/api/tags")
        models = response.json().get("models", [])
        for model in models:
            print(f"- {model['name']}")
        return models

    def test_generate(self, model="llama2", prompt="你好，请简单介绍一下自己"):
        print(f"\n=== 测试文本生成 (模型: {model}) ===")
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload
        )
        result = response.json()
        print(f"回复: {result.get('response', '')[:200]}...")
        return result

    def test_chat(self, model="llama2"):
        print(f"\n=== 测试多轮聊天 (模型: {model}) ===")
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "1+2等于几？"},
                {"role": "assistant", "content": "1+2等于3"},
                {"role": "user", "content": "那再+3呢？"}
            ],
            "stream": False
        }
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload
        )
        result = response.json()
        print(f"回复: {result.get('message', {}).get('content', '')}")
        return result

    def test_embed(self, model="nomic-embed-text:latest", text="Hello world"):
        print(f"\n=== 测试向量生成 (模型: {model}) ===")
        payload = {
            "model": model,
            "input": text
        }
        response = requests.post(
            f"{self.base_url}/api/embed",
            json=payload
        )
        result = response.json()
        embeddings = result.get("embeddings", [])
        if embeddings:
            print(f"向量维度: {len(embeddings[0])}")
            print(f"向量前5个值: {embeddings[0][:5]}")
        return result

    def test_streaming(self, model="llama2"):
        print(f"\n=== 测试流式生成 (模型: {model}) ===")
        payload = {
            "model": model,
            "prompt": "用一句话介绍人工智能",
            "stream": True
        }
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            stream=True
        )
        print("流式回复: ", end="")
        for line in response.iter_lines(): # iter_lines()返回生成器，边接收边处理，不阻塞主线程
            if line:
                data = json.loads(line)  # 将字符串解析为字典
                print(data.get("response", ""), end="", flush=True) # 实时刷新：flush=True在长文本生成时至关重要
        print("\n")

    def run_all_tests(self, model="llama2"):
        """运行所有测试"""
        print("=" * 50)
        print("开始测试 Ollama API")
        print("=" * 50)

        try:
            self.test_version()
            self.test_tags()
            self.test_generate(model)
            self.test_chat(model)
            self.test_embed()
            self.test_streaming(model)
            print("\n✅ 所有测试完成！")
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            print("请确保 Ollama 服务正在运行")


if __name__ == "__main__":
    tester = OllamaTester()
    # 替换为你已安装的模型名称
    tester.run_all_tests(model="qwen3:0.6b")