from legacy.groq_client import ask_groq

from legacy.prompts import (
    tool_selection_prompt
)

def choose_tool(user_query):

    prompt = tool_selection_prompt(
        user_query
    )

    response = ask_groq(prompt)

    return response.strip()