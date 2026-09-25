from app.config import NOTE_STORE_PATH
from app.rag.vector_store import build_vector_store, load_vector_store

# Run 1: simulate first-ever run
store1 = build_vector_store(["Rent is due on the 1st.", "Dentist appointment Tuesday."], NOTE_STORE_PATH)
print("After run 1:", [text for text, _ in store1])

# Run 2: same two chunks, plus one genuinely new one
store2 = build_vector_store(["Rent is due on the 1st.", "Dentist appointment Tuesday.", "Call contractor about fence."], NOTE_STORE_PATH)
print("After run 2:", [text for text, _ in store2])