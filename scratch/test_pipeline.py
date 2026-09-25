from app.rag.pipeline import run_rag_pipeline

results = run_rag_pipeline("what's my grocery list?")
for r in results:
    print(r)