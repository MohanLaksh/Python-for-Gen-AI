from typing import Optional
from roles.base_role import BaseRole
from prompts import (
    SUMMARIZER_SYSTEM_PROMPT,
    SUMMARIZER_BULLET_TEMPLATE,
    SUMMARIZER_STUDY_GUIDE_TEMPLATE,
    SUMMARIZER_CONDENSED_TEMPLATE,
    SUMMARIZER_HIERARCHICAL_TEMPLATE
)


class SummarizerRole(BaseRole):
    def __init__(self):
        super().__init__("Summarizer")
        self.system_prompt = SUMMARIZER_SYSTEM_PROMPT

    def prepare_prompt(self, user_input: str, context: Optional[dict] = None) -> str:
        context = context or {}

        summary_type = context.get('summary_type', 'bullet')
        content = context.get('content', user_input)
        topic = context.get('topic', 'the content')

        if summary_type == 'bullet':
            prompt = SUMMARIZER_BULLET_TEMPLATE.format(
                topic=topic,
                content=content
            )
        elif summary_type == 'study_guide':
            prompt = SUMMARIZER_STUDY_GUIDE_TEMPLATE.format(
                topic=topic,
                content=content
            )
        elif summary_type == 'condensed':
            prompt = SUMMARIZER_CONDENSED_TEMPLATE.format(
                topic=topic,
                content=content
            )
        elif summary_type == 'hierarchical':
            prompt = SUMMARIZER_HIERARCHICAL_TEMPLATE.format(
                topic=topic,
                content=content
            )
        else:
            prompt = SUMMARIZER_BULLET_TEMPLATE.format(
                topic=topic,
                content=content
            )

        return f"{self.system_prompt}\n\n{prompt}"

    def process_response(self, response: str) -> str:
        return response
