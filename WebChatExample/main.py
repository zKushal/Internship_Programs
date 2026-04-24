from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from dotenv import load_dotenv

load_dotenv()

model= GroqModel("openai/gpt-oss-120b")


agent = Agent(model, instructions='You are a helpful assistant.')

@agent.tool_plain   
def get_weather(city: str) -> str:
    return f'The weather in {city} is sunny'

app = agent.to_web()