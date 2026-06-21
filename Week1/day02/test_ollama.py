import requests


url = "http://localhost:11434/api/generate"
payload = {
"model": "qwen3:0.6b",
"prompt": "十个字介绍自己",
"stream": False
}
response = requests.post(url, json=payload)
print(response.json()["response"])