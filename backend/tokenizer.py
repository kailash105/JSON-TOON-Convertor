import tiktoken

def count_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def calculate_cost(tokens, model="gpt-4o-mini"):
    rate_per_1k = 0.002  # $ per 1K tokens
    return round(tokens / 1000 * rate_per_1k, 6)
