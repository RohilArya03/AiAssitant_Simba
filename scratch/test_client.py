import time
from app.llm.client import generate

start = time.time()
result = generate([{"role": "user", "content": "Say hello in one sentence."}])
elapsed = time.time() - start

print(result)
print(f"Total time: {elapsed:.2f}s")