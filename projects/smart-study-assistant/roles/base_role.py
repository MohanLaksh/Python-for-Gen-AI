from abc import ABC, abstractmethod
from typing import Optional


class BaseRole(ABC):
    def __init__(self, role_name: str):
        self.role_name = role_name

    @abstractmethod
    def prepare_prompt(self, user_input: str, context: Optional[dict] = None) -> str:
        pass

    @abstractmethod
    def process_response(self, response: str) -> str:
        pass

    def get_role_name(self) -> str:
        return self.role_name
