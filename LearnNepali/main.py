from assistant import build_agent
import asyncio


async def main():
    agent = build_agent()
    history = []
    print("Welcome to the Nepali learning assistant! How can I help you today?")
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            print("Please enter a message or type 'exit' to quit.")
            continue

        if user_input.lower() in ["exit", "quit", "stop", "end", "goodbye"]:
            print("Thank you for using the Nepali learning assistant! Goodbye!")
            break
        response = await agent.run(user_input, message_history=history)
        history = response.all_messages()
        print(f"Assistant: {response}") 

if __name__ == "__main__":
    asyncio.run(main())