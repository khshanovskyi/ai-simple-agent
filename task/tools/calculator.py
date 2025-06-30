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
            num1 = float(arguments["num1"])
            num2 = float(arguments["num2"])
            operation = arguments["operation"]

            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                if num2 == 0:
                    return "Error: Division by zero"
                result = num1 / num2
            else:
                return f"Error: Unknown operation '{operation}'"

            return f"Result: {result}"
        except Exception as e:
            return f"Error processing calculation: {str(e)}"