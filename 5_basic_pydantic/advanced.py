from pydantic import BaseModel, Field, field_validator, model_validator
import re
import tiktoken

class PromptTemplate(BaseModel):
    template: str = Field(..., description="The template to use for the prompt", min_length=1, max_length=1000)
    variables: list[str] = Field(..., description="The variables to use for the prompt", min_length=1, max_length=1000)
    max_tokens: int = Field(..., description="The maximum number of tokens to use for the prompt", min_value=1, max_value=1000)
    model: str = Field(default="gpt-4-turbo")


    def validate_template(self) -> str:
        placeholders = re.findall(r"{(\w+)}", self.template)
        if not placeholders:
            raise ValueError("Template must contain placeholders")
        if not all(placeholder in self.variables for placeholder in placeholders):
            raise ValueError("All placeholders must be in the variables list")
        return self.template

    def validate_tokens(self) -> int:
        encoding = tiktoken.encoding_for_model(self.model)
        tokens = len(encoding.encode(self.template))
        if tokens > self.max_tokens:
            raise ValueError("Template is too long")
        return tokens

    def format_prompt(self, **kwargs) -> str:
        return self.template.format(**kwargs)



prompt_template = PromptTemplate(
    template="""You are a helpful assistant for a {domain} professional.
        User Profile:
        - Name: {user_name}
        - Experience Level: {experience_level}

        Task:
        Explain {topic} in a {tone} manner using {example_type} examples.

        Constraints:
        - Language: {language}
        - Max words: {max_words}
    """,
    variables=["domain", "user_name", "experience_level", "topic", "tone", "example_type", "language", "max_words"],
    max_tokens=50,
    model="gpt-4-turbo"
)

formatted_prompt = prompt_template.format_prompt(
    domain="software engineering",
    user_name="John Doe",
    experience_level="senior",
    topic="software engineering",
    tone="formal",
    example_type="case study",
    language="English",
    max_words=100
)
print(formatted_prompt)