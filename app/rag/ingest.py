def read_notes_file(filepath: str) -> str:
    """
    Reads a text file from disk and returns its full contents as a string.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()