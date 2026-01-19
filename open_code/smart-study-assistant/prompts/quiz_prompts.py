QUIZ_SYSTEM_PROMPT = """You are an expert quiz creator specializing in educational assessments. Your role is to generate high-quality practice questions that test understanding and help students learn.

Your questions should:
1. Be clear, unambiguous, and well-formatted
2. Test key concepts rather than trivial details
3. Include plausible distractors for multiple-choice questions
4. Be appropriately challenging for the specified level
5. Come with detailed answer explanations

Output format: Use Markdown for clear formatting.
"""

QUIZ_MCQ_TEMPLATE = """Generate {num_questions} multiple-choice questions about {topic} for {difficulty} level students.

Format each question as:
```
## Question 1
{question text}

A) {option A}
B) {option B}
C) {option C}
D) {option D}

**Answer:** {correct option}
**Explanation:** {detailed explanation of why this is correct and why others are wrong}
```

Ensure:
- Questions test understanding, not just memorization
- Distractors are plausible but clearly incorrect
- Difficulty matches {difficulty} level
- Questions cover different aspects of {topic}
"""

QUIZ_TRUE_FALSE_TEMPLATE = """Generate {num_questions} true/false questions about {topic} for {difficulty} level students.

Format each question as:
```
## Question 1
{statement}

**Answer:** True/False
**Explanation:** {explanation}
```

Ensure:
- Statements are clear and unambiguous
- Mix of true and false statements
- Explanations clarify the reasoning
"""

QUIZ_FILL_BLANK_TEMPLATE = """Generate {num_questions} fill-in-the-blank questions about {topic} for {difficulty} level students.

Format each question as:
```
## Question 1
{question text with _____ for blanks}

**Answer:** {correct answer(s)}
**Explanation:** {context or explanation}
```

Ensure:
- Blanks represent key terms or concepts
- Answers are specific and unambiguous
- Questions test understanding of relationships
"""

QUIZ_MIXED_TEMPLATE = """Generate a mixed quiz about {topic} for {difficulty} level students.

Include:
- {num_mcq} multiple-choice questions
- {num_tf} true/false questions
- {num_fb} fill-in-the-blank questions

Format each section clearly with headers. Provide answer keys at the end.
"""
