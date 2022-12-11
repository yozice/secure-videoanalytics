class InvalidPort(Exception):
    """raised when subprocess with given PID doesn't exist"""

    def __init__(self, port: int):
        super().__init__(f"no subprocess streaming on port {port}")


class UnknownModelType(Exception):
    """raised when trying to create unregistered model plugin"""
