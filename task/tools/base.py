from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    @abstractmethod
    def execute(self, arguments: dict[str, Any]) -> str:
        pass