from app.orchestration.router import execute_tool_call
from unittest.mock import patch
from app.orchestration.router import answer_question
from app.llm.client import ModelServingError
from app.orchestration.router import TOOL_FUNCTIONS
from app.orchestration.router import build_synthesis_messages

import logging

logging.basicConfig(level=logging.ERROR)

def test_execute_tool_call_unregistered_tool():
    fake_tool_call = {
        "function": {
            "name": "check_weather",
            "arguments": {}
        }
    }
    result = execute_tool_call(fake_tool_call)
    assert "not available" in result


def test_execute_tool_call_get_current_time():
    fake_tool_call = {
        "function": {
            "name": "get_current_time",
            "arguments": {}
        }
    }
    result = execute_tool_call(fake_tool_call)
    assert "current date and time" in result.lower()



def test_answer_question_appends_assistant_message_before_tool_result():
    fake_response = {
        "role": "assistant",
        "content": "",
        "tool_calls": [{"function": {"name": "get_current_time", "arguments": {}}}]
    }
    
    with patch("app.orchestration.router.generate_with_tools", return_value=fake_response):
        result = answer_question("what time is it?")

    assert "current date and time" in result.lower()


def test_answer_question_handles_ollama_down_gracefully():
    with patch("app.orchestration.router.generate_with_tools", side_effect=ModelServingError("Ollama is not running. Start it and try again.")):
        result = answer_question("hello")
    
    assert "Sorry, I'm having trouble right now" in result

def test_answer_question_combines_multiple_non_synthesis_tool_results():
    fake_response = {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {"function": {"name": "get_current_time", "arguments": {}}},
            {"function": {"name": "get_current_time", "arguments": {}}}
        ]
    }
    
    with patch("app.orchestration.router.generate_with_tools", return_value=fake_response), \
         patch("app.orchestration.router.execute_tool_call", side_effect=["Result A", "Result B"]):
        result = answer_question("...")
    
    assert "Result A" in result
    assert "Result B" in result

def test_registry_contains_expected_tools():
    assert "search_notes" in TOOL_FUNCTIONS
    assert "get_current_time" in TOOL_FUNCTIONS
    assert len(TOOL_FUNCTIONS) == 2

def test_answer_question_returns_direct_reply_when_no_tool_called():
    fake_response = {"role": "assistant", "content": "Hello! How can I help?"}

    with patch("app.orchestration.router.generate_with_tools", return_value=fake_response):
        result = answer_question("hi")

    assert result == "Hello! How can I help?"

def test_execute_tool_call_logs_and_returns_error_string_when_tool_raises(caplog):
    def broken_tool(**kwargs):
        raise ValueError("boom")

    fake_tool_call = {"function": {"name": "broken", "arguments": {}}}

    with patch.dict(TOOL_FUNCTIONS, {"broken": broken_tool}):
        with caplog.at_level(logging.ERROR):
            result = execute_tool_call(fake_tool_call)

    assert "Error executing tool broken" in result
    assert "boom" in caplog.text


def test_build_synthesis_messages_includes_question_and_results_without_tool_role():
    messages = build_synthesis_messages("what's my grocery list?", ["Grocery list: milk, eggs."])

    roles = [m["role"] for m in messages]
    assert roles[0] == "system"
    assert "tool" not in roles

    all_text = " ".join(m["content"] for m in messages)
    assert "what's my grocery list?" in all_text
    assert "Grocery list: milk, eggs." in all_text