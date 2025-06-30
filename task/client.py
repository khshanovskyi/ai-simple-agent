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
            #TODO: add 'tools'
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

                #TODO:
                # 1. Get `message` from `choice` and assign to `message_data` variable
                # 2. Get `content` from `message` and assign to `content` variable
                # 3. Get `tool_calls` from `message` and assign to `tool_calls` variable
                # 4. Create `ai_response` Message (with AI role, `content` and `tool_calls`)
                # 5. If `choice` `finish_reason` is `tool_calls`:
                #       Yes:
                #           - append `ai_response` to `messages`
                #           - call `_process_tool_calls` with `tool_calls` and assign result to `tool_messages` variable
                #           - add `tool_messages` to `messages` (use `extend` method)
                #           - make recursive call (return `get_completion` with `messages` and `print_request`)
                #       No: return `ai_response` (final assistant response)

                return None
            raise ValueError("No Choice has been present in the response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")


    def _process_tool_calls(self, tool_calls: list[dict[str, Any]]) -> list[Message]:
        """Process tool calls and add results to messages."""
        tool_messages = []
        for tool_call in tool_calls:
            #TODO:
            # 1. Get `id` from `tool_call` and assign to `tool_call_id` variable
            # 2. Get `function` from `tool_call` and assign to `function` variable
            # 3. Get `name` from `function` and assign to `function_name` variable
            # 4. Get `arguments` from `function` as json (json.loads) and assign to `arguments` variable
            # 5. Call `_call_tool` with `function_name` and `arguments`, and assign to `tool_execution_result` variable
            # 6. Append to `tool_messages` Message with:
            #       - role=Role.TOOL
            #       - name=function_name
            #       - tool_call_id=tool_call_id
            #       - content=tool_execution_result
            # 7. print(f"FUNCTION '{function_name}'\n{tool_execution_result}\n{'-'*50}")
            # 8. Return `tool_messages`
            # -----
            # FYI: It is important to provide `tool_call_id` in TOOL Message. By `tool_call_id` LLM make a  relation
            #      between Assistant message `tool_calls[i][id]` and message in history.
            #      In case if no Tool message presented in history (no message at all or with different tool_call_id),
            #      then LLM with answer with Error (that not find tool message with specified id).

        return tool_messages

    def _call_tool(self, function_name: str, arguments: dict[str, Any]) -> str:
        #TODO:
        # If `function_name` is `SIMPLE_CALCULATOR` -> return CalculatorTool#execute()
        # If `function_name` is `NASA_IMG_STEALER` -> return ImageStealerTool(self._api_key)#execute()
        # If `function_name` is `WEB_SEARCH` -> return WebSearchTool#execute()

        return f"Unknown function: {function_name}"
