import pytest
import logging
import time

import tests.emc_bench.bdd_steps.ni_cards as ni_steps

_LOGGER = logging.getLogger("Test.Sanity.NICards")


@pytest.mark.hardware
class TestNICardsSanity:
    """
    Sanity checks for National Instruments hardware (Relay and Analog Input).
    """

    def test_relay_toggle_channel_0(self, ni_relay):
        """
        Verifies that relay channel 0 can be toggled ON and OFF without error.
        """
        _LOGGER.info("--- Verifying NI Relay Channel 0 Toggle ---")
        test_channel = 0

        _LOGGER.info(f"Closing relay channel {test_channel}...")
        ni_steps.set_relay_state(ni_relay, test_channel, state=True)
        time.sleep(0.2)

        _LOGGER.info(f"Opening relay channel {test_channel}...")
        ni_steps.set_relay_state(ni_relay, test_channel, state=False)
        time.sleep(0.2)

        _LOGGER.info("Relay toggle commands executed successfully.")

    def test_analog_read_channel_0(self, ni_analog):
        """
        Verifies that a voltage reading can be obtained from AI channel 0.
        """
        _LOGGER.info("--- Verifying NI Analog Read Channel 0 ---")
        test_channel = 0

        voltage = ni_steps.measure_voltage(ni_analog, test_channel)
        _LOGGER.info(
            f"Successfully read {voltage:.4f} V from AI channel {test_channel}."
        )

        assert isinstance(
            voltage, float
        ), "The value read from the analog input is not a float."
