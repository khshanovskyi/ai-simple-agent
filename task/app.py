import os

from task.client import DialClient
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role
from task.prompts import SYSTEM_PROMPT
from task.tools.users.create_user_tool import CreateUserTool
from task.tools.users.delete_user_tool import DeleteUserTool
from task.tools.users.get_user_by_id_tool import GetUserByIdTool
from task.tools.users.search_users_tool import SearchUsersTool
from task.tools.users.update_user_tool import UpdateUserTool
from task.tools.users.user_client import UserClient
from task.tools.web_search import WebSearchTool

DIAL_ENDPOINT = "https://ai-proxy.lab.epam.com"
API_KEY = os.getenv("DIAL_API_KEY")
DIAL_DEPLOYMENT = os.getenv("DIAL_DEPLOYMENT", "gpt-4o")


def main():
    if not API_KEY:
        print("Error: DIAL_API_KEY environment variable is not set.")
        return
    user_client = UserClient()
    tools = [
        WebSearchTool(api_key=API_KEY, endpoint=DIAL_ENDPOINT),
        GetUserByIdTool(user_client),
        SearchUsersTool(user_client),
        CreateUserTool(user_client),
        UpdateUserTool(user_client),
        DeleteUserTool(user_client),
    ]
    client = DialClient(
        endpoint=DIAL_ENDPOINT,
        deployment_name=DIAL_DEPLOYMENT,
        api_key=API_KEY,
        tools=tools,
    )
    conversation = Conversation()
    conversation.add_message(Message(role=Role.SYSTEM, content=SYSTEM_PROMPT))
    while True:
        user_input = input("> ").strip()
        if not user_input:
            continue
        conversation.add_message(Message(role=Role.USER, content=user_input))
        assistant_message = client.get_completion(
            conversation.get_messages(), print_request=False
        )
        conversation.add_message(assistant_message)
        print(assistant_message.content or "(No response text)")
        print()


if __name__ == "__main__":
    main()