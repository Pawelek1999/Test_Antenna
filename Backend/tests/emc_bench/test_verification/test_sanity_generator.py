import pytest
import logging
import time

import tests.emc_bench.bdd_steps.generator_smb100a as gen_steps

_LOGGER = logging.getLogger("Test.Sanity.Generator")


@pytest.mark.hardware
class TestGeneratorSanity:
    """
    Sanity checks for the Rohde & Schwarz SMB100A Signal Generator.
    """

    def test_connection_and_idn(self, generator):
        """
        Verifies a successful connection and correct device identification.
        """
        _LOGGER.info("--- Verifying Generator Connection and IDN ---")
        idn = generator.get_idn()
        _LOGGER.info(f"Received IDN: {idn}")
        assert (
            "Rohde&Schwarz" in idn
        ), "The device identification string is not as expected."
        assert "SMB100A" in idn, "The device model is not SMB100A."

    def test_safe_power_set_and_read(self, generator):
        """
        Verifies the ability to set and read back a safe power level.
        """
        _LOGGER.info("--- Verifying Generator Power Control ---")
        test_power = 10
        gen_steps.set_generator_power(generator, test_power)
        time.sleep(2)

        read_power = generator.get_power()
        _LOGGER.info(f"Set power to {test_power} dBm, read back {read_power} dBm.")
        assert test_power == 10, "Read-back power does not match the set value."

    def test_safe_freq_set_and_read(self, generator):
        """
        Verifies the ability to set and read back a safe frequency value.
        """
        _LOGGER.info("--- Verifying Generator Frequency ---")
        test_freq = 869_850_000
        gen_steps.set_generator_frequency(generator, test_freq)
        time.sleep(2)

        read_freq = generator.get_frequency()
        _LOGGER.info(f"Set power to {test_freq} dBm, read back {read_freq} dBm.")
        assert (
            abs(read_freq - test_freq) < 0.1
        ), "Read-back power does not match the set value."

    def test_rf_output_toggle(self, generator):
        """
        Verifies that the RF output can be enabled and disabled.
        """
        _LOGGER.info("--- Verifying Generator RF Output Toggle ---")

        _LOGGER.info("Enabling RF Output...")
        gen_steps.enable_rf_output(generator)
        time.sleep(2)
        assert generator.get_output_rf_state() is True, "RF output failed to enable."

        _LOGGER.info("Disabling RF Output...")
        gen_steps.disable_rf_output(generator)
        assert generator.get_output_rf_state() is False, "RF output failed to disable."
