from enum import StrEnum


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    AI = "assistant"
    TOOL = "tool"
