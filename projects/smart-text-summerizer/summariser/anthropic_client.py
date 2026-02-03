from anthropic import Anthropic
from summariser.base import BaseLLMClient
from schemas.summary_schema import SummaryOutput
from config import config
from utils.retry import create_retry_decorator
import json
from jinja2 import Template
import os

class AnthropicClient(BaseLLMClient):
    def __init__(self):
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = config.DEFAULT_MODEL_ANTHROPIC
        self.retry = create_retry_decorator()

    def _render_prompt(self, template_path: str, context: dict) -> str:
        with open(template_path, 'r') as f:
            template = Template(f.read())
        return template.render(context)

    def summarize(self, text: str, tone: str = "neutral", schema: str = "") -> SummaryOutput:
        # Load prompt template
        prompt_path = os.path.join(os.path.dirname(__file__), '../prompts/summarise.j2')
        
        # Prepare schema for prompt
        if not schema:
            schema = json.dumps(SummaryOutput.model_json_schema(), indent=2)
            
        prompt = self._render_prompt(prompt_path, {
            "input_text": text,
            "tone": tone,
            "output_schema": schema
        })

        @self.retry
        def _call_api():
            return self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system="You are an expert summarization assistant. Return output strictly in JSON format.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

        response = _call_api()
        content = response.content[0].text
        
        # Sometimes key is strictly inside ```json ... ``` blocks, simple cleanup might be needed
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        return SummaryOutput.model_validate_json(content)
