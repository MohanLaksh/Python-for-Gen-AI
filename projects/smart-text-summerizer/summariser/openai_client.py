from openai import OpenAI
from summariser.base import BaseLLMClient
from schemas.summary_schema import SummaryOutput
from config import config
from utils.retry import create_retry_decorator
import json
from jinja2 import Template
import os

class OpenAIClient(BaseLLMClient):
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.DEFAULT_MODEL_OPENAI
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
            return self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )

        response = _call_api()
        content = response.choices[0].message.content
        return SummaryOutput.model_validate_json(content)
