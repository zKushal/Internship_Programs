import json
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

from chat_db import (
    create_todos,
    delete_todo,
    get_recent_messages,
    initialize_database,
    list_todos,
    save_message,
    search_todos,
    update_todo_status,
)

# =========================
# INIT
# =========================
env_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY not found")

client = Groq(api_key=api_key)
initialize_database()

pending_plan = False

VALID_INTENTS = {
    "chat",
    "create_todos",
    "update_status",
    "delete_todo",
    "get_todo",
    "list_todos",
    "plan_learning",
    "confirm_create_todos",
}

VALID_STATUS = {"pending", "learning", "completed"}

# =========================
# SYSTEM PROMPT (FIXED)
# =========================
SYSTEM_PROMPT = """
You are a Learning Planner Agent.

You help users plan learning and manage todos.

RULES:
- Never create todos without confirmation
- First collect learning details
- Then propose plan
- Ask confirmation before creating todos

INTENTS:
chat, plan_learning, confirm_create_todos,
create_todos, update_status, delete_todo,
get_todo, list_todos

OUTPUT MUST BE JSON ONLY.
"""


# =========================
# MESSAGE BUILDER
# =========================
def build_messages(user_input: str):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for role, content, _ in get_recent_messages(6):
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_input})
    return messages


# =========================
# AGENT CALL
# =========================
def call_agent(user_input: str):
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=build_messages(user_input),
            response_format={"type": "json_object"},
        )

        content = completion.choices[0].message.content or "{}"

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return fallback_response("Invalid model response")

        return validate_response(data)

    except Exception:
        return fallback_response("Something went wrong.")


# =========================
# VALIDATION
# =========================
def validate_response(data: dict):
    intent = str(data.get("intent", "chat")).lower()
    if intent not in VALID_INTENTS:
        intent = "chat"

    status = str(data.get("status", "")).lower()
    if status not in VALID_STATUS:
        status = "pending"

    return {
        "intent": intent,
        "reply": str(data.get("reply", "")),
        "tasks": data.get("tasks", []),
        "todo_id": int(data.get("todo_id", 0) or 0),
        "status": status,
        "query": str(data.get("query", "")),
        "status_filter": str(data.get("status_filter", "all")).lower(),
    }


def fallback_response(message):
    return {
        "intent": "chat",
        "reply": message,
        "tasks": [],
        "todo_id": 0,
        "status": "",
        "query": "",
        "status_filter": "all",
    }


# =========================
# FORMATTERS
# =========================
def format_todos(todos):
    if not todos:
        return "No todos found."

    return "\n".join(
        f"[{t[0]}] {t[1]} ({t[3]})\n  {t[2]}"
        for t in todos
    )


def format_result(reply, todos=None):
    output = f"Reply:\n{reply.strip() or 'Done.'}"
    if todos is not None:
        output += f"\n\nTodos:\n{format_todos(todos)}"
    return output


# =========================
# MAIN LOOP
# =========================
while True:
    user_input = input("\nYou: ").strip()

    if not user_input:
        continue

    if user_input.lower() in {"exit", "quit"}:
        print("\nAssistant:\nGoodbye.")
        break

    # FIXED: learning detection INSIDE loop
    if "learn" in user_input.lower():
        pending_plan = True
        print("\nAssistant:")
        print("Great! Let's plan your learning journey 😊")
        print("1. How many days?")
        print("2. Time per day?")
        print("3. Level?")
        continue

    agent_output = call_agent(user_input)

    intent = agent_output["intent"]
    reply = agent_output["reply"]

    # =========================
    # INTENT HANDLER
    # =========================
    if intent == "create_todos":
        tasks = agent_output["tasks"]
        result = create_todos(tasks) if tasks else []
        output = format_result(reply or "Todos created.", result)

    elif intent == "update_status":
        result = update_todo_status(
            agent_output["todo_id"],
            agent_output["status"]
        )
        output = format_result(reply, [result] if result else [])

    elif intent == "delete_todo": # intent used for both delete and confirm_create
        result = delete_todo(agent_output["todo_id"])
        output = format_result(reply, [result] if result else [])

    elif intent == "get_todo":
        result = search_todos(agent_output["query"])
        output = format_result(reply, result)

    elif intent == "list_todos":
        result = list_todos(agent_output["status_filter"])
        output = format_result(reply, result)

    else:
        output = format_result(reply)

    print(f"\nAssistant:\n{output}")

    save_message("user", user_input)
    save_message("assistant", output)