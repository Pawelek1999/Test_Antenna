class NIError(Exception):
    """Base exception class for NI-DAQmx related errors."""

    pass


class NIConnectionError(NIError):
    """Raised when the NI device is not found or cannot be initialized."""

    pass


class NIConfigurationError(NIError):
    """Raised when the channel or port configuration is invalid."""

    pass


class NIOperationError(NIError):
    """Raised when the executed operation failed"""

    pass
