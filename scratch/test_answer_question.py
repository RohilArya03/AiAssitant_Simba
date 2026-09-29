from app.orchestration.router import execute_tool_call

fake_tool_call = {
    "function": {
        "name": "check_weather",
        "arguments": {}
    }
}

result = execute_tool_call(fake_tool_call)
print(result)