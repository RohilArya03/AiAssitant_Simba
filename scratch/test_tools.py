from app.llm.client import generate, generate_with_tools

# confirm generate() still works exactly as before
print(generate([{"role": "user", "content": "say hello in one word"}]))

# confirm generate_with_tools() still returns the full message dict correctly
tools = [{
    "type": "function",
    "function": {
        "name": "search_notes",
        "description": "Searches the user's personal notes for saved information like groceries, recipes, or reminders",
        "parameters": {
            "type": "object",
            "properties": {"question": {"type": "string", "description": "the user's question"}},
            "required": ["question"]
        }
    }
}]
result = generate_with_tools([{"role": "user", "content": "what's my grocery list?"}], tools)
print(result)