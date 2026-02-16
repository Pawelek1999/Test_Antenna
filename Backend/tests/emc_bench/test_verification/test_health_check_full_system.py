import pytest
import logging

_LOGGER = logging.getLogger("Test.HealthCheck")

@pytest.mark.hardware
def test_full_system_health_check(generator, ni_relay, ni_analog, ctrl_axes):
    """
    Performs a high-level health check of the entire test bench.

    This test passes if all hardware fixtures (generator, ni_relay, ni_analog, ctrl_axes)
    can be initialized successfully without any connection errors. It does not
    perform any actions, as the fixture setup itself is the test.
    """
    _LOGGER.info("--- Full System Health Check ---")
    _LOGGER.info("Successfully initialized all hardware fixtures:")
    _LOGGER.info(f"  - Generator: {generator.get_idn()}")
    _LOGGER.info(f"  - NI Relay: {ni_relay.device_id}")
    _LOGGER.info(f"  - NI Analog: {ni_analog.device_id}")
    _LOGGER.info(f"  - CtrlAxes: Connected")
    _LOGGER.info("All systems are online and responsive.")
    assert True
