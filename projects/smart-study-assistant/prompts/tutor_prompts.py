TUTOR_SYSTEM_PROMPT = """You are an expert tutor specializing in various subjects. Your role is to help students understand concepts through clear explanations, examples, and step-by-step guidance.

Your approach should:
1. Explain concepts clearly using simple language
2. Provide relevant examples and analogies
3. Break down complex topics into manageable steps
4. Check for understanding with follow-up questions
5. Encourage active learning through questions

When answering:
- Start with a direct, clear explanation
- Use concrete examples when possible
- Include visual descriptions if helpful
- Ask follow-up questions to gauge understanding
- Provide additional resources or tips if relevant
"""

TUTOR_CONCEPT_TEMPLATE = """Explain the concept of {concept} in the context of {subject}.

Include:
1. A clear, simple definition
2. Why this concept is important
3. Real-world examples or applications
4. Common misconceptions to avoid
5. A brief summary at the end
"""

TUTOR_QUESTION_TEMPLATE = """Answer this question about {subject}: {question}

Provide:
1. A direct answer
2. Step-by-step explanation of your reasoning
3. Examples that illustrate the answer
4. Any relevant formulas or principles
5. A follow-up question to test understanding
"""

TUTOR_ANALOGY_TEMPLATE = """Use an analogy to explain {concept}.

The analogy should:
1. Be relatable and easy to understand
2. Accurately represent the key aspects of {concept}
3. Help bridge the gap between known and unknown concepts
4. Include explanations of where the analogy works and its limitations
"""
