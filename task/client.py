import json
from typing import Any

import requests

from task.models.message import Message
from task.models.role import Role
from task.tools.base import BaseTool


class DialClient:

    def __init__(
            self,
            endpoint: str,
            deployment_name: str,
            api_key: str,
            tools: list[BaseTool] | None = None
    ):
        if not api_key:
            raise ValueError("api_key is required")
        self.__endpoint = f"{endpoint}/openai/deployments/{deployment_name}/chat/completions"
        self.__api_key = api_key
        tools = tools or []
        self.__tools_dict = {t.name: t for t in tools}
        self.__tools = [t.schema for t in tools]


    def get_completion(self, messages: list[Message], print_request: bool = True) -> Message:
        headers = {
            "api-key": self.__api_key,
            "Content-Type": "application/json",
        }
        request_data = {
            "messages": [msg.to_dict() for msg in messages],
            "tools": self.__tools,
        }
        if print_request:
            print("Request messages:", [m.to_dict() for m in messages])
        response = requests.post(
            url=self.__endpoint,
            headers=headers,
            json=request_data,
        )
        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}: {response.text}")
        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            raise RuntimeError("No choices in response")
        choice = choices[0]
        message_data = choice.get("message", {})
        content = message_data.get("content") or ""
        tool_calls = message_data.get("tool_calls")
        ai_response = Message(
            role=Role.AI,
            content=content,
            tool_calls=tool_calls,
        )
        finish_reason = choice.get("finish_reason", "")
        if finish_reason == "tool_calls" and tool_calls:
            messages = list(messages)
            messages.append(ai_response)
            tool_messages = self._process_tool_calls(tool_calls)
            messages.extend(tool_messages)
            return self.get_completion(messages, print_request)
        return ai_response


    def _process_tool_calls(self, tool_calls: list[dict[str, Any]]) -> list[Message]:
        """Process tool calls and add results to messages."""
        tool_messages = []
        for tool_call in tool_calls:
            tool_call_id = tool_call.get("id", "")
            function = tool_call.get("function", {})
            function_name = function.get("name", "")
            arguments = json.loads(function.get("arguments") or "{}")
            tool_execution_result = self._call_tool(function_name, arguments)
            tool_messages.append(
                Message(
                    role=Role.TOOL,
                    name=function_name,
                    tool_call_id=tool_call_id,
                    content=tool_execution_result,
                )
            )
            print(f"FUNCTION '{function_name}'\n{tool_execution_result}\n{'-'*50}")
        return tool_messages

    def _call_tool(self, function_name: str, arguments: dict[str, Any]) -> str:
        tool = self.__tools_dict.get(function_name)
        if tool is not None:
            return tool.execute(arguments)
        return f"Unknown function: {function_name}"
