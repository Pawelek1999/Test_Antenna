import logging
from typing import TYPE_CHECKING

from tests.exceptions import UsageStepError, SetupError

if TYPE_CHECKING:
    from drivers.rs_smb100a import SMB100A

_LOGGER = logging.getLogger("SMB100A.Steps")


def set_generator_frequency(generator: "SMB100A", frequency_hz: float) -> None:
    """
    Sets the frequency of the SMB100A generator.

    Args:
        generator: The SMB100A driver instance.
        frequency_hz: The target frequency in Hertz.
    Raises:
        UsageStepError: If the frequency is invalid (<= 0).
        SetupError: If the command fails.
    """
    _LOGGER.info(f"Setting generator frequency to {frequency_hz} Hz.")
    if frequency_hz <= 0:
        raise UsageStepError(f"Invalid frequency: {frequency_hz} Hz. Must be positive.")

    try:
        generator.set_frequency(frequency_hz)
    except Exception as e:
        _LOGGER.error(f"Failed to set frequency: {e}")
        raise SetupError(f"Could not set generator frequency to {frequency_hz} Hz.") from e


def set_generator_power(generator: "SMB100A", power_dbm: float) -> None:
    """
    Sets the power level of the SMB100A generator.

    Args:
        generator: The SMB100A driver instance.
        power_dbm: The target power level in dBm.
    Raises:
        UsageStepError: If the power level is out of the valid range.
        SetupError: If the command fails.
    """
    _LOGGER.info(f"Setting generator power to {power_dbm} dBm.")
    # The valid range is checked within the driver, but an early check here is good practice.
    if not -120 <= power_dbm <= 20:
        raise UsageStepError(f"Invalid power: {power_dbm} dBm. Allowed range: -120 to 20 dBm.")

    try:
        generator.set_power(power_dbm)
    except Exception as e:
        _LOGGER.error(f"Failed to set power: {e}")
        raise SetupError(f"Could not set generator power to {power_dbm} dBm.") from e


def enable_rf_output(generator: "SMB100A") -> None:
    """
    Enables the RF output of the generator.

    Args:
        generator: The SMB100A driver instance.
    """
    _LOGGER.info("Enabling RF output.")
    try:
        generator.set_output_rf(True)
    except Exception as e:
        _LOGGER.error(f"Failed to enable RF output: {e}")
        raise SetupError("Could not enable RF output.") from e


def disable_rf_output(generator: "SMB100A") -> None:
    """
    Disables the RF output of the generator.

    Args:
        generator: The SMB100A driver instance.
    """
    _LOGGER.info("Disabling RF output.")
    try:
        generator.set_output_rf(False)
    except Exception as e:
        _LOGGER.error(f"Failed to disable RF output: {e}")
        raise SetupError("Could not disable RF output.") from e


def verify_generator_settings(
    generator: "SMB100A", expected_freq_hz: float, expected_power_dbm: float, expected_rf_state: bool
) -> None:
    """
    Verifies that the generator's settings match the expected values.

    Args:
        generator: The SMB100A driver instance.
        expected_freq_hz: The expected frequency in Hz.
        expected_power_dbm: The expected power in dBm.
        expected_rf_state: The expected RF output state (True for ON, False for OFF).
    Raises:
        SetupError: If any setting does not match the expected value.
    """
    _LOGGER.info("Verifying generator settings...")

    current_freq = generator.get_frequency()
    if abs(current_freq - expected_freq_hz) > 0.1:  # Allow small tolerance
        raise SetupError(f"Frequency mismatch! Expected: {expected_freq_hz} Hz, Got: {current_freq} Hz.")

    current_power = generator.get_power()
    if abs(current_power - expected_power_dbm) > 0.1:
        raise SetupError(f"Power mismatch! Expected: {expected_power_dbm} dBm, Got: {current_power} dBm.")

    current_rf_state = generator.get_output_rf_state()
    if current_rf_state is not expected_rf_state:
        raise SetupError(f"RF State mismatch! Expected: {expected_rf_state}, Got: {current_rf_state}.")

    _LOGGER.info("Generator settings verified successfully.")
