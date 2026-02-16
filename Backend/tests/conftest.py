import pytest
import logging
import os
from tests.exceptions import TestBenchError

# Configure a separate logger for hardware-specific errors.
hw_logger = logging.getLogger("hardware_debug")
hw_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("hardware_errors.log")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
hw_logger.addHandler(handler)


def pytest_addoption(parser):
    """Adds custom hardware configuration options to pytest."""
    parser.addini("GENERATOR_ADDRESS", "VISA address for the signal generator")
    parser.addini("NI_RELAY_DEVICE_ID", "Device ID for the NI Relay card")
    parser.addini("NI_ANALOG_DEVICE_ID", "Device ID for the NI Analog Input card")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to intercept test execution results.
    If a test fails with a hardware-related error (TestBenchError),
    it logs the details to a dedicated hardware error log.
    """
    outcome = yield
    report = outcome.get_result()

    if report.failed and call.excinfo:
        if call.excinfo.errisinstance(TestBenchError):
            exc = call.excinfo.value
            exc_type = call.excinfo.type.__name__

            hw_logger.error("=" * 50)
            hw_logger.error(f"HARDWARE ERROR in test: {item.nodeid}")
            hw_logger.error(f"Exception Type: {exc_type}")
            hw_logger.error(f"Message: {exc}")
            hw_logger.error("=" * 50)
        else:
            logging.getLogger("pytest").warning(f"Test failed with unexpected error: {call.excinfo.value}")


@pytest.fixture(scope="session")
def hardware_config(request):
    """
    Provides hardware configuration from pytest.ini or environment variables.
    
    This fixture centralizes access to hardware addresses and IDs, allowing
    easy configuration without modifying test code.
    """
    config = request.config
    return {
        "generator_address": config.getini("GENERATOR_ADDRESS") or os.getenv("GENERATOR_ADDRESS"),
        "ni_relay_id": config.getini("NI_RELAY_DEVICE_ID") or os.getenv("NI_RELAY_DEVICE_ID"),
        "ni_analog_id": config.getini("NI_ANALOG_DEVICE_ID") or os.getenv("NI_ANALOG_DEVICE_ID"),
    }
