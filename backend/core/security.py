import secrets

def create_dummy_token(username: str) -> str:
    """Simple dummy token generator."""
    return f"{username}_{secrets.token_hex(8)}"
