#Function to split a paragraph into sentences using regex
def split_paragraph_into_sentences(paragraph: str) -> list[str]:
    import re
    # This regex splits on sentence-ending punctuation followed by whitespace or end of string
    # Known limitation: doesn't distinguish abbreviations (e.g. "Dr.") from real sentence ends
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(paragraph)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


#Function to add a piece of text to the current chunk, or finalize the current chunk
#if adding the piece would exceed max_chunk_size. Recursively falls back to word-level
#splitting if a single piece is already too big on its own.
def add_piece(piece: str, chunks: list[str], current_chunk: str, max_chunk_size: int) -> str:
    # Case 1: the piece itself is too big, even alone — split it into words and pack those instead
    if len(piece) > max_chunk_size:
        if current_chunk:
            chunks.append(current_chunk)
            current_chunk = ""
        words = piece.split()
        for word in words:
            current_chunk = add_piece(word, chunks, current_chunk, max_chunk_size)
        return current_chunk

    # Case 2: adding this piece to current_chunk would overflow — finalize and start fresh
    if len(current_chunk) + len(piece) + 1 > max_chunk_size:
        if current_chunk:
            chunks.append(current_chunk)
        current_chunk = piece
    # Case 3: it fits — append it
    else:
        if current_chunk:
            current_chunk += " " + piece
        else:
            current_chunk = piece

    return current_chunk


#Function to pack paragraphs into chunks of a specified maximum size, with sentence-level
#fallback splitting for long paragraphs (and word-level fallback inside add_piece, for
#the rare case where even a single sentence is too big)
def pack_paragraphs(paragraphs: list[str], max_chunk_size: int = 500) -> list[str]:
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(paragraph) > max_chunk_size:
            sentences = split_paragraph_into_sentences(paragraph)
            for sentence in sentences:
                current_chunk = add_piece(sentence, chunks, current_chunk, max_chunk_size)
        else:
            current_chunk = add_piece(paragraph, chunks, current_chunk, max_chunk_size)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks