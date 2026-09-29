import pkgutil
import importlib
import app.orchestration.tools as tools_package
from app.llm.client import generate, generate_with_tools, ModelServingError

TOOLS = []
TOOL_FUNCTIONS = {}

for _, module_name, _ in pkgutil.iter_modules(tools_package.__path__):
    module = importlib.import_module(f"app.orchestration.tools.{module_name}")
    
    tool_def = getattr(module, "TOOL_DEFINITION", None)
    tool_execute = getattr(module, "execute", None)
    
    if tool_def is not None and tool_execute is not None:
        TOOLS.append(tool_def)
        TOOL_FUNCTIONS[tool_def["function"]["name"]] = tool_execute

def execute_tool_call(tool_call: dict) -> str:
    """
    Run a registered tool call and return the tool output as a string.
    """
    tool_name = tool_call["function"]["name"]
    tool_args = tool_call["function"]["arguments"]
    
    if tool_name not in TOOL_FUNCTIONS:
        return f"(Tool '{tool_name}' is not available.)"
    try:
        tool_result = TOOL_FUNCTIONS[tool_name](**tool_args)
        return "\n".join(tool_result)
    except Exception as e:
        return f"Error executing tool {tool_name}: {str(e)}"



def answer_question(question: str) -> str:
    """
    Ask the model a question, run any required tool calls, and return the final answer.
    """
    messages = [{"role": "user", "content": question}]
    
    try:
        response = generate_with_tools(messages, TOOLS)
    except ModelServingError as e:
        return f"Sorry, I'm having trouble right now: {e}"
    
    messages.append(response)
    
    if "tool_calls" in response:
        for tool_call in response["tool_calls"]:
            result = execute_tool_call(tool_call)
            messages.append({"role": "tool", "content": result})
        
        try:
            final_response = generate(messages)
            return final_response
        except ModelServingError as e:
            return f"Sorry, I'm having trouble right now: {e}"
    
    return response["content"]