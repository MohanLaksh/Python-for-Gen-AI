from typing import Optional
from roles.base_role import BaseRole
from prompts import (
    TUTOR_SYSTEM_PROMPT,
    TUTOR_CONCEPT_TEMPLATE,
    TUTOR_QUESTION_TEMPLATE,
    TUTOR_ANALOGY_TEMPLATE
)


class TutorRole(BaseRole):
    def __init__(self):
        super().__init__("Tutor")
        self.system_prompt = TUTOR_SYSTEM_PROMPT

    def prepare_prompt(self, user_input: str, context: Optional[dict] = None) -> str:
        context = context or {}

        request_type = context.get('request_type', 'question')

        if request_type == 'concept':
            concept = context.get('concept', '')
            subject = context.get('subject', 'general')
            prompt = TUTOR_CONCEPT_TEMPLATE.format(concept=concept, subject=subject)
        elif request_type == 'analogy':
            concept = context.get('concept', '')
            prompt = TUTOR_ANALOGY_TEMPLATE.format(concept=concept)
        else:
            subject = context.get('subject', 'general')
            prompt = TUTOR_QUESTION_TEMPLATE.format(
                question=user_input,
                subject=subject
            )

        return f"{self.system_prompt}\n\n{prompt}"

    def process_response(self, response: str) -> str:
        return response
