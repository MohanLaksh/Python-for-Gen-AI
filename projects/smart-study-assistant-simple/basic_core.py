from llm import call_llm
from prompts import tutor_prompt, quiz_prompt

def tutor(topic, level):
    prompt = tutor_prompt(topic, level)
    return call_llm(prompt)

def quiz(topic):
    prompt = quiz_prompt(topic)
    return call_llm(prompt)
