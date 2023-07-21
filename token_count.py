import tiktoken

def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    token_integers = encoding.encode(text)
    return len(token_integers)