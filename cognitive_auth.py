class CognitiveAuthManager:
    """Minimal authentication manager used for tests."""

    def __init__(self):
        self._users = {}

    def register_user(self, username: str, password: str, metadata: dict | None = None) -> str:
        """Register a new user and return a pseudo cocoon id."""
        if username in self._users:
            raise ValueError("User already exists")
        self._users[username] = {"password": password, "metadata": metadata or {}}
        return f"cocoon_{username}"

    def validate_user(self, username: str, password: str) -> bool:
        """Validate credentials for a user."""
        return self._users.get(username, {}).get("password") == password

    def collapse_user_node(self, username: str) -> bool:
        """Remove a user and return True if removed."""
        return self._users.pop(username, None) is not None
