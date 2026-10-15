import pkgutil
import importlib
import logging
import json
from typing import Optional
import app.orchestration.tools as tools_package
from app.llm.client import generate, generate_with_tools, ModelServingError

TOOLS = []
TOOL_FUNCTIONS = {}
TOOL_DEFINITIONS = {}

for _, module_name, _ in pkgutil.iter_modules(tools_package.__path__):
    module = importlib.import_module(f"app.orchestration.tools.{module_name}")
    
    tool_def = getattr(module, "TOOL_DEFINITION", None)
    tool_execute = getattr(module, "execute", None)
    
    if tool_def is not None and tool_execute is not None:
        TOOLS.append(tool_def)
        TOOL_FUNCTIONS[tool_def["function"]["name"]] = tool_execute
        TOOL_DEFINITIONS[tool_def["function"]["name"]] = tool_def

def build_synthesis_messages(question: str, results: list) -> list:
    """
    Build a list of messages for the model to synthesize a final answer.
    """
    system_prompt = "The notes belong to the user. Answer the question based on the provided notes. " \
    "Do not say you can not access the notes and do not ask for more details when the answer is in the notes. " \
    "If the notes do not have the information needed, say so."  # your instruction text
    notes = "\n".join(results)     # all results as one string
    user_prompt = f"Notes:\n{notes}\n\nQuestion: {question}"

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

def extract_text_tool_call(content: str) -> Optional[dict]:
    cleaned = content.replace("\\'", "'")  # model wrote \' which is invalid JSON
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        return None

    if not isinstance(parsed, dict):
        return None
    name = parsed.get("name")
    parameters = parsed.get("parameters")
    if name not in TOOL_FUNCTIONS or not isinstance(parameters, dict):
        return None

    return {"function": {"name": name, "arguments": parameters}}

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
        logging.exception(f"Error executing tool {tool_name}: {str(e)}")
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

    if "tool_calls" not in response:
        text_call = extract_text_tool_call(response.get("content", ""))
        if text_call:
            response["tool_calls"] = [text_call]
    
    messages.append(response)
    
    if "tool_calls" in response:
        any_needs_synthesis = False
        collected_results = []  # <-- new: track every result, not just the last one
        
        for tool_call in response["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            if TOOL_DEFINITIONS.get(tool_name, {}).get("use_original_question"):
                tool_call["function"]["arguments"]["question"] = question
            result = execute_tool_call(tool_call)
            messages.append({"role": "tool", "content": result})
            collected_results.append(result)  # <-- new

            if TOOL_DEFINITIONS.get(tool_name, {}).get("needs_synthesis", True):
                any_needs_synthesis = True
        
        if any_needs_synthesis:
            try:
                final_response = generate(build_synthesis_messages(question, collected_results))
                return final_response
            except ModelServingError as e:
                return f"Sorry, I'm having trouble right now: {e}"
        else:
            # If no tool calls need synthesis, return the concatenated results
            return "\n".join(collected_results)
    else:
        return response["content"]