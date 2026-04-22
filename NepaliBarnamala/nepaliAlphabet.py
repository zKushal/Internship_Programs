import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from chat_db import (
    create_todos,
    delete_todo,
    get_learning_memory,
    get_recent_messages,
    initialize_database,
    list_todos,
    save_message,
    search_todos,
    update_todo_status,
)


env_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError(
        f"GROQ_API_KEY was not found. Add it to {env_path} or set it in your environment."
    )

client = Groq(api_key=api_key)
initialize_database()

SYSTEM_PROMPT = """
You are a learning planner assistant.

Your job is to read the user's request and return valid JSON only.
Do not include markdown fences.

Supported intents:
- "chat": normal answer only
- "create_todos": build a learning todo list based on what the user wants to learn
- "update_status": mark a todo as pending, learning, or completed
- "delete_todo": delete one todo when the user says it is unnecessary
- "get_todo": search for a single todo by id, title, or keyword
- "list_todos": list todos by status: all, learning, pending, completed
- "recall_learning": answer from the database using the user's learning todos

Rules:
- If the user wants to learn something, do not create todos immediately.
- First ask follow-up questions as "chat" to collect the requirements for the plan.
- Before creating todos, confirm that the user actually wants a todo list.
- Collect the missing details that matter, such as:
  - what they want to learn
  - how many days they want the plan for
  - how much time they can spend each day
  - current level or background
  - goal or outcome they want
  - any deadline, preference, or constraint
- If any key planning detail is missing, use "chat" and ask concise questions.
- Only use "create_todos" after the user has clearly confirmed yes and enough details are available.
- If the user asks for explanation, teaching, examples, or more detail about a topic, use "chat", not "create_todos".
- For created todos, generate 3 to 7 practical learning tasks that match the user's timeframe and goal.
- Use short titles and clear descriptions.
- Default the first created todo to "learning" and the rest to "pending".
- For "update_status", include "todo_id" and "status".
- For "delete_todo", include "todo_id".
- For "get_todo", include "query".
- For "list_todos", include "status_filter".
- If the user asks what they learned previously, answer from learning records stored in the database, not from raw chat prompts.
- For normal conversation, use "chat".

Return this schema exactly:
{
  "intent": "chat | create_todos | update_status | delete_todo | get_todo | list_todos | recall_learning",
  "reply": "short helpful message for the user",
  "confirmed": false,
  "collecting_requirements": false,
  "tasks": [
    {
      "title": "task title",
      "description": "task description",
      "status": "learning | pending | completed"
    }
  ],
  "todo_id": 0,
  "status": "pending | learning | completed",
  "query": "",
  "status_filter": "all | pending | learning | completed"
}
""".strip()

TODO_GENERATION_PROMPT = """
You are a learning plan generator.

Read the user's planning requirements and return valid JSON only.
Do not include markdown fences.

Generate 3 to 7 practical learning todos that match the user's goal, timeframe, level,
available time, and constraints. Use short titles and clear descriptions.
Set the first task to "learning" and the rest to "pending".

Return this schema exactly:
{
  "tasks": [
    {
      "title": "task title",
      "description": "task description",
      "status": "learning | pending | completed"
    }
  ]
}
""".strip()


def build_messages(user_input: str) -> list[dict[str, str]]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for role, content, _ in get_recent_messages(8):
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_input})
    return messages


def call_agent(user_input: str) -> dict:
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=build_messages(user_input),
        response_format={"type": "json_object"},
    )

    content = completion.choices[0].message.content or "{}"
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "intent": "chat",
            "reply": content.strip() or "I could not understand that clearly.",
            "confirmed": False,
            "collecting_requirements": False,
            "tasks": [],
            "todo_id": 0,
            "status": "",
            "query": "",
            "status_filter": "all",
        }


def parse_bool_flag(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "y", "1"}
    if isinstance(value, (int, float)):
        return value == 1
    return False


def generate_todos_from_requirements(requirements: list[str]) -> list[dict[str, str]]:
    if not requirements:
        return []

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": TODO_GENERATION_PROMPT},
            {
                "role": "user",
                "content": "\n".join(requirements),
            },
        ],
        response_format={"type": "json_object"},
    )

    content = completion.choices[0].message.content or "{}"
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        return []

    tasks = payload.get("tasks", [])
    if not isinstance(tasks, list):
        return []

    normalized_tasks: list[dict[str, str]] = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        normalized_tasks.append(
            {
                "title": str(task.get("title", "")).strip(),
                "description": str(task.get("description", "")).strip(),
                "status": str(task.get("status", "pending")).strip().lower() or "pending",
            }
        )

    return normalized_tasks


def is_cancel_request(text: str) -> bool:
    normalized = text.strip().lower()
    return normalized in {
        "no",
        "nope",
        "cancel",
        "stop",
        "don't create",
        "do not create",
        "not now",
    }


def is_affirmative_request(text: str) -> bool:
    normalized = text.strip().lower()
    return normalized in {
        "yes",
        "y",
        "yeah",
        "yep",
        "sure",
        "ok",
        "okay",
        "please do",
        "create it",
        "go ahead",
    }


def is_explicit_todo_request(text: str) -> bool:
    normalized = text.strip().lower()
    todo_phrases = (
        "create todo",
        "create todos",
        "make todo",
        "make todos",
        "create a plan",
        "make a plan",
        "learning plan",
        "study plan",
        "roadmap",
    )
    return any(phrase in normalized for phrase in todo_phrases)


def is_teaching_request(text: str) -> bool:
    normalized = text.strip().lower()
    teaching_phrases = (
        "teach me",
        "full detail",
        "full details",
        "with example",
        "examples",
        "real life",
        "current scenarios",
        "details on",
        "more detail",
        "explain",
    )
    return any(phrase in normalized for phrase in teaching_phrases)


def format_todos(todos: list[dict]) -> str:
    if not todos:
        return "No todos found."

    lines = []
    for todo in todos:
        lines.append(
            f"[{todo['id']}] {todo['title']} | status: {todo['status']}\n"
            f"    {todo['description']}"
        )
    return "\n".join(lines)


def format_result(reply: str, todos: list[dict] | None = None) -> str:
    sections = [f"Reply:\n{reply.strip() or 'Done.'}"]
    if todos is not None:
        sections.append(f"Todos:\n{format_todos(todos)}")
    return "\n\n".join(sections)


def is_learning_recall_request(text: str) -> bool:
    normalized = text.strip().lower()
    recall_phrases = (
        "what did i learn",
        "what i learned",
        "what have i learned",
        "learned previously",
        "learn previously",
        "previous learning",
        "completed topics",
        "completed todo",
        "what am i learning",
        "current learning",
        "show my progress",
    )
    return any(phrase in normalized for phrase in recall_phrases)


def build_learning_memory_reply() -> str:
    memory = get_learning_memory()
    learned_items = memory["completed"]
    current_items = memory["learning"]

    if learned_items:
        lines = ["Based on your learning records, you previously learned:"]
        for index, item in enumerate(learned_items[:5], start=1):
            lines.append(f"{index}. {item['title']} - {item['description']}")
        return "\n".join(lines)

    if current_items:
        lines = ["You do not have completed items yet, but you are currently learning:"]
        for index, item in enumerate(current_items[:5], start=1):
            lines.append(f"{index}. {item['title']} - {item['description']}")
        return "\n".join(lines)

    return "I checked your database, but I could not find any learning records yet."

planning_requirements: list[str] = []
planning_session_active = False

while True:
    user_input = input("\n\nYou: ").strip()

    if not user_input:
        continue

    if user_input.lower() in {"exit", "quit"}:
        print("\nAssistant:\nReply:\nGoodbye.")
        break

    if is_learning_recall_request(user_input):
        assistant_output = format_result(build_learning_memory_reply())
        print(f"\nAssistant:\n{assistant_output}")
        save_message("user", user_input)
        save_message("assistant", assistant_output)
        continue

    agent_output = call_agent(user_input)
    intent = str(agent_output.get("intent", "chat")).strip().lower()
    reply = str(agent_output.get("reply", "")).strip()
    confirmed = parse_bool_flag(agent_output.get("confirmed", False))
    collecting_requirements = parse_bool_flag(
        agent_output.get("collecting_requirements", False)
    )
    explicit_todo_request = is_explicit_todo_request(user_input)
    teaching_request = is_teaching_request(user_input)
    confirmed = confirmed or (
        planning_session_active and is_affirmative_request(user_input)
    )

    if teaching_request:
        confirmed = False

    if intent == "create_todos" and not (
        explicit_todo_request or (planning_session_active and confirmed)
    ):
        intent = "chat"

    assistant_output = ""

    if is_cancel_request(user_input):
        planning_requirements.clear()
        planning_session_active = False
        assistant_output = format_result(reply or "Okay, I will not create a todo list.")
        print(f"\nAssistant:\n{assistant_output}")
        save_message("user", user_input)
        save_message("assistant", assistant_output)
        continue

    if collecting_requirements:
        planning_session_active = True

    if intent == "create_todos":
        planning_session_active = True

    if planning_session_active and intent not in {
        "update_status",
        "delete_todo",
        "get_todo",
        "list_todos",
    }:
        planning_requirements.append(user_input)

    if intent == "create_todos" or (planning_session_active and confirmed):
        tasks = agent_output.get("tasks", [])
        if not isinstance(tasks, list):
            tasks = []

        if confirmed and tasks:
            created = create_todos(tasks)
            planning_requirements.clear()
            planning_session_active = False
            assistant_output = format_result(
                reply or "I created a learning todo list for you.",
                created,
            )
        elif confirmed:
            generated_tasks = generate_todos_from_requirements(planning_requirements)
            if generated_tasks:
                created = create_todos(generated_tasks)
                planning_requirements.clear()
                planning_session_active = False
                assistant_output = format_result(
                    reply or "I created a learning todo list for you.",
                    created,
                )
            else:
                assistant_output = format_result(
                    reply
                    or "I still need a bit more detail before I can create the todo list."
                )
        else:
            assistant_output = format_result(
                reply
                or "Before I create a todo list, tell me what you want to learn, how many days you have, how much time you can spend each day, and confirm that you want me to create it."
            )
    elif intent == "update_status":
        todo_id = int(agent_output.get("todo_id", 0) or 0)
        status = str(agent_output.get("status", "pending"))
        updated = update_todo_status(todo_id, status) if todo_id else None
        if updated:
            assistant_output = format_result(
                reply or f"Todo {todo_id} status updated.",
                [updated],
            )
        else:
            assistant_output = format_result(
                f"I could not find todo id {todo_id}.",
                [],
            )
    elif intent == "delete_todo":
        todo_id = int(agent_output.get("todo_id", 0) or 0)
        deleted = delete_todo(todo_id) if todo_id else None
        if deleted:
            assistant_output = format_result(
                reply or f"Todo {todo_id} was deleted.",
                [deleted],
            )
        else:
            assistant_output = format_result(
                f"I could not find todo id {todo_id} to delete.",
                [],
            )
    elif intent == "get_todo":
        query = str(agent_output.get("query", "")).strip()
        results = search_todos(query)
        assistant_output = format_result(
            reply or f"Here are the todos matching '{query}'.",
            results,
        )
    elif intent == "list_todos":
        status_filter = str(agent_output.get("status_filter", "all")).strip().lower()
        results = list_todos(status_filter or "all")
        assistant_output = format_result(
            reply or f"Here are your {status_filter or 'all'} todos.",
            results,
        )
    elif intent == "recall_learning":
        assistant_output = format_result(reply or build_learning_memory_reply())
    else:
        assistant_output = format_result(reply or "How can I help you learn today?")

    print(f"\nAssistant:\n{assistant_output}")
    save_message("user", user_input)
    save_message("assistant", assistant_output)
