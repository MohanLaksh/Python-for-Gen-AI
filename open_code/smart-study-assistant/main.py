#!/usr/bin/env python3

import click
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from config import settings
from models import OpenAIClient, GeminiClient, ClaudeClient
from roles import TutorRole, QuizCreatorRole, SummarizerRole
from router import TaskClassifier, ModelRouter, TaskType, ComplexityLevel
from session import SessionManager
from utils import parse_context_string

console = Console()


class StudyAssistant:
    def __init__(self):
        self.classifier = TaskClassifier()
        self.router = ModelRouter()
        self.session_manager = SessionManager(max_history=settings.max_history_length)
        self.session_manager.create_session()

        self.roles = {
            TaskType.TUTOR: TutorRole(),
            TaskType.QUIZ: QuizCreatorRole(),
            TaskType.SUMMARY: SummarizerRole()
        }

    def process_input(
        self,
        user_input: str,
        context: Optional[dict] = None,
        override_role: Optional[str] = None,
        override_model: Optional[str] = None
    ) -> str:
        context = context or {}

        task_type = None
        complexity = None

        if override_role:
            task_type = self._get_task_type_from_name(override_role)
            complexity = ComplexityLevel.MODERATE
        else:
            task_type, complexity = self.classifier.classify(user_input)

        role = self.roles[task_type]
        model_client = self.router.route(task_type, complexity, override_model)

        routing_info = self.router.get_routing_info(task_type, complexity)
        console.print(
            f"[dim]→ Role: {role.get_role_name()}, Model: {routing_info.get('model', 'Unknown')}[/dim]"
        )

        prompt = role.prepare_prompt(user_input, context)
        history = self.session_manager.get_history()

        try:
            response = model_client.generate_response(prompt, history)

            current_session = self.session_manager.get_current_session()
            if current_session:
                self.session_manager.add_message(
                    current_session,
                    'user',
                    user_input
                )
                self.session_manager.add_message(
                    current_session,
                    'assistant',
                    response
                )

            return role.process_response(response)

        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            return ""

    def _get_task_type_from_name(self, name: str) -> TaskType:
        name_lower = name.lower()
        if 'quiz' in name_lower:
            return TaskType.QUIZ
        elif 'summar' in name_lower:
            return TaskType.SUMMARY
        else:
            return TaskType.TUTOR


@click.group()
def cli():
    pass


def _print_help():
    help_text = """
[bold]Available Commands:[/bold]
  /help           Show this help message
  /clear           Clear conversation context
  /role <name>     Set role (tutor, quiz, summary)
  /model <name>    Set model (openai, gemini, claude)
  /context <kv>     Set context (format: key=value, topic=value)
  /quit            Exit the assistant

[bold]Examples:[/bold]
  What is machine learning?
  Generate a quiz about Python
  Summarize: Python is a high-level programming language...
  /context subject=Computer Science, difficulty=advanced
"""
    console.print(help_text)


@cli.command()
@click.option('--role', '-r', type=click.Choice(['tutor', 'quiz', 'summary']),
              help='Force specific role')
@click.option('--model', '-m', type=click.Choice(['openai', 'gemini', 'claude']),
              help='Force specific model')
@click.option('--context', '-c', type=str,
              help='Additional context (format: key=value, topic=value)')
@click.argument('query', required=False)
def chat(role, model, context, query):
    console.print(Panel(
        Text("Smart Study Assistant", style="bold blue"),
        subtitle="Your Multi-Role Study Companion"
    ))

    assistant = StudyAssistant()

    available_models = assistant.router.get_available_models()
    if not available_models:
        console.print("[red]Error: No API keys configured. Please set at least one API key in .env file.[/red]")
        return

    console.print(f"[green]Available models: {', '.join(available_models)}[/green]")
    console.print("[dim]Type your questions or commands below.[/dim]")
    console.print("[dim]Commands: /help, /clear, /role, /model, /quit[/dim]\n")

    if query:
        context_dict = parse_context_string(context) if context else {}
        response = assistant.process_input(query, context_dict, role, model)
        console.print(f"\n[bold]{response}[/bold]\n")

    while True:
        try:
            user_input = console.input("\n[bold cyan]> [/bold cyan]").strip()

            if not user_input:
                continue

            if user_input.lower() in ['/quit', '/exit', '/q']:
                console.print("[yellow]Goodbye![/yellow]")
                break

            if user_input.lower() == '/help':
                _print_help()
                continue

            if user_input.lower() == '/clear':
                assistant.session_manager.clear_session()
                console.print("[green]Context cleared.[/green]")
                continue

            if user_input.lower().startswith('/role '):
                role = user_input[6:].strip()
                console.print(f"[green]Role set to: {role}[/green]")
                continue

            if user_input.lower().startswith('/model '):
                model = user_input[7:].strip()
                console.print(f"[green]Model set to: {model}[/green]")
                continue

            if user_input.lower().startswith('/context '):
                context_str = user_input[9:].strip()
                context_dict = parse_context_string(context_str)
                console.print(f"[green]Context: {context_dict}[/green]")
                continue

            context_dict = parse_context_string(context) if context else {}
            response = assistant.process_input(user_input, context_dict, role, model)

            if response:
                console.print(f"\n[bold]{response}[/bold]\n")

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type /quit to exit.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]\n")


if __name__ == '__main__':
    cli()
