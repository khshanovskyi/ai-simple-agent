# DIAL AI Simple Agent Task
Python implementation for building AI-powered chat applications using the DIAL API with advanced tool integration.

## 🎯 Task Overview

Implement simple Agent from scratch. In this task you need to practice to add custom tools and make requests to DIAL API.

## 🎓 Learning Goals

By exploring and working with this project, you will learn:

- **Tool Calling Systems**: Learn how to implement and integrate AI tools for enhanced functionality
- **Multi-Modal AI**: Work with text, image analysis, and web search capabilities

## 🏗️ Architecture

```
task/
├── models/
│   ├── conversation.py   # ✅ Complete
│   ├── message.py        # ✅ Complete
│   └── role.py           # ✅ Complete
├── tools/                # Tool implementations
│   ├── base.py           # ✅ Abstract base tool interface
│   ├── calculator.py     # 🚧 TODO: implement logic
│   ├── web_search.py     # 🚧 TODO: provide tool config according to DIAL Specification
│   └── nasa/             # 🚧 TODO: provide tool config according to DIAL Specification
├── client.py             # 🚧 TODO: implement all point described in TODO seactions
├── app.py                # 🚧 Add tool configs and play with different models
└── _constants.py         # ✅ Complete. (Add `NASA_API_KEY`)
```

## 📋 Requirements

- **Python**: 3.11 or higher
- **Dependencies**: Listed in `requirements.txt`
- **API Access**: DIAL API key with appropriate permissions
- **Network**: EPAM VPN connection for internal API access

## 🔧 Setup Instructions

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv .venv
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. API Configuration

1. **Connect to EPAM VPN** (required for internal API access)
2. **Obtain DIAL API Key**:
    - Visit: https://support.epam.com/ess?id=sc_cat_item&table=sc_cat_item&sys_id=910603f1c3789e907509583bb001310c
3. **Add DIAL API Key as Environment Variable**
4. **Optional - NASA API Key** (for enhanced NASA tool functionality):
    - Visit: https://api.nasa.gov/


## Example Interaction

```
Type your question or 'exit' to quit.
> Hello, how can you help me?
🤖: Hello! I'm an AI assistant with several capabilities:

1. **General Conversation**: I can answer questions and have discussions
2. **Mathematical Calculations**: I can perform complex calculations  
3. **NASA Image Analysis**: I can analyze Mars rover images from specific sols
4. **Web Search**: I can search the web for current information

What would you like to explore?

> Calculate 15.5 * 23 + 100
🤖: I'll calculate that for you.

[Tool execution: Calculator]
🤖: The result is 456.5

> Show me a Mars image from sol 401
🤖: I'll fetch and analyze a Mars rover image from sol 401.

[Tool execution: NASA Image Stealer]
🤖: Here's the largest image from Mars sol 1000:
URL: https://mars.jpl.nasa.gov/msl-raw-images/...
Description: This image shows the Martian landscape with rocky terrain...

> What is weather on Mars now?
🤖: I'll search what is the weather on Mars now:

[Tool execution: WEB search]
🤖: Current weather on Mars is...

> exit
Exiting the chat. Goodbye!
```

## 🛠️ Tool System

### Calculator Tool
Performs mathematical operations with support for:
- Addition, subtraction, multiplication, division
- Error handling for edge cases (division by zero)
- Floating-point number support

### NASA Image Stealer Tool
Analyzes Mars rover images:
- Fetches images from specific Mars sols
- Finds the largest available image by Content-Length
- Uses AI vision to describe image content
- Async processing for optimal performance

### Web Search Tool
Provides current web information:
- Real-time search capabilities
- Integration with Google Search via Gemini model
- Formatted results with source attribution

## 🔧 Configuration

### Tool Configuration

Tools are configured using OpenAI's function calling specification:

```python
TOOL_CONFIG = {
    "type": "function",
    "function": {
        "name": "tool_name",
        "description": "Tool description",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            "required": ["param1"]
        }
    }
}
```

## 🧪 Testing

## Request sample:
```
Find descriptions of largest NASA pictures for sol 401, 402 and 452 and tell me if they have smth similar?
```

```
489.4929 * 3564.111111
```

```
Find descriptions of largest NASA pictures for sol (10*40 (calculate it)) and tell me if they have smth similar?
```

## 🔍 API Reference

### DIAL Endpoint
```
POST https://ai-proxy.lab.epam.com/openai/deployments/{model}/chat/completions
```

### Request Format
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Hello!"
    }
  ],
  "tools": [...] // Optional tool definitions
}
```

### Response Format
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you?",
        "tool_calls": [...] // Present when tools are called
      },
      "finish_reason": "stop" // or "tool_calls"
    }
  ]
}
```

## 🎨 Extending the System

### Adding New Tools

1. **Create Tool Class**:
```python
from task.tools.base import BaseTool

class MyTool(BaseTool):
    TOOL_CONFIG = {
        "type": "function",
        "function": {
            "name": "my_tool",
            "description": "My custom tool",
            "parameters": {...}
        }
    }

    def execute(self, arguments: dict) -> str:
        # Tool implementation
        return "Tool result"
```

2. **Register Tool**:
```python
# In app.py
client = DialClient(
    tools=[
        CalculatorTool.TOOL_CONFIG,
        MyTool.TOOL_CONFIG,  # Add here
        ...
    ]
)
```

3. **Update Client**:
```python
# In client.py _call_tool method
if function_name == "my_tool":
    return MyTool().execute(arguments)
```

---
# <img src="dialx-banner.png">