import datetime

TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Gets the current date and time. Use this whenever the user asks about the current time, date, or day. Example questions: 'what time is it', 'what's today's date', 'what day is it'.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "needs_synthesis": False
}

def execute() -> list[str]:
    """
    Returns the current date and time as a string.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [f"The current date and time is: {current_time}"]