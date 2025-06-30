from task.client import DialClient
from task._constants import DEFAULT_SYSTEM_PROMPT, DIAL_ENDPOINT, API_KEY
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role
from task.tools.calculator import CalculatorTool
from task.tools.nasa.nasa_image_stealler import NasaImageStealerTool
from task.tools.web_search import WebSearchTool


def main():
    client = DialClient(
        endpoint=DIAL_ENDPOINT,
        #TODO: Here you can chose different models. With DIAL you are not depend on vendor Specification, you can use
        # any model that you want with DIAL Specification. https://dialx.ai/dial_api#operation/sendChatCompletionRequest
        deployment_name="gpt-4o",
        # deployment_name="gemini-2.5-pro-preview-03-25",
        # deployment_name="anthropic.claude-3-7-sonnet-20250219-v1:0",
        api_key=API_KEY,
        tools=[
            #TODO: add tools:
            # -CalculatorTool.TOOL_CONFIG
            # -NasaImageStealerTool.TOOL_CONFIG
            # -WebSearchTool.TOOL_CONFIG
        ]
    )

    conversation = Conversation()
    conversation.add_message(Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT))

    print("Type your question or 'exit' to quit.")

    while True:
        user_input = input("> ").strip()

        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break

        conversation.add_message(Message(Role.USER, user_input))

        ai_message = client.get_completion(conversation.get_messages(), print_request=True)
        conversation.add_message(ai_message)
        print("🤖:", ai_message.content)
        print("=" * 100)
        print()


main()
