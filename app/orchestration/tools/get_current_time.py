import datetime

TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Gets the current date and time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

def execute() -> list[str]:
    """
    Returns the current date and time as a string.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [f"The current date and time is: {current_time}"]