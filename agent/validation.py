import re

# Common stop words to exclude during tokenization to focus on core semantic tokens
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'for', 'to', 'of',
    'is', 'are', 'was', 'were', 'what', 'how', 'why', 'where', 'when', 'who',
    'which', 'this', 'that', 'these', 'those', 'with', 'about', 'by', 'as',
    'search', 'query', 'run', 'get', 'fetch', 'find', 'lookup', 'latest'
}

def tokenize(text: str) -> set:
    """
    Tokenizes a string by converting it to lowercase, removing punctuation, 
    and filtering out common stop words.
    """
    # Replace punctuation with space and convert to lowercase
    normalized = re.sub(r'[^\w\s-]', ' ', text.lower())
    # Split by whitespace
    raw_tokens = normalized.split()
    # Filter stop words and empty tokens
    return {token for token in raw_tokens if token and token not in STOP_WORDS}

def compute_jaccard_similarity(str_a: str, str_b: str) -> float:
    """
    Computes the Jaccard similarity coefficient between two sets of tokens.
    Jaccard Index = |Intersection| / |Union|
    """
    set_a = tokenize(str_a)
    set_b = tokenize(str_b)

    if not set_a and not set_b:
        return 1.0  # Both empty sets are considered identical
    
    if not set_a or not set_b:
        return 0.0

    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)

    return len(intersection) / len(union)

def validate_tool_query(proposed_query: str, history: list, threshold: float = 0.7) -> dict:
    """
    Validates a proposed tool call argument string against a history of prior arguments.
    Returns a dict containing validation parameters and loop warnings.
    """
    highest_similarity = 0.0
    matching_query = None

    for past_query in history:
        similarity = compute_jaccard_similarity(proposed_query, past_query)
        if similarity > highest_similarity:
            highest_similarity = similarity
            matching_query = past_query

    is_loop = highest_similarity >= threshold

    warning_message = None
    if is_loop:
        warning_message = (
            f"LOOPING BEHAVIOR DETECTED: Your proposed tool query (\"{proposed_query}\") "
            f"is highly similar to a previous query you ran (\"{matching_query}\") "
            f"with a Jaccard Similarity of {highest_similarity * 100:.1f}%. "
            f"You are repeating search strategies. DO NOT call this tool with the same or "
            f"slightly tweaked parameters. Instead, immediately pivot your strategy: query a "
            f"different source, check alternative symbols, re-read a different section of "
            f"the context, or synthesize what you already have."
        )

    return {
        "is_loop": is_loop,
        "similarity": highest_similarity,
        "matching_query": matching_query,
        "warning_message": warning_message
    }
