from typing import Optional
from config import settings
from models import OpenAIClient, GeminiClient, ClaudeClient
from models.base_model import BaseLLMClient
from router.task_classifier import TaskType, ComplexityLevel


class ModelRouter:
    def __init__(self):
        self.clients = {}
        self._initialize_clients()

        self.routing_rules = {
            (TaskType.TUTOR, ComplexityLevel.SIMPLE): settings.openai_model,
            (TaskType.TUTOR, ComplexityLevel.MODERATE): settings.anthropic_model,
            (TaskType.TUTOR, ComplexityLevel.COMPLEX): settings.openai_advanced_model,
            (TaskType.QUIZ, ComplexityLevel.SIMPLE): settings.gemini_model,
            (TaskType.QUIZ, ComplexityLevel.MODERATE): settings.gemini_model,
            (TaskType.QUIZ, ComplexityLevel.COMPLEX): settings.openai_model,
            (TaskType.SUMMARY, ComplexityLevel.SIMPLE): settings.openai_model,
            (TaskType.SUMMARY, ComplexityLevel.MODERATE): settings.openai_model,
            (TaskType.SUMMARY, ComplexityLevel.COMPLEX): settings.anthropic_model,
        }

        self._build_client_map()

    def _initialize_clients(self):
        if settings.openai_api_key:
            self.clients['openai'] = OpenAIClient()
        if settings.gemini_api_key:
            self.clients['gemini'] = GeminiClient()
        if settings.anthropic_api_key:
            self.clients['claude'] = ClaudeClient()

    def _build_client_map(self):
        self.client_map = {}
        for task_type, complexity in self.routing_rules:
            model = self.routing_rules[(task_type, complexity)]
            if 'gpt' in model.lower() or 'openai' in model.lower():
                self.client_map[(task_type, complexity)] = 'openai'
            elif 'gemini' in model.lower() or 'google' in model.lower():
                self.client_map[(task_type, complexity)] = 'gemini'
            elif 'claude' in model.lower() or 'anthropic' in model.lower():
                self.client_map[(task_type, complexity)] = 'claude'

    def route(
        self,
        task_type: TaskType,
        complexity: ComplexityLevel,
        override_model: Optional[str] = None
    ) -> BaseLLMClient:
        if override_model:
            return self._get_client_by_name(override_model)

        key = (task_type, complexity)
        if key in self.client_map:
            client_name = self.client_map[key]
            return self._get_client_by_name(client_name)

        return self._get_default_client()

    def _get_client_by_name(self, name: str) -> BaseLLMClient:
        if name in self.clients:
            return self.clients[name]

        return self._get_default_client()

    def _get_default_client(self) -> BaseLLMClient:
        for client in ['openai', 'gemini', 'claude']:
            if client in self.clients:
                return self.clients[client]

        raise ValueError("No AI client available. Please configure at least one API key.")

    def get_available_models(self) -> list:
        return list(self.clients.keys())

    def get_routing_info(
        self,
        task_type: TaskType,
        complexity: ComplexityLevel
    ) -> dict:
        key = (task_type, complexity)
        if key in self.routing_rules:
            model = self.routing_rules[key]
            client_name = self.client_map.get(key, 'unknown')
            return {
                'task_type': task_type.value,
                'complexity': complexity.value,
                'model': model,
                'client': client_name
            }
        return {}
