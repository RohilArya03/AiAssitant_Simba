import re
from app.llm.client import generate

def parse_score(response: str) -> int:
    """
    Extracts the first number found in the LLM's response,
    defensively handling cases where it doesn't respond with a clean number alone.
    """
    match = re.search(r'\d+', response)
    if match:
        return int(match.group())
    return -1  # Return -1 if no number is found, indicating an error or unexpected response


def rerank(question: str, candidates: list[str]) -> list[str]:
    """
    Takes the top-k candidates from search() and re-orders them
    by LLM-judged relevance to the question.
    """
    scored = []
    for chunk in candidates:
        prompt = f"""
        Question: {question}
        Chunk: {chunk}

On a scale of 1-10, how relevant is this chunk to answering the question?
Respond with ONLY the number, nothing else."""
 
        response = generate([{"role": "user", "content": prompt}])
        score = parse_score(response)
        scored.append((chunk, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, _ in scored]