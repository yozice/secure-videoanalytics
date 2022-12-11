class InvalidPID(Exception):
    """raised when subprocess with given PID doesn't exist"""

    def __init__(self, pid: int):
        super().__init__(f"no subprocess with PID {pid}")
