def tutor_prompt(topic, level):
    return f"""
You are a friendly tutor.
Explain the topic "{topic}" for a {level} learner.
Use simple examples.
End with one question to check understanding.
"""

def quiz_prompt(topic):
    return f"""
Create 3 multiple choice questions on "{topic}".
Provide correct answers with explanation.
"""
