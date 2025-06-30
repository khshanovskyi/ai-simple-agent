from typing import Any

import requests

from task._constants import DIAL_ENDPOINT, WEB_SEARCH
from task.tools.base import BaseTool


class WebSearchTool(BaseTool):

    TOOL_CONFIG = {
        "type": "function",
        "function": {
            "name": WEB_SEARCH,
            "description": "Tool for WEB searching.",
            "parameters": {
                "type": "object",
                "properties": {
                    "request": {
                        "type": "string",
                        "description": "Search request."
                    }
                },
                "required": ["request"]
            }
        }
    }

    def __init__(self, api_key: str):
        self.api_key = api_key

    def execute(self, arguments: dict[str, Any]) -> str:
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        request_data = {
            "messages": [
                {
                    "role": "user",
                    "content": str(arguments["request"])
                }
            ]
        }

        endpoint = DIAL_ENDPOINT.format(model="gemini-2.0-flash-exp-google-search")
        response = requests.post(url=endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                return data["error"]
            return data["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} {response.text}"

