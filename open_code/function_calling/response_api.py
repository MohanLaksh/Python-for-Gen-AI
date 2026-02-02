from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.responses.create(
  model="gpt-4.1",
  store=True,
  input="Tell me a three sentence bedtime story about a unicorn."
)

print("response", response.output[0].content[0].text)

response2= client.responses.create(
  model="gpt-4.1",
  input="How many stories have you told about a unicorn?"
)

print("response2", response2.output[0].content[0].text)