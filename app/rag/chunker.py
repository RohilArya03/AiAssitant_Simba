def split_paragraph_into_sentences(paragraph: str) -> list[str]:
    """
    Split a paragraph into sentences using sentence-ending punctuation.
    """
    import re
    # This does not distinguish abbreviations such as "Dr." from sentence ends.
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(paragraph)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def add_piece(piece: str, chunks: list[str], current_chunk: str, max_chunk_size: int) -> str:
    """
    Add a piece to the current chunk, splitting oversized pieces into words.
    """
    # Split oversized pieces before attempting to append them to a chunk.
    if len(piece) > max_chunk_size:
        if current_chunk:
            chunks.append(current_chunk)
            current_chunk = ""
        words = piece.split()
        for word in words:
            current_chunk = add_piece(word, chunks, current_chunk, max_chunk_size)
        return current_chunk

    # Case 2: adding this piece to current_chunk would overflow — finalize and start fresh
    # Finalize the current chunk when adding this piece would exceed the limit.
    if len(current_chunk) + len(piece) + 1 > max_chunk_size:
        if current_chunk:
            chunks.append(current_chunk)
        current_chunk = piece
    else:
        if current_chunk:
            current_chunk += " " + piece
        else:
            current_chunk = piece

    return current_chunk


def pack_paragraphs(paragraphs: list[str], max_chunk_size: int = 500) -> list[str]:
    """
    Pack paragraphs into chunks no larger than max_chunk_size.
    """
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

def split_into_paragraphs(text: str) -> list[str]:
    """
    Split raw text into paragraphs based on blank lines.
    """
    paragraphs = text.split("\n\n")
    # Ignore empty paragraphs and normalize surrounding whitespace.
    return [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]