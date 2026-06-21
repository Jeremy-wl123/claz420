## 作业：LLM 调用代码的工程化重构

### 背景
现有代码片段（`llm_call.py`）实现了一个简易的 LLM（通义千问、DeepSeek）调用功能，但代码耦合度高、可维护性差。请对该代码进行**模块化重构**，按以下目录结构组织工程，并实现**配置管理、客户端封装、业务服务、数据模型和单元测试**。

```
project/
├── config/            # 环境变量和模型配置
├── clients/           # 客户端创建（OpenAI 兼容客户端）
├── services/          # 模型调用业务逻辑
├── schemas/           # 请求与响应数据结构（Pydantic 模型）
├── tests/             # 单元测试与模拟响应
└── main.py            # 示例调用入口（可选）
```

### 要求
1. **配置模块**：从环境变量读取 API Key，支持 `qwen` 和 `deepseek` 两个 provider 的静态配置（base_url、model 名称等）。
2. **客户端模块**：提供创建 OpenAI 客户端的函数，统一超时和重试参数。
3. **业务服务模块**：实现 `call_llm` 核心函数，支持不同 provider 的特有参数（如 DeepSeek 的 `reasoning_effort` 和 `extra_body`）。
4. **数据模型模块**：使用 Pydantic 定义：
   - `Message`（role, content）
   - `ChatRequest`（provider, messages）
   - `ChatResponse`（content, usage?）
5. **单元测试**：使用 `pytest` 和 `unittest.mock` 模拟 API 调用，至少覆盖：
   - 客户端创建时缺少 API Key 抛出异常
   - `call_llm` 正常返回内容
   - 不同 provider 传递给客户端的参数正确性

### 提交形式
- 提供完整的代码文件树和每个文件的核心内容。
- 编写一个简短的 `README.md` 说明如何运行测试和示例。

---

## 示例答案（重构后的工程结构）

### 文件树
```
llm_engineering/
├── config/
│   ├── __init__.py
│   └── settings.py
├── clients/
│   ├── __init__.py
│   └── openai_client.py
├── services/
│   ├── __init__.py
│   └── llm_service.py
├── schemas/
│   ├── __init__.py
│   └── models.py
├── tests/
│   ├── __init__.py
│   ├── test_clients.py
│   ├── test_llm_service.py
│   └── conftest.py
├── main.py
├── requirements.txt
└── README.md
```

### 文件内容

#### `requirements.txt`
```
openai>=1.0.0
pydantic>=2.0.0
pytest>=7.0.0
python-dotenv>=1.0.0
```

#### `config/settings.py`
```python
import os
from typing import Literal, Dict, Any

Provider = Literal["qwen", "deepseek"]

PROVIDER_CONFIGS: Dict[Provider, Dict[str, Any]] = {
    "qwen": {
        "api_key_env": "DASHSCOPE_API_KEY",
        "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        "model": "qwen3.5-plus",
    },
    "deepseek": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-v4-pro",
    },
}

def get_api_key(provider: Provider) -> str:
    env_var = PROVIDER_CONFIGS[provider]["api_key_env"]
    api_key = os.getenv(env_var)
    if not api_key:
        raise RuntimeError(f"未检测到环境变量 {env_var}")
    return api_key

def get_model_name(provider: Provider) -> str:
    return PROVIDER_CONFIGS[provider]["model"]

def get_base_url(provider: Provider) -> str:
    return PROVIDER_CONFIGS[provider]["base_url"]
```

#### `clients/openai_client.py`
```python
from openai import OpenAI
from config.settings import get_api_key, get_base_url, Provider

def create_openai_client(provider: Provider) -> OpenAI:
    api_key = get_api_key(provider)
    base_url = get_base_url(provider)
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=60.0,
        max_retries=2,
    )
```

#### `schemas/models.py`
```python
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    provider: Literal["qwen", "deepseek"]
    messages: List[Message]

class ChatResponse(BaseModel):
    content: str
    model: Optional[str] = None
    usage: Optional[dict] = None
```

#### `services/llm_service.py`
```python
from typing import List, Dict, Any
from clients.openai_client import create_openai_client
from config.settings import get_model_name, Provider
from schemas.models import Message, ChatResponse

def call_llm(provider: Provider, messages: List[Message]) -> ChatResponse:
    client = create_openai_client(provider)
    model = get_model_name(provider)
    
    # 将 Message 对象转为字典格式
    msg_dicts = [msg.model_dump() for msg in messages]
    
    request_kwargs: Dict[str, Any] = {
        "model": model,
        "messages": msg_dicts,
    }
    
    if provider == "deepseek":
        request_kwargs["reasoning_effort"] = "high"
        request_kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
    
    response = client.chat.completions.create(**request_kwargs)
    content = response.choices[0].message.content or ""
    
    return ChatResponse(
        content=content,
        model=response.model,
        usage=response.usage.model_dump() if response.usage else None
    )
```

#### `main.py`（示例调用）
```python
import os
from dotenv import load_dotenv
from schemas.models import Message
from services.llm_service import call_llm

load_dotenv()  # 可选，加载 .env 文件

if __name__ == "__main__":
    messages = [
        Message(role="system", content="你是一名 AI 课程助教。"),
        Message(role="user", content="解释 API Key 的作用。"),
    ]
    
    print("=== 通义千问 ===")
    resp_qwen = call_llm("qwen", messages)
    print(resp_qwen.content)
    
    print("\n=== DeepSeek ===")
    resp_deepseek = call_llm("deepseek", messages)
    print(resp_deepseek.content)
```

#### `tests/conftest.py`
```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_openai_response():
    mock_choice = Mock()
    mock_choice.message.content = "这是一个模拟的回答。"
    mock_response = Mock()
    mock_response.choices = [mock_choice]
    mock_response.model = "test-model"
    mock_response.usage = Mock()
    mock_response.usage.model_dump.return_value = {"total_tokens": 10}
    return mock_response

@pytest.fixture
def sample_messages():
    from schemas.models import Message
    return [
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content="Hello"),
    ]
```

#### `tests/test_clients.py`
```python
import pytest
from clients.openai_client import create_openai_client
from config.settings import get_api_key

def test_create_client_missing_api_key(monkeypatch):
    # 清除环境变量
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    from config.settings import get_api_key
    with pytest.raises(RuntimeError, match="未检测到环境变量 DASHSCOPE_API_KEY"):
        get_api_key("qwen")

def test_create_client_success(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "fake-key")
    client = create_openai_client("qwen")
    assert client.api_key == "fake-key"
    assert client.base_url == "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
```

#### `tests/test_llm_service.py`
```python
from unittest.mock import patch
from services.llm_service import call_llm
from schemas.models import ChatResponse

@patch("services.llm_service.create_openai_client")
def test_call_llm_qwen(mock_create_client, sample_messages, mock_openai_response):
    mock_client = mock_create_client.return_value
    mock_client.chat.completions.create.return_value = mock_openai_response
    
    response = call_llm("qwen", sample_messages)
    assert isinstance(response, ChatResponse)
    assert response.content == "这是一个模拟的回答。"
    
    # 验证 deepseek 特有参数没有被传入
    call_args = mock_client.chat.completions.create.call_args[1]
    assert "reasoning_effort" not in call_args

@patch("services.llm_service.create_openai_client")
def test_call_llm_deepseek_extra_params(mock_create_client, sample_messages, mock_openai_response):
    mock_client = mock_create_client.return_value
    mock_client.chat.completions.create.return_value = mock_openai_response
    
    response = call_llm("deepseek", sample_messages)
    assert response.content == "这是一个模拟的回答。"
    
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args["reasoning_effort"] == "high"
    assert call_args["extra_body"] == {"thinking": {"type": "enabled"}}
```

#### `README.md`
```markdown
# LLM Engineering Demo

## 环境准备
1. 创建虚拟环境并安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 设置环境变量（或创建 `.env` 文件）：
   ```
   DASHSCOPE_API_KEY=your_qwen_key
   DEEPSEEK_API_KEY=your_deepseek_key
   ```

## 运行示例
```bash
python main.py
```

## 运行测试
```bash
pytest tests/ -v
```

## 模块说明
- `config/` – 配置管理（provider 映射、API Key 获取）
- `clients/` – OpenAI 客户端工厂
- `services/` – 核心业务逻辑（支持不同 provider 的特殊参数）
- `schemas/` – Pydantic 请求/响应模型
- `tests/` – 单元测试（使用 mock 避免真实网络调用）
```

---

### 评分要点（供教师参考）
- 是否正确分离配置、客户端、业务、模型和测试。
- 是否使用 Pydantic 定义数据模型。
- 是否支持不同 provider 的特有参数（如 DeepSeek 的 `extra_body`）。
- 单元测试是否覆盖正常流程和异常情况。
- 代码风格和文档注释质量。