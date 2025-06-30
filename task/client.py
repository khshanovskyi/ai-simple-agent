import json
from typing import Any

import requests

from task._constants import WEB_SEARCH, SIMPLE_CALCULATOR, NASA_IMG_STEALER
from task.models.message import Message
from task.models.role import Role
from task.tools.calculator import CalculatorTool
from task.tools.nasa.nasa_image_stealler import NasaImageStealerTool
from task.tools.web_search import WebSearchTool


class DialClient:

    def __init__(
            self,
            endpoint: str,
            deployment_name: str,
            api_key: str,
            tools: list[dict[str, Any]] | None = None
    ):
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be null or empty")

        self._endpoint = endpoint.format(model=deployment_name)
        self._api_key = api_key
        self._tools = tools or []

        print(self._endpoint)
        print(json.dumps(self._tools, indent=4))


    def get_completion(self, messages: list[Message], print_request: bool = True) -> Message:
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }
        request_data = {
            "messages": [msg.to_dict() for msg in messages],
            "tools": self._tools,
        }

        if print_request:
            print(self._endpoint)
            print("REQUEST:", json.dumps({"messages": [msg.to_dict() for msg in messages]}, indent=2))

        response = requests.post(url=self._endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()

            choices = data.get("choices", [])
            if choices:
                choice = choices[0]
                print("RESPONSE:", json.dumps(choice, indent=2))
                print("-"*100)

                message_data = choice.get("message", {})
                content = message_data.get("content")
                tool_calls = message_data.get("tool_calls")

                ai_response = Message(
                    role=Role.AI,
                    content=content,
                    tool_calls=tool_calls
                )

                if choice.get("finish_reason") == "tool_calls":
                    messages.append(ai_response)

                    tool_messages = self._process_tool_calls(tool_calls)
                    messages.extend(tool_messages)

                    # Recursive call to get final response
                    return self.get_completion(messages, print_request)

                return ai_response
            raise ValueError("No Choice has been present in the response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")


    def _process_tool_calls(self, tool_calls: list[dict[str, Any]]) -> list[Message]:
        """Process tool calls and add results to messages."""
        tool_messages = []
        for tool_call in tool_calls:
            tool_call_id = tool_call["id"]
            function = tool_call["function"]
            function_name = function["name"]
            arguments = json.loads(function["arguments"])

            tool_execution_result = self._call_tool(function_name, arguments)

            tool_messages.append(Message(
                role=Role.TOOL,
                name=function_name,
                tool_call_id=tool_call_id,
                content=tool_execution_result
            ))

            print(f"FUNCTION '{function_name}'\n{tool_execution_result}\n{'-'*50}")

        return tool_messages

    def _call_tool(self, function_name: str, arguments: dict[str, Any]) -> str:
        if function_name == SIMPLE_CALCULATOR:
            return CalculatorTool().execute(arguments)
        elif function_name == NASA_IMG_STEALER:
            return NasaImageStealerTool(self._api_key).execute(arguments)
        elif function_name == WEB_SEARCH:
            return WebSearchTool(self._api_key).execute(arguments)

        return f"Unknown function: {function_name}"
