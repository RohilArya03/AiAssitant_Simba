from app.rag.embeddings import embed_text

result = embed_text("Dentist appointment Tuesday")
print(type(result))
print(len(result))