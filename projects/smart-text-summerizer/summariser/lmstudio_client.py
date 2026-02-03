from openai import OpenAI
from summariser.base import BaseLLMClient
from schemas.summary_schema import SummaryOutput
from config import config
from utils.retry import create_retry_decorator
import json
from jinja2 import Template
import os

class LMStudioClient(BaseLLMClient):
    def __init__(self):
        # LM Studio is API compatible with OpenAI
        self.client = OpenAI(
            base_url=config.LMSTUDIO_BASE_URL,
            api_key="lm-studio" # Key is usually ignored or can be any string
        )
        self.model = config.DEFAULT_MODEL_LMSTUDIO
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
                # LM Studio might not support response_format="json_object" depending on the model/version
                # But we can try or rely on prompt instruction. 
                # For safety, let's keep it if the model supports it, else we rely on prompt.
                # Usually better to rely on prompt for generic local models.
                temperature=0.7 
            )

        response = _call_api()
        content = response.choices[0].message.content
        
        # Cleanup potential markdown ticks if local model is chatty
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()

        return SummaryOutput.model_validate_json(content)
