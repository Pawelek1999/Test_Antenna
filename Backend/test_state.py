RESULT_FILE = "result.json"

class TestState:
    """Prosta klasa do zarządzania stanem testu w pamięci."""
    def __init__(self):
        self._is_running = False

    def start(self):
        self._is_running = True

    def stop(self):
        self._is_running = False

    def is_active(self):
        return self._is_running