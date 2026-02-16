# drivers/exceptions.py


class TestBenchError(Exception):
    """Base exception for all issues related to the test environment/setup."""

    pass


class UsageStepError(TestBenchError):
    """Raised when a test step is used incorrectly (e.g., missing arguments, wrong order)."""

    pass


class SetupError(TestBenchError):
    """Raised when the environment cannot be prepared for the test (e.g., hardware init failed)."""

    pass


class TeardownError(TestBenchError):
    """Raised when the environment cannot be cleaned up after the test."""

    pass


class ConfigurationMissingError(TestBenchError):
    """Raised when the user forgot to define a required parameter in the YAML/JSON config file."""

    pass


class ResourceLockedError(TestBenchError):
    """Raised when a tester tries to use a device that is already being used by another process or test."""

    pass


class NotSupportedHardwareError(UsageStepError):
    """Raised when a tester calls a step on hardware that doesn't support it (e.g., 'set_speed' on a static axis)."""

    pass


class InvalidCommandSequenceError(UsageStepError):
    """Raised when steps are called in a non-logical order (e.g., 'move_axis' before 'home_axis')."""

    pass
