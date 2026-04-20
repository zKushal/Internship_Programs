from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print(os.getenv("GROQ_API_KEY"))

completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": """
            You are a helpful agent. Extract contact information and return ONLY valid JSON.

            Rules:
            - Output must be pure JSON
            - No explanation
            - Keys: ID, name, Email

            Example:
            Input: My ID is 101 and my name is Katwal P. My email is katwal@gmail.com
            Output:
            {"ID":101,"name":"Katwal P","Email":"katwal@gmail.com"}
            """
        },
        {
            "role": "user",     
            "content": "My student ID is 209 and my name is Lamichane. S and I have email address Lamichane@gmail.com"
        }
    ],
    temperature=0.5,
    stream=True
)

for chunk in completion:
    delta = chunk.choices[0].delta
    if hasattr(delta, "content") and delta.content:
        print(delta.content, end="")