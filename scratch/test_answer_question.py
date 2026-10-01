from app.llm.client import generate

messages = [
    {'role': 'user', 'content': "what's my grocery list?"},
    {'role': 'assistant', 'content': '', 'tool_calls': [{'id': 'call_53l2pynx', 'function': {'index': 0, 'name': 'search_notes', 'arguments': {'question': 'grocery list'}}}]},
    {'role': 'tool', 'content': 'Rent is due on the 1st of the month, pay via e-transfer. Grocery list: milk, eggs, bread, coffee.\nDentist appointment is Tuesday at 2pm with Dr. Martinez downtown.\nHyrox training session Thursday evening, focus on sled push and burpees.\nNeed to call the contractor about the fence repair estimate.'}
]

print(generate(messages))