import groq
import json
import os


ALLOWED_CHANNEL_ID = [
    1341047125839970487,
]
MAX_HISTORY = 20


CONFIG = {}
for file in os.listdir("config"):
    with open(f"config/{file}", "r", encoding="utf-8") as f:
        CONFIG[f"{file.split('.')[0]}"] = f.read()


def clear_message():
    global MESSAGES
    MESSAGES = [
        {
            "role": "system",
            "content": str(CONFIG.get("system_message"))
        }
    ]


clear_message()


def append_message(role, content):
    global MESSAGES
    MESSAGES.append({"role": role, "content": content})

    # Keep only the last MAX_HISTORY messages
    if len(MESSAGES) > MAX_HISTORY:
        MESSAGES = [MESSAGES[0]] + MESSAGES[-(MAX_HISTORY - 1):]

    # update messages_log.json
    with open("messages_log.json", "w") as f:
        json.dump(MESSAGES, f, indent=4)


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = groq.Groq(api_key=GROQ_API_KEY)


def completion(message):
    completion = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=MESSAGES,
        temperature=1,
        max_completion_tokens=512,
        top_p=1,
        stream=False,
        stop=None,
    )

    append_message("assistant", completion.choices[0].message.content)

    with open("messages.json", "w") as f:
        json.dump(MESSAGES, f, indent=4)

    response = completion.choices[0].message.content
    return response
