from collections import Counter
from unittest.mock import patch
from app.llm.client import generate_with_tools
from app.orchestration.router import answer_question
from app.rag.pipeline import run_rag_pipeline

TEST_NOTES_PATH = "eval/fixtures/test_notes.txt"
EVAL_STORE = "eval_store.pkl"
RUNS = 20
CASE = {"question": "what's my grocery list?", "expected_contains": ["milk", "eggs", "bread", "coffee"]}

seen = {"tool_calls": None, "chunks": None}

def spy_generate_with_tools(messages, tools):
    response = generate_with_tools(messages, tools)
    seen["tool_calls"] = response.get("tool_calls")
    return response

def run_on_fixture(question):
    chunks = run_rag_pipeline(question, notes_file_path=TEST_NOTES_PATH, store_filename=EVAL_STORE)
    seen["chunks"] = chunks
    return chunks

def run_eval():
    outcomes = Counter()
    for i in range(RUNS):
        seen["tool_calls"] = None
        seen["chunks"] = None
        with patch("app.orchestration.router.generate_with_tools", side_effect=spy_generate_with_tools), \
             patch("app.orchestration.tools.search_notes.run_rag_pipeline", side_effect=run_on_fixture):
            answer = answer_question(CASE["question"])

        if answer and all(x in answer.lower() for x in CASE["expected_contains"]):
            outcomes["pass"] += 1
            continue

        if seen["tool_calls"] is None:
            label = "no tool call"
        elif seen["chunks"] is None:
            label = "tool call made, pipeline never ran (bad args?)"
        else:
            label = "tool ran, final answer bad"
        outcomes[label] += 1
        print(f"FAIL run {i+1}: {label}\n  tool_calls: {seen['tool_calls']}\n  chunks: {seen['chunks']}\n  answer: {answer}\n")

    print(dict(outcomes))

if __name__ == "__main__":
    run_eval()