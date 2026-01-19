from typing import Optional
from roles.base_role import BaseRole
from prompts import (
    QUIZ_SYSTEM_PROMPT,
    QUIZ_MCQ_TEMPLATE,
    QUIZ_TRUE_FALSE_TEMPLATE,
    QUIZ_FILL_BLANK_TEMPLATE,
    QUIZ_MIXED_TEMPLATE
)


class QuizCreatorRole(BaseRole):
    def __init__(self):
        super().__init__("Quiz Creator")
        self.system_prompt = QUIZ_SYSTEM_PROMPT

    def prepare_prompt(self, user_input: str, context: Optional[dict] = None) -> str:
        context = context or {}

        quiz_type = context.get('quiz_type', 'mcq')
        topic = context.get('topic', user_input)
        num_questions = context.get('num_questions', 5)
        difficulty = context.get('difficulty', 'medium')

        if quiz_type == 'mcq':
            prompt = QUIZ_MCQ_TEMPLATE.format(
                num_questions=num_questions,
                topic=topic,
                difficulty=difficulty
            )
        elif quiz_type == 'true_false':
            prompt = QUIZ_TRUE_FALSE_TEMPLATE.format(
                num_questions=num_questions,
                topic=topic,
                difficulty=difficulty
            )
        elif quiz_type == 'fill_blank':
            prompt = QUIZ_FILL_BLANK_TEMPLATE.format(
                num_questions=num_questions,
                topic=topic,
                difficulty=difficulty
            )
        elif quiz_type == 'mixed':
            num_mcq = context.get('num_mcq', 3)
            num_tf = context.get('num_tf', 3)
            num_fb = context.get('num_fb', 2)
            prompt = QUIZ_MIXED_TEMPLATE.format(
                topic=topic,
                difficulty=difficulty,
                num_mcq=num_mcq,
                num_tf=num_tf,
                num_fb=num_fb
            )
        else:
            prompt = QUIZ_MCQ_TEMPLATE.format(
                num_questions=num_questions,
                topic=topic,
                difficulty=difficulty
            )

        return f"{self.system_prompt}\n\n{prompt}"

    def process_response(self, response: str) -> str:
        return response
