import logging
from typing import TYPE_CHECKING

from tests.exceptions import UsageStepError, SetupError

if TYPE_CHECKING:
    from drivers.ni.do_9485 import NI9485Handler
    from drivers.ni.usb_6361 import NIUSB6361Handler

_LOGGER = logging.getLogger("NI_Cards.Steps")


# --- NI 9485 (Digital Output) Steps ---

def set_relay_state(relay_driver: "NI9485Handler", channel: int, state: bool) -> None:
    """
    Sets the state of a specific relay channel.

    Args:
        relay_driver: The NI 9485 driver instance.
        channel: The relay channel number (0-7).
        state: True for ON (Closed), False for OFF (Open).
    Raises:
        UsageStepError: If the channel number is invalid.
        SetupError: If the relay operation fails.
    """
    state_str = "ON" if state else "OFF"
    _LOGGER.info(f"Setting relay channel {channel} to {state_str}.")

    if not 0 <= channel <= 7:
        raise UsageStepError(f"Invalid relay channel: {channel}. Must be between 0 and 7.")

    try:
        relay_driver.write_relay(channel, state)
    except Exception as e:
        _LOGGER.error(f"Failed to set relay {channel} to {state_str}: {e}")
        raise SetupError(f"Could not set relay {channel} to {state_str}.") from e


def open_all_relays(relay_driver: "NI9485Handler") -> None:
    """
    Opens all relays, putting the device in a safe state.

    Args:
        relay_driver: The NI 9485 driver instance.
    """
    _LOGGER.info("Opening all relays (safe state).")
    try:
        relay_driver.safe_state()
    except Exception as e:
        _LOGGER.error(f"Failed to open all relays: {e}")
        raise SetupError("Could not open all relays.") from e


# --- NI USB-6361 (Analog Input) Steps ---

def measure_voltage(
    ai_driver: "NIUSB6361Handler", channel: int, min_expected: float = -10.0, max_expected: float = 10.0
) -> float:
    """
    Measures the voltage on a specific analog input channel.

    Args:
        ai_driver: The NI USB-6361 driver instance.
        channel: The analog input channel number.
        min_expected: The minimum expected voltage for range configuration.
        max_expected: The maximum expected voltage for range configuration.
    Returns:
        The measured voltage in Volts.
    Raises:
        SetupError: If the measurement fails.
    """
    _LOGGER.info(f"Measuring voltage on AI channel {channel}.")
    try:
        voltage = ai_driver.read_analog_input(channel, min_val=min_expected, max_val=max_expected)
        _LOGGER.info(f"Measured {voltage:.4f} V on AI{channel}.")
        return voltage
    except Exception as e:
        _LOGGER.error(f"Failed to measure voltage on AI{channel}: {e}")
        raise SetupError(f"Could not measure voltage on AI{channel}.") from e


def verify_voltage_in_range(ai_driver: "NIUSB6361Handler", channel: int, min_limit: float, max_limit: float) -> None:
    """
    Verifies that the voltage on a channel is within the specified limits.

    Args:
        ai_driver: The NI USB-6361 driver instance.
        channel: The analog input channel number.
        min_limit: The minimum acceptable voltage.
        max_limit: The maximum acceptable voltage.
    Raises:
        SetupError: If the measured voltage is outside the specified range.
    """
    _LOGGER.info(f"Verifying voltage on AI{channel} is between {min_limit}V and {max_limit}V.")
    
    # Adjust measurement range to cover limits plus a margin
    meas_min = min(min_limit, -10.0)
    meas_max = max(max_limit, 10.0)
    
    voltage = measure_voltage(ai_driver, channel, min_expected=meas_min, max_expected=meas_max)
    
    if not min_limit <= voltage <= max_limit:
        raise SetupError(
            f"Voltage out of range on AI{channel}! "
            f"Expected: [{min_limit}, {max_limit}], Got: {voltage:.4f} V."
        )
    
    _LOGGER.info(f"Voltage verification passed: {voltage:.4f} V is within range.")
