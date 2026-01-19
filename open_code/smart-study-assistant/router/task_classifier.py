from typing import Tuple, Optional
from enum import Enum


class TaskType(Enum):
    TUTOR = "tutor"
    QUIZ = "quiz"
    SUMMARY = "summary"


class ComplexityLevel(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


class TaskClassifier:
    def __init__(self):
        self.tutor_keywords = [
            'explain', 'what is', 'how does', 'why', 'when', 'where',
            'define', 'describe', 'tell me about', 'understand', 'help me',
            'clarify', 'example', 'analogy', 'concept', 'principle'
        ]

        self.quiz_keywords = [
            'quiz', 'test', 'questions', 'practice', 'generate', 'create quiz',
            'quiz me', 'test me', 'questions about', 'mcq', 'multiple choice',
            'true false', 'fill in', 'exam', 'assessment'
        ]

        self.summary_keywords = [
            'summarize', 'summary', 'condense', 'shorten', 'outline',
            'key points', 'main ideas', 'bullet points', 'study guide',
            'notes', 'summarize this', 'brief summary'
        ]

        self.complexity_keywords = {
            'complex': [
                'analyze', 'design', 'optimize', 'architecture', 'advanced',
                'comprehensive', 'deep dive', 'detailed', 'complex',
                'multi-step', 'strategy', 'framework'
            ],
            'moderate': [
                'compare', 'explain', 'describe', 'analyze', 'evaluate',
                'discuss', 'example', 'how to', 'steps', 'process'
            ],
            'simple': [
                'what is', 'define', 'list', 'identify', 'true/false',
                'status', 'simple', 'basic', 'quick'
            ]
        }

    def classify(self, user_input: str) -> Tuple[TaskType, ComplexityLevel]:
        task_type = self._classify_task_type(user_input)
        complexity = self._classify_complexity(user_input)

        return task_type, complexity

    def _classify_task_type(self, user_input: str) -> TaskType:
        user_input_lower = user_input.lower()

        quiz_score = sum(1 for kw in self.quiz_keywords if kw in user_input_lower)
        summary_score = sum(1 for kw in self.summary_keywords if kw in user_input_lower)
        tutor_score = sum(1 for kw in self.tutor_keywords if kw in user_input_lower)

        if quiz_score > 0 and quiz_score >= summary_score and quiz_score >= tutor_score:
            return TaskType.QUIZ
        elif summary_score > 0 and summary_score >= tutor_score:
            return TaskType.SUMMARY
        else:
            return TaskType.TUTOR

    def _classify_complexity(self, user_input: str) -> ComplexityLevel:
        user_input_lower = user_input.lower()

        complex_score = sum(
            1 for kw in self.complexity_keywords['complex']
            if kw in user_input_lower
        )
        moderate_score = sum(
            1 for kw in self.complexity_keywords['moderate']
            if kw in user_input_lower
        )
        simple_score = sum(
            1 for kw in self.complexity_keywords['simple']
            if kw in user_input_lower
        )

        if complex_score > 0:
            return ComplexityLevel.COMPLEX
        elif moderate_score > 0:
            return ComplexityLevel.MODERATE
        else:
            return ComplexityLevel.SIMPLE
