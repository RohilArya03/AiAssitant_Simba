from app.rag.pipeline import run_rag_pipeline

TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "search_notes",
        "description": "Searches the user's personal notes for saved information like groceries, recipes, or reminders. "
                       "Example questions: 'what's my grocery list', 'what recipe did I save for biryani'.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "the user's question to search for in their notes"}
            },
            "required": ["question"]
        }
    }
}

def execute(question: str) -> list[str]:
    """
    Thin wrapper matching the tool's declared parameter name,
    so the router can call it generically regardless of the underlying function's real name.
    """
    return run_rag_pipeline(question)