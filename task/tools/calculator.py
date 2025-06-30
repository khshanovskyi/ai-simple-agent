from typing import Any

from task._constants import SIMPLE_CALCULATOR
from task.tools.base import BaseTool


class CalculatorTool(BaseTool):
   #TODO: Read configuration, additional you can read about it here:
   # https://dialx.ai/dial_api#operation/sendChatCompletionRequest (-> tools -> function)
    TOOL_CONFIG = {
        "type": "function",
        "function": {
            "name": SIMPLE_CALCULATOR,
            "description": "Provides results of the basic math calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "First operand."
                    },
                    "num2": {
                        "type": "number",
                        "description": "Second operand."
                    },
                    "operation": {
                        "type": "string",
                        "description": "Operation that should be performed",
                        "enum": ["add", "subtract", "multiply", "divide"]
                    }
                },
                "required": ["num1", "num2", "operation"]
            }
        }
    }

    def execute(self, arguments: dict[str, Any]) -> str:
        try:
            #TODO:
            # 1. Get `num1` from `arguments` as `float` and assign to `num1` variable
            # 2. Get `num2` from `arguments` as `float` and assign to `num2` variable
            # 3. Get `operation` from `arguments` as `float` and assign to `operation` variable
            # ---
            # 4. Check all available operations from `TOOL_CONFIG`.
            # 4.1. If `operation` is 'add' then `result = num1 + num2`
            # 4.2. If `operation` is 'subtract' then `result = num1 - num2`
            # 4.3. If `operation` is 'multiply' then `result = num1 * num2`
            # 4.4. If `operation` is 'divide' then:
            #       - if num2 == 0 ->  return "Error: Division by zero"
            #       - else `result = num1 / num2`
            # 4.5. Else: return f"Error: Unknown operation '{operation}'"
            result = 0

            return f"Result: {result}"
        except Exception as e:
            return f"Error processing calculation: {str(e)}"